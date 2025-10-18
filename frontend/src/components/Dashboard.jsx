import React, { useState } from 'react';
import { 
  MapIcon, 
  CommandLineIcon, 
  CalendarDaysIcon, 
  AcademicCapIcon, 
  BriefcaseIcon,
  ArrowRightIcon,
  SparklesIcon,
  ClockIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import TravelPlanner from './TravelPlanner';
import EventPlanner from './EventPlanner';
import TechPlannerComingSoon from './TechPlannerComingSoon';
import EventPlannerComingSoon from './EventPlannerComingSoon';
import LearningPlannerComingSoon from './LearningPlannerComingSoon';
import BusinessPlannerComingSoon from './BusinessPlannerComingSoon';

const Dashboard = () => {
  const [selectedAgent, setSelectedAgent] = useState(null);

  const agents = [
    {
      id: 'travel',
      title: 'Travel Planner Agent',
      description: 'Finds flights, hotels, activities, creates itineraries, optimizes budget',
      icon: MapIcon,
      color: 'from-blue-500 to-cyan-500',
      features: ['Flight Booking', 'Hotel Reservations', 'Itinerary Planning', 'Budget Optimization'],
      comingSoon: false
    },
    {
      id: 'tech',
      title: 'Tech Project Planner',
      description: 'Plan and manage software development projects with AI assistance',
      icon: CommandLineIcon,
      color: 'from-blue-500 to-indigo-600',
      features: ['Project Architecture', 'Sprint Planning', 'Code Review', 'Tech Stack Selection'],
      comingSoon: false
    },
    {
      id: 'event',
      title: 'Event Planner Agent',
      description: 'Handles vendors, guest lists, budget allocation, schedules',
      icon: CalendarDaysIcon,
      color: 'from-green-500 to-emerald-500',
      features: ['Vendor Management', 'Guest List Organization', 'Schedule Planning', 'Budget Tracking'],
      comingSoon: false
    },
    {
      id: 'learning',
      title: 'Learning Path Planner Agent',
      description: 'Creates study plans, recommends resources, evaluates progress',
      icon: AcademicCapIcon,
      color: 'from-orange-500 to-red-500',
      features: ['Study Plan Creation', 'Resource Recommendations', 'Progress Tracking', 'Skill Assessment'],
      comingSoon: true
    },
    {
      id: 'business',
      title: 'Business Startup Planner Agent',
      description: 'Builds business model, funding steps, marketing strategies',
      icon: BriefcaseIcon,
      color: 'from-indigo-500 to-purple-500',
      features: ['Business Model Canvas', 'Funding Strategy', 'Market Analysis', 'Growth Planning'],
      comingSoon: true
    }
  ];

  const stats = [
    { label: 'Active Agents', value: '5', icon: SparklesIcon },
    { label: 'Plans Created', value: '1,247', icon: CheckCircleIcon },
    { label: 'Average Planning Time', value: '3 min', icon: ClockIcon }
  ];

  if (selectedAgent === 'travel') {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <button
                onClick={() => setSelectedAgent(null)}
                className="flex items-center text-gray-600 hover:text-gray-900 transition-colors"
              >
                <ArrowRightIcon className="h-5 w-5 mr-2 rotate-180" />
                Back to Dashboard
              </button>
              <h1 className="text-xl font-semibold text-gray-900">Travel Planner Agent</h1>
            </div>
          </div>
        </div>
        <TravelPlanner />
      </div>
    );
  }

  if (selectedAgent === 'tech') {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <button
                onClick={() => setSelectedAgent(null)}
                className="flex items-center text-gray-600 hover:text-gray-900 transition-colors"
              >
                <ArrowRightIcon className="h-5 w-5 mr-2 rotate-180" />
                Back to Dashboard
              </button>
            </div>
          </div>
        </div>
        <TechPlannerComingSoon onBack={() => setSelectedAgent(null)} />
      </div>
    );
  }

  if (selectedAgent === 'event') {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <button
                onClick={() => setSelectedAgent(null)}
                className="flex items-center text-gray-600 hover:text-gray-900 transition-colors"
              >
                <ArrowRightIcon className="h-5 w-5 mr-2 rotate-180" />
                Back to Dashboard
              </button>
              <h1 className="text-xl font-semibold text-gray-900">Event Planner Agent</h1>
            </div>
          </div>
        </div>
        <EventPlanner />
      </div>
    );
  }

  if (selectedAgent === 'learning') {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <button
                onClick={() => setSelectedAgent(null)}
                className="flex items-center text-gray-600 hover:text-gray-900 transition-colors"
              >
                <ArrowRightIcon className="h-5 w-5 mr-2 rotate-180" />
                Back to Dashboard
              </button>
            </div>
          </div>
        </div>
        <LearningPlannerComingSoon />
      </div>
    );
  }

  if (selectedAgent === 'business') {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <button
                onClick={() => setSelectedAgent(null)}
                className="flex items-center text-gray-600 hover:text-gray-900 transition-colors"
              >
                <ArrowRightIcon className="h-5 w-5 mr-2 rotate-180" />
                Back to Dashboard
              </button>
            </div>
          </div>
        </div>
        <BusinessPlannerComingSoon />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      {/* Header */}
      <div className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-20">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <SparklesIcon className="h-6 w-6 text-white" />
                </div>
              </div>
              <div className="ml-4">
                <h1 className="text-2xl font-bold text-gray-900">AI Planner Hub</h1>
                <p className="text-sm text-gray-600">Multi-Agent Planning Platform</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                All Systems Online
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {stats.map((stat, index) => (
            <div key={index} className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <stat.icon className="h-8 w-8 text-blue-500" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Welcome Section */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Welcome to Your AI Planning Assistant
            </h2>
            <p className="text-lg text-gray-600 mb-6 max-w-3xl mx-auto">
              Choose from our specialized AI agents to create comprehensive plans for any domain. 
              Each agent is powered by advanced AI to deliver personalized, actionable planning solutions.
            </p>
            <div className="inline-flex items-center px-4 py-2 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
              <SparklesIcon className="h-4 w-4 mr-2" />
              Powered by Advanced AI Technology
            </div>
          </div>
        </div>

        {/* Agent Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {agents.map((agent) => (
            <div
              key={agent.id}
              className={`bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden group ${
                !agent.comingSoon ? 'cursor-pointer hover:scale-105' : 'opacity-75'
              }`}
              onClick={() => !agent.comingSoon && setSelectedAgent(agent.id)}
            >
              {/* Card Header */}
              <div className={`h-32 bg-gradient-to-r ${agent.color} relative`}>
                <div className="absolute inset-0 bg-black bg-opacity-10"></div>
                <div className="relative h-full flex items-center justify-center">
                  <agent.icon className="h-12 w-12 text-white" />
                </div>
                {agent.comingSoon && (
                  <div className="absolute top-4 right-4">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                      Coming Soon
                    </span>
                  </div>
                )}
              </div>

              {/* Card Content */}
              <div className="p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-2">{agent.title}</h3>
                <p className="text-gray-600 mb-4 line-clamp-2">{agent.description}</p>

                {/* Features */}
                <div className="space-y-2 mb-4">
                  {agent.features && agent.features.slice(0, 3).map((feature, index) => (
                    <div key={index} className="flex items-center text-sm text-gray-600">
                      <CheckCircleIcon className="h-4 w-4 text-green-500 mr-2 flex-shrink-0" />
                      {feature}
                    </div>
                  ))}
                  {agent.features && agent.features.length > 3 && (
                    <div className="text-sm text-gray-500">
                      +{agent.features.length - 3} more features
                    </div>
                  )}
                </div>

                {/* Action Button */}
                <div className="flex items-center justify-between">
                  {agent.comingSoon ? (
                    <span className="text-sm text-gray-500 font-medium">Available Soon</span>
                  ) : (
                    <button className="flex items-center text-blue-600 hover:text-blue-800 font-medium transition-colors group">
                      Get Started
                      <ArrowRightIcon className="h-4 w-4 ml-1 group-hover:translate-x-1 transition-transform" />
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Footer Info */}
        <div className="mt-12 text-center">
          <div className="bg-white rounded-xl shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">How It Works</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm text-gray-600">
              <div className="flex flex-col items-center">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mb-2">
                  <span className="text-blue-600 font-bold">1</span>
                </div>
                <p>Choose your planning domain</p>
              </div>
              <div className="flex flex-col items-center">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mb-2">
                  <span className="text-blue-600 font-bold">2</span>
                </div>
                <p>Provide your requirements</p>
              </div>
              <div className="flex flex-col items-center">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mb-2">
                  <span className="text-blue-600 font-bold">3</span>
                </div>
                <p>Get your AI-generated plan</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
