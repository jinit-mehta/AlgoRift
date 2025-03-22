"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { useUserStore } from "@/lib/user-store"
import { useGeolocation } from "@/hooks/use-geolocation"
import { MapPin, AlertCircle } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"

export function UserDashboard() {
  const { userStats } = useUserStore()
  const { city, isLoading, error } = useGeolocation()

  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>User Dashboard</CardTitle>
            <CardDescription>Personalized event recommendations for you</CardDescription>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="text-sm">
              {userStats.points} Points
            </Badge>
            <Badge variant="secondary" className="text-sm">
              Level {userStats.level}
            </Badge>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col md:flex-row gap-4 items-start md:items-center">
          <div className="w-full md:w-64">
            {isLoading ? (
              <div className="flex items-center gap-2 text-muted-foreground">
                <MapPin className="h-4 w-4" />
                <span>Detecting your location...</span>
              </div>
            ) : error ? (
              <Alert variant="destructive" className="py-2">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{error}. Using default location.</AlertDescription>
              </Alert>
            ) : (
              <div className="flex items-center gap-2">
                <MapPin className="h-4 w-4 text-primary" />
                <span className="font-medium">Current location: {city}</span>
              </div>
            )}
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 w-full">
            <div className="flex flex-col p-4 bg-muted rounded-lg">
              <span className="text-sm text-muted-foreground">Events Attended</span>
              <span className="text-2xl font-bold">{userStats.eventsAttended}</span>
            </div>
            <div className="flex flex-col p-4 bg-muted rounded-lg">
              <span className="text-sm text-muted-foreground">Friends</span>
              <span className="text-2xl font-bold">{userStats.friends}</span>
            </div>
            <div className="flex flex-col p-4 bg-muted rounded-lg">
              <span className="text-sm text-muted-foreground">Badges</span>
              <span className="text-2xl font-bold">{userStats.badges}</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

