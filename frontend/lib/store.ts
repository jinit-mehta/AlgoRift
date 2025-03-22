"use client"

import { create } from "zustand"
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
import { mockData } from "@/lib/mock-data"

interface OrganizerStore {
  // Data
  users: User[]
  selectedUser: string
  recommendations: Event[]
  friends: Friend[]
  eventIdeas: EventIdea[]
  schedule: TimeSlot[]
  pricingStrategy: PricingStrategy[]
  insights: Insight[]
  userStats: UserStats
  analytics: Analytics
  searchQuery: string
  isLoading: boolean

  // Actions
  setSelectedUser: (userId: string) => void
  setSearchQuery: (query: string) => void
  refreshData: () => void
}

export const useOrganizerStore = create<OrganizerStore>((set, get) => ({
  // Initial state with mock data
  ...mockData,
  selectedUser: mockData.users[0]?.id || "",
  searchQuery: "",
  isLoading: false,

  // Actions
  setSelectedUser: (userId: string) => {
    set({ selectedUser: userId, isLoading: true })

    // Simulate API call delay
    setTimeout(() => {
      // Filter recommendations based on selected user
      const filteredRecommendations = mockData.recommendations.filter(
        (_, index) => index % 2 === (userId === "U0324" ? 0 : 1),
      )

      // Update state with "filtered" data
      set({
        recommendations: filteredRecommendations,
        isLoading: false,
      })
    }, 500)
  },

  setSearchQuery: (query: string) => {
    set({ searchQuery: query })
  },

  refreshData: () => {
    set({ isLoading: true })

    // Simulate API call delay
    setTimeout(() => {
      set({
        ...mockData,
        selectedUser: get().selectedUser,
        isLoading: false,
      })
    }, 1000)
  },
}))

