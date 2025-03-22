"use client"

import { useState, useEffect } from "react"

interface GeolocationState {
  latitude: number | null
  longitude: number | null
  city: string | null
  isLoading: boolean
  error: string | null
}

export function useGeolocation() {
  const [state, setState] = useState<GeolocationState>({
    latitude: null,
    longitude: null,
    city: null,
    isLoading: true,
    error: null,
  })

  useEffect(() => {
    if (!navigator.geolocation) {
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: "Geolocation is not supported by your browser",
      }))
      return
    }

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        try {
          const { latitude, longitude } = position.coords

          // Reverse geocoding to get city name
          const response = await fetch(
            `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&zoom=10`,
          )

          if (!response.ok) {
            throw new Error("Failed to fetch location data")
          }

          const data = await response.json()
          const city =
            data.address?.city || data.address?.town || data.address?.village || data.address?.county || "Unknown"

          setState({
            latitude,
            longitude,
            city,
            isLoading: false,
            error: null,
          })
        } catch (error) {
          setState((prev) => ({
            ...prev,
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            isLoading: false,
            error: "Failed to get city name",
          }))
        }
      },
      (error) => {
        setState((prev) => ({
          ...prev,
          isLoading: false,
          error: error.message,
        }))
      },
    )
  }, [])

  return state
}

