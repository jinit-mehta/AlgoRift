"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { useOrganizerStore } from "@/lib/store"

export function OrganizerInsights() {
  const { insights } = useOrganizerStore()

  // Function to determine badge color based on strategy
  const getStrategyColor = (strategy: string) => {
    switch (strategy.toLowerCase()) {
      case "early bird":
        return "bg-green-500"
      case "premium":
        return "bg-purple-500"
      case "discount":
        return "bg-blue-500"
      case "standard":
        return "bg-gray-500"
      default:
        return "bg-blue-500"
    }
  }

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>Top Insights</CardTitle>
        <CardDescription>Key metrics for top-performing events</CardDescription>
      </CardHeader>
      <CardContent>
        {insights.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-40 text-muted-foreground">
            <p>No insights available.</p>
          </div>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Event</TableHead>
                <TableHead className="text-right">Revenue</TableHead>
                <TableHead className="text-right">Strategy</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {insights.map((insight, index) => (
                <TableRow key={index}>
                  <TableCell className="font-medium">
                    <div>
                      <span className="block truncate">{insight.eventName}</span>
                      <span className="text-xs text-muted-foreground">{insight.city}</span>
                    </div>
                  </TableCell>
                  <TableCell className="text-right">
                    <div>
                      <span className="block font-medium">${insight.revenue}</span>
                      <span className="text-xs text-muted-foreground">{insight.tickets} tickets</span>
                    </div>
                  </TableCell>
                  <TableCell className="text-right">
                    <Badge className={getStrategyColor(insight.strategy)}>{insight.strategy}</Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </CardContent>
    </Card>
  )
}

