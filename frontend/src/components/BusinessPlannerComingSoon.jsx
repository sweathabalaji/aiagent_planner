import React from 'react';
import { BriefcaseIcon, ChartBarIcon, LightBulbIcon } from '@heroicons/react/24/outline';

const BusinessPlannerComingSoon = () => {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center">
        <div className="flex justify-center mb-8">
          <div className="p-6 bg-orange-100 rounded-full">
            <BriefcaseIcon className="h-16 w-16 text-orange-600" />
          </div>
        </div>
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Business Startup Planner</h1>
        <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
          Launch your startup with AI-powered business planning assistance. 
          From market analysis to financial projections, get intelligent insights for your entrepreneurial journey.
        </p>
        
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <LightBulbIcon className="h-8 w-8 text-orange-600 mb-4 mx-auto" />
            <h3 className="font-semibold text-gray-900 mb-2">Business Model</h3>
            <p className="text-gray-600 text-sm">AI-generated business model canvas and strategy</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <ChartBarIcon className="h-8 w-8 text-orange-600 mb-4 mx-auto" />
            <h3 className="font-semibold text-gray-900 mb-2">Market Analysis</h3>
            <p className="text-gray-600 text-sm">Intelligent market research and competitor analysis</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <BriefcaseIcon className="h-8 w-8 text-orange-600 mb-4 mx-auto" />
            <h3 className="font-semibold text-gray-900 mb-2">Financial Planning</h3>
            <p className="text-gray-600 text-sm">Smart financial projections and funding strategies</p>
          </div>
        </div>

        <div className="bg-orange-50 border border-orange-200 rounded-lg p-8">
          <h2 className="text-2xl font-semibold text-orange-900 mb-4">Coming Soon!</h2>
          <p className="text-orange-700 mb-6">
            We're creating the ultimate entrepreneurial companion with AI-driven insights. 
            This agent will guide you through every step of launching and scaling your startup.
          </p>
          <button 
            disabled 
            className="bg-orange-200 text-orange-500 px-6 py-3 rounded-lg font-medium cursor-not-allowed"
          >
            Available Soon
          </button>
        </div>
      </div>
    </div>
  );
};

export default BusinessPlannerComingSoon;
