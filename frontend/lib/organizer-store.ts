"use client"

import { create } from "zustand"
import type { EventIdea, TimeSlot, PricingStrategy, Insight, Analytics, OrganizerStats } from "@/lib/types"
import { mockOrganizerData } from "@/lib/mock-organizer-data"

interface OrganizerStore {
  // Data
  cities: string[]
  selectedCity: string
  eventIdeas: EventIdea[]
  schedule: TimeSlot[]
  pricingStrategy: PricingStrategy[]
  insights: Insight[]
  analytics: Analytics
  organizerStats: OrganizerStats
  isLoading: boolean

  // Actions
  setSelectedCity: (city: string) => void
  refreshData: () => void
}

export const useOrganizerStore = create<OrganizerStore>((set, get) => ({
  // Initial state with mock data
  ...mockOrganizerData,
  selectedCity: "all",
  isLoading: false,

  // Actions
  setSelectedCity: (city: string) => {
    set({ selectedCity: city, isLoading: true })

    // Simulate API call delay
    setTimeout(() => {
      // Filter insights based on selected city
      const filteredInsights =
        city === "all"
          ? mockOrganizerData.insights
          : mockOrganizerData.insights.filter((insight) => insight.city === city)

      // Update state with "filtered" data
      set({
        insights: filteredInsights,
        isLoading: false,
      })
    }, 500)
  },

  refreshData: () => {
    set({ isLoading: true })

    // Simulate API call delay
    setTimeout(() => {
      set({
        ...mockOrganizerData,
        selectedCity: get().selectedCity,
        isLoading: false,
      })
    }, 1000)
  },
}))

