import { useState } from 'react';
import { AcademicCapIcon, ClockIcon, ChartBarIcon, LightBulbIcon } from '@heroicons/react/24/outline';

export default function LearningForm({ onSubmit, isLoading }) {
  const [formData, setFormData] = useState({
    topic: '',
    skill_level: 'Beginner',
    duration_weeks: 8,
    learning_goals: '',
    time_per_week: 10
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6 space-y-6">
        {/* Header */}
        <div className="border-b border-gray-200 pb-4">
          <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <AcademicCapIcon className="w-7 h-7 text-purple-600" />
            Create Your Learning Path
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Get a personalized study plan with real courses, books, and resources
          </p>
        </div>

        {/* Topic Input */}
        <div>
          <label htmlFor="topic" className="block text-sm font-medium text-gray-700 mb-2">
            <LightBulbIcon className="w-5 h-5 inline mr-1 text-yellow-500" />
            What do you want to learn?
          </label>
          <input
            type="text"
            id="topic"
            name="topic"
            value={formData.topic}
            onChange={handleChange}
            placeholder="e.g., Python Programming, Machine Learning, Web Development"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            required
          />
          <p className="mt-1 text-sm text-gray-500">
            Be specific for better recommendations
          </p>
        </div>

        {/* Skill Level */}
        <div>
          <label htmlFor="skill_level" className="block text-sm font-medium text-gray-700 mb-2">
            <ChartBarIcon className="w-5 h-5 inline mr-1 text-blue-500" />
            Current Skill Level
          </label>
          <select
            id="skill_level"
            name="skill_level"
            value={formData.skill_level}
            onChange={handleChange}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            required
          >
            <option value="Beginner">Beginner - Just starting out</option>
            <option value="Intermediate">Intermediate - Some experience</option>
            <option value="Advanced">Advanced - Looking to master</option>
          </select>
        </div>

        {/* Duration and Time Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Duration */}
          <div>
            <label htmlFor="duration_weeks" className="block text-sm font-medium text-gray-700 mb-2">
              <ClockIcon className="w-5 h-5 inline mr-1 text-green-500" />
              Learning Duration
            </label>
            <div className="space-y-2">
              <input
                type="range"
                id="duration_weeks"
                name="duration_weeks"
                min="1"
                max="52"
                value={formData.duration_weeks}
                onChange={handleChange}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-purple-600"
              />
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">1 week</span>
                <span className="text-lg font-semibold text-purple-600">
                  {formData.duration_weeks} weeks
                </span>
                <span className="text-sm text-gray-600">52 weeks</span>
              </div>
            </div>
          </div>

          {/* Time Per Week */}
          <div>
            <label htmlFor="time_per_week" className="block text-sm font-medium text-gray-700 mb-2">
              <ClockIcon className="w-5 h-5 inline mr-1 text-orange-500" />
              Time Per Week
            </label>
            <div className="space-y-2">
              <input
                type="range"
                id="time_per_week"
                name="time_per_week"
                min="1"
                max="40"
                value={formData.time_per_week}
                onChange={handleChange}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-purple-600"
              />
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">1 hour</span>
                <span className="text-lg font-semibold text-purple-600">
                  {formData.time_per_week} hours/week
                </span>
                <span className="text-sm text-gray-600">40 hours</span>
              </div>
            </div>
          </div>
        </div>

        {/* Learning Goals */}
        <div>
          <label htmlFor="learning_goals" className="block text-sm font-medium text-gray-700 mb-2">
            🎯 Learning Goals & Objectives
          </label>
          <textarea
            id="learning_goals"
            name="learning_goals"
            value={formData.learning_goals}
            onChange={handleChange}
            rows="4"
            placeholder="What do you want to achieve? What projects do you want to build? What skills do you need for your career?"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
            required
          />
          <p className="mt-1 text-sm text-gray-500">
            Describe your goals, career aspirations, or specific projects you want to work on
          </p>
        </div>

        {/* Summary Card */}
        <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-4 border border-purple-200">
          <h3 className="font-semibold text-gray-900 mb-2">📊 Learning Plan Summary</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
            <div>
              <span className="text-gray-600">Total Hours:</span>
              <p className="font-semibold text-purple-700">
                {formData.duration_weeks * formData.time_per_week}h
              </p>
            </div>
            <div>
              <span className="text-gray-600">Duration:</span>
              <p className="font-semibold text-purple-700">
                {formData.duration_weeks} weeks
              </p>
            </div>
            <div>
              <span className="text-gray-600">Weekly Time:</span>
              <p className="font-semibold text-purple-700">
                {formData.time_per_week}h
              </p>
            </div>
            <div>
              <span className="text-gray-600">Level:</span>
              <p className="font-semibold text-purple-700">
                {formData.skill_level}
              </p>
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading}
          className={`w-full py-4 px-6 rounded-lg font-semibold text-white transition-all duration-200 flex items-center justify-center gap-2 ${
            isLoading
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5'
          }`}
        >
          {isLoading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
              Generating Your Learning Path...
            </>
          ) : (
            <>
              <AcademicCapIcon className="w-6 h-6" />
              Generate Learning Path
            </>
          )}
        </button>
      </div>

      {/* Tips Section */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="font-semibold text-blue-900 mb-2 flex items-center gap-2">
          💡 Tips for Better Results
        </h3>
        <ul className="text-sm text-blue-800 space-y-1 list-disc list-inside">
          <li>Be specific about your topic (e.g., "React.js Frontend Development" vs "Programming")</li>
          <li>Set realistic time commitments you can maintain consistently</li>
          <li>Clearly describe your end goals and what you want to build</li>
          <li>Consider your schedule - it's better to study regularly than in long bursts</li>
        </ul>
      </div>
    </form>
  );
}
