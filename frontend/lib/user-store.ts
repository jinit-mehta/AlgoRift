"use client"

import { create } from "zustand"
import type { User, Event, Friend, UserStats, RecommendationMetrics } from "@/lib/types"
import { mockUserData } from "@/lib/mock-user-data"

interface UserStore {
  // Data
  user: User
  recommendations: Event[]
  friends: Friend[]
  userStats: UserStats
  metrics: RecommendationMetrics
  searchQuery: string
  isLoading: boolean

  // Actions
  setSearchQuery: (query: string) => void
  refreshData: () => void
  updateUserLocation: (location: string) => void
}

export const useUserStore = create<UserStore>((set, get) => ({
  // Initial state with mock data - using a single static user
  user: mockUserData.users[0],
  recommendations: mockUserData.recommendations,
  friends: mockUserData.friends,
  userStats: mockUserData.userStats,
  metrics: mockUserData.metrics,
  searchQuery: "",
  isLoading: false,

  // Actions
  setSearchQuery: (query: string) => {
    set({ searchQuery: query })
  },

  refreshData: () => {
    set({ isLoading: true })

    // Simulate API call delay
    setTimeout(() => {
      set({
        recommendations: mockUserData.recommendations,
        friends: mockUserData.friends,
        userStats: mockUserData.userStats,
        metrics: mockUserData.metrics,
        isLoading: false,
      })
    }, 1000)
  },

  updateUserLocation: (location: string) => {
    set((state) => ({
      user: {
        ...state.user,
        location,
      },
    }))
  },
}))

