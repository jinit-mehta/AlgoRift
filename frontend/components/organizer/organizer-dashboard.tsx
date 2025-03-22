"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useOrganizerStore } from "@/lib/organizer-store"
import { CalendarDays, Users, DollarSign, TrendingUp } from "lucide-react"

export function OrganizerDashboard() {
  const { organizerStats, cities, selectedCity, setSelectedCity } = useOrganizerStore()

  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>Organizer Dashboard</CardTitle>
            <CardDescription>Overview of event performance and analytics</CardDescription>
          </div>
          <div className="w-48">
            <Select value={selectedCity} onValueChange={setSelectedCity}>
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
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
          <div className="flex items-center p-4 border rounded-lg">
            <div className="rounded-full p-3 bg-blue-100 mr-4">
              <CalendarDays className="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Total Events</p>
              <p className="text-2xl font-bold">{organizerStats.totalEvents}</p>
              <p className="text-xs text-green-600">
                <TrendingUp className="inline h-3 w-3 mr-1" />+{organizerStats.eventGrowth}% from last month
              </p>
            </div>
          </div>

          <div className="flex items-center p-4 border rounded-lg">
            <div className="rounded-full p-3 bg-green-100 mr-4">
              <Users className="h-6 w-6 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Total Attendees</p>
              <p className="text-2xl font-bold">{organizerStats.totalAttendees}</p>
              <p className="text-xs text-green-600">
                <TrendingUp className="inline h-3 w-3 mr-1" />+{organizerStats.attendeeGrowth}% from last month
              </p>
            </div>
          </div>

          <div className="flex items-center p-4 border rounded-lg">
            <div className="rounded-full p-3 bg-purple-100 mr-4">
              <DollarSign className="h-6 w-6 text-purple-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Total Revenue</p>
              <p className="text-2xl font-bold">${organizerStats.totalRevenue.toLocaleString()}</p>
              <p className="text-xs text-green-600">
                <TrendingUp className="inline h-3 w-3 mr-1" />+{organizerStats.revenueGrowth}% from last month
              </p>
            </div>
          </div>

          <div className="flex items-center p-4 border rounded-lg">
            <div className="rounded-full p-3 bg-yellow-100 mr-4">
              <DollarSign className="h-6 w-6 text-yellow-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Avg. Ticket Price</p>
              <p className="text-2xl font-bold">${organizerStats.avgTicketPrice}</p>
              <p className="text-xs text-muted-foreground">Across all events</p>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

