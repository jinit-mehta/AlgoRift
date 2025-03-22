"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { EventCard } from "@/components/event-card"
import { useOrganizerStore } from "@/lib/store"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export function EventRecommendations() {
  const { recommendations, searchQuery } = useOrganizerStore()

  // Filter recommendations based on search query
  const filteredRecommendations = recommendations.filter(
    (event) =>
      searchQuery === "" ||
      event.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      event.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
      event.location.toLowerCase().includes(searchQuery.toLowerCase()),
  )

  // Group events by category
  const categories = [...new Set(recommendations.map((event) => event.category))]

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>Event Recommendations</CardTitle>
        <CardDescription>
          Personalized event suggestions based on user preferences
          {searchQuery && <span className="ml-1 font-medium">filtered by &quot;{searchQuery}&quot;</span>}
        </CardDescription>
      </CardHeader>
      <CardContent>
        {filteredRecommendations.length === 0 ? (
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
            </TabsList>

            <TabsContent value="all" className="m-0">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {filteredRecommendations.map((event) => (
                  <EventCard key={event.id} event={event} />
                ))}
              </div>
            </TabsContent>

            {categories.map((category) => (
              <TabsContent key={category} value={category} className="m-0">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {filteredRecommendations
                    .filter((event) => event.category === category)
                    .map((event) => (
                      <EventCard key={event.id} event={event} />
                    ))}
                </div>
              </TabsContent>
            ))}
          </Tabs>
        )}
      </CardContent>
    </Card>
  )
}

