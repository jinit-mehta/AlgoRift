"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { useOrganizerStore } from "@/lib/store"

export function UserDashboard() {
  const { users, selectedUser, setSelectedUser, userStats } = useOrganizerStore()

  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>User Dashboard</CardTitle>
            <CardDescription>Select a user to view their personalized data</CardDescription>
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
            <Select value={selectedUser} onValueChange={setSelectedUser}>
              <SelectTrigger>
                <SelectValue placeholder="Select a user" />
              </SelectTrigger>
              <SelectContent>
                {users.map((user) => (
                  <SelectItem key={user.id} value={user.id}>
                    {user.id} ({user.location})
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
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

