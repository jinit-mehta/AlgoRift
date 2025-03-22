import type {
  User,
  Event,
  Friend,
  EventIdea,
  TimeSlot,
  PricingStrategy,
  Insight,
  UserStats,
  Analytics,
} from "@/lib/types"

// Mock users
const users: User[] = [
  { id: "U0324", name: "Alex Johnson", location: "New York" },
  { id: "U0456", name: "Sam Wilson", location: "Chicago" },
  { id: "U0789", name: "Taylor Reed", location: "Los Angeles" },
]

// Mock events
const recommendations: Event[] = [
  {
    id: "E0123",
    name: "Summer Music Festival",
    date: "July 15, 2023",
    time: "4:00 PM - 11:00 PM",
    location: "Central Park, New York",
    category: "Music",
    pricing: {
      type: "Early Bird",
      price: 45,
    },
    friendsAttending: [
      { name: "John Smith" },
      { name: "Emma Davis" },
      { name: "Michael Brown" },
      { name: "Sophia Wilson" },
    ],
  },
  {
    id: "E0124",
    name: "Tech Conference 2023",
    date: "August 5, 2023",
    time: "9:00 AM - 5:00 PM",
    location: "Convention Center, New York",
    category: "Tech",
    pricing: {
      type: "Standard",
      price: 120,
    },
    friendsAttending: [{ name: "David Lee" }, { name: "Sarah Johnson" }],
  },
  {
    id: "E0125",
    name: "Basketball Tournament",
    date: "July 22, 2023",
    time: "1:00 PM - 6:00 PM",
    location: "Sports Arena, Brooklyn",
    category: "Sports",
    pricing: {
      type: "Group Discount",
      price: 25,
    },
    friendsAttending: [{ name: "James Wilson" }, { name: "Robert Taylor" }, { name: "Jennifer Moore" }],
  },
  {
    id: "E0126",
    name: "Food & Wine Festival",
    date: "September 10, 2023",
    time: "12:00 PM - 8:00 PM",
    location: "Riverside Park, New York",
    category: "Food",
    pricing: {
      type: "Premium",
      price: 75,
    },
    friendsAttending: [{ name: "Emily Clark" }],
  },
  {
    id: "E0127",
    name: "Art Exhibition Opening",
    date: "July 30, 2023",
    time: "6:00 PM - 9:00 PM",
    location: "Modern Art Gallery, Manhattan",
    category: "Art",
    pricing: {
      type: "Early Access",
      price: 35,
    },
    friendsAttending: [{ name: "Olivia Martin" }, { name: "William Johnson" }],
  },
  {
    id: "E0128",
    name: "Comedy Night",
    date: "August 12, 2023",
    time: "8:00 PM - 10:30 PM",
    location: "Laugh Factory, New York",
    category: "Entertainment",
    pricing: {
      type: "Last Minute",
      price: 30,
    },
    friendsAttending: [{ name: "Daniel Brown" }, { name: "Sophia Wilson" }, { name: "Emma Davis" }],
  },
]

// Mock friends
const friends: Friend[] = [
  {
    name: "John Smith",
    mutualEvents: 3,
    attendingEvent: "Summer Music Festival",
  },
  {
    name: "Emma Davis",
    mutualEvents: 5,
    attendingEvent: "Summer Music Festival",
  },
  {
    name: "David Lee",
    mutualEvents: 2,
    attendingEvent: "Tech Conference 2023",
  },
  {
    name: "Sarah Johnson",
    mutualEvents: 4,
    attendingEvent: "Tech Conference 2023",
  },
  {
    name: "Michael Brown",
    mutualEvents: 1,
    attendingEvent: "Summer Music Festival",
  },
]

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
]

// Mock user stats
const userStats: UserStats = {
  points: 450,
  level: 4,
  eventsAttended: 12,
  friends: 28,
  badges: 5,
  earnedBadges: [
    { name: "Event Explorer", type: "explorer" },
    { name: "Social Butterfly", type: "social" },
    { name: "First Event", type: "explorer" },
    { name: "Trendsetter", type: "social" },
    { name: "Event Host", type: "organizer" },
  ],
  nextRewards: [
    { name: "Free Premium Ticket", pointsNeeded: 500 },
    { name: "Early Access Pass", pointsNeeded: 600 },
    { name: "VIP Status", pointsNeeded: 1000 },
  ],
}

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
}

export const mockData = {
  users,
  recommendations,
  friends,
  eventIdeas,
  schedule,
  pricingStrategy,
  insights,
  userStats,
  analytics,
}

