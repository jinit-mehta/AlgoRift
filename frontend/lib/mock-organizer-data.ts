import type { EventIdea, TimeSlot, PricingStrategy, Insight, Analytics, OrganizerStats } from "@/lib/types"

// Mock cities
const cities: string[] = ["New York", "Chicago", "Los Angeles", "San Francisco", "Miami"]

// Mock event ideas
const eventIdeas: EventIdea[] = [
  {
    name: "Rooftop Yoga Sunrise",
    description: "Early morning yoga session on a rooftop with breakfast included.",
    category: "Wellness",
    location: "New York",
    estimatedAttendance: 50,
  },
  {
    name: "Virtual Reality Gaming Tournament",
    description: "Competitive VR gaming with prizes and live streaming.",
    category: "Tech",
    location: "Chicago",
    estimatedAttendance: 200,
  },
  {
    name: "Sustainable Fashion Show",
    description: "Showcase of eco-friendly fashion designs from local creators.",
    category: "Fashion",
    location: "New York",
    estimatedAttendance: 150,
  },
  {
    name: "Indie Film Night",
    description: "Screening of independent short films with director Q&A sessions.",
    category: "Entertainment",
    location: "Los Angeles",
    estimatedAttendance: 100,
  },
  {
    name: "AI and Future of Work Conference",
    description: "Industry leaders discuss how AI is transforming careers and businesses.",
    category: "Tech",
    location: "San Francisco",
    estimatedAttendance: 300,
  },
  {
    name: "Urban Gardening Workshop",
    description: "Hands-on workshop teaching apartment dwellers how to grow food at home.",
    category: "Education",
    location: "Chicago",
    estimatedAttendance: 75,
  },
  {
    name: "Beachfront Silent Disco",
    description: "Dance party where attendees wear wireless headphones on the beach.",
    category: "Music",
    location: "Miami",
    estimatedAttendance: 250,
  },
]

// Mock schedule
const schedule: TimeSlot[] = [
  {
    day: "SAT",
    time: "7:00 PM",
    confidence: "High",
    reason: "Historical data shows high attendance for weekend evening events",
  },
  {
    day: "SUN",
    time: "2:00 PM",
    confidence: "Medium",
    reason: "Good for family-friendly events, moderate competition",
  },
  {
    day: "THU",
    time: "6:30 PM",
    confidence: "High",
    reason: "Low competition from other events, after work hours",
  },
  {
    day: "TUE",
    time: "7:30 PM",
    confidence: "Low",
    reason: "Historically lower attendance on weekday evenings",
  },
  {
    day: "FRI",
    time: "8:00 PM",
    confidence: "High",
    reason: "End of work week, people looking for entertainment",
  },
]

// Mock pricing strategies
const pricingStrategy: PricingStrategy[] = [
  {
    type: "Early Bird",
    price: 45,
    trend: "up",
    trendPercentage: 12,
    description: "Offer limited tickets at reduced price 30 days before event",
  },
  {
    type: "Premium Package",
    price: 120,
    trend: "up",
    trendPercentage: 8,
    description: "VIP access with exclusive perks and priority seating",
  },
  {
    type: "Last Minute",
    price: 65,
    trend: "down",
    trendPercentage: 5,
    description: "Slightly discounted tickets 48 hours before event",
  },
  {
    type: "Group Discount",
    price: 40,
    trend: "up",
    trendPercentage: 15,
    description: "Special pricing for groups of 5+ people",
  },
]

// Mock insights
const insights: Insight[] = [
  {
    eventName: "Summer Music Festival",
    city: "New York",
    revenue: 45000,
    tickets: 1000,
    rating: 4.8,
    strategy: "Early Bird",
  },
  {
    eventName: "Tech Conference",
    city: "Chicago",
    revenue: 36000,
    tickets: 300,
    rating: 4.5,
    strategy: "Premium",
  },
  {
    eventName: "Food Festival",
    city: "New York",
    revenue: 28500,
    tickets: 570,
    rating: 4.7,
    strategy: "Standard",
  },
  {
    eventName: "Art Exhibition",
    city: "Los Angeles",
    revenue: 18200,
    tickets: 520,
    rating: 4.3,
    strategy: "Discount",
  },
  {
    eventName: "Comedy Night",
    city: "New York",
    revenue: 12600,
    tickets: 420,
    rating: 4.6,
    strategy: "Early Bird",
  },
  {
    eventName: "Wellness Retreat",
    city: "Miami",
    revenue: 32400,
    tickets: 180,
    rating: 4.9,
    strategy: "Premium",
  },
  {
    eventName: "Startup Pitch Night",
    city: "San Francisco",
    revenue: 15800,
    tickets: 320,
    rating: 4.4,
    strategy: "Standard",
  },
]

// Mock analytics
const analytics: Analytics = {
  seasonalTrends: [
    { month: "Jan", music: 45, sports: 30, tech: 60 },
    { month: "Feb", music: 50, sports: 25, tech: 70 },
    { month: "Mar", music: 60, sports: 35, tech: 65 },
    { month: "Apr", music: 70, sports: 40, tech: 60 },
    { month: "May", music: 80, sports: 55, tech: 55 },
    { month: "Jun", music: 95, sports: 65, tech: 50 },
    { month: "Jul", music: 100, sports: 70, tech: 45 },
    { month: "Aug", music: 90, sports: 65, tech: 50 },
    { month: "Sep", music: 75, sports: 55, tech: 60 },
    { month: "Oct", music: 65, sports: 45, tech: 70 },
    { month: "Nov", music: 55, sports: 35, tech: 80 },
    { month: "Dec", music: 50, sports: 30, tech: 75 },
  ],
  salesVelocity: [
    { day: "30 days", tickets: 10 },
    { day: "25 days", tickets: 15 },
    { day: "20 days", tickets: 25 },
    { day: "15 days", tickets: 40 },
    { day: "10 days", tickets: 65 },
    { day: "5 days", tickets: 90 },
    { day: "1 day", tickets: 120 },
  ],
  sentimentAnalysis: [
    { event: "Music Fest", positive: 75, neutral: 20, negative: 5 },
    { event: "Tech Conf", positive: 65, neutral: 25, negative: 10 },
    { event: "Food Fest", positive: 80, neutral: 15, negative: 5 },
    { event: "Art Show", positive: 60, neutral: 30, negative: 10 },
    { event: "Comedy", positive: 85, neutral: 10, negative: 5 },
  ],
  anomalyDetection: [
    { date: "Jan 5", expected: 120, actual: 118, anomaly: null },
    { date: "Jan 12", expected: 150, actual: 145, anomaly: null },
    { date: "Jan 19", expected: 130, actual: 132, anomaly: null },
    { date: "Jan 26", expected: 140, actual: 85, anomaly: 85 },
    { date: "Feb 2", expected: 160, actual: 158, anomaly: null },
    { date: "Feb 9", expected: 170, actual: 172, anomaly: null },
    { date: "Feb 16", expected: 150, actual: 210, anomaly: 210 },
    { date: "Feb 23", expected: 180, actual: 182, anomaly: null },
    { date: "Mar 2", expected: 200, actual: 198, anomaly: null },
    { date: "Mar 9", expected: 190, actual: 192, anomaly: null },
  ],
}

// Mock organizer stats
const organizerStats: OrganizerStats = {
  totalEvents: 42,
  totalAttendees: 8750,
  totalRevenue: 328500,
  avgTicketPrice: 37.5,
  eventGrowth: 15,
  attendeeGrowth: 22,
  revenueGrowth: 18,
}

export const mockOrganizerData = {
  cities,
  eventIdeas,
  schedule,
  pricingStrategy,
  insights,
  analytics,
  organizerStats,
}

