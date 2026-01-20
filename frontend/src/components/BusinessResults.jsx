import { 
  BriefcaseIcon,
  LightBulbIcon,
  CurrencyDollarIcon,
  ChartBarIcon,
  ShieldCheckIcon,
  TrophyIcon,
  RocketLaunchIcon,
  ArrowTrendingUpIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';

export default function BusinessResults({ results }) {
  if (!results || !results.business_plan) {
    return null;
  }

  const plan = results.business_plan;
  const overview = plan.business_overview || {};
  const canvas = plan.business_model_canvas || {};
  const funding = plan.funding_strategy || {};
  const market = plan.market_analysis || {};
  const competitive = plan.competitive_analysis || {};
  const financial = plan.financial_projections || {};
  const gtm = plan.go_to_market_strategy || {};
  const nextSteps = plan.next_steps || [];

  return (
    <div className="space-y-6">
      {/* Business Overview */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-lg shadow-xl p-8">
        <div className="flex items-start gap-4">
          <BriefcaseIcon className="w-12 h-12 flex-shrink-0" />
          <div className="flex-1">
            <h1 className="text-3xl font-bold mb-2">{overview.business_name || 'Your Business'}</h1>
            <p className="text-xl text-blue-100 mb-4">{overview.tagline || ''}</p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
              <div className="bg-white/10 backdrop-blur rounded-lg p-3">
                <div className="text-sm text-blue-100">Industry</div>
                <div className="text-lg font-semibold">{overview.industry}</div>
              </div>
              <div className="bg-white/10 backdrop-blur rounded-lg p-3">
                <div className="text-sm text-blue-100">Business Model</div>
                <div className="text-lg font-semibold">{overview.business_model}</div>
              </div>
              <div className="bg-white/10 backdrop-blur rounded-lg p-3">
                <div className="text-sm text-blue-100">Location</div>
                <div className="text-lg font-semibold">{overview.location}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Business Model Canvas */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
          <LightBulbIcon className="w-7 h-7 text-yellow-500" />
          Business Model Canvas
        </h2>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Value Propositions */}
          {canvas.value_propositions && canvas.value_propositions.length > 0 && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                <span className="text-yellow-600">💡</span> Value Propositions
              </h3>
              {canvas.value_propositions.map((vp, idx) => (
                <div key={idx} className="mb-3">
                  <div className="font-medium text-gray-900">{vp.title}</div>
                  <div className="text-sm text-gray-700 mt-1">{vp.description}</div>
                  {vp.benefits && vp.benefits.length > 0 && (
                    <ul className="mt-2 space-y-1">
                      {vp.benefits.map((benefit, bidx) => (
                        <li key={bidx} className="text-sm text-gray-600 flex items-start gap-1">
                          <CheckCircleIcon className="w-4 h-4 text-green-500 flex-shrink-0 mt-0.5" />
                          {benefit}
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Customer Segments */}
          {canvas.customer_segments && canvas.customer_segments.length > 0 && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                <span className="text-blue-600">👥</span> Customer Segments
              </h3>
              {canvas.customer_segments.map((seg, idx) => (
                <div key={idx} className="mb-3">
                  <div className="font-medium text-gray-900">{seg.segment}</div>
                  <div className="text-sm text-gray-700 mt-1">{seg.description}</div>
                  <div className="text-sm text-gray-600 mt-1">Market Size: {seg.size}</div>
                  {seg.characteristics && seg.characteristics.length > 0 && (
                    <ul className="mt-2 space-y-1">
                      {seg.characteristics.map((char, cidx) => (
                        <li key={cidx} className="text-sm text-gray-600">• {char}</li>
                      ))}
                    </ul>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Revenue Streams */}
          {canvas.revenue_streams && canvas.revenue_streams.length > 0 && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                <span className="text-green-600">💰</span> Revenue Streams
              </h3>
              {canvas.revenue_streams.map((stream, idx) => (
                <div key={idx} className="mb-3 pb-3 border-b border-green-200 last:border-0">
                  <div className="font-medium text-gray-900">{stream.stream}</div>
                  <div className="grid grid-cols-2 gap-2 mt-2 text-sm">
                    <div>
                      <span className="text-gray-600">Type:</span> <span className="font-medium">{stream.type}</span>
                    </div>
                    <div>
                      <span className="text-gray-600">Potential:</span> <span className="font-medium">{stream.potential}</span>
                    </div>
                  </div>
                  <div className="text-sm text-gray-700 mt-1">{stream.pricing_model}</div>
                </div>
              ))}
            </div>
          )}

          {/* Key Resources */}
          {canvas.key_resources && canvas.key_resources.length > 0 && (
            <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                <span className="text-purple-600">🔑</span> Key Resources
              </h3>
              {canvas.key_resources.map((resource, idx) => (
                <div key={idx} className="mb-3">
                  <div className="font-medium text-gray-900">{resource.category}</div>
                  <ul className="mt-1 space-y-1">
                    {resource.resources && resource.resources.map((r, ridx) => (
                      <li key={ridx} className="text-sm text-gray-700">• {r}</li>
                    ))}
                  </ul>
                  <div className="text-sm text-gray-600 mt-1 italic">{resource.importance}</div>
                </div>
              ))}
            </div>
          )}

          {/* Channels */}
          {canvas.channels && canvas.channels.length > 0 && (
            <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                <span className="text-indigo-600">📢</span> Channels
              </h3>
              {canvas.channels.map((channel, idx) => (
                <div key={idx} className="mb-3 pb-3 border-b border-indigo-200 last:border-0">
                  <div className="font-medium text-gray-900">{channel.channel}</div>
                  <div className="text-sm text-gray-700 mt-1">{channel.purpose}</div>
                  <div className="flex gap-4 mt-2 text-sm">
                    <span className="text-gray-600">Type: <span className="font-medium">{channel.type}</span></span>
                    <span className="text-gray-600">Cost: <span className="font-medium">{channel.cost}</span></span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Cost Structure */}
          {canvas.cost_structure && canvas.cost_structure.length > 0 && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                <span className="text-red-600">💸</span> Cost Structure
              </h3>
              {canvas.cost_structure.map((cost, idx) => (
                <div key={idx} className="mb-3">
                  <div className="font-medium text-gray-900">{cost.category}</div>
                  <ul className="mt-1 space-y-1">
                    {cost.items && cost.items.map((item, iidx) => (
                      <li key={iidx} className="text-sm text-gray-700">• {item}</li>
                    ))}
                  </ul>
                  <div className="flex gap-4 mt-2 text-sm">
                    <span className="text-gray-600">Type: <span className="font-medium">{cost.type}</span></span>
                    <span className="text-gray-600">Priority: <span className="font-medium">{cost.priority}</span></span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Funding Strategy */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
          <CurrencyDollarIcon className="w-7 h-7 text-green-500" />
          Funding Strategy
        </h2>

        {/* Funding Stages */}
        {funding.funding_stages && funding.funding_stages.length > 0 && (
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Funding Stages</h3>
            <div className="space-y-4">
              {funding.funding_stages.map((stage, idx) => (
                <div key={idx} className="bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-semibold text-lg text-gray-900">{stage.stage}</h4>
                    <span className="bg-green-600 text-white px-3 py-1 rounded-full text-sm font-medium">{stage.amount}</span>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-600 font-medium">Timing:</span> {stage.timing}
                    </div>
                    <div>
                      <span className="text-gray-600 font-medium">Valuation:</span> {stage.valuation_range}
                    </div>
                  </div>
                  <div className="mt-2">
                    <span className="text-gray-600 font-medium">Purpose:</span> {stage.purpose}
                  </div>
                  {stage.milestones && stage.milestones.length > 0 && (
                    <div className="mt-3">
                      <span className="text-gray-600 font-medium">Milestones:</span>
                      <ul className="mt-1 space-y-1">
                        {stage.milestones.map((milestone, midx) => (
                          <li key={midx} className="text-gray-700 flex items-center gap-2">
                            <CheckCircleIcon className="w-4 h-4 text-green-500" />
                            {milestone}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Funding Sources */}
        {funding.funding_sources && funding.funding_sources.length > 0 && (
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Funding Sources</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {funding.funding_sources.map((source, idx) => (
                <div key={idx} className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                  <h4 className="font-semibold text-gray-900 mb-2">{source.source}</h4>
                  <p className="text-sm text-gray-700 mb-3">{source.description}</p>
                  <div className="text-sm mb-2">
                    <span className="text-gray-600 font-medium">Typical Amount:</span> {source.typical_amount}
                  </div>
                  <div className="text-sm mb-2">
                    <span className="text-gray-600 font-medium">Best For:</span> {source.best_for}
                  </div>
                  <div className="grid grid-cols-2 gap-2 mt-3">
                    <div>
                      <div className="text-xs text-gray-600 font-medium mb-1">Pros:</div>
                      <ul className="space-y-1">
                        {source.pros && source.pros.slice(0, 2).map((pro, pidx) => (
                          <li key={pidx} className="text-xs text-green-700">✓ {pro}</li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <div className="text-xs text-gray-600 font-medium mb-1">Cons:</div>
                      <ul className="space-y-1">
                        {source.cons && source.cons.slice(0, 2).map((con, cidx) => (
                          <li key={cidx} className="text-xs text-red-700">✗ {con}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Market Analysis */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
          <ChartBarIcon className="w-7 h-7 text-blue-500" />
          Market Analysis
        </h2>

        {/* Market Size */}
        {market.market_size && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-5 mb-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Market Size & Opportunity</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-white rounded-lg p-4 shadow-sm">
                <div className="text-sm text-gray-600 mb-1">TAM (Total Addressable Market)</div>
                <div className="text-xl font-bold text-blue-600">{market.market_size.total_addressable_market}</div>
              </div>
              <div className="bg-white rounded-lg p-4 shadow-sm">
                <div className="text-sm text-gray-600 mb-1">SAM (Serviceable Addressable)</div>
                <div className="text-xl font-bold text-blue-600">{market.market_size.serviceable_addressable_market}</div>
              </div>
              <div className="bg-white rounded-lg p-4 shadow-sm">
                <div className="text-sm text-gray-600 mb-1">SOM (Serviceable Obtainable)</div>
                <div className="text-xl font-bold text-blue-600">{market.market_size.serviceable_obtainable_market}</div>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4 mt-4">
              <div className="text-sm">
                <span className="text-gray-600 font-medium">Growth Rate:</span> <span className="text-green-600 font-semibold">{market.market_size.growth_rate}</span>
              </div>
              <div className="text-sm">
                <span className="text-gray-600 font-medium">Market Maturity:</span> <span className="font-semibold">{market.market_size.market_maturity}</span>
              </div>
            </div>
          </div>
        )}

        {/* Market Trends */}
        {market.market_trends && market.market_trends.length > 0 && (
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Market Trends</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {market.market_trends.map((trend, idx) => (
                <div key={idx} className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-semibold text-gray-900">{trend.trend}</h4>
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      trend.opportunity_level === 'High' ? 'bg-green-100 text-green-700' :
                      trend.opportunity_level === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-gray-100 text-gray-700'
                    }`}>
                      {trend.opportunity_level}
                    </span>
                  </div>
                  <p className="text-sm text-gray-700 mb-2">{trend.description}</p>
                  <p className="text-sm text-gray-600"><strong>Impact:</strong> {trend.impact}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Competitive Analysis */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
          <ShieldCheckIcon className="w-7 h-7 text-purple-500" />
          Competitive Analysis
        </h2>

        {/* SWOT Analysis */}
        {competitive.swot_analysis && (
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">SWOT Analysis</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <h4 className="font-semibold text-green-900 mb-3 flex items-center gap-2">
                  <TrophyIcon className="w-5 h-5" />
                  Strengths
                </h4>
                <ul className="space-y-2">
                  {competitive.swot_analysis.strengths && competitive.swot_analysis.strengths.map((item, idx) => (
                    <li key={idx} className="text-sm text-gray-700 flex items-start gap-2">
                      <span className="text-green-600 font-bold">+</span>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <h4 className="font-semibold text-red-900 mb-3">⚠️ Weaknesses</h4>
                <ul className="space-y-2">
                  {competitive.swot_analysis.weaknesses && competitive.swot_analysis.weaknesses.map((item, idx) => (
                    <li key={idx} className="text-sm text-gray-700 flex items-start gap-2">
                      <span className="text-red-600 font-bold">-</span>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h4 className="font-semibold text-blue-900 mb-3">🎯 Opportunities</h4>
                <ul className="space-y-2">
                  {competitive.swot_analysis.opportunities && competitive.swot_analysis.opportunities.map((item, idx) => (
                    <li key={idx} className="text-sm text-gray-700 flex items-start gap-2">
                      <span className="text-blue-600 font-bold">→</span>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
              <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
                <h4 className="font-semibold text-orange-900 mb-3">⚡ Threats</h4>
                <ul className="space-y-2">
                  {competitive.swot_analysis.threats && competitive.swot_analysis.threats.map((item, idx) => (
                    <li key={idx} className="text-sm text-gray-700 flex items-start gap-2">
                      <span className="text-orange-600 font-bold">!</span>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* Competitive Advantages */}
        {competitive.competitive_advantages && competitive.competitive_advantages.length > 0 && (
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Competitive Advantages</h3>
            <div className="space-y-3">
              {competitive.competitive_advantages.map((adv, idx) => (
                <div key={idx} className="bg-gradient-to-r from-purple-50 to-indigo-50 border border-purple-200 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-semibold text-gray-900">{adv.advantage}</h4>
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      adv.impact === 'High' ? 'bg-green-100 text-green-700' :
                      adv.impact === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-gray-100 text-gray-700'
                    }`}>
                      {adv.impact} Impact
                    </span>
                  </div>
                  <p className="text-sm text-gray-700 mb-2">{adv.description}</p>
                  <p className="text-sm text-gray-600"><strong>Sustainability:</strong> {adv.sustainability}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Financial Projections */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
          <ArrowTrendingUpIcon className="w-7 h-7 text-green-500" />
          Financial Projections
        </h2>

        {/* Revenue Projections */}
        {financial.revenue_projections && financial.revenue_projections.length > 0 && (
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">3-Year Revenue Forecast</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {financial.revenue_projections.map((proj, idx) => (
                <div key={idx} className="bg-gradient-to-br from-green-50 to-emerald-50 border border-green-200 rounded-lg p-5">
                  <div className="text-center mb-4">
                    <div className="text-sm text-gray-600 mb-1">Year {proj.year}</div>
                    <div className="text-3xl font-bold text-green-600">{proj.revenue}</div>
                  </div>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Customers:</span>
                      <span className="font-semibold">{proj.customers}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Avg Value:</span>
                      <span className="font-semibold">{proj.avg_customer_value}</span>
                    </div>
                    {proj.growth_rate && proj.growth_rate !== 'N/A' && (
                      <div className="flex justify-between">
                        <span className="text-gray-600">Growth:</span>
                        <span className="font-semibold text-green-600">{proj.growth_rate}</span>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Startup Costs */}
        {financial.startup_costs && financial.startup_costs.length > 0 && (
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Startup Costs</h3>
            <div className="bg-gray-50 border border-gray-200 rounded-lg overflow-hidden">
              <table className="w-full">
                <thead className="bg-gray-100">
                  <tr>
                    <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">Category</th>
                    <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">Items</th>
                    <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">Cost</th>
                    <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">Timing</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {financial.startup_costs.map((cost, idx) => (
                    <tr key={idx}>
                      <td className="px-4 py-3 text-sm font-medium text-gray-900">{cost.category}</td>
                      <td className="px-4 py-3 text-sm text-gray-700">{cost.items && cost.items.join(', ')}</td>
                      <td className="px-4 py-3 text-sm font-semibold text-gray-900">{cost.estimated_cost}</td>
                      <td className="px-4 py-3 text-sm text-gray-600">{cost.timing}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>

      {/* Go-to-Market Strategy */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
          <RocketLaunchIcon className="w-7 h-7 text-orange-500" />
          Go-to-Market Strategy
        </h2>

        {/* Launch Strategy */}
        {gtm.launch_strategy && (
          <div className="bg-orange-50 border border-orange-200 rounded-lg p-5 mb-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Launch Strategy</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <div className="text-sm text-gray-600 mb-1">Approach</div>
                <div className="font-semibold text-gray-900">{gtm.launch_strategy.launch_approach}</div>
              </div>
              <div>
                <div className="text-sm text-gray-600 mb-1">Timeline</div>
                <div className="font-semibold text-gray-900">{gtm.launch_strategy.timeline}</div>
              </div>
            </div>
            {gtm.launch_strategy.initial_markets && gtm.launch_strategy.initial_markets.length > 0 && (
              <div className="mt-4">
                <div className="text-sm text-gray-600 mb-2">Initial Markets</div>
                <div className="flex flex-wrap gap-2">
                  {gtm.launch_strategy.initial_markets.map((market, idx) => (
                    <span key={idx} className="bg-white px-3 py-1 rounded-full text-sm font-medium text-gray-700 border border-orange-200">
                      {market}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Marketing Channels */}
        {gtm.marketing_channels && gtm.marketing_channels.length > 0 && (
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Marketing Channels</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {gtm.marketing_channels.map((channel, idx) => (
                <div key={idx} className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-3">
                    <h4 className="font-semibold text-gray-900">{channel.channel}</h4>
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      channel.priority === 'High' ? 'bg-red-100 text-red-700' :
                      channel.priority === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-gray-100 text-gray-700'
                    }`}>
                      {channel.priority} Priority
                    </span>
                  </div>
                  <div className="space-y-2 text-sm">
                    <div>
                      <span className="text-gray-600 font-medium">Tactics:</span>
                      <ul className="mt-1 space-y-1">
                        {channel.tactics && channel.tactics.map((tactic, tidx) => (
                          <li key={tidx} className="text-gray-700">• {tactic}</li>
                        ))}
                      </ul>
                    </div>
                    <div className="flex justify-between pt-2 border-t border-gray-200">
                      <span className="text-gray-600">Expected ROI:</span>
                      <span className="font-semibold text-green-600">{channel.expected_roi}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Next Steps */}
      {nextSteps && nextSteps.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
            <CheckCircleIcon className="w-7 h-7 text-blue-500" />
            Next Steps & Action Plan
          </h2>
          <div className="space-y-4">
            {nextSteps.map((step, idx) => (
              <div key={idx} className="bg-gradient-to-r from-blue-50 to-indigo-50 border-l-4 border-blue-500 rounded-r-lg p-5">
                <div className="flex justify-between items-start mb-3">
                  <div className="flex items-start gap-3">
                    <div className="bg-blue-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold flex-shrink-0">
                      {step.step}
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">{step.action}</h3>
                      <div className="flex gap-4 mt-1 text-sm">
                        <span className="text-gray-600">⏱️ {step.timeline}</span>
                        <span className={`font-medium ${
                          step.priority === 'Critical' ? 'text-red-600' :
                          step.priority === 'High' ? 'text-orange-600' :
                          'text-blue-600'
                        }`}>
                          {step.priority} Priority
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
                <ul className="space-y-2 ml-11">
                  {step.tasks && step.tasks.map((task, tidx) => (
                    <li key={tidx} className="text-sm text-gray-700 flex items-start gap-2">
                      <CheckCircleIcon className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                      {task}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Download/Export Actions */}
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 text-center">
        <p className="text-gray-700 mb-4">
          💼 Your comprehensive business plan is ready! Review each section carefully and adapt it to your specific needs.
        </p>
        <p className="text-sm text-gray-600">
          Consult with legal, financial, and industry experts before making major business decisions.
        </p>
      </div>
    </div>
  );
}
