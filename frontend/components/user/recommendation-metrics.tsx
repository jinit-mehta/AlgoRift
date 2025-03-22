"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { useUserStore } from "@/lib/user-store"

export function RecommendationMetrics() {
  const { metrics } = useUserStore()

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>Recommendation Metrics</CardTitle>
        <CardDescription>Performance of our recommendation system</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-medium">Precision</h3>
              <span className="text-xs font-medium">{metrics.precision.toFixed(2)}</span>
            </div>
            <Progress value={metrics.precision * 100} className="h-2" />
            <p className="text-xs text-muted-foreground">Ratio of relevant recommendations to total recommendations</p>
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-medium">Recall</h3>
              <span className="text-xs font-medium">{metrics.recall.toFixed(2)}</span>
            </div>
            <Progress value={metrics.recall * 100} className="h-2" />
            <p className="text-xs text-muted-foreground">Ratio of relevant recommendations to all relevant events</p>
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-medium">F1 Score</h3>
              <span className="text-xs font-medium">{metrics.f1Score.toFixed(2)}</span>
            </div>
            <Progress value={metrics.f1Score * 100} className="h-2" />
            <p className="text-xs text-muted-foreground">Harmonic mean of precision and recall</p>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

