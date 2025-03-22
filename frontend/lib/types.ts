export interface User {
  id: string
  name: string
  location: string
  avatar?: string
}

export interface Friend {
  name: string
  avatar?: string
  mutualEvents: number
  attendingEvent: string
}

export interface Event {
  id: string
  name: string
  date: string
  time: string
  location: string
  category: string
  image?: string
  pricing: {
    type: string
    price: number
  }
  friendsAttending: {
    name: string
    avatar?: string
  }[]
}

export interface EventIdea {
  name: string
  description: string
  category: string
  location: string
  estimatedAttendance: number
}

export interface TimeSlot {
  day: string
  time: string
  confidence: string
  reason: string
}

export interface PricingStrategy {
  type: string
  price: number
  trend: "up" | "down"
  trendPercentage: number
  description: string
}

export interface Insight {
  eventName: string
  city: string
  revenue: number
  tickets: number
  rating: number
  strategy: string
}

export interface UserStats {
  points: number
  level: number
  eventsAttended: number
  friends: number
  badges: number
  earnedBadges: {
    name: string
    type: "explorer" | "organizer" | "social"
  }[]
  nextRewards: {
    name: string
    pointsNeeded: number
  }[]
}

export interface RecommendationMetrics {
  precision: number
  recall: number
  f1Score: number
}

export interface Analytics {
  seasonalTrends: {
    month: string
    music: number
    sports: number
    tech: number
  }[]
  salesVelocity: {
    day: string
    tickets: number
  }[]
  sentimentAnalysis: {
    event: string
    positive: number
    neutral: number
    negative: number
  }[]
  anomalyDetection: {
    date: string
    expected: number
    actual: number
    anomaly: number | null
  }[]
}

export interface OrganizerStats {
  totalEvents: number
  totalAttendees: number
  totalRevenue: number
  avgTicketPrice: number
  eventGrowth: number
  attendeeGrowth: number
  revenueGrowth: number
}

