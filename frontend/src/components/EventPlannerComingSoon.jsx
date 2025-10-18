import React from 'react';
import { CalendarDaysIcon, UserGroupIcon, MapPinIcon } from '@heroicons/react/24/outline';

const EventPlannerComingSoon = () => {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center">
        <div className="flex justify-center mb-8">
          <div className="p-6 bg-purple-100 rounded-full">
            <CalendarDaysIcon className="h-16 w-16 text-purple-600" />
          </div>
        </div>
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Event Planner</h1>
        <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
          Create memorable events with AI-powered planning assistance. 
          From corporate conferences to personal celebrations, get intelligent recommendations and logistics support.
        </p>
        
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <CalendarDaysIcon className="h-8 w-8 text-purple-600 mb-4 mx-auto" />
            <h3 className="font-semibold text-gray-900 mb-2">Timeline Planning</h3>
            <p className="text-gray-600 text-sm">AI-generated event timelines and milestone tracking</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <UserGroupIcon className="h-8 w-8 text-purple-600 mb-4 mx-auto" />
            <h3 className="font-semibold text-gray-900 mb-2">Guest Management</h3>
            <p className="text-gray-600 text-sm">Smart invitation and RSVP management system</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <MapPinIcon className="h-8 w-8 text-purple-600 mb-4 mx-auto" />
            <h3 className="font-semibold text-gray-900 mb-2">Venue Selection</h3>
            <p className="text-gray-600 text-sm">Find and compare perfect venues for your event</p>
          </div>
        </div>

        <div className="bg-purple-50 border border-purple-200 rounded-lg p-8">
          <h2 className="text-2xl font-semibold text-purple-900 mb-4">Coming Soon!</h2>
          <p className="text-purple-700 mb-6">
            We're designing the ultimate event planning experience with AI assistance. 
            This agent will help you create unforgettable events with intelligent planning and coordination.
          </p>
          <button 
            disabled 
            className="bg-purple-200 text-purple-500 px-6 py-3 rounded-lg font-medium cursor-not-allowed"
          >
            Available Soon
          </button>
        </div>
      </div>
    </div>
  );
};

export default EventPlannerComingSoon;
