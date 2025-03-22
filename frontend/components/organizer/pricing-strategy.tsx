"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { DollarSign, TrendingUp, TrendingDown } from "lucide-react"
import { useOrganizerStore } from "@/lib/organizer-store"

export function PricingStrategy() {
  const { pricingStrategy } = useOrganizerStore()

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>Pricing Strategy</CardTitle>
        <CardDescription>AI-optimized pricing recommendations</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {pricingStrategy.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-40 text-muted-foreground">
              <p>No pricing strategies available.</p>
            </div>
          ) : (
            pricingStrategy.map((strategy, index) => (
              <div key={index} className="p-3 border rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-medium text-sm">{strategy.type}</h3>
                  <Badge variant={strategy.trend === "up" ? "default" : "destructive"} className="text-xs">
                    {strategy.trend === "up" ? (
                      <TrendingUp className="h-3 w-3 mr-1" />
                    ) : (
                      <TrendingDown className="h-3 w-3 mr-1" />
                    )}
                    {strategy.trendPercentage}%
                  </Badge>
                </div>

                <div className="flex items-center gap-1 mb-1">
                  <DollarSign className="h-4 w-4" />
                  <span className="text-lg font-bold">${strategy.price}</span>
                </div>

                <p className="text-xs text-muted-foreground">{strategy.description}</p>
              </div>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  )
}

