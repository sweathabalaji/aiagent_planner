import React, { useState } from 'react'
import {
  ArrowLeft, Plane, Building, MapPin, Calendar, RefreshCw,
  ChevronDown, ChevronUp, Clock, Star, Utensils, Navigation,
  Lightbulb, DollarSign, Info, Coffee, Sun, Sunset, Moon
} from 'lucide-react'

/* ─── tiny helpers ────────────────────────────────────────────────── */
const fmt = (n) => {
  const num = Number(n)
  return isNaN(num) ? '0' : Math.round(num).toLocaleString('en-IN')
}

const StarRating = ({ rating }) => {
  const r = Math.min(5, Math.max(0, Number(rating) || 0))
  return (
    <span className="flex items-center gap-0.5">
      {[1, 2, 3, 4, 5].map(s => (
        <Star
          key={s}
          className={`h-3.5 w-3.5 ${s <= Math.round(r) ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300'}`}
        />
      ))}
      <span className="text-xs text-gray-500 ml-1">{r.toFixed(1)}</span>
    </span>
  )
}

const Badge = ({ children, color = 'blue' }) => {
  const colours = {
    blue: 'bg-blue-100 text-blue-700',
    green: 'bg-green-100 text-green-700',
    purple: 'bg-purple-100 text-purple-700',
    orange: 'bg-orange-100 text-orange-700',
    gray: 'bg-gray-100 text-gray-700',
    red: 'bg-red-100 text-red-700',
    yellow: 'bg-yellow-100 text-yellow-700'
  }
  return (
    <span className={`inline-block text-xs font-medium px-2 py-0.5 rounded-full ${colours[color] || colours.blue}`}>
      {children}
    </span>
  )
}

const periodIcon = (period = '') => {
  const p = period.toLowerCase()
  if (p.includes('morning')) return <Coffee className="h-4 w-4 text-amber-500" />
  if (p.includes('afternoon')) return <Sun className="h-4 w-4 text-orange-400" />
  if (p.includes('late afternoon') || p.includes('sunset')) return <Sunset className="h-4 w-4 text-rose-400" />
  if (p.includes('evening') || p.includes('night')) return <Moon className="h-4 w-4 text-indigo-400" />
  return <Clock className="h-4 w-4 text-blue-400" />
}

const typeColor = (type = '') => {
  const t = type.toLowerCase()
  if (t.includes('historic')) return 'orange'
  if (t.includes('nature')) return 'green'
  if (t.includes('cultural')) return 'purple'
  if (t.includes('shopping')) return 'yellow'
  if (t.includes('food')) return 'red'
  return 'blue'
}

/* ─── section toggle ─────────────────────────────────────────────── */
const SectionToggle = ({ title, icon, count, children, defaultOpen = true }) => {
  const [open, setOpen] = useState(defaultOpen)
  return (
    <div className="card mb-6">
      <button
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-center justify-between text-left mb-2"
      >
        <h3 className="text-xl font-semibold text-gray-900 flex items-center gap-2">
          {icon}
          {title}
          {count !== undefined && (
            <span className="text-sm font-normal text-gray-500">({count})</span>
          )}
        </h3>
        {open ? <ChevronUp className="h-5 w-5 text-gray-400" /> : <ChevronDown className="h-5 w-5 text-gray-400" />}
      </button>
      {open && <div className="mt-4">{children}</div>}
    </div>
  )
}

/* ─── flight card ────────────────────────────────────────────────── */
const FlightCard = ({ flight, idx }) => (
  <div className="border border-gray-200 rounded-xl p-4 hover:shadow-md transition-all bg-white">
    <div className="flex justify-between items-start gap-4">
      <div className="flex-1">
        {/* airline + class */}
        <div className="flex flex-wrap items-center gap-2 mb-2">
          <span className="text-blue-700 font-bold text-lg">{flight.airline || `Option ${idx + 1}`}</span>
          {flight.class && <Badge color="blue">{flight.class}</Badge>}
          {flight.stops && (
            <Badge color={flight.stops?.toLowerCase().includes('direct') ? 'green' : 'orange'}>
              {flight.stops}
            </Badge>
          )}
        </div>

        {/* times */}
        {(flight.departure || flight.arrival) && (
          <div className="flex items-center gap-3 text-sm text-gray-700 mb-2">
            <span className="font-semibold">{flight.departure || '—'}</span>
            <span className="text-gray-400 flex-1 text-center border-t border-dashed border-gray-300 relative">
              <span className="absolute -top-2.5 left-1/2 -translate-x-1/2 bg-white px-1 text-xs text-gray-400">
                {flight.duration || ''}
              </span>
            </span>
            <span className="font-semibold">{flight.arrival || '—'}</span>
          </div>
        )}

        {/* route */}
        <div className="text-sm text-gray-500">{flight.route || ''}</div>

        {flight.source && (
          <div className="text-xs text-gray-400 mt-1">Source: {flight.source}</div>
        )}
      </div>

      {/* price + link */}
      <div className="text-right shrink-0">
        <div className="text-2xl font-bold text-blue-600">₹{fmt(flight.price)}</div>
        <div className="text-xs text-gray-500 mb-2">per person (one-way)</div>
        {flight.url && (
          <a
            href={flight.url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block text-xs bg-blue-600 text-white px-3 py-1.5 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Book Now →
          </a>
        )}
      </div>
    </div>
  </div>
)

/* ─── hotel card ─────────────────────────────────────────────────── */
const HotelCard = ({ hotel, nights }) => {
  const ppn = Number(hotel.price_per_night || hotel.price || 0)
  const total = hotel.total_price || ppn * (nights || 1)
  const cat = (hotel.category || '').toLowerCase()

  return (
    <div className="border border-gray-200 rounded-xl p-4 hover:shadow-md transition-all bg-white">
      <div className="flex justify-between items-start gap-4">
        <div className="flex-1">
          {/* name + category */}
          <div className="flex flex-wrap items-center gap-2 mb-1">
            <span className="font-bold text-gray-900 text-lg">{hotel.name || 'Hotel'}</span>
            {cat && (
              <Badge color={cat === 'luxury' ? 'purple' : cat === 'budget' ? 'green' : 'blue'}>
                {cat.charAt(0).toUpperCase() + cat.slice(1)}
              </Badge>
            )}
          </div>

          {/* star rating */}
          {hotel.rating && <StarRating rating={hotel.rating} />}

          {/* location */}
          <div className="flex items-center gap-1 text-sm text-gray-600 mt-1">
            <MapPin className="h-3.5 w-3.5 text-gray-400" />
            <span>{hotel.location || hotel.address || 'City Center'}</span>
          </div>

          {/* room type */}
          {hotel.room_type && (
            <div className="text-sm text-gray-500 mt-1">Room: {hotel.room_type}</div>
          )}

          {/* amenities */}
          {hotel.amenities && hotel.amenities.length > 0 && (
            <div className="flex flex-wrap gap-1 mt-2">
              {hotel.amenities.slice(0, 6).map((a, i) => (
                <Badge key={i} color="gray">{a}</Badge>
              ))}
              {hotel.amenities.length > 6 && (
                <Badge color="gray">+{hotel.amenities.length - 6} more</Badge>
              )}
            </div>
          )}

          {hotel.source && (
            <div className="text-xs text-gray-400 mt-2">Source: {hotel.source}</div>
          )}
        </div>

        {/* price + link */}
        <div className="text-right shrink-0">
          <div className="text-2xl font-bold text-green-600">₹{fmt(total)}</div>
          <div className="text-xs text-gray-500">total stay</div>
          {ppn > 0 && (
            <div className="text-sm text-gray-600 mt-0.5">₹{fmt(ppn)} / night</div>
          )}
          {nights && (
            <div className="text-xs text-gray-400">{nights} night{nights > 1 ? 's' : ''}</div>
          )}
          {hotel.url && (
            <a
              href={hotel.url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block mt-2 text-xs bg-green-600 text-white px-3 py-1.5 rounded-lg hover:bg-green-700 transition-colors"
            >
              View Hotel →
            </a>
          )}
        </div>
      </div>
    </div>
  )
}

/* ─── activity card ──────────────────────────────────────────────── */
const ActivityCard = ({ activity, idx }) => {
  const [expanded, setExpanded] = useState(false)

  return (
    <div className="bg-white border border-gray-100 rounded-xl p-4 hover:shadow-sm transition-all">
      {/* header row */}
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3 flex-1 min-w-0">
          {/* slot number */}
          <div className="shrink-0 w-7 h-7 rounded-full bg-blue-600 text-white text-xs flex items-center justify-center font-bold">
            {idx + 1}
          </div>

          <div className="min-w-0 flex-1">
            {/* time + period */}
            <div className="flex flex-wrap items-center gap-2 mb-1">
              <span className="flex items-center gap-1 text-blue-600 text-sm font-semibold">
                {periodIcon(activity.period)}
                {activity.time || ''}
              </span>
              {activity.type && (
                <Badge color={typeColor(activity.type)}>{activity.type}</Badge>
              )}
              {activity.rating > 0 && (
                <span className="text-xs text-yellow-600">⭐ {Number(activity.rating).toFixed(1)}</span>
              )}
            </div>

            {/* place name */}
            <div className="font-bold text-gray-900 text-base leading-tight">
              {activity.activity || activity.name || `Place ${idx + 1}`}
            </div>

            {/* location */}
            {activity.location && (
              <div className="flex items-center gap-1 text-xs text-gray-500 mt-0.5">
                <MapPin className="h-3 w-3" />
                {activity.location}
              </div>
            )}
          </div>
        </div>

        {/* cost */}
        <div className="text-right shrink-0">
          {Number(activity.cost) > 0 ? (
            <>
              <div className="text-sm font-bold text-purple-600">₹{fmt(activity.cost)}</div>
              <div className="text-xs text-gray-500">entry fee</div>
            </>
          ) : (
            <div className="text-sm text-green-600 font-medium">Free Entry</div>
          )}
        </div>
      </div>

      {/* description */}
      {activity.description && (
        <p className="text-sm text-gray-600 mt-2 leading-relaxed line-clamp-2">
          {activity.description}
        </p>
      )}

      {/* expand toggle */}
      {(activity.tips || activity.meal_suggestion || activity.transport || activity.url) && (
        <button
          onClick={() => setExpanded(e => !e)}
          className="mt-2 text-xs text-blue-500 hover:text-blue-700 flex items-center gap-1"
        >
          {expanded ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />}
          {expanded ? 'Show less' : 'Tips, food & transport'}
        </button>
      )}

      {expanded && (
        <div className="mt-3 space-y-2 pl-2 border-l-2 border-blue-100">
          {activity.tips && (
            <div className="flex items-start gap-2 text-xs text-gray-600">
              <Lightbulb className="h-3.5 w-3.5 text-yellow-500 mt-0.5 shrink-0" />
              <span><strong>Tip:</strong> {activity.tips}</span>
            </div>
          )}
          {activity.meal_suggestion && (
            <div className="flex items-start gap-2 text-xs text-gray-600">
              <Utensils className="h-3.5 w-3.5 text-red-400 mt-0.5 shrink-0" />
              <span><strong>Eat nearby:</strong> {activity.meal_suggestion}</span>
            </div>
          )}
          {activity.transport && (
            <div className="flex items-start gap-2 text-xs text-gray-600">
              <Navigation className="h-3.5 w-3.5 text-blue-400 mt-0.5 shrink-0" />
              <span><strong>Get there:</strong> {activity.transport}</span>
            </div>
          )}
          {activity.url && (
            <a
              href={activity.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-blue-500 hover:underline block"
            >
              More Info →
            </a>
          )}
        </div>
      )}
    </div>
  )
}

/* ─── day card ───────────────────────────────────────────────────── */
const DayCard = ({ day, idx }) => {
  const [open, setOpen] = useState(idx === 0)

  return (
    <div className="border border-gray-200 rounded-xl overflow-hidden">
      {/* day header */}
      <button
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-center gap-4 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 hover:from-blue-100 hover:to-indigo-100 transition-colors text-left"
      >
        <div className="w-10 h-10 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold text-lg shrink-0">
          {day.day}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex flex-wrap items-center gap-2">
            <span className="font-bold text-gray-900">
              {day.theme || `Day ${day.day}`}
            </span>
            {day.date && (
              <span className="text-sm text-gray-500">({day.date})</span>
            )}
          </div>
          <div className="flex items-center gap-3 mt-0.5 text-xs text-gray-500">
            <span>{(day.activities || []).length} activities</span>
            {day.estimated_cost > 0 && <span>Est. ₹{fmt(day.estimated_cost)}</span>}
          </div>
        </div>
        {open ? <ChevronUp className="h-5 w-5 text-gray-400 shrink-0" /> : <ChevronDown className="h-5 w-5 text-gray-400 shrink-0" />}
      </button>

      {open && (
        <div className="p-4 space-y-3 bg-gray-50">
          {/* activities */}
          {(day.activities || []).length > 0 ? (
            <div className="space-y-3">
              {day.activities.map((act, ai) => (
                <ActivityCard key={ai} activity={act} idx={ai} />
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-400 italic text-center py-4">No activities planned for this day</p>
          )}

          {/* meals section */}
          {day.meals && (
            <div className="mt-4 bg-amber-50 border border-amber-200 rounded-xl p-4">
              <h5 className="font-semibold text-amber-800 mb-3 flex items-center gap-2">
                <Utensils className="h-4 w-4" />
                Recommended Meals for Day {day.day}
              </h5>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-sm">
                {day.meals.breakfast && (
                  <div>
                    <div className="text-xs font-medium text-amber-700 mb-1">🌅 Breakfast</div>
                    <div className="text-gray-700">{day.meals.breakfast}</div>
                  </div>
                )}
                {day.meals.lunch && (
                  <div>
                    <div className="text-xs font-medium text-amber-700 mb-1">☀️ Lunch</div>
                    <div className="text-gray-700">{day.meals.lunch}</div>
                  </div>
                )}
                {day.meals.dinner && (
                  <div>
                    <div className="text-xs font-medium text-amber-700 mb-1">🌙 Dinner</div>
                    <div className="text-gray-700">{day.meals.dinner}</div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

/* ─── main component ─────────────────────────────────────────────── */
const TravelResults = ({ results, onBack, onPlanAnother }) => {
  const [selectedVariant, setSelectedVariant] = useState(0)

  const variant = results?.variants?.[selectedVariant]
  const userReq = results?.user_request || {}
  const nights = variant?.itinerary?.length || userReq.nights || 3

  if (!results || !variant) {
    return (
      <div className="text-center py-16">
        <p className="text-gray-500 mb-4">No results available</p>
        <button onClick={onBack} className="btn-primary">
          <ArrowLeft className="h-4 w-4 mr-2" /> Back to Form
        </button>
      </div>
    )
  }

  const variantIcon = (name = '') => {
    const n = name.toLowerCase()
    if (n.includes('budget')) return '💰'
    if (n.includes('premium') || n.includes('luxury')) return '👑'
    return '⭐'
  }

  return (
    <div className="max-w-5xl mx-auto animate-fade-in space-y-0">

      {/* ── header ── */}
      <div className="card mb-6">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-1">Your Travel Plan is Ready! 🎉</h1>
            <p className="text-gray-500">
              {userReq.destination && `Trip to ${userReq.destination}`}
              {userReq.origin && ` from ${userReq.origin}`}
              {userReq.budget && ` • Budget ₹${fmt(userReq.budget)}`}
              {userReq.travelers && ` • ${userReq.travelers} traveler(s)`}
            </p>
          </div>
          <div className="flex gap-3">
            <button onClick={onBack} className="btn-secondary flex items-center gap-2">
              <ArrowLeft className="h-4 w-4" /> Back
            </button>
            <button onClick={onPlanAnother} className="btn-primary flex items-center gap-2">
              <RefreshCw className="h-4 w-4" /> Plan Another Trip
            </button>
          </div>
        </div>
      </div>

      {/* ── variant selector ── */}
      <div className="card mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Choose Your Plan</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {results.variants.map((v, idx) => (
            <button
              key={idx}
              onClick={() => setSelectedVariant(idx)}
              className={`p-4 rounded-xl border-2 transition-all duration-200 text-left ${
                selectedVariant === idx
                  ? 'border-blue-500 bg-blue-50 shadow-md'
                  : 'border-gray-200 hover:border-blue-300 bg-white'
              }`}
            >
              <div className="flex justify-between items-start mb-2">
                <div className="font-bold text-gray-900 flex items-center gap-1">
                  <span>{variantIcon(v.variant)}</span>
                  <span>{v.variant || `Option ${idx + 1}`}</span>
                </div>
                <div className="text-right">
                  <div className="text-xl font-bold text-blue-600">₹{fmt(v.estimated_cost)}</div>
                  <div className="text-xs text-gray-400">total cost</div>
                </div>
              </div>

              <div className="text-xs text-gray-500 space-y-0.5 mb-2">
                <div>{(v.flights || []).length} flight option(s)</div>
                <div>{(v.hotels || []).length} hotel option(s)</div>
                <div>{(v.itinerary || []).length}-day itinerary • {(v.itinerary || []).length * 5} places</div>
              </div>

              <div className="flex flex-wrap gap-1">
                {v.within_budget && <Badge color="green">✓ Within Budget</Badge>}
                {v.savings > 0 && <Badge color="green">Saves ₹{fmt(v.savings)}</Badge>}
                {!v.within_budget && <Badge color="orange">Above Budget</Badge>}
              </div>

              {v.features && v.features.length > 0 && (
                <div className="mt-2 text-xs text-gray-500 line-clamp-2">
                  {v.features.slice(0, 2).join(' • ')}
                </div>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* ── cost breakdown ── */}
      {variant.cost_breakdown && (
        <div className="card mb-6 bg-gradient-to-r from-amber-50 to-orange-50 border border-orange-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <DollarSign className="h-5 w-5 text-orange-500" />
            Cost Breakdown — {variant.variant}
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
            {[
              { label: 'Flights', key: 'flights', color: 'text-blue-600', icon: '✈️' },
              { label: 'Accommodation', key: 'accommodation', color: 'text-green-600', icon: '🏨' },
              { label: 'Activities', key: 'activities', color: 'text-purple-600', icon: '🎟️' },
              { label: 'Meals & Transport', key: 'daily_expenses', color: 'text-orange-600', icon: '🍽️' }
            ].map(({ label, key, color, icon }) => (
              <div key={key} className="text-center p-3 bg-white rounded-xl border border-orange-100 shadow-sm">
                <div className="text-xl mb-1">{icon}</div>
                <div className={`text-lg font-bold ${color}`}>₹{fmt(variant.cost_breakdown[key])}</div>
                <div className="text-xs text-gray-500">{label}</div>
              </div>
            ))}
          </div>
          <div className="p-3 bg-white rounded-xl border border-orange-200 text-center">
            <div className="text-2xl font-bold text-gray-900">
              Total: ₹{fmt(variant.cost_breakdown.total || variant.estimated_cost)}
            </div>
            <div className="text-sm text-gray-500 mt-1">
              {variant.within_budget ? '✅ Within your budget' : '⚠️ Exceeds budget'}
              {variant.savings > 0 && ` • Saves ₹${fmt(variant.savings)}`}
            </div>
          </div>
        </div>
      )}

      {/* ── flights ── */}
      <SectionToggle
        title="Flight Options"
        icon={<Plane className="h-5 w-5 text-blue-600" />}
        count={(variant.flights || []).length}
      >
        {(variant.flights || []).length > 0 ? (
          <div className="space-y-3">
            {variant.flights.map((flight, idx) => (
              <FlightCard key={idx} flight={flight} idx={idx} />
            ))}
          </div>
        ) : (
          <p className="text-gray-400 text-center py-6">No flights found for this route</p>
        )}
        <p className="text-xs text-gray-400 mt-3 text-center">
          Prices are indicative. Always verify on the airline/booking website before purchase.
        </p>
      </SectionToggle>

      {/* ── hotels ── */}
      <SectionToggle
        title="Hotel Options"
        icon={<Building className="h-5 w-5 text-green-600" />}
        count={(variant.hotels || []).length}
      >
        {(variant.hotels || []).length > 0 ? (
          <div className="space-y-3">
            {variant.hotels.map((hotel, idx) => (
              <HotelCard key={idx} hotel={hotel} nights={nights} />
            ))}
          </div>
        ) : (
          <p className="text-gray-400 text-center py-6">No hotels found for this destination</p>
        )}
        <p className="text-xs text-gray-400 mt-3 text-center">
          Hotel rates are estimates. Verify availability and pricing on Booking.com, Agoda or MakeMyTrip.
        </p>
      </SectionToggle>

      {/* ── itinerary ── */}
      <SectionToggle
        title="Daily Itinerary"
        icon={<Calendar className="h-5 w-5 text-purple-600" />}
        count={`${(variant.itinerary || []).length} days · ${(variant.itinerary || []).length * 5} places`}
      >
        {(variant.itinerary || []).length > 0 ? (
          <div className="space-y-4">
            {variant.itinerary.map((day, idx) => (
              <DayCard key={idx} day={day} idx={idx} />
            ))}
          </div>
        ) : (
          <p className="text-gray-400 text-center py-6">No itinerary generated</p>
        )}
      </SectionToggle>

      {/* ── features ── */}
      {variant.features && variant.features.length > 0 && (
        <div className="card mb-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
            <Info className="h-5 w-5 text-blue-500" />
            Plan Features
          </h3>
          <div className="flex flex-wrap gap-2">
            {variant.features.map((f, i) => (
              <span key={i} className="bg-blue-50 border border-blue-200 text-blue-800 text-sm px-3 py-1.5 rounded-full">
                ✓ {f}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* ── trip summary ── */}
      <div className="card mb-6 bg-gradient-to-r from-blue-50 to-cyan-50">
        <h3 className="text-xl font-semibold text-gray-900 mb-4 text-center">Trip Summary</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
          {[
            { val: (variant.flights || []).length, label: 'Flight Options', color: 'text-blue-600' },
            { val: (variant.hotels || []).length, label: 'Hotel Options', color: 'text-green-600' },
            { val: (variant.itinerary || []).length, label: 'Days Planned', color: 'text-purple-600' },
            { val: `₹${fmt(variant.estimated_cost)}`, label: 'Estimated Total', color: 'text-orange-600' }
          ].map(({ val, label, color }, i) => (
            <div key={i}>
              <div className={`text-2xl font-bold ${color}`}>{val}</div>
              <div className="text-sm text-gray-500">{label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* ── AI recommendations ── */}
      {results.recommendations && (
        <div className="card mb-6 bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200">
          <div className="flex items-center gap-3 mb-5">
            <div className="w-9 h-9 bg-green-100 rounded-full flex items-center justify-center text-xl">🤖</div>
            <h3 className="text-xl font-semibold text-gray-900">AI Travel Recommendations</h3>
          </div>

          {results.recommendations.summary && (
            <div className="mb-5 p-4 bg-white rounded-xl border border-green-100">
              <h4 className="font-semibold text-gray-900 mb-3">Trip Overview</h4>
              <div className="space-y-2 text-sm text-gray-700">
                {results.recommendations.summary.destination_overview && (
                  <p><strong>Destination:</strong> {results.recommendations.summary.destination_overview}</p>
                )}
                {results.recommendations.summary.budget_analysis && (
                  <p><strong>Budget:</strong> {results.recommendations.summary.budget_analysis}</p>
                )}
                {results.recommendations.summary.best_time_insight && (
                  <p><strong>Best Time:</strong> {results.recommendations.summary.best_time_insight}</p>
                )}
                {results.recommendations.summary.trip_highlights?.length > 0 && (
                  <div>
                    <strong>Top Highlights:</strong>
                    <div className="flex flex-wrap gap-1.5 mt-1">
                      {results.recommendations.summary.trip_highlights.map((h, i) => (
                        <Badge key={i} color="green">{h}</Badge>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {results.recommendations.variant_analysis && (
            <div className="mb-5 p-4 bg-white rounded-xl border border-green-100">
              <h4 className="font-semibold text-gray-900 mb-3">Plan Analysis</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                {results.recommendations.variant_analysis.best_value && (
                  <div className="p-3 bg-yellow-50 rounded-lg border border-yellow-200">
                    <div className="font-medium text-yellow-800 mb-1">🏆 Best Value</div>
                    <div className="text-yellow-700">{results.recommendations.variant_analysis.best_value.variant}</div>
                    <div className="text-xs text-yellow-600 mt-1">
                      {results.recommendations.variant_analysis.best_value.reason}
                    </div>
                  </div>
                )}
                {results.recommendations.variant_analysis.most_comprehensive && (
                  <div className="p-3 bg-purple-50 rounded-lg border border-purple-200">
                    <div className="font-medium text-purple-800 mb-1">📋 Most Comprehensive</div>
                    <div className="text-purple-700">
                      {results.recommendations.variant_analysis.most_comprehensive.variant}
                    </div>
                    <div className="text-xs text-purple-600 mt-1">
                      {results.recommendations.variant_analysis.most_comprehensive.reason}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[
              {
                key: 'personalized_tips', title: '💡 Personal Tips', color: 'green',
                data: results.recommendations.personalized_tips
              },
              {
                key: 'smart_savings', title: '💰 Smart Savings', color: 'yellow',
                data: results.recommendations.smart_savings
              },
              {
                key: 'safety_tips', title: '🛡️ Safety Tips', color: 'blue',
                data: results.recommendations.safety_tips
              }
            ].filter(s => s.data?.length > 0).map(section => (
              <div key={section.key} className="p-4 bg-white rounded-xl border border-green-100">
                <h5 className="font-semibold text-gray-900 mb-2">{section.title}</h5>
                <ul className="text-xs text-gray-600 space-y-1.5">
                  {section.data.slice(0, 5).map((tip, i) => (
                    <li key={i} className="flex items-start gap-1.5">
                      <span className="text-green-500 mt-0.5">•</span>
                      <span>{tip}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default TravelResults
