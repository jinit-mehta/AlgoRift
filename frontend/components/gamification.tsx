"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Award, Trophy, Star } from "lucide-react"
import { useOrganizerStore } from "@/lib/store"

export function Gamification() {
  const { userStats } = useOrganizerStore()

  // Calculate progress to next level
  const progressToNextLevel = Math.min(Math.round(((userStats.points % 100) / 100) * 100), 100)

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>Gamification</CardTitle>
        <CardDescription>Badges, points, and rewards</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-medium">Level Progress</h3>
              <span className="text-xs text-muted-foreground">
                {userStats.points} / {(userStats.level + 1) * 100} points
              </span>
            </div>
            <Progress value={progressToNextLevel} className="h-2" />
            <p className="text-xs text-muted-foreground">
              {100 - (userStats.points % 100)} points until Level {userStats.level + 1}
            </p>
          </div>

          <div>
            <h3 className="text-sm font-medium mb-3">Earned Badges</h3>
            <div className="grid grid-cols-2 gap-2">
              {userStats.earnedBadges.map((badge, index) => (
                <div key={index} className="flex items-center gap-2 p-2 border rounded-lg">
                  {badge.type === "explorer" ? (
                    <Award className="h-4 w-4 text-blue-500" />
                  ) : badge.type === "organizer" ? (
                    <Trophy className="h-4 w-4 text-yellow-500" />
                  ) : (
                    <Star className="h-4 w-4 text-purple-500" />
                  )}
                  <span className="text-xs">{badge.name}</span>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h3 className="text-sm font-medium mb-2">Next Rewards</h3>
            <div className="space-y-2">
              {userStats.nextRewards.map((reward, index) => (
                <div key={index} className="flex items-center justify-between p-2 border rounded-lg">
                  <span className="text-xs">{reward.name}</span>
                  <Badge variant="outline" className="text-xs">
                    {reward.pointsNeeded} points
                  </Badge>
                </div>
              ))}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

