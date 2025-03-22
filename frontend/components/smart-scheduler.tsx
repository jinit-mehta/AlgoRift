"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Calendar, Clock } from "lucide-react"
import { useOrganizerStore } from "@/lib/store"

export function SmartScheduler() {
  const { schedule } = useOrganizerStore()

  // Function to determine badge color based on confidence
  const getConfidenceColor = (confidence: string) => {
    switch (confidence.toLowerCase()) {
      case "high":
        return "bg-green-500"
      case "medium":
        return "bg-yellow-500"
      case "low":
        return "bg-red-500"
      default:
        return "bg-blue-500"
    }
  }

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>Smart Scheduler</CardTitle>
        <CardDescription>AI-recommended time slots for optimal attendance</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {schedule.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-40 text-muted-foreground">
              <p>No scheduling recommendations available.</p>
            </div>
          ) : (
            schedule.map((slot, index) => (
              <div key={index} className="flex items-start gap-3 p-3 border rounded-lg">
                <div className="flex flex-col items-center justify-center bg-muted rounded-md p-2 min-w-12 text-center">
                  <Calendar className="h-4 w-4 mb-1" />
                  <span className="text-xs font-medium">{slot.day}</span>
                </div>

                <div className="flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <div className="flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      <span className="text-sm font-medium">{slot.time}</span>
                    </div>
                    <Badge className={getConfidenceColor(slot.confidence)}>{slot.confidence}</Badge>
                  </div>

                  <p className="text-xs text-muted-foreground">{slot.reason}</p>
                </div>
              </div>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  )
}

