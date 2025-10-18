import React, { useState } from 'react'
import { Code, GitBranch, Users, CheckCircle, Clock, Target, ArrowLeft, Send } from 'lucide-react'

const TechPlanner = ({ onBack }) => {
  const [formData, setFormData] = useState({
    project_name: '',
    project_description: '',
    project_type: 'web',
    tech_stack: [],
    timeline: '',
    team_size: 3,
    complexity: 'medium',
    features: [],
    budget_range: ''
  })
  
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [selectedTemplate, setSelectedTemplate] = useState(null)

  const projectTypes = [
    { id: 'web', name: 'Web Application', icon: '🌐' },
    { id: 'mobile', name: 'Mobile App', icon: '📱' },
    { id: 'desktop', name: 'Desktop App', icon: '💻' },
    { id: 'ai', name: 'AI/ML Project', icon: '🤖' },
    { id: 'blockchain', name: 'Blockchain', icon: '⛓️' },
    { id: 'microservices', name: 'Microservices', icon: '🔗' }
  ]

  const techOptions = [
    'React', 'Vue.js', 'Angular', 'Node.js', 'Python', 'Django', 'FastAPI', 'Flask',
    'MongoDB', 'PostgreSQL', 'MySQL', 'Redis', 'Docker', 'Kubernetes', 'AWS', 'Azure'
  ]

  const commonFeatures = [
    'User Authentication', 'Dashboard', 'API Integration', 'Database Management',
    'File Upload', 'Search Functionality', 'Real-time Updates', 'Admin Panel',
    'Payment Processing', 'Email Notifications', 'Data Analytics', 'Mobile Responsive'
  ]

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const handleTechStackChange = (tech) => {
    setFormData(prev => ({
      ...prev,
      tech_stack: prev.tech_stack.includes(tech)
        ? prev.tech_stack.filter(t => t !== tech)
        : [...prev.tech_stack, tech]
    }))
  }

  const handleFeatureChange = (feature) => {
    setFormData(prev => ({
      ...prev,
      features: prev.features.includes(feature)
        ? prev.features.filter(f => f !== feature)
        : [...prev.features, feature]
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      const response = await fetch('/api/tech/plan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      })
      
      if (response.ok) {
        const data = await response.json()
        setResults(data)
      } else {
        throw new Error('Failed to create project plan')
      }
    } catch (error) {
      console.error('Error:', error)
      alert('Error creating project plan. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  if (results) {
    return <TechPlanResults results={results} onBack={() => setResults(null)} onPlanAnother={() => {
      setResults(null)
      setFormData({
        project_name: '',
        project_description: '',
        project_type: 'web',
        tech_stack: [],
        timeline: '',
        team_size: 3,
        complexity: 'medium',
        features: [],
        budget_range: ''
      })
    }} />
  }

  return (
    <div className="max-w-4xl mx-auto animate-fade-in">
      {/* Header */}
      <div className="card mb-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 flex items-center">
              <Code className="h-8 w-8 mr-3 text-blue-600" />
              Tech Project Planner
            </h1>
            <p className="text-gray-600 mt-2">AI-powered software development planning</p>
          </div>
          <button onClick={onBack} className="btn-secondary flex items-center">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back
          </button>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Project Basics */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Project Basics</h2>
          
          <div className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="label">Project Name</label>
                <input
                  type="text"
                  value={formData.project_name}
                  onChange={(e) => handleInputChange('project_name', e.target.value)}
                  className="input-field"
                  placeholder="My Awesome Project"
                  required
                />
              </div>
              
              <div>
                <label className="label">Timeline</label>
                <input
                  type="text"
                  value={formData.timeline}
                  onChange={(e) => handleInputChange('timeline', e.target.value)}
                  className="input-field"
                  placeholder="12 weeks"
                  required
                />
              </div>
            </div>

            <div>
              <label className="label">Project Description</label>
              <textarea
                value={formData.project_description}
                onChange={(e) => handleInputChange('project_description', e.target.value)}
                className="input-field"
                placeholder="Describe how your project works, its main purpose, key functionality, and what problem it solves. This helps the AI provide better recommendations."
                rows="4"
                required
              />
              <p className="text-sm text-gray-500 mt-1">
                Provide a detailed description to get more accurate AI recommendations and project analysis.
              </p>
            </div>
          </div>
        </div>

        {/* Project Type */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Project Type</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {projectTypes.map(type => (
              <button
                key={type.id}
                type="button"
                onClick={() => handleInputChange('project_type', type.id)}
                className={`p-4 rounded-lg border-2 transition-all text-center ${
                  formData.project_type === type.id
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-blue-300'
                }`}
              >
                <div className="text-2xl mb-2">{type.icon}</div>
                <div className="font-medium">{type.name}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Tech Stack */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Tech Stack</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {techOptions.map(tech => (
              <button
                key={tech}
                type="button"
                onClick={() => handleTechStackChange(tech)}
                className={`p-3 rounded-lg border transition-all text-sm ${
                  formData.tech_stack.includes(tech)
                    ? 'border-blue-500 bg-blue-50 text-blue-700'
                    : 'border-gray-200 hover:border-blue-300'
                }`}
              >
                {tech}
              </button>
            ))}
          </div>
        </div>

        {/* Project Details */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Project Details</h2>
          
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="label">Team Size</label>
              <select
                value={formData.team_size}
                onChange={(e) => handleInputChange('team_size', parseInt(e.target.value))}
                className="input-field"
              >
                <option value={1}>1 person (Solo)</option>
                <option value={2}>2 people</option>
                <option value={3}>3 people</option>
                <option value={5}>5 people</option>
                <option value={8}>8+ people</option>
              </select>
            </div>
            
            <div>
              <label className="label">Complexity</label>
              <select
                value={formData.complexity}
                onChange={(e) => handleInputChange('complexity', e.target.value)}
                className="input-field"
              >
                <option value="simple">Simple</option>
                <option value="medium">Medium</option>
                <option value="complex">Complex</option>
              </select>
            </div>

            <div className="md:col-span-2">
              <label className="label">Budget Range (Optional)</label>
              <input
                type="text"
                value={formData.budget_range}
                onChange={(e) => handleInputChange('budget_range', e.target.value)}
                className="input-field"
                placeholder="e.g., $10,000 - $50,000"
              />
            </div>
          </div>
        </div>

        {/* Features */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Key Features</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {commonFeatures.map(feature => (
              <button
                key={feature}
                type="button"
                onClick={() => handleFeatureChange(feature)}
                className={`p-3 rounded-lg border transition-all text-sm text-left ${
                  formData.features.includes(feature)
                    ? 'border-green-500 bg-green-50 text-green-700'
                    : 'border-gray-200 hover:border-green-300'
                }`}
              >
                {feature}
              </button>
            ))}
          </div>
        </div>

        {/* Submit */}
        <div className="card">
          <button
            type="submit"
            disabled={loading || !formData.project_name || !formData.project_description || formData.tech_stack.length === 0}
            className="btn-primary w-full py-4 text-lg flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-3"></div>
                Creating AI-Powered Plan...
              </>
            ) : (
              <>
                <Send className="h-5 w-5 mr-3" />
                Create AI-Powered Project Plan
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  )
}

// Results Component
const TechPlanResults = ({ results, onBack, onPlanAnother }) => {
  const [activeTab, setActiveTab] = useState('overview')

  // Function to parse the agent's final answer into structured sections
  const parseAgentFinalAnswer = (agentResult) => {
    if (!agentResult || typeof agentResult !== 'string') return null;
    
    const sections = {};
    
    // Parse different section patterns from the agent output
    const lines = agentResult.split('\n');
    let currentSection = null;
    let currentContent = [];
    
    for (const line of lines) {
      // Detect major section headers with more flexible patterns
      if (line.includes('## 1. PROJECT ABSTRACT') || line.includes('## PROJECT OVERVIEW') || line.includes('PROJECT ABSTRACT') || line.includes('PROJECT OVERVIEW')) {
        if (currentSection) sections[currentSection] = currentContent.join('\n');
        currentSection = 'projectAbstract';
        currentContent = [];
      } else if (line.includes('## 2. RESEARCH INSIGHTS') || line.includes('## RESEARCH ANALYSIS') || line.includes('RESEARCH INSIGHTS') || line.includes('RESEARCH ANALYSIS')) {
        if (currentSection) sections[currentSection] = currentContent.join('\n');
        currentSection = 'researchInsights';
        currentContent = [];
      } else if (line.includes('## 3. ARCHITECTURE RECOMMENDATIONS') || line.includes('## SYSTEM ARCHITECTURE') || line.includes('ARCHITECTURE RECOMMENDATIONS') || line.includes('SYSTEM ARCHITECTURE') || line.includes('## ARCHITECTURE') || line.includes('ARCHITECTURE PATTERNS')) {
        if (currentSection) sections[currentSection] = currentContent.join('\n');
        currentSection = 'architectureRecommendations';
        currentContent = [];
      } else if (line.includes('## 4. IMPLEMENTATION ROADMAP') || line.includes('## AI SUGGESTIONS') || line.includes('## DEVELOPMENT PLAN') || line.includes('IMPLEMENTATION ROADMAP') || line.includes('AI SUGGESTIONS') || line.includes('DEVELOPMENT PLAN')) {
        if (currentSection) sections[currentSection] = currentContent.join('\n');
        currentSection = 'implementationRoadmap';
        currentContent = [];
      } else if (line.includes('## TECHNOLOGY STACK') || line.includes('## TECH STACK') || line.includes('TECHNOLOGY STACK') || line.includes('TECH STACK') || line.includes('## TECH RECOMMENDATIONS')) {
        if (currentSection) sections[currentSection] = currentContent.join('\n');
        currentSection = 'techStack';
        currentContent = [];
      } else if (line.includes('## CODE EXAMPLES') || line.includes('## SAMPLE CODE') || line.includes('CODE EXAMPLES') || line.includes('SAMPLE CODE') || line.includes('## IMPLEMENTATION EXAMPLES')) {
        if (currentSection) sections[currentSection] = currentContent.join('\n');
        currentSection = 'codeExamples';
        currentContent = [];
      } else if (line.includes('## PERFORMANCE') || line.includes('PERFORMANCE OPTIMIZATION') || line.includes('## OPTIMIZATION')) {
        if (currentSection) sections[currentSection] = currentContent.join('\n');
        currentSection = 'performanceOptimization';
        currentContent = [];
      } else if (line.includes('## SECURITY') || line.includes('SECURITY RECOMMENDATIONS') || line.includes('## SECURITY BEST PRACTICES')) {
        if (currentSection) sections[currentSection] = currentContent.join('\n');
        currentSection = 'securityRecommendations';
        currentContent = [];
      } else if (currentSection) {
        currentContent.push(line);
      }
    }
    
    // Add the last section
    if (currentSection) {
      sections[currentSection] = currentContent.join('\n');
    }
    
    return sections;
  }

  // Render markdown content with proper formatting
  const renderMarkdownContent = (content) => {
    if (!content) return null;
    
    // Simple markdown parsing for code blocks, headers, and lists
    const lines = content.split('\n');
    const elements = [];
    let inCodeBlock = false;
    let codeLanguage = '';
    let codeContent = [];
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      
      // Handle code blocks
      if (line.startsWith('```')) {
        if (inCodeBlock) {
          // End code block
          elements.push(
            <div key={i} className="bg-gray-900 text-green-400 p-4 my-3 rounded-lg border">
              <div className="text-xs text-gray-400 mb-2">{codeLanguage || 'code'}</div>
              <pre className="text-sm overflow-x-auto whitespace-pre-wrap">
                <code>{codeContent.join('\n')}</code>
              </pre>
            </div>
          );
          inCodeBlock = false;
          codeContent = [];
          codeLanguage = '';
        } else {
          // Start code block
          inCodeBlock = true;
          codeLanguage = line.replace('```', '') || 'code';
        }
        continue;
      }
      
      if (inCodeBlock) {
        codeContent.push(line);
        continue;
      }
      
      // Handle headers
      if (line.startsWith('### ')) {
        elements.push(<h4 key={i} className="text-lg font-semibold mt-6 mb-3 text-gray-800">{line.replace('### ', '')}</h4>);
      } else if (line.startsWith('## ')) {
        elements.push(<h3 key={i} className="text-xl font-bold mt-8 mb-4 text-gray-900">{line.replace('## ', '')}</h3>);
      } else if (line.startsWith('# ')) {
        elements.push(<h2 key={i} className="text-2xl font-bold mt-10 mb-6 text-gray-900">{line.replace('# ', '')}</h2>);
      }
      // Handle lists
      else if (line.startsWith('- ') || line.startsWith('* ')) {
        elements.push(<li key={i} className="ml-6 mb-2 list-disc">{line.replace(/^[-*] /, '')}</li>);
      }
      // Handle numbered lists
      else if (/^\d+\. /.test(line)) {
        elements.push(<li key={i} className="ml-6 mb-2 list-decimal">{line.replace(/^\d+\. /, '')}</li>);
      }
      // Handle bold text
      else if (line.includes('**')) {
        const parts = line.split('**');
        const formattedLine = parts.map((part, idx) => 
          idx % 2 === 1 ? <strong key={idx} className="font-semibold text-gray-900">{part}</strong> : part
        );
        elements.push(<p key={i} className="mb-3 leading-relaxed">{formattedLine}</p>);
      }
      // Handle inline code
      else if (line.includes('`')) {
        const parts = line.split('`');
        const formattedLine = parts.map((part, idx) => 
          idx % 2 === 1 ? <code key={idx} className="bg-gray-100 px-2 py-1 rounded text-sm font-mono">{part}</code> : part
        );
        elements.push(<p key={i} className="mb-3 leading-relaxed">{formattedLine}</p>);
      }
      // Regular text
      else if (line.trim()) {
        elements.push(<p key={i} className="mb-3 leading-relaxed text-gray-700">{line}</p>);
      }
      // Empty line for spacing
      else {
        elements.push(<div key={i} className="mb-2" />);
      }
    }
    
    return <div className="prose max-w-none">{elements}</div>;
  };

  // Try to parse the raw agent response if available
  const agentSections = results.agent_raw_response ? parseAgentFinalAnswer(results.agent_raw_response) : null;

  const tabs = [
    // Primary tabs - main analysis and planning
    { id: 'overview', name: 'Project Overview', icon: <Code className="h-4 w-4" /> },
    { id: 'agent-output', name: 'Full Agent Analysis', icon: <Target className="h-4 w-4" /> },
    { id: 'research', name: 'Research Insights', icon: <GitBranch className="h-4 w-4" /> },
    { id: 'architecture-recs', name: 'Architecture Recommendations', icon: <Code className="h-4 w-4" /> },
    { id: 'ai-suggestions', name: 'AI Suggestions', icon: <Target className="h-4 w-4" /> },
    { id: 'implementation', name: 'Implementation Roadmap', icon: <Clock className="h-4 w-4" /> },
    
    // Secondary tabs - detailed specifications
    { id: 'architecture', name: 'System Architecture', icon: <Code className="h-4 w-4" /> },
    { id: 'sprints', name: 'Sprint Plan', icon: <GitBranch className="h-4 w-4" /> },
    { id: 'team', name: 'Team Structure', icon: <Users className="h-4 w-4" /> },
    { id: 'milestones', name: 'Milestones', icon: <Target className="h-4 w-4" /> },
    { id: 'guidelines', name: 'Code Guidelines', icon: <CheckCircle className="h-4 w-4" /> },
  ]

  return (
    <div className="max-w-6xl mx-auto animate-fade-in">
      {/* Header */}
      <div className="card mb-8">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{results.project_name}</h1>
            <p className="text-gray-600">Project plan generated successfully</p>
          </div>
          <div className="flex space-x-3">
            <button onClick={onBack} className="btn-secondary flex items-center">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back
            </button>
            <button onClick={onPlanAnother} className="btn-primary flex items-center">
              <Code className="h-4 w-4 mr-2" />
              Plan Another
            </button>
          </div>
        </div>
      </div>

        {/* Summary Cards */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <div className="card bg-blue-50 border-blue-200">
            <Clock className="h-8 w-8 text-blue-600 mb-3" />
            <div className="text-2xl font-bold text-blue-900">{results.estimated_timeline}</div>
            <div className="text-blue-700 text-sm">Timeline</div>
          </div>
          <div className="card bg-green-50 border-green-200">
            <GitBranch className="h-8 w-8 text-green-600 mb-3" />
            <div className="text-2xl font-bold text-green-900">{results.sprint_plan?.length || 0}</div>
            <div className="text-green-700 text-sm">Sprints</div>
          </div>
          <div className="card bg-purple-50 border-purple-200">
            <Users className="h-8 w-8 text-purple-600 mb-3" />
            <div className="text-2xl font-bold text-purple-900">{results.team_structure?.structure || 'N/A'}</div>
            <div className="text-purple-700 text-sm">Team Size</div>
          </div>
          <div className="card bg-orange-50 border-orange-200">
            <Target className="h-8 w-8 text-orange-600 mb-3" />
            <div className="text-2xl font-bold text-orange-900">{results.ai_suggestions?.length || 0}</div>
            <div className="text-orange-700 text-sm">AI Suggestions</div>
          </div>
        </div>      {/* Tabs */}
      <div className="card">
        <div className="border-b border-gray-200 mb-6">
          {/* Primary Navigation */}
          <div className="mb-4">
            <h3 className="text-sm font-semibold text-gray-700 mb-3 flex items-center">
              <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
              Main Analysis & Planning
            </h3>
            <nav className="flex flex-wrap gap-2">
              {tabs.slice(0, 6).map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center py-3 px-4 rounded-lg font-medium text-sm transition-all ${
                    activeTab === tab.id
                      ? 'bg-blue-500 text-white shadow-md'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200 hover:text-gray-900'
                  }`}
                >
                  {tab.icon}
                  <span className="ml-2">{tab.name}</span>
                </button>
              ))}
            </nav>
          </div>
          
          {/* Secondary Navigation */}
          <div className="border-t border-gray-100 pt-4">
            <h3 className="text-sm font-semibold text-gray-700 mb-3 flex items-center">
              <span className="w-2 h-2 bg-indigo-500 rounded-full mr-2"></span>
              Detailed Specifications
            </h3>
            <nav className="flex flex-wrap gap-2">
              {tabs.slice(6).map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center py-2 px-3 rounded-md font-medium text-xs transition-all ${
                    activeTab === tab.id
                      ? 'bg-indigo-500 text-white shadow-sm'
                      : 'bg-gray-50 text-gray-600 hover:bg-gray-100 hover:text-gray-800'
                  }`}
                >
                  {tab.icon}
                  <span className="ml-1">{tab.name}</span>
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold">Project Overview</h3>
            
            {/* Project Abstract */}
            <div className="bg-blue-50 p-6 rounded-lg border-l-4 border-blue-400">
              <h4 className="font-medium mb-3 text-blue-900 flex items-center">
                <Code className="h-5 w-5 mr-2" />
                Project Abstract
              </h4>
              <div className="text-blue-800 leading-relaxed whitespace-pre-line">
                {results.project_abstract || 'No abstract available'}
              </div>
            </div>

            {/* Quick Stats */}
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="bg-gray-50 p-4 rounded-lg text-center">
                <div className="text-2xl font-bold text-gray-900">{results.research_insights?.length || 0}</div>
                <div className="text-sm text-gray-600">Research Papers</div>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg text-center">
                <div className="text-2xl font-bold text-gray-900">{results.ai_suggestions?.length || 0}</div>
                <div className="text-sm text-gray-600">AI Recommendations</div>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg text-center">
                <div className="text-2xl font-bold text-gray-900">{results.sprint_plan?.length || 0}</div>
                <div className="text-sm text-gray-600">Sprint Plans</div>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg text-center">
                <div className="text-2xl font-bold text-gray-900">{results.tech_stack_recommendations?.length || 0}</div>
                <div className="text-sm text-gray-600">Tech Recommendations</div>
              </div>
            </div>

            {/* Status Badge */}
            <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg border border-green-200">
              <div className="flex items-center">
                <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
                <span className="font-medium text-green-900">
                  Plan Status: {results.status === 'success' ? 'Successfully Generated' : 
                              results.status === 'success_fallback' ? 'Generated (Fallback Mode)' : 
                              'Generated'}
                </span>
              </div>
              {results.status === 'success_fallback' && (
                <span className="text-sm text-green-700 bg-green-100 px-3 py-1 rounded-full">
                  Enhanced Fallback Plan
                </span>
              )}
            </div>
          </div>
        )}

        {activeTab === 'agent-output' && (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold">Complete AI Agent Analysis</h3>
            
            {results.agent_raw_response ? (
              <div className="bg-gradient-to-br from-gray-50 to-blue-50 border-2 border-blue-200 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <Target className="h-6 w-6 text-blue-600 mr-3" />
                  <h4 className="text-xl font-semibold text-blue-900">AI Agent's Complete Analysis</h4>
                  <span className="ml-auto bg-blue-100 text-blue-800 text-sm px-3 py-1 rounded-full">
                    Raw Agent Output
                  </span>
                </div>
                
                <div className="bg-white rounded-lg border p-6 max-h-96 overflow-y-auto">
                  {renderMarkdownContent(results.agent_raw_response)}
                </div>
                
                <div className="mt-4 text-sm text-blue-700 bg-blue-100 p-3 rounded">
                  <strong>Note:</strong> This is the complete, unfiltered output from the AI agent, including all reasoning, 
                  research findings, architecture decisions, and implementation recommendations.
                </div>
              </div>
            ) : (
              <div className="text-center py-12 text-gray-500">
                <Target className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                <p>No raw agent output available for this project.</p>
                <p className="text-sm mt-2">The agent response may not have been captured or saved.</p>
              </div>
            )}
            
            {/* Parsed Sections from Agent Output */}
            {(() => {
              const agentSections = results.agent_raw_response ? parseAgentFinalAnswer(results.agent_raw_response) : null;
              
              if (!agentSections) return null;
              
              return (
                <div className="space-y-6">
                  <h4 className="text-lg font-semibold text-gray-900 border-b pb-2">Parsed Agent Sections</h4>
                  
                  {agentSections.projectAbstract && (
                    <div className="bg-blue-50 p-6 rounded-lg border-l-4 border-blue-400">
                      <h5 className="font-semibold text-blue-900 mb-3">Project Abstract</h5>
                      {renderMarkdownContent(agentSections.projectAbstract)}
                    </div>
                  )}
                  
                  {agentSections.researchInsights && (
                    <div className="bg-green-50 p-6 rounded-lg border-l-4 border-green-400">
                      <h5 className="font-semibold text-green-900 mb-3">Research Insights</h5>
                      {renderMarkdownContent(agentSections.researchInsights)}
                    </div>
                  )}
                  
                  {agentSections.architectureRecommendations && (
                    <div className="bg-purple-50 p-6 rounded-lg border-l-4 border-purple-400">
                      <h5 className="font-semibold text-purple-900 mb-3">Architecture Recommendations</h5>
                      {renderMarkdownContent(agentSections.architectureRecommendations)}
                    </div>
                  )}
                  
                  {agentSections.implementationRoadmap && (
                    <div className="bg-orange-50 p-6 rounded-lg border-l-4 border-orange-400">
                      <h5 className="font-semibold text-orange-900 mb-3">Implementation Roadmap</h5>
                      {renderMarkdownContent(agentSections.implementationRoadmap)}
                    </div>
                  )}
                  
                  {agentSections.techStack && (
                    <div className="bg-indigo-50 p-6 rounded-lg border-l-4 border-indigo-400">
                      <h5 className="font-semibold text-indigo-900 mb-3">Technology Stack</h5>
                      {renderMarkdownContent(agentSections.techStack)}
                    </div>
                  )}
                  
                  {agentSections.codeExamples && (
                    <div className="bg-gray-50 p-6 rounded-lg border-l-4 border-gray-400">
                      <h5 className="font-semibold text-gray-900 mb-3">Code Examples</h5>
                      {renderMarkdownContent(agentSections.codeExamples)}
                    </div>
                  )}
                </div>
              );
            })()}
          </div>
        )}

        {activeTab === 'research' && (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold">Research Insights & Academic Papers</h3>
            
            {results.research_insights && results.research_insights.length > 0 ? (
              <div className="space-y-4">
                {results.research_insights.map((insight, index) => (
                  <div key={index} className="border rounded-lg p-6 bg-white hover:shadow-lg transition-shadow">
                    {/* Parse the insight to extract title, research content, and source */}
                    {(() => {
                      const parts = insight.split('\n');
                      const title = parts[0]?.replace(/^\*\*|\*\*$/g, '') || `Research Finding ${index + 1}`;
                      const researchLine = parts.find(line => line.startsWith('Research:')) || '';
                      const sourceLine = parts.find(line => line.startsWith('Source:')) || '';
                      const research = researchLine.replace('Research:', '').trim();
                      const source = sourceLine.replace('Source:', '').trim();
                      
                      return (
                        <>
                          <div className="flex items-start justify-between mb-3">
                            <h4 className="font-semibold text-lg text-gray-900 flex items-center">
                              <GitBranch className="h-5 w-5 mr-2 text-blue-600" />
                              {title}
                            </h4>
                            <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                              Paper #{index + 1}
                            </span>
                          </div>
                          
                          {research && (
                            <div className="mb-4">
                              <h5 className="font-medium text-gray-700 mb-2">Research Summary:</h5>
                              <p className="text-gray-600 leading-relaxed bg-gray-50 p-4 rounded-lg">
                                {research}
                              </p>
                            </div>
                          )}
                          
                          {source && source !== '#' && (
                            <div className="flex items-center justify-between pt-3 border-t border-gray-200">
                              <span className="text-sm text-gray-500">Source:</span>
                              {source.startsWith('http') ? (
                                <a 
                                  href={source} 
                                  target="_blank" 
                                  rel="noopener noreferrer"
                                  className="text-blue-600 hover:text-blue-800 text-sm font-medium flex items-center"
                                >
                                  View Research Paper
                                  <svg className="h-4 w-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                                  </svg>
                                </a>
                              ) : (
                                <span className="text-sm text-gray-600 bg-gray-100 px-3 py-1 rounded">
                                  {source}
                                </span>
                              )}
                            </div>
                          )}
                        </>
                      );
                    })()}
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12 text-gray-500">
                <GitBranch className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                <p>No research insights available for this project.</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'architecture-recs' && (
          <div className="space-y-8">
            <h3 className="text-lg font-semibold">Architecture Recommendations</h3>
            
            {/* Display Agent's Architecture Recommendations */}
            {results.agent_raw_response ? (
              (() => {
                const agentSections = parseAgentFinalAnswer(results.agent_raw_response);
                
                return (
                  <div className="space-y-6">
                    {/* Agent Architecture Section */}
                    {agentSections.architectureRecommendations && (
                      <div className="bg-gradient-to-br from-blue-50 to-indigo-100 p-8 rounded-lg border">
                        <h4 className="text-xl font-semibold text-blue-900 mb-6 flex items-center">
                          <Code className="h-6 w-6 mr-3" />
                          AI-Generated Architecture Recommendations
                        </h4>
                        {renderMarkdownContent(agentSections.architectureRecommendations)}
                      </div>
                    )}
                    
                    {/* Agent Tech Stack Section */}
                    {agentSections.techStack && (
                      <div className="bg-gradient-to-br from-green-50 to-teal-100 p-8 rounded-lg border">
                        <h4 className="text-xl font-semibold text-green-900 mb-6 flex items-center">
                          <span className="text-2xl mr-3">🛠️</span>
                          Technology Stack Analysis
                        </h4>
                        {renderMarkdownContent(agentSections.techStack)}
                      </div>
                    )}
                    
                    {/* Code Examples from Agent */}
                    {agentSections.codeExamples && (
                      <div className="bg-gradient-to-br from-purple-50 to-pink-100 p-8 rounded-lg border">
                        <h4 className="text-xl font-semibold text-purple-900 mb-6 flex items-center">
                          <Code className="h-6 w-6 mr-3" />
                          Code Examples & Implementation
                        </h4>
                        {renderMarkdownContent(agentSections.codeExamples)}
                      </div>
                    )}
                    
                    {/* Fallback to Full Agent Response if sections not found */}
                    {(!agentSections.architectureRecommendations && !agentSections.techStack && !agentSections.codeExamples) && (
                      <div className="bg-gradient-to-br from-blue-50 to-indigo-100 p-8 rounded-lg border">
                        <h4 className="text-xl font-semibold text-blue-900 mb-6 flex items-center">
                          <Code className="h-6 w-6 mr-3" />
                          Complete Agent Architecture Analysis
                        </h4>
                        {renderMarkdownContent(results.agent_raw_response)}
                      </div>
                    )}
                  </div>
                );
              })()
            ) : (
              /* Fallback to structured architecture display if no agent response */
              results.architecture && Object.keys(results.architecture).length > 0 ? (
                <div className="space-y-6">
                  {/* Display structured architecture from backend */}
                  {Object.entries(results.architecture).map(([layer, components]) => (
                    <div key={layer} className="border rounded-lg p-6 bg-white hover:shadow-lg transition-shadow">
                      <div className="flex items-center mb-4">
                        <div className="p-2 rounded-lg bg-blue-100 mr-3">
                          {layer === 'frontend' && <span className="text-2xl">🖥️</span>}
                          {layer === 'backend' && <span className="text-2xl">⚙️</span>}
                          {layer === 'database' && <span className="text-2xl">🗄️</span>}
                          {layer === 'infrastructure' && <span className="text-2xl">☁️</span>}
                          {layer === 'security' && <span className="text-2xl">🔒</span>}
                          {layer === 'testing' && <span className="text-2xl">🧪</span>}
                          {!['frontend', 'backend', 'database', 'infrastructure', 'security', 'testing'].includes(layer) && <span className="text-2xl">🔧</span>}
                        </div>
                        <h4 className="font-semibold capitalize text-xl text-gray-900">{layer} Layer</h4>
                      </div>
                      
                      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-3">
                        {Array.isArray(components) ? components.map((component, index) => (
                          <div key={index} className="bg-gray-50 px-4 py-3 rounded-lg text-sm font-medium text-gray-700 border border-gray-200 hover:border-blue-300 transition-colors">
                            {component}
                          </div>
                        )) : (
                          <div className="bg-gray-50 px-4 py-3 rounded-lg text-sm font-medium text-gray-700">
                            {typeof components === 'string' ? components : JSON.stringify(components)}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                  
                  {/* Architecture Visualization Placeholder */}
                  <div className="bg-gradient-to-br from-blue-50 to-indigo-100 p-8 rounded-lg border-2 border-dashed border-blue-300">
                    <div className="text-center">
                      <Code className="h-16 w-16 mx-auto text-blue-400 mb-4" />
                      <h4 className="text-lg font-semibold text-blue-900 mb-2">Architecture Visualization</h4>
                      <p className="text-blue-700 mb-4">
                        A detailed system architecture diagram would be displayed here, showing the relationships between all components.
                      </p>
                      <div className="text-sm text-blue-600 bg-blue-100 inline-block px-4 py-2 rounded-full">
                        💡 Consider tools like Lucidchart, draw.io, or Miro for creating architecture diagrams
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                /* No architecture data available */
                <div className="text-center py-12 text-gray-500">
                  <Code className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                  <p>No architecture recommendations available for this project.</p>
                  <p className="text-sm mt-2">The AI agent will provide detailed architecture recommendations when you create a new project plan.</p>
                </div>
              )
            )}
          </div>
        )}

        {activeTab === 'implementation' && (
          <div className="space-y-8">
            <h3 className="text-lg font-semibold">Implementation Roadmap & AI Suggestions</h3>
            
            {/* Display Agent's Implementation Roadmap */}
            {results.agent_raw_response ? (
              (() => {
                const agentSections = parseAgentFinalAnswer(results.agent_raw_response);
                
                return (
                  <div className="space-y-6">
                    {/* Agent Implementation Roadmap */}
                    {agentSections.implementationRoadmap && (
                      <div className="bg-gradient-to-br from-green-50 to-blue-100 p-8 rounded-lg border">
                        <h4 className="text-xl font-semibold text-green-900 mb-6 flex items-center">
                          <Target className="h-6 w-6 mr-3" />
                          AI-Generated Implementation Roadmap
                        </h4>
                        {renderMarkdownContent(agentSections.implementationRoadmap)}
                      </div>
                    )}
                    
                    {/* Performance Optimization from Agent */}
                    {agentSections.performanceOptimization && (
                      <div className="bg-gradient-to-br from-yellow-50 to-orange-100 p-8 rounded-lg border">
                        <h4 className="text-xl font-semibold text-yellow-900 mb-6 flex items-center">
                          <Target className="h-6 w-6 mr-3" />
                          Performance Optimization Strategy
                        </h4>
                        {renderMarkdownContent(agentSections.performanceOptimization)}
                      </div>
                    )}
                    
                    {/* Security Recommendations from Agent */}
                    {agentSections.securityRecommendations && (
                      <div className="bg-gradient-to-br from-red-50 to-pink-100 p-8 rounded-lg border">
                        <h4 className="text-xl font-semibold text-red-900 mb-6 flex items-center">
                          <CheckCircle className="h-6 w-6 mr-3" />
                          Security Best Practices
                        </h4>
                        {renderMarkdownContent(agentSections.securityRecommendations)}
                      </div>
                    )}
                    
                    {/* Fallback to Full Agent Response if sections not found */}
                    {(!agentSections.implementationRoadmap && !agentSections.performanceOptimization && !agentSections.securityRecommendations) && (
                      <div className="bg-gradient-to-br from-blue-50 to-indigo-100 p-8 rounded-lg border">
                        <h4 className="text-xl font-semibold text-blue-900 mb-6 flex items-center">
                          <Target className="h-6 w-6 mr-3" />
                          Complete Agent Implementation Analysis
                        </h4>
                        {renderMarkdownContent(results.agent_raw_response)}
                      </div>
                    )}
                  </div>
                );
              })()
            ) : (
              /* Fallback to sprint plan if no agent response */
              results.sprint_plan && results.sprint_plan.length > 0 ? (
                <div className="space-y-6">
                  <div className="bg-gradient-to-r from-green-50 to-blue-50 p-6 rounded-lg border">
                    <h4 className="font-semibold text-gray-900 mb-3">Implementation Overview</h4>
                    <div className="grid md:grid-cols-3 gap-4 text-center">
                      <div>
                        <div className="text-2xl font-bold text-green-600">{results.sprint_plan.length}</div>
                        <div className="text-sm text-gray-600">Development Phases</div>
                      </div>
                      <div>
                        <div className="text-2xl font-bold text-blue-600">
                          {results.sprint_plan.reduce((total, sprint) => {
                            const durationMatch = sprint.duration?.match(/(\d+)/);
                            return total + (durationMatch ? parseInt(durationMatch[1]) : 2);
                          }, 0)}
                        </div>
                        <div className="text-sm text-gray-600">Total Weeks</div>
                      </div>
                      <div>
                        <div className="text-2xl font-bold text-purple-600">
                          {results.sprint_plan.reduce((total, sprint) => total + (sprint.features?.length || 0), 0)}
                        </div>
                        <div className="text-sm text-gray-600">Total Features</div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Sprint-based Implementation */}
                  {results.sprint_plan.map((sprint, index) => (
                    <div key={index} className="border rounded-lg p-6 bg-white hover:shadow-lg transition-shadow">
                      <div className="flex justify-between items-start mb-4">
                        <div className="flex items-center">
                          <div className="bg-blue-100 text-blue-800 w-8 h-8 rounded-full flex items-center justify-center font-semibold mr-3">
                            {sprint.sprint_number}
                          </div>
                          <h4 className="font-semibold text-lg">Phase {sprint.sprint_number}: Implementation</h4>
                        </div>
                        <div className="text-right">
                          <span className="bg-gray-100 text-gray-700 text-sm px-3 py-1 rounded-full">
                            {sprint.duration}
                          </span>
                        </div>
                      </div>
                      
                      <div className="grid md:grid-cols-2 gap-6">
                        <div>
                          <h5 className="font-medium text-sm mb-3 text-gray-700 flex items-center">
                            <Target className="h-4 w-4 mr-1" />
                            Features ({sprint.features?.length || 0})
                          </h5>
                          <ul className="space-y-2">
                            {sprint.features?.map((feature, i) => (
                              <li key={i} className="text-sm text-gray-600 flex items-start">
                                <CheckCircle className="h-4 w-4 mr-2 mt-0.5 text-green-500 flex-shrink-0" />
                                {feature}
                              </li>
                            ))}
                          </ul>
                        </div>
                        
                        <div>
                          <h5 className="font-medium text-sm mb-3 text-gray-700 flex items-center">
                            <Users className="h-4 w-4 mr-1" />
                            Deliverables ({sprint.deliverables?.length || 0})
                          </h5>
                          <ul className="space-y-2">
                            {sprint.deliverables?.map((deliverable, i) => (
                              <li key={i} className="text-sm text-gray-600 flex items-start">
                                <span className="text-purple-500 mr-2 mt-1">📦</span>
                                {deliverable}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  ))}
                  
                  {/* General Implementation Tips */}
                  <div className="bg-yellow-50 p-6 rounded-lg border-l-4 border-yellow-400">
                    <h4 className="font-medium mb-3 text-yellow-900 flex items-center">
                      <Target className="h-5 w-5 mr-2" />
                      Implementation Best Practices
                    </h4>
                    <ul className="space-y-2 text-yellow-800">
                      <li className="flex items-start">
                        <span className="text-yellow-600 mr-2">•</span>
                        Follow test-driven development (TDD) for reliable code
                      </li>
                      <li className="flex items-start">
                        <span className="text-yellow-600 mr-2">•</span>
                        Implement continuous integration and automated testing
                      </li>
                      <li className="flex items-start">
                        <span className="text-yellow-600 mr-2">•</span>
                        Use version control with meaningful commit messages
                      </li>
                      <li className="flex items-start">
                        <span className="text-yellow-600 mr-2">•</span>
                        Regular code reviews and documentation updates
                      </li>
                    </ul>
                  </div>
                </div>
              ) : (
                /* No implementation data available */
                <div className="text-center py-12 text-gray-500">
                  <Target className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                  <p>No implementation roadmap available for this project.</p>
                  <p className="text-sm mt-2">The AI agent will provide detailed implementation plans when you create a new project plan.</p>
                </div>
              )
            )}
          </div>
        )}

        {activeTab === 'ai-suggestions' && (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold">AI-Powered Recommendations</h3>
            
            {results.ai_suggestions && results.ai_suggestions.length > 0 ? (
              <div className="space-y-4">
                {results.ai_suggestions.map((suggestion, index) => (
                  <div key={index} className="border rounded-lg p-6 bg-gradient-to-r from-purple-50 to-pink-50 hover:shadow-lg transition-shadow">
                    {/* Parse suggestion to extract category and content */}
                    {(() => {
                      const match = suggestion.match(/^\*\*([^*]+)\*\*:\s*(.+)$/);
                      const category = match ? match[1] : `Suggestion ${index + 1}`;
                      const content = match ? match[2] : suggestion;
                      
                      const getCategoryIcon = (cat) => {
                        if (cat.includes('Architecture')) return '🏗️';
                        if (cat.includes('Technology') || cat.includes('Stack')) return '🛠️';
                        if (cat.includes('Development') || cat.includes('Methodology')) return '⚡';
                        if (cat.includes('Performance')) return '🚀';
                        if (cat.includes('Security')) return '🔒';
                        if (cat.includes('Monitoring')) return '📊';
                        if (cat.includes('Deployment')) return '🚀';
                        if (cat.includes('Code') || cat.includes('Quality')) return '✨';
                        if (cat.includes('Testing')) return '🧪';
                        if (cat.includes('Documentation')) return '📚';
                        return '💡';
                      };
                      
                      return (
                        <>
                          <div className="flex items-start mb-3">
                            <span className="text-2xl mr-3">{getCategoryIcon(category)}</span>
                            <div className="flex-1">
                              <h4 className="font-semibold text-lg text-gray-900 mb-2">
                                {category}
                              </h4>
                              <p className="text-gray-700 leading-relaxed">
                                {content}
                              </p>
                            </div>
                            <span className="bg-purple-100 text-purple-800 text-xs px-2 py-1 rounded-full ml-2">
                              AI Recommended
                            </span>
                          </div>
                        </>
                      );
                    })()}
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12 text-gray-500">
                <Target className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                <p>No AI suggestions available for this project.</p>
              </div>
            )}
            
            {/* Tech Stack Recommendations */}
            {results.tech_stack_recommendations && results.tech_stack_recommendations.length > 0 && (
              <div className="bg-orange-50 p-6 rounded-lg border-l-4 border-orange-400">
                <h4 className="font-medium mb-3 text-orange-900 flex items-center">
                  <Code className="h-5 w-5 mr-2" />
                  Additional Technology Recommendations
                </h4>
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-2">
                  {results.tech_stack_recommendations.map((tech, index) => (
                    <div key={index} className="bg-orange-100 px-3 py-2 rounded text-sm text-orange-800 font-medium">
                      {tech}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'architecture' && (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold">System Architecture</h3>
            
            {results.architecture && Object.keys(results.architecture).length > 0 ? (
              <div className="space-y-6">
                {Object.entries(results.architecture).map(([layer, components]) => (
                  <div key={layer} className="border rounded-lg p-6 bg-white hover:shadow-lg transition-shadow">
                    <div className="flex items-center mb-4">
                      {/* Layer icons */}
                      <div className="p-2 rounded-lg bg-blue-100 mr-3">
                        {layer === 'frontend' && <span className="text-2xl">🖥️</span>}
                        {layer === 'backend' && <span className="text-2xl">⚙️</span>}
                        {layer === 'database' && <span className="text-2xl">🗄️</span>}
                        {layer === 'infrastructure' && <span className="text-2xl">☁️</span>}
                        {layer === 'security' && <span className="text-2xl">🔒</span>}
                        {layer === 'testing' && <span className="text-2xl">🧪</span>}
                        {!['frontend', 'backend', 'database', 'infrastructure', 'security', 'testing'].includes(layer) && <span className="text-2xl">🔧</span>}
                      </div>
                      <h4 className="font-semibold capitalize text-xl text-gray-900">{layer} Layer</h4>
                    </div>
                    
                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-3">
                      {Array.isArray(components) ? components.map((component, index) => (
                        <div key={index} className="bg-gray-50 px-4 py-3 rounded-lg text-sm font-medium text-gray-700 border border-gray-200 hover:border-blue-300 transition-colors">
                          {component}
                        </div>
                      )) : (
                        <div className="bg-gray-50 px-4 py-3 rounded-lg text-sm font-medium text-gray-700">
                          {typeof components === 'string' ? components : JSON.stringify(components)}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
                
                {/* Architecture Diagram Placeholder */}
                <div className="bg-gradient-to-br from-blue-50 to-indigo-100 p-8 rounded-lg border-2 border-dashed border-blue-300">
                  <div className="text-center">
                    <Code className="h-16 w-16 mx-auto text-blue-400 mb-4" />
                    <h4 className="text-lg font-semibold text-blue-900 mb-2">Architecture Visualization</h4>
                    <p className="text-blue-700 mb-4">
                      A detailed system architecture diagram would be displayed here, showing the relationships between all components.
                    </p>
                    <div className="text-sm text-blue-600 bg-blue-100 inline-block px-4 py-2 rounded-full">
                      💡 Consider tools like Lucidchart, draw.io, or Miro for creating architecture diagrams
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-12 text-gray-500">
                <Code className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                <p>No architecture information available for this project.</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'sprints' && (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold">Sprint Planning & Development Timeline</h3>
            
            {results.sprint_plan && results.sprint_plan.length > 0 ? (
              <div className="space-y-6">
                {/* Sprint Timeline Overview */}
                <div className="bg-gradient-to-r from-green-50 to-blue-50 p-6 rounded-lg border">
                  <h4 className="font-semibold text-gray-900 mb-3">Sprint Overview</h4>
                  <div className="grid md:grid-cols-3 gap-4 text-center">
                    <div>
                      <div className="text-2xl font-bold text-green-600">{results.sprint_plan.length}</div>
                      <div className="text-sm text-gray-600">Total Sprints</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-blue-600">
                        {results.sprint_plan.reduce((total, sprint) => {
                          const weeks = parseInt(sprint.duration?.split(' ')[0]) || 2;
                          return total + weeks;
                        }, 0)}
                      </div>
                      <div className="text-sm text-gray-600">Total Weeks</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-purple-600">
                        {results.sprint_plan.reduce((total, sprint) => total + (sprint.features?.length || 0), 0)}
                      </div>
                      <div className="text-sm text-gray-600">Total Features</div>
                    </div>
                  </div>
                </div>

                {/* Individual Sprint Cards */}
                {results.sprint_plan.map((sprint, index) => (
                  <div key={index} className="border rounded-lg p-6 bg-white hover:shadow-lg transition-shadow">
                    <div className="flex justify-between items-start mb-4">
                      <div className="flex items-center">
                        <div className="bg-blue-100 text-blue-800 w-8 h-8 rounded-full flex items-center justify-center font-semibold mr-3">
                          {sprint.sprint_number}
                        </div>
                        <h4 className="font-semibold text-lg">Sprint {sprint.sprint_number}</h4>
                      </div>
                      <div className="text-right">
                        <span className="bg-gray-100 text-gray-700 text-sm px-3 py-1 rounded-full">
                          {sprint.duration}
                        </span>
                        {sprint.estimated_effort && (
                          <div className="text-xs text-gray-500 mt-1">
                            {sprint.estimated_effort}
                          </div>
                        )}
                      </div>
                    </div>
                    
                    <div className="grid md:grid-cols-3 gap-6">
                      {/* Features */}
                      <div>
                        <h5 className="font-medium text-sm mb-3 text-gray-700 flex items-center">
                          <Target className="h-4 w-4 mr-1" />
                          Features ({sprint.features?.length || 0})
                        </h5>
                        <ul className="space-y-2">
                          {sprint.features?.map((feature, i) => (
                            <li key={i} className="text-sm text-gray-600 flex items-start">
                              <CheckCircle className="h-4 w-4 mr-2 mt-0.5 text-green-500 flex-shrink-0" />
                              {feature}
                            </li>
                          ))}
                        </ul>
                      </div>
                      
                      {/* Goals */}
                      <div>
                        <h5 className="font-medium text-sm mb-3 text-gray-700 flex items-center">
                          <GitBranch className="h-4 w-4 mr-1" />
                          Goals ({sprint.goals?.length || 0})
                        </h5>
                        <ul className="space-y-2">
                          {sprint.goals?.map((goal, i) => (
                            <li key={i} className="text-sm text-gray-600 flex items-start">
                              <span className="text-blue-500 mr-2 mt-1">•</span>
                              {goal}
                            </li>
                          ))}
                        </ul>
                      </div>
                      
                      {/* Deliverables */}
                      <div>
                        <h5 className="font-medium text-sm mb-3 text-gray-700 flex items-center">
                          <Users className="h-4 w-4 mr-1" />
                          Deliverables ({sprint.deliverables?.length || 0})
                        </h5>
                        <ul className="space-y-2">
                          {sprint.deliverables?.map((deliverable, i) => (
                            <li key={i} className="text-sm text-gray-600 flex items-start">
                              <span className="text-purple-500 mr-2 mt-1">📦</span>
                              {deliverable}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                ))}
                
                {/* Sprint Planning Tips */}
                <div className="bg-yellow-50 p-6 rounded-lg border-l-4 border-yellow-400">
                  <h4 className="font-medium mb-3 text-yellow-900 flex items-center">
                    <Clock className="h-5 w-5 mr-2" />
                    Sprint Planning Best Practices
                  </h4>
                  <ul className="space-y-2 text-yellow-800">
                    <li className="flex items-start">
                      <span className="text-yellow-600 mr-2">•</span>
                      Plan for 80% capacity to account for unexpected issues
                    </li>
                    <li className="flex items-start">
                      <span className="text-yellow-600 mr-2">•</span>
                      Include buffer time for code reviews and testing
                    </li>
                    <li className="flex items-start">
                      <span className="text-yellow-600 mr-2">•</span>
                      Regular sprint retrospectives to improve team velocity
                    </li>
                    <li className="flex items-start">
                      <span className="text-yellow-600 mr-2">•</span>
                      Maintain consistent sprint duration for predictability
                    </li>
                  </ul>
                </div>
              </div>
            ) : (
              <div className="text-center py-12 text-gray-500">
                <GitBranch className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                <p>No sprint plan available for this project.</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'team' && (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold">Team Structure & Organization</h3>
            
            {results.team_structure ? (
              <div className="space-y-6">
                {/* Team Overview */}
                <div className="bg-blue-50 p-6 rounded-lg border-l-4 border-blue-400">
                  <div className="flex items-center justify-between mb-4">
                    <h4 className="font-semibold text-blue-900 flex items-center text-lg">
                      <Users className="h-6 w-6 mr-2" />
                      {results.team_structure.structure}
                    </h4>
                    <span className="bg-blue-100 text-blue-800 text-sm px-3 py-1 rounded-full">
                      Recommended Structure
                    </span>
                  </div>
                  <p className="text-blue-800">{results.team_structure.management}</p>
                </div>

                {/* Team Roles */}
                <div className="bg-white border rounded-lg p-6">
                  <h4 className="font-semibold mb-4 flex items-center">
                    <Users className="h-5 w-5 mr-2 text-gray-600" />
                    Recommended Team Roles
                  </h4>
                  <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {results.team_structure.roles?.map((role, index) => (
                      <div key={index} className="p-4 bg-gray-50 rounded-lg border hover:shadow-md transition-shadow">
                        <div className="flex items-center mb-2">
                          {/* Role icons */}
                          <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                            {role.toLowerCase().includes('lead') || role.toLowerCase().includes('manager') ? '👨‍💼' :
                             role.toLowerCase().includes('frontend') ? '🎨' :
                             role.toLowerCase().includes('backend') ? '⚙️' :
                             role.toLowerCase().includes('qa') || role.toLowerCase().includes('test') ? '🧪' :
                             role.toLowerCase().includes('devops') ? '🚀' :
                             role.toLowerCase().includes('designer') ? '🎨' :
                             role.toLowerCase().includes('architect') ? '🏗️' : '👨‍💻'}
                          </div>
                          <span className="font-medium text-gray-900 text-sm">{role}</span>
                        </div>
                        
                        {/* Role responsibilities */}
                        <div className="text-xs text-gray-600">
                          {role.toLowerCase().includes('lead') ? 'Technical leadership and architecture decisions' :
                           role.toLowerCase().includes('manager') ? 'Project coordination and team management' :
                           role.toLowerCase().includes('frontend') ? 'User interface and user experience development' :
                           role.toLowerCase().includes('backend') ? 'Server-side logic and database management' :
                           role.toLowerCase().includes('qa') ? 'Quality assurance and testing procedures' :
                           role.toLowerCase().includes('devops') ? 'Deployment and infrastructure management' :
                           role.toLowerCase().includes('designer') ? 'UI/UX design and user research' :
                           'Software development and implementation'}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Team Organization Tips */}
                <div className="bg-green-50 p-6 rounded-lg border-l-4 border-green-400">
                  <h4 className="font-medium mb-3 text-green-900 flex items-center">
                    <Target className="h-5 w-5 mr-2" />
                    Team Organization Best Practices
                  </h4>
                  <div className="grid md:grid-cols-2 gap-4">
                    <ul className="space-y-2 text-green-800">
                      <li className="flex items-start">
                        <span className="text-green-600 mr-2">•</span>
                        Clear role definitions and responsibilities
                      </li>
                      <li className="flex items-start">
                        <span className="text-green-600 mr-2">•</span>
                        Regular team meetings and communication
                      </li>
                      <li className="flex items-start">
                        <span className="text-green-600 mr-2">•</span>
                        Cross-functional collaboration opportunities
                      </li>
                    </ul>
                    <ul className="space-y-2 text-green-800">
                      <li className="flex items-start">
                        <span className="text-green-600 mr-2">•</span>
                        Pair programming and knowledge sharing
                      </li>
                      <li className="flex items-start">
                        <span className="text-green-600 mr-2">•</span>
                        Regular retrospectives for continuous improvement
                      </li>
                      <li className="flex items-start">
                        <span className="text-green-600 mr-2">•</span>
                        Documentation and onboarding processes
                      </li>
                    </ul>
                  </div>
                </div>

                {/* Communication Structure */}
                <div className="bg-purple-50 p-6 rounded-lg border-l-4 border-purple-400">
                  <h4 className="font-medium mb-3 text-purple-900 flex items-center">
                    <GitBranch className="h-5 w-5 mr-2" />
                    Communication & Collaboration
                  </h4>
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <h5 className="font-medium text-sm mb-2 text-purple-800">Daily Activities</h5>
                      <ul className="text-sm text-purple-700 space-y-1">
                        <li>• Daily standup meetings (15 min)</li>
                        <li>• Slack/Teams for quick communication</li>
                        <li>• Code reviews via pull requests</li>
                        <li>• Shared documentation updates</li>
                      </ul>
                    </div>
                    <div>
                      <h5 className="font-medium text-sm mb-2 text-purple-800">Weekly Activities</h5>
                      <ul className="text-sm text-purple-700 space-y-1">
                        <li>• Sprint planning sessions</li>
                        <li>• Technical architecture reviews</li>
                        <li>• Demo and feedback sessions</li>
                        <li>• Team retrospectives</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-12 text-gray-500">
                <Users className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                <p>No team structure information available.</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'milestones' && (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold">Project Milestones</h3>
            {results.milestones?.map((milestone, index) => (
              <div key={index} className="border rounded-lg p-4">
                <div className="flex justify-between items-start mb-3">
                  <h4 className="font-medium">{milestone.name}</h4>
                  <span className="text-sm text-gray-500">Week {milestone.week}</span>
                </div>
                <p className="text-sm text-gray-600 mb-3">{milestone.description}</p>
                <div>
                  <h5 className="font-medium text-sm mb-2">Deliverables</h5>
                  <ul className="text-sm text-gray-600 space-y-1">
                    {milestone.deliverables?.map((deliverable, i) => (
                      <li key={i}>• {deliverable}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )) || <p className="text-gray-500">No milestones available</p>}
          </div>
        )}

        {activeTab === 'guidelines' && (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold">Code Review Guidelines</h3>
            
            {results.code_review_guidelines && results.code_review_guidelines.length > 0 ? (
              <div className="space-y-4">
                {results.code_review_guidelines.map((guideline, index) => (
                  <div key={index} className="flex items-start p-4 bg-gray-50 rounded-lg border">
                    <CheckCircle className="h-5 w-5 text-green-600 mr-3 mt-0.5 flex-shrink-0" />
                    <div className="flex-1">
                      <p className="text-gray-800">{guideline}</p>
                    </div>
                    <span className="bg-gray-200 text-gray-700 text-xs px-2 py-1 rounded-full ml-2">
                      #{index + 1}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12 text-gray-500">
                <CheckCircle className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                <p>No code review guidelines available.</p>
              </div>
            )}
            
            {/* Best Practices Section */}
            <div className="bg-blue-50 p-6 rounded-lg border-l-4 border-blue-400">
              <h4 className="font-medium mb-3 text-blue-900 flex items-center">
                <Code className="h-5 w-5 mr-2" />
                Development Best Practices
              </h4>
              <ul className="space-y-2 text-blue-800">
                <li className="flex items-start">
                  <span className="text-blue-600 mr-2">•</span>
                  Follow test-driven development (TDD) practices
                </li>
                <li className="flex items-start">
                  <span className="text-blue-600 mr-2">•</span>
                  Implement continuous integration and deployment
                </li>
                <li className="flex items-start">
                  <span className="text-blue-600 mr-2">•</span>
                  Use version control with meaningful commit messages
                </li>
                <li className="flex items-start">
                  <span className="text-blue-600 mr-2">•</span>
                  Document APIs and maintain updated README files
                </li>
                <li className="flex items-start">
                  <span className="text-blue-600 mr-2">•</span>
                  Regular security audits and dependency updates
                </li>
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default TechPlanner
