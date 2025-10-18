import React from 'react';
import { 
  CodeBracketIcon, 
  CalendarDaysIcon, 
  AcademicCapIcon, 
  BriefcaseIcon,
  ClockIcon,
  BellIcon
} from '@heroicons/react/24/outline';

const ComingSoonPlanner = ({ agentType, title, description, features, color, icon: Icon }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      {/* Header */}
      <div className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-20">
            <div className="flex items-center">
              <div className={`w-12 h-12 bg-gradient-to-r ${color} rounded-lg flex items-center justify-center`}>
                <Icon className="h-7 w-7 text-white" />
              </div>
              <div className="ml-4">
                <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
                <p className="text-sm text-gray-600">{description}</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                <ClockIcon className="h-4 w-4 mr-1" />
                Coming Soon
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Main Content */}
        <div className="text-center mb-12">
          <div className={`w-24 h-24 bg-gradient-to-r ${color} rounded-full flex items-center justify-center mx-auto mb-6`}>
            <Icon className="h-12 w-12 text-white" />
          </div>
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            {title} is Coming Soon!
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            We're working hard to bring you the most advanced AI-powered planning experience. 
            Stay tuned for the launch of this exciting feature.
          </p>
        </div>

        {/* Features Preview */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">What to Expect</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {features.map((feature, index) => (
              <div key={index} className="flex items-start">
                <div className={`w-8 h-8 bg-gradient-to-r ${color} rounded-lg flex items-center justify-center flex-shrink-0`}>
                  <span className="text-white font-bold text-sm">{index + 1}</span>
                </div>
                <div className="ml-4">
                  <h4 className="font-semibold text-gray-900">{feature.title}</h4>
                  <p className="text-gray-600 text-sm">{feature.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Notification Signup */}
        <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
          <BellIcon className="h-12 w-12 text-blue-500 mx-auto mb-4" />
          <h3 className="text-2xl font-bold text-gray-900 mb-4">Get Notified When It's Ready</h3>
          <p className="text-gray-600 mb-6">
            Be the first to know when {title.toLowerCase()} launches. We'll send you an email as soon as it's available.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
            <input
              type="email"
              placeholder="Enter your email"
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <button className={`px-6 py-3 bg-gradient-to-r ${color} text-white rounded-lg font-medium hover:opacity-90 transition-opacity`}>
              Notify Me
            </button>
          </div>
        </div>

        {/* Timeline */}
        <div className="mt-12 text-center">
          <h3 className="text-xl font-bold text-gray-900 mb-6">Development Timeline</h3>
          <div className="bg-white rounded-xl shadow-md p-6">
            <div className="flex items-center justify-center space-x-8">
              <div className="text-center">
                <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center mb-2">
                  <span className="text-white font-bold">✓</span>
                </div>
                <p className="text-sm font-medium text-gray-900">Planning</p>
                <p className="text-xs text-gray-500">Completed</p>
              </div>
              <div className="w-16 h-1 bg-blue-200 rounded"></div>
              <div className="text-center">
                <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center mb-2">
                  <span className="text-white font-bold">2</span>
                </div>
                <p className="text-sm font-medium text-gray-900">Development</p>
                <p className="text-xs text-gray-500">In Progress</p>
              </div>
              <div className="w-16 h-1 bg-gray-200 rounded"></div>
              <div className="text-center">
                <div className="w-12 h-12 bg-gray-300 rounded-full flex items-center justify-center mb-2">
                  <span className="text-gray-600 font-bold">3</span>
                </div>
                <p className="text-sm font-medium text-gray-900">Testing</p>
                <p className="text-xs text-gray-500">Upcoming</p>
              </div>
              <div className="w-16 h-1 bg-gray-200 rounded"></div>
              <div className="text-center">
                <div className="w-12 h-12 bg-gray-300 rounded-full flex items-center justify-center mb-2">
                  <span className="text-gray-600 font-bold">4</span>
                </div>
                <p className="text-sm font-medium text-gray-900">Launch</p>
                <p className="text-xs text-gray-500">Q1 2025</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Specific agent configurations
export const TechPlannerComingSoon = () => (
  <ComingSoonPlanner
    agentType="tech"
    title="Tech Project Planner Agent"
    description="Creates development roadmaps, suggests tools/frameworks, sets milestones"
    color="from-purple-500 to-pink-500"
    icon={CodeBracketIcon}
    features={[
      {
        title: "Intelligent Roadmap Creation",
        description: "AI-powered project timelines based on your tech stack and team size"
      },
      {
        title: "Technology Stack Recommendations",
        description: "Get personalized suggestions for frameworks, tools, and libraries"
      },
      {
        title: "Milestone & Sprint Planning",
        description: "Automated sprint planning with realistic time estimates"
      },
      {
        title: "Resource Allocation",
        description: "Optimize team assignments and workload distribution"
      },
      {
        title: "Risk Assessment",
        description: "Identify potential blockers and dependencies early"
      },
      {
        title: "Progress Tracking",
        description: "Real-time project monitoring with automated reporting"
      }
    ]}
  />
);

export const EventPlannerComingSoon = () => (
  <ComingSoonPlanner
    agentType="event"
    title="Event Planner Agent"
    description="Handles vendors, guest lists, budget allocation, schedules"
    color="from-green-500 to-emerald-500"
    icon={CalendarDaysIcon}
    features={[
      {
        title: "Vendor Management",
        description: "Find, compare, and manage vendors for catering, venues, and services"
      },
      {
        title: "Guest List Organization",
        description: "Smart guest management with RSVP tracking and dietary preferences"
      },
      {
        title: "Budget Planning & Tracking",
        description: "Automated budget allocation with real-time expense monitoring"
      },
      {
        title: "Timeline Coordination",
        description: "Create detailed event schedules with automated reminders"
      },
      {
        title: "Venue Selection",
        description: "AI-powered venue recommendations based on your requirements"
      },
      {
        title: "Logistics Management",
        description: "Coordinate transportation, setup, and breakdown activities"
      }
    ]}
  />
);

export const LearningPlannerComingSoon = () => (
  <ComingSoonPlanner
    agentType="learning"
    title="Learning Path Planner Agent"
    description="Creates study plans, recommends resources, evaluates progress"
    color="from-orange-500 to-red-500"
    icon={AcademicCapIcon}
    features={[
      {
        title: "Personalized Study Plans",
        description: "Custom learning paths based on your goals and learning style"
      },
      {
        title: "Resource Recommendations",
        description: "Curated courses, books, and materials from top platforms"
      },
      {
        title: "Progress Tracking",
        description: "Monitor your learning journey with detailed analytics"
      },
      {
        title: "Skill Assessment",
        description: "Regular evaluations to measure your progress and identify gaps"
      },
      {
        title: "Schedule Optimization",
        description: "Smart scheduling that adapts to your availability and pace"
      },
      {
        title: "Community Integration",
        description: "Connect with study groups and mentors in your field"
      }
    ]}
  />
);

export const BusinessPlannerComingSoon = () => (
  <ComingSoonPlanner
    agentType="business"
    title="Business Startup Planner Agent"
    description="Builds business model, funding steps, marketing strategies"
    color="from-indigo-500 to-purple-500"
    icon={BriefcaseIcon}
    features={[
      {
        title: "Business Model Canvas",
        description: "Interactive canvas creation with AI-powered insights and validation"
      },
      {
        title: "Funding Strategy",
        description: "Personalized funding roadmap with investor matching"
      },
      {
        title: "Market Analysis",
        description: "Comprehensive market research and competitive analysis"
      },
      {
        title: "Financial Projections",
        description: "Automated financial modeling with scenario planning"
      },
      {
        title: "Marketing Strategy",
        description: "Data-driven marketing plans with channel recommendations"
      },
      {
        title: "Legal & Compliance",
        description: "Guidance on business structure, permits, and regulations"
      }
    ]}
  />
);

export default ComingSoonPlanner;
