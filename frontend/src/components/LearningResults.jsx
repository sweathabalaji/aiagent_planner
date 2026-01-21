import { 
  AcademicCapIcon, 
  BookOpenIcon, 
  ClockIcon, 
  CheckCircleIcon,
  CalendarIcon,
  LightBulbIcon,
  ChartBarIcon,
  GlobeAltIcon,
  UserGroupIcon,
  WrenchScrewdriverIcon,
  ArrowRightIcon,
  SparklesIcon
} from '@heroicons/react/24/outline';
import { useState, useEffect, useRef } from 'react';
import TodoList from './TodoList';
import MCQAssessment from './MCQAssessment';
import Certificate from './Certificate';

export default function LearningResults({ learningPath }) {
  const { learning_plan, resources, schedule, progress_tracking, metadata, todo_list, session_id } = learningPath;
  const overview = learning_plan?.overview || {};
  const phases = learning_plan?.phases || [];
  const weeklySchedule = schedule?.weekly_schedule || [];
  const allResources = resources?.all_resources || {};
  const recommended = resources?.recommended || {};

  // State for managing workflow
  const [showTodoList, setShowTodoList] = useState(true);
  const [showAssessment, setShowAssessment] = useState(false);
  const [showCertificate, setShowCertificate] = useState(false);
  const [assessmentData, setAssessmentData] = useState(null);
  const assessmentRef = useRef(null);

  const handleTodosCompleted = () => {
    console.log('handleTodosCompleted called - showing assessment');
    setShowAssessment(true);
    // Scroll to assessment section after a brief delay
    setTimeout(() => {
      assessmentRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 300);
  };

  const handleAssessmentComplete = (results) => {
    setAssessmentData(results);
    if (results.passed) {
      setShowCertificate(true);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Card */}
      <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg shadow-lg p-8 text-white">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-3">
              <AcademicCapIcon className="w-10 h-10" />
              <h1 className="text-3xl font-bold">{overview.title || metadata.topic}</h1>
            </div>
            <p className="text-lg text-purple-100 mb-4">{overview.description}</p>
            <div className="flex flex-wrap gap-4 text-sm">
              <div className="flex items-center gap-2 bg-white/20 rounded-full px-4 py-2">
                <ClockIcon className="w-5 h-5" />
                <span>{overview.total_hours || 0} total hours</span>
              </div>
              <div className="flex items-center gap-2 bg-white/20 rounded-full px-4 py-2">
                <CalendarIcon className="w-5 h-5" />
                <span>{metadata.duration_weeks} weeks</span>
              </div>
              <div className="flex items-center gap-2 bg-white/20 rounded-full px-4 py-2">
                <ChartBarIcon className="w-5 h-5" />
                <span>{metadata.level}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Learning Phases */}
      {phases.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
            <SparklesIcon className="w-7 h-7 text-purple-600" />
            Learning Phases
          </h2>
          <div className="space-y-6">
            {phases.map((phase, index) => (
              <div key={index} className="border-l-4 border-purple-500 pl-6 pb-6 last:pb-0">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="text-xl font-bold text-gray-900">
                      Phase {phase.phase_number}: {phase.phase_name}
                    </h3>
                    <p className="text-sm text-gray-600 mt-1">
                      Duration: {phase.duration_weeks} weeks
                    </p>
                  </div>
                  <span className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm font-semibold">
                    Week {phases.slice(0, index).reduce((acc, p) => acc + (p.duration_weeks || 0), 0) + 1}-
                    {phases.slice(0, index + 1).reduce((acc, p) => acc + (p.duration_weeks || 0), 0)}
                  </span>
                </div>

                {/* Concepts */}
                {phase.concepts && phase.concepts.length > 0 && (
                  <div className="mb-3">
                    <h4 className="font-semibold text-gray-700 mb-2 flex items-center gap-2">
                      <LightBulbIcon className="w-5 h-5 text-yellow-500" />
                      Key Concepts
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {phase.concepts.map((concept, i) => (
                        <span key={i} className="bg-yellow-50 text-yellow-700 px-3 py-1 rounded-full text-sm border border-yellow-200">
                          {concept}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Skills */}
                {phase.skills && phase.skills.length > 0 && (
                  <div className="mb-3">
                    <h4 className="font-semibold text-gray-700 mb-2 flex items-center gap-2">
                      <CheckCircleIcon className="w-5 h-5 text-green-500" />
                      Skills to Master
                    </h4>
                    <ul className="space-y-1">
                      {phase.skills.map((skill, i) => (
                        <li key={i} className="text-gray-700 flex items-center gap-2">
                          <ArrowRightIcon className="w-4 h-4 text-green-500" />
                          {skill}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Project */}
                {phase.project && (
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-3">
                    <h4 className="font-semibold text-blue-900 mb-1">🚀 Practical Project</h4>
                    <p className="text-blue-800 text-sm">{phase.project}</p>
                  </div>
                )}

                {/* Assessment */}
                {phase.assessment && (
                  <div className="bg-gray-50 border border-gray-200 rounded-lg p-3">
                    <h4 className="font-semibold text-gray-700 text-sm mb-1">📝 Progress Check</h4>
                    <p className="text-gray-600 text-sm">{phase.assessment}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recommended Resources */}
      {recommended && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
            <BookOpenIcon className="w-7 h-7 text-blue-600" />
            Recommended Resources
          </h2>

          {/* Strategy */}
          {recommended.study_strategy && (
            <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-lg p-4 mb-6">
              <h3 className="font-semibold text-gray-900 mb-2">📚 Study Strategy</h3>
              <p className="text-gray-700">{recommended.study_strategy}</p>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Top Courses */}
            {recommended.top_courses && recommended.top_courses.length > 0 && (
              <ResourceCard
                title="Top Courses"
                icon={<AcademicCapIcon className="w-6 h-6 text-purple-600" />}
                resources={recommended.top_courses}
                color="purple"
              />
            )}

            {/* Top Books */}
            {recommended.top_books && recommended.top_books.length > 0 && (
              <ResourceCard
                title="Recommended Books"
                icon={<BookOpenIcon className="w-6 h-6 text-blue-600" />}
                resources={recommended.top_books}
                color="blue"
              />
            )}

            {/* Top Tutorials */}
            {recommended.top_tutorials && recommended.top_tutorials.length > 0 && (
              <ResourceCard
                title="Hands-on Tutorials"
                icon={<LightBulbIcon className="w-6 h-6 text-yellow-600" />}
                resources={recommended.top_tutorials}
                color="yellow"
              />
            )}

            {/* Practice Platforms */}
            {recommended.top_practice && recommended.top_practice.length > 0 && (
              <ResourceCard
                title="Practice Platforms"
                icon={<WrenchScrewdriverIcon className="w-6 h-6 text-green-600" />}
                resources={recommended.top_practice}
                color="green"
              />
            )}
          </div>

          {/* All Resources Categories */}
          <div className="mt-6 pt-6 border-t border-gray-200">
            <h3 className="font-semibold text-gray-900 mb-4">📖 Additional Resources</h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {allResources.communities && allResources.communities.length > 0 && (
                <ResourceBadge
                  label="Communities"
                  count={allResources.communities.length}
                  icon={<UserGroupIcon className="w-5 h-5" />}
                  color="indigo"
                />
              )}
              {allResources.tools && allResources.tools.length > 0 && (
                <ResourceBadge
                  label="Tools & Software"
                  count={allResources.tools.length}
                  icon={<WrenchScrewdriverIcon className="w-5 h-5" />}
                  color="gray"
                />
              )}
              {allResources.practice_platforms && allResources.practice_platforms.length > 0 && (
                <ResourceBadge
                  label="More Practice"
                  count={allResources.practice_platforms.length}
                  icon={<GlobeAltIcon className="w-5 h-5" />}
                  color="teal"
                />
              )}
            </div>
          </div>
        </div>
      )}

      {/* Study Schedule */}
      {weeklySchedule.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
            <CalendarIcon className="w-7 h-7 text-green-600" />
            Week-by-Week Schedule
          </h2>
          <div className="space-y-4">
            {weeklySchedule.map((week, index) => (
              <WeekCard key={index} week={week} />
            ))}
          </div>

          {/* Daily Routine */}
          {schedule.daily_routine && (
            <div className="mt-6 pt-6 border-t border-gray-200">
              <h3 className="font-semibold text-gray-900 mb-3">📅 Daily Study Routine</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <RoutineCard
                  title="Study Pattern"
                  content={schedule.daily_routine.recommended_pattern}
                  color="blue"
                />
                <RoutineCard
                  title="Break Strategy"
                  content={schedule.daily_routine.break_strategy}
                  color="green"
                />
                <RoutineCard
                  title="Review Schedule"
                  content={schedule.daily_routine.review_frequency}
                  color="purple"
                />
              </div>
            </div>
          )}
        </div>
      )}

      {/* Progress Tracking */}
      {progress_tracking && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
            <ChartBarIcon className="w-7 h-7 text-orange-600" />
            Progress Tracking
          </h2>

          {/* Self Evaluation */}
          {progress_tracking.self_evaluation && (
            <div className="space-y-4">
              <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
                <h3 className="font-semibold text-orange-900 mb-3">🎯 Weekly Self-Evaluation</h3>
                {progress_tracking.self_evaluation.weekly_questions && (
                  <ul className="space-y-2">
                    {progress_tracking.self_evaluation.weekly_questions.map((q, i) => (
                      <li key={i} className="text-orange-800 flex items-start gap-2">
                        <span className="font-semibold">{i + 1}.</span>
                        <span>{q}</span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>

              {progress_tracking.self_evaluation.mastery_indicators && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <h3 className="font-semibold text-green-900 mb-2">✅ Signs of Mastery</h3>
                  <ul className="space-y-1">
                    {progress_tracking.self_evaluation.mastery_indicators.map((indicator, i) => (
                      <li key={i} className="text-green-800 flex items-center gap-2">
                        <CheckCircleIcon className="w-4 h-4" />
                        {indicator}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Final Project */}
      {learning_plan.final_project && (
        <div className="bg-gradient-to-r from-purple-100 to-blue-100 border-2 border-purple-300 rounded-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-3 flex items-center gap-2">
            🏆 Capstone Project
          </h2>
          <p className="text-gray-800 text-lg">{learning_plan.final_project}</p>
        </div>
      )}

      {/* Todo List Section */}
      {showTodoList && todo_list && session_id && (
        <TodoList 
          todoList={todo_list} 
          sessionId={session_id}
          onAllCompleted={handleTodosCompleted}
        />
      )}

      {/* MCQ Assessment Section */}
      {console.log('Rendering check - showAssessment:', showAssessment, 'session_id:', session_id)}
      {showAssessment && session_id && (
        <div ref={assessmentRef}>
          <MCQAssessment 
            sessionId={session_id}
            onAssessmentComplete={handleAssessmentComplete}
          />
        </div>
      )}

      {/* Certificate Section */}
      {showCertificate && session_id && assessmentData && (
        <Certificate 
          sessionId={session_id}
          assessmentScore={assessmentData.score}
        />
      )}
    </div>
  );
}

// Helper Components
function ResourceCard({ title, icon, resources, color }) {
  return (
    <div className={`border-2 border-${color}-200 rounded-lg p-4 bg-${color}-50`}>
      <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
        {icon}
        {title}
      </h3>
      <div className="space-y-3">
        {resources.slice(0, 3).map((resource, i) => (
          <div key={i} className="bg-white rounded-lg p-3 shadow-sm border border-gray-200">
            <a
              href={resource.url}
              target="_blank"
              rel="noopener noreferrer"
              className="font-medium text-blue-600 hover:text-blue-800 text-sm block mb-1"
            >
              {resource.title || 'Resource'}
            </a>
            {resource.reason && (
              <p className="text-xs text-gray-600 mt-1">{resource.reason}</p>
            )}
            {resource.description && !resource.reason && (
              <p className="text-xs text-gray-600 mt-1">{resource.description.slice(0, 100)}...</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

function ResourceBadge({ label, count, icon, color }) {
  return (
    <div className={`bg-${color}-50 border border-${color}-200 rounded-lg p-3 flex items-center justify-between`}>
      <div className="flex items-center gap-2">
        <div className={`text-${color}-600`}>{icon}</div>
        <span className="text-sm font-medium text-gray-700">{label}</span>
      </div>
      <span className={`bg-${color}-200 text-${color}-800 px-2 py-1 rounded-full text-xs font-semibold`}>
        {count}
      </span>
    </div>
  );
}

function WeekCard({ week }) {
  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-3">
        <div>
          <h3 className="font-bold text-gray-900">Week {week.week}: {week.focus}</h3>
          {week.date_range && (
            <p className="text-sm text-gray-600 mt-1">{week.date_range}</p>
          )}
        </div>
        {week.milestone && (
          <span className="bg-green-100 text-green-700 px-2 py-1 rounded-full text-xs font-semibold">
            Milestone
          </span>
        )}
      </div>

      {week.topics && week.topics.length > 0 && (
        <div className="mb-2">
          <p className="text-sm font-medium text-gray-700 mb-1">Topics:</p>
          <div className="flex flex-wrap gap-1">
            {week.topics.map((topic, i) => (
              <span key={i} className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs">
                {topic}
              </span>
            ))}
          </div>
        </div>
      )}

      {week.activities && week.activities.length > 0 && (
        <div className="mt-3 space-y-1">
          {week.activities.map((activity, i) => (
            <div key={i} className="flex items-center justify-between text-sm">
              <span className="text-gray-700">{activity.activity}</span>
              <span className="text-purple-600 font-semibold">{activity.hours}h</span>
            </div>
          ))}
        </div>
      )}

      {week.milestone && (
        <div className="mt-3 pt-3 border-t border-gray-200">
          <p className="text-sm text-gray-700">
            <span className="font-semibold">Goal:</span> {week.milestone}
          </p>
        </div>
      )}
    </div>
  );
}

function RoutineCard({ title, content, color }) {
  return (
    <div className={`bg-${color}-50 border border-${color}-200 rounded-lg p-4`}>
      <h4 className={`font-semibold text-${color}-900 mb-2 text-sm`}>{title}</h4>
      <p className={`text-${color}-800 text-sm`}>{content}</p>
    </div>
  );
}
