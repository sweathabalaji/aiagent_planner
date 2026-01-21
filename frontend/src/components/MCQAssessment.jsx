import { useState } from 'react';
import { 
  AcademicCapIcon, 
  CheckCircleIcon, 
  XCircleIcon,
  ClockIcon,
  TrophyIcon
} from '@heroicons/react/24/outline';

export default function MCQAssessment({ sessionId, onAssessmentComplete }) {
  const [assessment, setAssessment] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [results, setResults] = useState(null);
  const [showResults, setShowResults] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);

  const syncTodos = async () => {
    setIsSyncing(true);
    try {
      const response = await fetch('http://localhost:8000/api/learning/sync-todos', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ session_id: sessionId }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to sync todos');
      }

      alert('✅ Todos synced successfully! Now you can generate the assessment.');
    } catch (error) {
      console.error('Error syncing todos:', error);
      alert(error.message || 'Failed to sync todos. Please try again.');
    } finally {
      setIsSyncing(false);
    }
  };

  const generateAssessment = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/learning/generate-assessment', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ session_id: sessionId }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to generate assessment');
      }

      const data = await response.json();
      setAssessment(data.assessment);
    } catch (error) {
      console.error('Error generating assessment:', error);
      const errorMsg = error.message || 'Failed to generate assessment. Please try again.';
      
      // If error mentions incomplete todos, show sync option
      if (errorMsg.includes('complete all todos')) {
        if (confirm(errorMsg + '\n\nClick OK to sync todos and try again.')) {
          await syncTodos();
        }
      } else {
        alert(errorMsg);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleAnswerSelect = (questionId, optionId) => {
    if (showResults) return; // Don't allow changes after submission
    setSelectedAnswers(prev => ({
      ...prev,
      [questionId]: optionId
    }));
  };

  const handleSubmit = async () => {
    const totalQuestions = assessment.questions.length;
    const answeredQuestions = Object.keys(selectedAnswers).length;

    if (answeredQuestions < totalQuestions) {
      alert(`Please answer all questions. You've answered ${answeredQuestions} out of ${totalQuestions}.`);
      return;
    }

    setIsSubmitting(true);
    try {
      const response = await fetch('http://localhost:8000/api/learning/submit-assessment', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          answers: selectedAnswers
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to submit assessment');
      }

      const data = await response.json();
      setResults(data);
      setShowResults(true);

      if (data.passed && onAssessmentComplete) {
        onAssessmentComplete(data);
      }
    } catch (error) {
      console.error('Error submitting assessment:', error);
      alert(error.message || 'Failed to submit assessment. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleRetake = () => {
    // Reset state to allow retaking
    setSelectedAnswers({});
    setResults(null);
    setShowResults(false);
    setAssessment(null);
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  if (!assessment) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8 text-center">
        <AcademicCapIcon className="w-16 h-16 text-purple-600 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Ready for Your Assessment?
        </h2>
        <p className="text-gray-600 mb-6">
          Test your knowledge with a comprehensive MCQ assessment covering all the topics you've learned.
        </p>
        <div className="flex gap-4 justify-center">
          <button
            onClick={generateAssessment}
            disabled={isLoading || isSyncing}
            className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105"
          >
            {isLoading ? 'Generating Assessment...' : 'Start Assessment'}
          </button>
          <button
            onClick={syncTodos}
            disabled={isLoading || isSyncing}
            className="bg-gray-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            title="Sync your completed todos with the database"
          >
            {isSyncing ? 'Syncing...' : 'Sync Todos'}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg p-6 text-white mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-2">{assessment.title}</h2>
            <p className="text-purple-100">{assessment.description}</p>
          </div>
          {!showResults && (
            <div className="text-right">
              <div className="flex items-center gap-2 text-sm">
                <ClockIcon className="w-5 h-5" />
                <span>No time limit</span>
              </div>
              <div className="text-sm mt-1">
                Passing Score: {assessment.passing_score}%
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Results Summary */}
      {showResults && results && (
        <div className={`rounded-lg p-6 mb-6 ${
          results.passed 
            ? 'bg-green-50 border-2 border-green-500' 
            : 'bg-orange-50 border-2 border-orange-500'
        }`}>
          <div className="flex items-center gap-4">
            {results.passed ? (
              <TrophyIcon className="w-16 h-16 text-green-600" />
            ) : (
              <AcademicCapIcon className="w-16 h-16 text-orange-600" />
            )}
            <div className="flex-1">
              <h3 className={`text-2xl font-bold mb-2 ${
                results.passed ? 'text-green-900' : 'text-orange-900'
              }`}>
                {results.passed ? '🎉 Congratulations!' : 'Keep Learning!'}
              </h3>
              <p className={results.passed ? 'text-green-800' : 'text-orange-800'}>
                You scored <span className="font-bold text-2xl">{results.score.toFixed(1)}%</span>
                {' '}({results.correct_count}/{results.total_questions} correct)
              </p>
              <p className={`text-sm mt-1 ${results.passed ? 'text-green-700' : 'text-orange-700'}`}>
                {results.passed 
                  ? 'You can now generate your completion certificate!' 
                  : `You need ${results.passing_score}% to pass. Review the topics and try again.`}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Questions */}
      <div className="space-y-6">
        {assessment.questions.map((question, index) => {
          const userAnswer = selectedAnswers[question.id];
          const isAnswered = userAnswer !== undefined;
          const result = showResults && results?.results.find(r => r.question_id === question.id);
          const isCorrect = result?.is_correct;

          return (
            <div 
              key={question.id} 
              className={`border rounded-lg p-5 ${
                showResults 
                  ? (isCorrect ? 'border-green-500 bg-green-50' : 'border-red-500 bg-red-50')
                  : 'border-gray-300'
              }`}
            >
              <div className="flex items-start gap-3 mb-4">
                <span className="flex-shrink-0 w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center font-bold">
                  {index + 1}
                </span>
                <div className="flex-1">
                  <h4 className="text-lg font-semibold text-gray-900">{question.question}</h4>
                </div>
                {showResults && (
                  <div className="flex-shrink-0">
                    {isCorrect ? (
                      <CheckCircleIcon className="w-8 h-8 text-green-600" />
                    ) : (
                      <XCircleIcon className="w-8 h-8 text-red-600" />
                    )}
                  </div>
                )}
              </div>

              {/* Options */}
              <div className="space-y-2 ml-11">
                {question.options.map((option) => {
                  const isSelected = userAnswer === option.id;
                  const isCorrectOption = showResults && option.id === question.correct_answer;
                  const isWrongSelection = showResults && isSelected && !isCorrect;

                  return (
                    <button
                      key={option.id}
                      onClick={() => handleAnswerSelect(question.id, option.id)}
                      disabled={showResults}
                      className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                        showResults
                          ? isCorrectOption
                            ? 'border-green-500 bg-green-100'
                            : isWrongSelection
                            ? 'border-red-500 bg-red-100'
                            : 'border-gray-300 bg-gray-50'
                          : isSelected
                          ? 'border-purple-600 bg-purple-50'
                          : 'border-gray-300 hover:border-purple-400 hover:bg-purple-50'
                      } ${!showResults && 'cursor-pointer'}`}
                    >
                      <div className="flex items-center gap-3">
                        <span className={`flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center text-sm font-bold ${
                          showResults
                            ? isCorrectOption
                              ? 'border-green-600 bg-green-600 text-white'
                              : isWrongSelection
                              ? 'border-red-600 bg-red-600 text-white'
                              : 'border-gray-400'
                            : isSelected
                            ? 'border-purple-600 bg-purple-600 text-white'
                            : 'border-gray-400'
                        }`}>
                          {option.id.toUpperCase()}
                        </span>
                        <span className={
                          showResults && (isCorrectOption || isWrongSelection)
                            ? 'font-semibold'
                            : ''
                        }>
                          {option.text}
                        </span>
                      </div>
                    </button>
                  );
                })}
              </div>

              {/* Explanation */}
              {showResults && result && (
                <div className={`mt-4 ml-11 p-4 rounded-lg ${
                  isCorrect ? 'bg-green-100' : 'bg-blue-50'
                }`}>
                  <p className="text-sm font-semibold text-gray-900 mb-1">
                    {isCorrect ? '✓ Correct!' : '✗ Incorrect'}
                  </p>
                  <p className="text-sm text-gray-700">
                    <span className="font-semibold">Explanation:</span> {result.explanation}
                  </p>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Submit Button */}
      {!showResults && (
        <div className="mt-8 flex justify-center">
          <button
            onClick={handleSubmit}
            disabled={isSubmitting || Object.keys(selectedAnswers).length < assessment.questions.length}
            className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-12 py-4 rounded-lg font-bold text-lg hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 shadow-lg"
          >
            {isSubmitting ? 'Submitting...' : 'Submit Assessment'}
          </button>
        </div>
      )}

      {/* Retake Button */}
      {showResults && (
        <div className="mt-8 flex justify-center gap-4">
          <button
            onClick={handleRetake}
            className="bg-gradient-to-r from-orange-500 to-red-500 text-white px-8 py-3 rounded-lg font-semibold hover:from-orange-600 hover:to-red-600 transition-all transform hover:scale-105 shadow-lg flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Retake Assessment
          </button>
          {results && results.passed && (
            <div className="text-center">
              <p className="text-green-700 text-sm font-medium">
                ✓ You've passed! Scroll down to generate your certificate.
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
