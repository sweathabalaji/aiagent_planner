import React from 'react';
import { AcademicCapIcon, BookOpenIcon, ClockIcon } from '@heroicons/react/24/outline';

const LearningPlannerComingSoon = () => {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center">
        <div className="flex justify-center mb-8">
          <div className="p-6 bg-green-100 rounded-full">
            <AcademicCapIcon className="h-16 w-16 text-green-600" />
          </div>
        </div>
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Learning Path Planner</h1>
        <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
          Design personalized learning journeys with AI-powered curriculum planning. 
          From skill development to certification paths, get intelligent study plans tailored to your goals.
        </p>
        
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <BookOpenIcon className="h-8 w-8 text-green-600 mb-4 mx-auto" />
            <h3 className="font-semibold text-gray-900 mb-2">Curriculum Design</h3>
            <p className="text-gray-600 text-sm">AI-generated learning paths and resource recommendations</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <ClockIcon className="h-8 w-8 text-green-600 mb-4 mx-auto" />
            <h3 className="font-semibold text-gray-900 mb-2">Progress Tracking</h3>
            <p className="text-gray-600 text-sm">Smart milestone tracking and adaptive scheduling</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <AcademicCapIcon className="h-8 w-8 text-green-600 mb-4 mx-auto" />
            <h3 className="font-semibold text-gray-900 mb-2">Skill Assessment</h3>
            <p className="text-gray-600 text-sm">Personalized assessments and learning gap analysis</p>
          </div>
        </div>

        <div className="bg-green-50 border border-green-200 rounded-lg p-8">
          <h2 className="text-2xl font-semibold text-green-900 mb-4">Coming Soon!</h2>
          <p className="text-green-700 mb-6">
            We're building an intelligent learning companion that adapts to your pace and style. 
            This agent will create personalized study plans and track your progress toward mastery.
          </p>
          <button 
            disabled 
            className="bg-green-200 text-green-500 px-6 py-3 rounded-lg font-medium cursor-not-allowed"
          >
            Available Soon
          </button>
        </div>
      </div>
    </div>
  );
};

export default LearningPlannerComingSoon;
