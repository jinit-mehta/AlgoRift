import type { User, Event, Friend, UserStats, RecommendationMetrics } from "@/lib/types"

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

// Mock recommendation metrics
const metrics: RecommendationMetrics = {
  precision: 0.85,
  recall: 0.78,
  f1Score: 0.81,
}

export const mockUserData = {
  users,
  recommendations,
  friends,
  userStats,
  metrics,
}

