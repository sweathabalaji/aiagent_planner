import React from "react"
import TechPlanner from "./TechPlanner"

const TechPlannerComingSoon = ({ onBack }) => {
  // Show the actual Tech Planner directly instead of Coming Soon page
  return <TechPlanner onBack={onBack} />
}

export default TechPlannerComingSoon