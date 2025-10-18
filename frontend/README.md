# Multi AI Agent Planner Frontend

A modern, responsive React frontend for the Multi AI Agent Planner application featuring intelligent travel planning, event planning, and tech project planning powered by AI agents.

## Features

- **🤖 AI-Powered Planning**: Multiple specialized AI agents for different planning needs
- **🌍 Travel Planning**: Comprehensive trip planning with flights, hotels, and itineraries
- **🎉 Event Planning**: Intelligent event planning with real venue and vendor recommendations
- **💻 Tech Planning**: Software project planning and architecture recommendations
- **🎨 Beautiful UI**: Modern design with Tailwind CSS and Heroicons
- **📱 Responsive**: Works seamlessly on desktop, tablet, and mobile
- **⚡ Interactive**: Smooth animations and transitions
- **👤 User-friendly**: Intuitive form design and clear results display
- **🔄 Real-time**: Live API integration with agentic backend services

## Technology Stack

- **React 18**: Modern React with hooks and functional components
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework for styling
- **Heroicons**: Beautiful SVG icons from the makers of Tailwind CSS
- **React Hot Toast**: Elegant toast notifications
- **Date-fns**: Modern date formatting utilities
- **FastAPI Backend**: Python-based API with AI agent integration
- **LangChain**: AI agent framework for intelligent planning
- **Tavily API**: Real-time search for venues and vendors

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn
- Python 3.8+ (for backend)
- Backend server running on port 8000
- Valid API keys for AI services (MOONSHOT, Tavily)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd "Multi AI agent Planner/frontend"
```

2. Install dependencies:
```bash
npm install
```

3. Start the backend server (from project root):
```bash
# Activate virtual environment
source venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt

# Start backend server
python backend/app.py
```

4. Start the frontend development server:
```bash
npm run dev
```

5. Open your browser and navigate to `http://localhost:5173`

### Build for Production

```bash
npm run build
```

## Project Structure

```
src/
├── components/              # React components
│   ├── Header.jsx          # Top navigation bar
│   ├── Hero.jsx            # Landing page hero section
│   ├── Dashboard.jsx       # Main dashboard with planner selection
│   ├── LoadingSpinner.jsx  # Loading animation component
│   │
│   ├── Travel Planning/
│   │   ├── TravelForm.jsx     # Trip planning form
│   │   ├── TravelResults.jsx  # Travel results display
│   │   └── TravelPlanner.jsx  # Main travel planner container
│   │
│   ├── Event Planning/
│   │   ├── EventForm.jsx      # Event planning form  
│   │   ├── EventResults.jsx   # Event results with AI analysis
│   │   ├── EventPlanner.jsx   # Main event planner container
│   │   └── EnhancedEventResults.jsx # Advanced event results display
│   │
│   ├── Tech Planning/
│   │   ├── TechPlanner.jsx    # Tech project planning form and results
│   │   └── TechPlannerComingSoon.jsx # Coming soon placeholder
│   │
│   └── Coming Soon/
│       ├── BusinessPlannerComingSoon.jsx
│       ├── LearningPlannerComingSoon.jsx
│       └── ComingSoonPlanner.jsx
│
├── App.jsx                 # Main app component with routing
├── main.jsx               # React entry point
└── index.css              # Global styles and Tailwind imports
```

## API Integration

The frontend communicates with the FastAPI backend at `http://localhost:8000` with the following endpoints:

### Travel Planning
- `POST /api/plan_trip` - Generate travel itineraries with AI agents

### Event Planning  
- `POST /api/plan_event` - Create event plans with real venue/vendor data
- Uses Tavily API for real-time venue and vendor search
- MOONSHOT LLM for intelligent event analysis

### Tech Planning
- `POST /api/plan_tech` - Generate software project plans and architecture

## AI Agent Features

### Travel Agent
- Multi-city itinerary planning
- Flight and hotel recommendations
- Points of interest suggestions
- Budget optimization

### Event Planning Agent
- **Real Venue Search**: Live venue recommendations via Tavily API
- **Vendor Discovery**: Catering, photography, decoration services
- **Cost Analysis**: Dynamic budget breakdown and optimization
- **Timeline Planning**: Intelligent event scheduling
- **No Mock Data**: All recommendations are from real businesses

### Tech Planning Agent
- Project architecture recommendations
- Technology stack suggestions
- Timeline and milestone planning
- Team size optimization

## Components Overview

### Dashboard Component
- Central hub for selecting different planners
- Beautiful gradient cards for each planning type
- Responsive grid layout with hover effects

### Travel Planning Components
- **TravelForm**: Comprehensive travel planning form with validation
- **TravelResults**: Multi-variant travel plans with detailed itineraries
- **TravelPlanner**: Container managing travel planning workflow

### Event Planning Components
- **EventForm**: Event details form with date/location/budget inputs
- **EventResults**: AI agent analysis display with real venue/vendor data
- **EventPlanner**: Event planning workflow management
- **Enhanced display**: Venue cards, vendor recommendations, cost breakdowns

### Tech Planning Components
- **TechPlanner**: Software project planning with tech stack selection
- **Project templates**: Pre-configured setups for common project types
- **Feature planning**: Detailed feature breakdown and timeline

### Shared Components
- **Header**: Navigation with planner type indicators
- **Hero**: Landing page with feature highlights
- **LoadingSpinner**: Animated loading states with progress indication

## Styling

The project uses Tailwind CSS with custom components and modern design patterns:

- **Design System**: Purple gradient theme with blue accents
- **Typography**: System font stack for optimal readability
- **Icons**: Heroicons for consistent iconography
- **Animations**: Smooth transitions, fade-ins, and hover effects
- **Responsive Design**: Mobile-first approach with breakpoint optimization
- **Cards & Layouts**: Modern card designs with shadows and borders
- **Color Palette**: 
  - Primary: Purple gradients (#7C3AED to #A855F7)
  - Secondary: Blue accents (#3B82F6)
  - Success: Green (#10B981)
  - Warning: Yellow (#F59E0B)

## Development Notes

- **State Management**: React hooks (useState, useEffect) for component state
- **API Communication**: Modern fetch API with async/await patterns
- **Error Handling**: Comprehensive error states and user feedback
- **Performance**: Optimized re-renders and efficient component structure
- **Code Organization**: Modular component structure with clear separation of concerns
- **Real Data Integration**: No mock data - all content from live AI agents and APIs
- **Accessibility**: Semantic HTML and ARIA labels for screen readers

## Environment Configuration

Create a `.env` file in the backend directory with:

```bash
MOONSHOT_API_KEY=your_moonshot_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## Deployment

For production deployment:

1. Build the frontend:
```bash
npm run build
```

2. Serve the built files with a static server
3. Ensure backend is deployed and accessible
4. Update API endpoints in the frontend if needed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
