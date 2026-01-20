import { useState } from 'react';
import { 
  BriefcaseIcon, 
  BuildingOfficeIcon, 
  UsersIcon, 
  CurrencyDollarIcon,
  MapPinIcon,
  LightBulbIcon 
} from '@heroicons/react/24/outline';

export default function BusinessForm({ onSubmit, isLoading }) {
  const [formData, setFormData] = useState({
    business_idea: '',
    industry: 'Technology',
    target_market: '',
    business_model: 'B2B SaaS',
    funding_needed: '₹40L',
    location: ''
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
            <BriefcaseIcon className="w-7 h-7 text-blue-600" />
            Build Your Business Plan
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Get a comprehensive startup plan with business model canvas, funding strategy, and market analysis
          </p>
        </div>

        {/* Business Idea */}
        <div>
          <label htmlFor="business_idea" className="block text-sm font-medium text-gray-700 mb-2">
            <LightBulbIcon className="w-5 h-5 inline mr-1 text-yellow-500" />
            Business Idea <span className="text-red-500">*</span>
          </label>
          <textarea
            id="business_idea"
            name="business_idea"
            value={formData.business_idea}
            onChange={handleChange}
            rows="4"
            placeholder="Describe your business idea: What problem does it solve? What makes it unique? Who are your customers?"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            required
          />
          <p className="mt-1 text-sm text-gray-500">
            Be specific about the value proposition and target problem
          </p>
        </div>

        {/* Industry and Business Model Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Industry */}
          <div>
            <label htmlFor="industry" className="block text-sm font-medium text-gray-700 mb-2">
              <BuildingOfficeIcon className="w-5 h-5 inline mr-1 text-purple-500" />
              Industry Sector <span className="text-red-500">*</span>
            </label>
            <select
              id="industry"
              name="industry"
              value={formData.industry}
              onChange={handleChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            >
              <option value="Technology">Technology</option>
              <option value="Healthcare">Healthcare</option>
              <option value="E-commerce">E-commerce</option>
              <option value="FinTech">FinTech</option>
              <option value="Education">Education</option>
              <option value="Food & Beverage">Food & Beverage</option>
              <option value="Real Estate">Real Estate</option>
              <option value="Manufacturing">Manufacturing</option>
              <option value="Retail">Retail</option>
              <option value="Consulting">Consulting</option>
              <option value="Entertainment">Entertainment</option>
              <option value="Marketing">Marketing</option>
              <option value="Logistics">Logistics</option>
              <option value="Energy">Energy</option>
              <option value="Other">Other</option>
            </select>
          </div>

          {/* Business Model */}
          <div>
            <label htmlFor="business_model" className="block text-sm font-medium text-gray-700 mb-2">
              <BriefcaseIcon className="w-5 h-5 inline mr-1 text-green-500" />
              Business Model <span className="text-red-500">*</span>
            </label>
            <select
              id="business_model"
              name="business_model"
              value={formData.business_model}
              onChange={handleChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            >
              <option value="B2B SaaS">B2B SaaS (Software as a Service)</option>
              <option value="B2C SaaS">B2C SaaS</option>
              <option value="B2B Marketplace">B2B Marketplace</option>
              <option value="B2C Marketplace">B2C Marketplace</option>
              <option value="E-commerce">E-commerce (Direct to Consumer)</option>
              <option value="Subscription">Subscription Service</option>
              <option value="Freemium">Freemium Model</option>
              <option value="Agency">Agency/Service Business</option>
              <option value="Affiliate">Affiliate/Commission Based</option>
              <option value="Advertising">Advertising Supported</option>
              <option value="Licensing">Licensing/Franchise</option>
              <option value="Hardware">Hardware Sales</option>
              <option value="Hybrid">Hybrid Model</option>
            </select>
          </div>
        </div>

        {/* Target Market */}
        <div>
          <label htmlFor="target_market" className="block text-sm font-medium text-gray-700 mb-2">
            <UsersIcon className="w-5 h-5 inline mr-1 text-blue-500" />
            Target Market <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            id="target_market"
            name="target_market"
            value={formData.target_market}
            onChange={handleChange}
            placeholder="e.g., Small businesses with 10-50 employees, Millennials interested in fitness, Enterprise companies"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required
          />
          <p className="mt-1 text-sm text-gray-500">
            Define your ideal customer segment with demographics or firmographics
          </p>
        </div>

        {/* Funding and Location Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Funding Needed */}
          <div>
            <label htmlFor="funding_needed" className="block text-sm font-medium text-gray-700 mb-2">
              <CurrencyDollarIcon className="w-5 h-5 inline mr-1 text-emerald-500" />
              Funding Needed <span className="text-red-500">*</span>
            </label>
            <select
              id="funding_needed"
              name="funding_needed"
              value={formData.funding_needed}
              onChange={handleChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            >
              <option value="Bootstrapped">Bootstrapped / Self-Funded</option>
              <option value="₹5L">₹5L - ₹10L</option>
              <option value="₹10L">₹10L - ₹25L</option>
              <option value="₹40L">₹40L - ₹1Cr</option>
              <option value="₹1Cr">₹1Cr - ₹5Cr</option>
              <option value="₹5Cr">₹5Cr - ₹10Cr</option>
              <option value="₹10Cr+">₹10Cr+</option>
            </select>
          </div>

          {/* Location */}
          <div>
            <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-2">
              <MapPinIcon className="w-5 h-5 inline mr-1 text-red-500" />
              Business Location <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              id="location"
              name="location"
              value={formData.location}
              onChange={handleChange}
              placeholder="e.g., San Francisco, CA or Remote/Global"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
            <p className="mt-1 text-sm text-gray-500">
              City, state, or region where you'll operate
            </p>
          </div>
        </div>

        {/* Info Box */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex gap-3">
            <div className="flex-shrink-0">
              <svg className="w-5 h-5 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="flex-1">
              <h4 className="text-sm font-medium text-blue-900 mb-1">What You'll Receive</h4>
              <ul className="text-sm text-blue-800 space-y-1">
                <li>✓ Business Model Canvas with all 9 building blocks</li>
                <li>✓ Comprehensive funding strategy with investor targeting</li>
                <li>✓ Market analysis with TAM/SAM/SOM calculations</li>
                <li>✓ Competitive analysis and SWOT breakdown</li>
                <li>✓ 3-year financial projections</li>
                <li>✓ Go-to-market strategy and growth tactics</li>
                <li>✓ Actionable next steps with timeline</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold py-4 px-6 rounded-lg hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl"
        >
          {isLoading ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Creating Your Business Plan...
            </span>
          ) : (
            <span className="flex items-center justify-center gap-2">
              <BriefcaseIcon className="w-5 h-5" />
              Generate Business Plan
            </span>
          )}
        </button>

        {/* Disclaimer */}
        <p className="text-xs text-gray-500 text-center">
          This AI-generated plan is for guidance purposes. Consult with professionals for legal and financial advice.
        </p>
      </div>
    </form>
  );
}
