"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useOrganizerStore } from "@/lib/organizer-store"
import {
  Chart,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  ChartLegend,
  ChartLegendItem,
} from "@/components/ui/chart"
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  XAxis,
  YAxis,
} from "recharts"

export function AnalyticsCharts() {
  const { analytics } = useOrganizerStore()

  return (
    <Card>
      <CardHeader>
        <CardTitle>Analytics</CardTitle>
        <CardDescription>Event performance and trends</CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="seasonal">
          <TabsList className="mb-4">
            <TabsTrigger value="seasonal">Seasonal Trends</TabsTrigger>
            <TabsTrigger value="sales">Sales Velocity</TabsTrigger>
            <TabsTrigger value="sentiment">Sentiment Analysis</TabsTrigger>
            <TabsTrigger value="anomalies">Anomaly Detection</TabsTrigger>
          </TabsList>

          <TabsContent value="seasonal" className="m-0">
            <div className="h-80">
              <ChartContainer>
                <Chart>
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={analytics.seasonalTrends}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="month" />
                      <YAxis />
                      <ChartTooltip content={<ChartTooltipContent />} />
                      <Line type="monotone" dataKey="music" stroke="#1976d2" strokeWidth={2} activeDot={{ r: 8 }} />
                      <Line type="monotone" dataKey="sports" stroke="#dc004e" strokeWidth={2} />
                      <Line type="monotone" dataKey="tech" stroke="#4caf50" strokeWidth={2} />
                    </LineChart>
                  </ResponsiveContainer>
                </Chart>
                <ChartLegend>
                  <ChartLegendItem name="Music Events" color="#1976d2" />
                  <ChartLegendItem name="Sports Events" color="#dc004e" />
                  <ChartLegendItem name="Tech Events" color="#4caf50" />
                </ChartLegend>
              </ChartContainer>
            </div>
          </TabsContent>

          <TabsContent value="sales" className="m-0">
            <div className="h-80">
              <ChartContainer>
                <Chart>
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={analytics.salesVelocity}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="day" />
                      <YAxis />
                      <ChartTooltip content={<ChartTooltipContent />} />
                      <Bar dataKey="tickets" fill="#1976d2" />
                    </BarChart>
                  </ResponsiveContainer>
                </Chart>
              </ChartContainer>
            </div>
          </TabsContent>

          <TabsContent value="sentiment" className="m-0">
            <div className="h-80">
              <ChartContainer>
                <Chart>
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={analytics.sentimentAnalysis}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="event" />
                      <YAxis />
                      <ChartTooltip content={<ChartTooltipContent />} />
                      <Area type="monotone" dataKey="positive" stackId="1" stroke="#4caf50" fill="#4caf50" />
                      <Area type="monotone" dataKey="neutral" stackId="1" stroke="#ff9800" fill="#ff9800" />
                      <Area type="monotone" dataKey="negative" stackId="1" stroke="#f44336" fill="#f44336" />
                    </AreaChart>
                  </ResponsiveContainer>
                </Chart>
                <ChartLegend>
                  <ChartLegendItem name="Positive" color="#4caf50" />
                  <ChartLegendItem name="Neutral" color="#ff9800" />
                  <ChartLegendItem name="Negative" color="#f44336" />
                </ChartLegend>
              </ChartContainer>
            </div>
          </TabsContent>

          <TabsContent value="anomalies" className="m-0">
            <div className="h-80">
              <ChartContainer>
                <Chart>
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={analytics.anomalyDetection}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis />
                      <ChartTooltip content={<ChartTooltipContent />} />
                      <Line type="monotone" dataKey="expected" stroke="#1976d2" strokeWidth={2} dot={false} />
                      <Line type="monotone" dataKey="actual" stroke="#dc004e" strokeWidth={2} activeDot={{ r: 8 }} />
                      <Line
                        type="monotone"
                        dataKey="anomaly"
                        stroke="#f44336"
                        strokeWidth={0}
                        dot={{ r: 6, fill: "#f44336" }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </Chart>
                <ChartLegend>
                  <ChartLegendItem name="Expected Attendance" color="#1976d2" />
                  <ChartLegendItem name="Actual Attendance" color="#dc004e" />
                  <ChartLegendItem name="Anomaly Detected" color="#f44336" />
                </ChartLegend>
              </ChartContainer>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}

