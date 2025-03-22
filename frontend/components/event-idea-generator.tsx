"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Sparkles, ThumbsUp, ThumbsDown } from "lucide-react"
import { useState } from "react"
import { useOrganizerStore } from "@/lib/store"

export function EventIdeaGenerator() {
  const { eventIdeas, users } = useOrganizerStore()
  const [city, setCity] = useState<string>("")
  const [category, setCategory] = useState<string>("")

  // Get unique cities and categories from users and event ideas
  const cities = [...new Set(users.map((user) => user.location))]
  const categories = [...new Set(eventIdeas.map((idea) => idea.category))]

  // Filter event ideas based on selected filters
  const filteredIdeas = eventIdeas.filter(
    (idea) =>
      (city === "all" || city === "" || idea.location === city) &&
      (category === "all" || category === "" || idea.category === category),
  )

  return (
    <Card className="h-full">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>Event Idea Generator</CardTitle>
            <CardDescription>AI-generated event ideas based on trends and user preferences</CardDescription>
          </div>
          <Sparkles className="h-5 w-5 text-yellow-500" />
        </div>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col gap-4">
          <div className="flex flex-col sm:flex-row gap-2">
            <Select value={city} onValueChange={setCity}>
              <SelectTrigger>
                <SelectValue placeholder="Filter by city" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Cities</SelectItem>
                {cities.map((city) => (
                  <SelectItem key={city} value={city}>
                    {city}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={category} onValueChange={setCategory}>
              <SelectTrigger>
                <SelectValue placeholder="Filter by category" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Categories</SelectItem>
                {categories.map((cat) => (
                  <SelectItem key={cat} value={cat}>
                    {cat}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-4">
            {filteredIdeas.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-40 text-muted-foreground">
                <p>No event ideas match your filters.</p>
                <Button
                  variant="link"
                  onClick={() => {
                    setCity("")
                    setCategory("")
                  }}
                >
                  Clear filters
                </Button>
              </div>
            ) : (
              filteredIdeas.map((idea, index) => (
                <div key={index} className="p-4 border rounded-lg">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-medium">{idea.name}</h3>
                    <Badge>{idea.category}</Badge>
                  </div>
                  <p className="text-sm text-muted-foreground mb-2">{idea.description}</p>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">
                      {idea.location} • {idea.estimatedAttendance} attendees
                    </span>
                    <div className="flex gap-2">
                      <Button variant="ghost" size="icon" className="h-8 w-8">
                        <ThumbsUp className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="icon" className="h-8 w-8">
                        <ThumbsDown className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

