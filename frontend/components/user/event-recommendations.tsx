"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { EventCard } from "@/components/user/event-card"
import { useUserStore } from "@/lib/user-store"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useGeolocation } from "@/hooks/use-geolocation"
import { Badge } from "@/components/ui/badge"
import { MapPin } from "lucide-react"

export function EventRecommendations() {
  const { recommendations, searchQuery } = useUserStore()
  const { city } = useGeolocation()

  // Filter recommendations based on search query and location
  const filteredRecommendations = recommendations.filter((event) => {
    // Search query filter
    const matchesSearch =
      searchQuery === "" ||
      event.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      event.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
      event.location.toLowerCase().includes(searchQuery.toLowerCase())

    // Location filter - if we have user's city, prioritize events in that city
    // but still show other events (we don't want to completely filter out non-local events)
    return matchesSearch
  })

  // Sort recommendations to prioritize local events if we have user's location
  const sortedRecommendations = [...filteredRecommendations].sort((a, b) => {
    if (city) {
      const aIsLocal = a.location.includes(city)
      const bIsLocal = b.location.includes(city)

      if (aIsLocal && !bIsLocal) return -1
      if (!aIsLocal && bIsLocal) return 1
    }
    return 0
  })

  // Group events by category
  const categories = [...new Set(recommendations.map((event) => event.category))]

  // Count local events
  const localEventsCount = city ? sortedRecommendations.filter((event) => event.location.includes(city)).length : 0

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Event Recommendations</span>
          {city && (
            <Badge variant="outline" className="flex items-center gap-1">
              <MapPin className="h-3 w-3" />
              {localEventsCount} events near {city}
            </Badge>
          )}
        </CardTitle>
        <CardDescription>
          Personalized event suggestions based on your preferences
          {searchQuery && <span className="ml-1 font-medium">filtered by &quot;{searchQuery}&quot;</span>}
        </CardDescription>
      </CardHeader>
      <CardContent>
        {sortedRecommendations.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-40 text-muted-foreground">
            <p>No events found matching your search criteria.</p>
          </div>
        ) : (
          <Tabs defaultValue="all">
            <TabsList className="mb-4">
              <TabsTrigger value="all">All</TabsTrigger>
              {categories.map((category) => (
                <TabsTrigger key={category} value={category}>
                  {category}
                </TabsTrigger>
              ))}
              {city && <TabsTrigger value="nearby">Nearby</TabsTrigger>}
            </TabsList>

            <TabsContent value="all" className="m-0">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {sortedRecommendations.map((event) => (
                  <EventCard key={event.id} event={event} isNearby={city ? event.location.includes(city) : false} />
                ))}
              </div>
            </TabsContent>

            {categories.map((category) => (
              <TabsContent key={category} value={category} className="m-0">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {sortedRecommendations
                    .filter((event) => event.category === category)
                    .map((event) => (
                      <EventCard key={event.id} event={event} isNearby={city ? event.location.includes(city) : false} />
                    ))}
                </div>
              </TabsContent>
            ))}

            {city && (
              <TabsContent value="nearby" className="m-0">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {sortedRecommendations
                    .filter((event) => event.location.includes(city))
                    .map((event) => (
                      <EventCard key={event.id} event={event} isNearby={true} />
                    ))}
                </div>
              </TabsContent>
            )}
          </Tabs>
        )}
      </CardContent>
    </Card>
  )
}

