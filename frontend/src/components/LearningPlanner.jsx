import { useState } from 'react';
import LearningForm from './LearningForm';
import LearningResults from './LearningResults';
import LoadingSpinner from './LoadingSpinner';
import { AcademicCapIcon } from '@heroicons/react/24/outline';
import { BookOpen, Brain, Search } from 'lucide-react';

export default function LearningPlanner() {
  const [isLoading, setIsLoading] = useState(false);
  const [learningPath, setLearningPath] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (formData) => {
    setIsLoading(true);
    setError(null);
    setLearningPath(null);

    try {
      const response = await fetch('http://localhost:8000/api/learning/plan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate learning path');
      }

      const data = await response.json();
      setLearningPath(data.learning_path);
    } catch (err) {
      setError(err.message || 'An error occurred while generating your learning path');
      console.error('Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setLearningPath(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <AcademicCapIcon className="w-12 h-12 text-purple-600" />
            <h1 className="text-4xl font-bold text-gray-900">Learning Path Planner</h1>
          </div>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            AI-powered personalized learning paths with real courses, books, and resources
          </p>
          <div className="mt-4 flex items-center justify-center gap-6 text-sm text-gray-600">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span>Real Resource Search</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
              <span>AI-Powered Planning</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></div>
              <span>Progress Tracking</span>
            </div>
          </div>
        </div>

        {/* Main Content */}
        {!learningPath && !isLoading && (
          <div className="max-w-4xl mx-auto">
            <LearningForm onSubmit={handleSubmit} isLoading={isLoading} />
          </div>
        )}

        {isLoading && (
          <div className="max-w-4xl mx-auto">
            <LoadingSpinner
              message="Creating your personalized learning path..."
              submessage="AI is analyzing and finding the best resources"
              steps={[
                { icon: Brain, text: "Analyzing learning goals with AI...", delay: 0 },
                { icon: Search, text: "Searching for real courses and resources...", delay: 1000 },
                { icon: BookOpen, text: "Creating structured learning path...", delay: 2000 },
              ]}
              duration="20-40 seconds"
            />
            <div className="mt-8 bg-white rounded-lg shadow-md p-6">
              <h3 className="font-semibold text-gray-900 mb-4">🔍 What we're doing:</h3>
              <ul className="space-y-3 text-sm text-gray-700">
                <li className="flex items-start gap-2">
                  <span className="text-purple-600 font-bold">1.</span>
                  <span>Analyzing your learning goals and creating a structured learning path with AI</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-purple-600 font-bold">2.</span>
                  <span>Searching for real online courses from Coursera, Udemy, edX using Tavily</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-purple-600 font-bold">3.</span>
                  <span>Finding recommended books and reading materials from real sources</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-purple-600 font-bold">4.</span>
                  <span>Discovering hands-on tutorials and practice platforms via web search</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-purple-600 font-bold">5.</span>
                  <span>Creating a week-by-week study schedule using AI agent</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-purple-600 font-bold">6.</span>
                  <span>Designing progress tracking and assessment milestones with LangChain</span>
                </li>
              </ul>
              <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-sm text-blue-800">
                  <strong>Note:</strong> We're using real-time web searches to find actual courses and resources. This may take 20-40 seconds.
                </p>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="max-w-4xl mx-auto">
            <div className="bg-red-50 border border-red-200 rounded-lg p-6 shadow-md">
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0">
                  <svg className="w-6 h-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-red-900 mb-2">Error Generating Learning Path</h3>
                  <p className="text-red-700 mb-4">{error}</p>
                  <button
                    onClick={handleReset}
                    className="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition-colors font-medium"
                  >
                    Try Again
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {learningPath && !isLoading && (
          <div className="max-w-6xl mx-auto">
            <div className="mb-6 flex items-center justify-between">
              <button
                onClick={handleReset}
                className="flex items-center gap-2 text-purple-600 hover:text-purple-700 font-semibold transition-colors"
              >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                Create New Learning Path
              </button>
              <button
                onClick={() => window.print()}
                className="flex items-center gap-2 bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors font-medium"
              >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
                </svg>
                Print Learning Path
              </button>
            </div>
            <LearningResults learningPath={learningPath} />
          </div>
        )}

        {/* Features Section */}
        {!learningPath && !isLoading && (
          <div className="mt-12 max-w-6xl mx-auto">
            <div className="bg-white rounded-lg shadow-md p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
                What Makes Our Learning Planner Special?
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <FeatureCard
                  icon="🎯"
                  title="Personalized Path"
                  description="AI creates a custom learning journey based on your goals, level, and available time"
                />
                <FeatureCard
                  icon="📚"
                  title="Real Resources"
                  description="Live search for actual courses, books, tutorials from top platforms - no mock data"
                />
                <FeatureCard
                  icon="📅"
                  title="Structured Schedule"
                  description="Week-by-week breakdown with time allocation and milestones"
                />
                <FeatureCard
                  icon="📊"
                  title="Progress Tracking"
                  description="Built-in assessment system to track your learning journey"
                />
                <FeatureCard
                  icon="🚀"
                  title="Project-Based"
                  description="Hands-on projects in each phase to apply what you learn"
                />
                <FeatureCard
                  icon="🤖"
                  title="AI-Powered"
                  description="Uses advanced AI to optimize your learning path for maximum effectiveness"
                />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function FeatureCard({ icon, title, description }) {
  return (
    <div className="text-center p-4">
      <div className="text-4xl mb-3">{icon}</div>
      <h3 className="font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-sm text-gray-600">{description}</p>
    </div>
  );
}
