import { useState, useEffect } from 'react';
import { CheckCircleIcon, ClockIcon, BookmarkIcon, BeakerIcon } from '@heroicons/react/24/outline';
import { CheckCircleIcon as CheckCircleSolidIcon } from '@heroicons/react/24/solid';

export default function TodoList({ todoList, sessionId, onAllCompleted }) {
  const [todos, setTodos] = useState(todoList?.items || []);
  const [completedCount, setCompletedCount] = useState(todoList?.completed_count || 0);
  const [isUpdating, setIsUpdating] = useState(false);
  const [hasTriggeredCallback, setHasTriggeredCallback] = useState(false);

  const totalCount = todoList?.total_count || 0;
  const progressPercentage = totalCount > 0 ? (completedCount / totalCount) * 100 : 0;

  // Check if all todos are completed and trigger callback
  useEffect(() => {
    if (completedCount === totalCount && totalCount > 0 && !hasTriggeredCallback && onAllCompleted) {
      console.log('All todos completed - triggering callback');
      setHasTriggeredCallback(true);
      onAllCompleted();
    }
  }, [completedCount, totalCount, hasTriggeredCallback, onAllCompleted]);

  const getIconForType = (type) => {
    switch (type) {
      case 'milestone':
        return <CheckCircleIcon className="w-5 h-5" />;
      case 'learning':
        return <BookmarkIcon className="w-5 h-5" />;
      case 'project':
        return <BeakerIcon className="w-5 h-5" />;
      default:
        return <ClockIcon className="w-5 h-5" />;
    }
  };

  const getColorForType = (type) => {
    switch (type) {
      case 'milestone':
        return 'text-purple-600 bg-purple-50 border-purple-200';
      case 'learning':
        return 'text-blue-600 bg-blue-50 border-blue-200';
      case 'project':
        return 'text-green-600 bg-green-50 border-green-200';
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const handleToggleTodo = async (todoId) => {
    setIsUpdating(true);
    
    // Optimistic update
    const updatedTodos = todos.map(todo => 
      todo.id === todoId ? { ...todo, completed: !todo.completed } : todo
    );
    const newCompletedCount = updatedTodos.filter(t => t.completed).length;
    
    setTodos(updatedTodos);
    setCompletedCount(newCompletedCount);

    try {
      const response = await fetch('http://localhost:8000/api/learning/update-todo', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          todo_id: todoId,
          completed: !todos.find(t => t.id === todoId).completed
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to update todo');
      }

      const data = await response.json();
      console.log('Todo update response:', data);
      console.log('All completed:', data.all_completed);
      console.log('onAllCompleted callback exists:', !!onAllCompleted);
      
      // Check if all completed
      if (data.all_completed && onAllCompleted) {
        console.log('Calling onAllCompleted callback');
        onAllCompleted();
      }
    } catch (error) {
      console.error('Error updating todo:', error);
      // Revert optimistic update on error
      setTodos(todos);
      setCompletedCount(completedCount);
      alert('Failed to update todo. Please try again.');
    } finally {
      setIsUpdating(false);
    }
  };

  // Group todos by week
  const todosByWeek = todos.reduce((acc, todo) => {
    const week = todo.week || 'General';
    if (!acc[week]) {
      acc[week] = [];
    }
    acc[week].push(todo);
    return acc;
  }, {});

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="mb-6">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <CheckCircleIcon className="w-7 h-7 text-green-600" />
            Learning Progress Checklist
          </h2>
          <div className="text-right">
            <div className="text-sm text-gray-600">
              {completedCount} of {totalCount} completed
            </div>
            <div className="text-2xl font-bold text-green-600">
              {progressPercentage.toFixed(0)}%
            </div>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
          <div
            className="bg-gradient-to-r from-green-500 to-emerald-600 h-full transition-all duration-500 ease-out"
            style={{ width: `${progressPercentage}%` }}
          />
        </div>

        {progressPercentage === 100 && (
          <div className="mt-4 bg-green-50 border border-green-200 rounded-lg p-4">
            <p className="text-green-800 font-semibold flex items-center gap-2">
              <CheckCircleSolidIcon className="w-5 h-5" />
              Congratulations! You've completed all learning tasks. 
              You can now take the MCQ assessment below.
            </p>
          </div>
        )}
      </div>

      {/* Todo Items by Week */}
      <div className="space-y-6">
        {Object.entries(todosByWeek).map(([week, weekTodos]) => (
          <div key={week} className="border-l-4 border-blue-500 pl-4">
            <h3 className="text-lg font-semibold text-gray-800 mb-3">
              {typeof week === 'number' ? `Week ${week}` : week}
            </h3>
            <div className="space-y-2">
              {weekTodos.map((todo) => (
                <div
                  key={todo.id}
                  className={`flex items-start gap-3 p-3 rounded-lg border transition-all duration-200 ${
                    todo.completed 
                      ? 'bg-gray-50 border-gray-300 opacity-75' 
                      : `${getColorForType(todo.type)} border hover:shadow-md`
                  }`}
                >
                  <button
                    onClick={() => handleToggleTodo(todo.id)}
                    disabled={isUpdating}
                    className="flex-shrink-0 mt-0.5 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded"
                  >
                    {todo.completed ? (
                      <CheckCircleSolidIcon className="w-6 h-6 text-green-600" />
                    ) : (
                      <div className="w-6 h-6 rounded-full border-2 border-gray-400 hover:border-blue-600 transition-colors" />
                    )}
                  </button>

                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className={todo.completed ? 'text-gray-500' : ''}>
                        {getIconForType(todo.type)}
                      </span>
                      <h4 className={`font-semibold ${
                        todo.completed 
                          ? 'text-gray-500 line-through' 
                          : 'text-gray-900'
                      }`}>
                        {todo.title}
                      </h4>
                    </div>
                    {todo.description && (
                      <p className={`text-sm ${
                        todo.completed ? 'text-gray-400' : 'text-gray-600'
                      }`}>
                        {todo.description}
                      </p>
                    )}
                    <div className="mt-1">
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        todo.completed 
                          ? 'bg-green-100 text-green-700' 
                          : 'bg-gray-100 text-gray-600'
                      }`}>
                        {todo.type}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Tips */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h4 className="font-semibold text-blue-900 mb-2">💡 Tips</h4>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• Check off items as you complete them to track your progress</li>
            <li>• Complete all todos to unlock the MCQ assessment</li>
            <li>• Take your time and ensure you understand each topic before moving on</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
