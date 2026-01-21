import { useState, useEffect } from 'react';
import { 
  BookOpenIcon, 
  ClockIcon, 
  CheckCircleIcon,
  AcademicCapIcon,
  CalendarIcon,
  ArrowRightIcon,
  TrophyIcon
} from '@heroicons/react/24/outline';

export default function PastLearnings({ onLoadLearning }) {
  const [learnings, setLearnings] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPastLearnings();
  }, []);

  const fetchPastLearnings = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/api/learning/paths?limit=20');
      
      if (!response.ok) {
        throw new Error('Failed to fetch past learnings');
      }

      const data = await response.json();
      setLearnings(data.paths || []);
    } catch (err) {
      console.error('Error fetching past learnings:', err);
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric' 
    });
  };

  const getStatusBadge = (learning) => {
    const todoList = learning.todo_list || {};
    const hasAssessment = learning.latest_assessment_result;
    const hasCertificate = learning.certificate_data;
    
    if (hasCertificate) {
      return (
        <span className="flex items-center gap-1 text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full">
          <TrophyIcon className="w-3 h-3" />
          Certified
        </span>
      );
    }
    
    if (hasAssessment && hasAssessment.passed) {
      return (
        <span className="flex items-center gap-1 text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
          <CheckCircleIcon className="w-3 h-3" />
          Passed
        </span>
      );
    }
    
    const completedCount = todoList.completed_count || 0;
    const totalCount = todoList.total_count || 0;
    const percentage = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;
    
    if (percentage === 100) {
      return (
        <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
          Ready for Assessment
        </span>
      );
    }
    
    return (
      <span className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded-full">
        {percentage}% Complete
      </span>
    );
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8 text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
        <p className="text-gray-600 mt-4">Loading your learning history...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <p className="text-red-800">Failed to load past learnings: {error}</p>
        <button 
          onClick={fetchPastLearnings}
          className="mt-4 text-red-600 hover:text-red-800 font-semibold"
        >
          Try Again
        </button>
      </div>
    );
  }

  if (learnings.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8 text-center">
        <BookOpenIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-xl font-semibold text-gray-700 mb-2">No Past Learnings Yet</h3>
        <p className="text-gray-500">Your completed learning paths will appear here.</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <BookOpenIcon className="w-7 h-7 text-purple-600" />
          Past Learnings
        </h2>
        <span className="text-sm text-gray-600">{learnings.length} path{learnings.length !== 1 ? 's' : ''}</span>
      </div>

      <div className="space-y-4">
        {learnings.map((learning) => {
          const metadata = learning.metadata || {};
          const todoList = learning.todo_list || {};
          const completedCount = todoList.completed_count || 0;
          const totalCount = todoList.total_count || 0;
          const progressPercentage = totalCount > 0 ? (completedCount / totalCount) * 100 : 0;

          return (
            <div
              key={learning.session_id}
              className="border border-gray-200 rounded-lg p-5 hover:border-purple-300 hover:shadow-md transition-all cursor-pointer"
              onClick={() => onLoadLearning(learning)}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-1">
                    {metadata.topic || 'Learning Path'}
                  </h3>
                  <div className="flex flex-wrap gap-3 text-sm text-gray-600">
                    <span className="flex items-center gap-1">
                      <CalendarIcon className="w-4 h-4" />
                      {formatDate(learning.created_at)}
                    </span>
                    {metadata.duration_weeks && (
                      <span className="flex items-center gap-1">
                        <ClockIcon className="w-4 h-4" />
                        {metadata.duration_weeks} weeks
                      </span>
                    )}
                    {metadata.difficulty && (
                      <span className="capitalize text-purple-600 font-medium">
                        {metadata.difficulty}
                      </span>
                    )}
                  </div>
                </div>
                <div className="flex flex-col items-end gap-2">
                  {getStatusBadge(learning)}
                  <button className="text-purple-600 hover:text-purple-800 flex items-center gap-1 text-sm font-medium">
                    View <ArrowRightIcon className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="mt-3">
                <div className="flex items-center justify-between text-xs text-gray-600 mb-1">
                  <span>Progress</span>
                  <span>{completedCount}/{totalCount} tasks</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                  <div
                    className="bg-gradient-to-r from-purple-500 to-blue-500 h-full transition-all duration-300"
                    style={{ width: `${progressPercentage}%` }}
                  />
                </div>
              </div>

              {/* Assessment Info */}
              {learning.latest_assessment_result && (
                <div className="mt-3 pt-3 border-t border-gray-100">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-600 flex items-center gap-1">
                      <AcademicCapIcon className="w-4 h-4" />
                      Latest Assessment
                    </span>
                    <span className={`font-semibold ${
                      learning.latest_assessment_result.passed 
                        ? 'text-green-600' 
                        : 'text-orange-600'
                    }`}>
                      Score: {learning.latest_assessment_result.score}%
                    </span>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
