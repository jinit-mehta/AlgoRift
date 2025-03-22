"use client"

import * as React from "react"

const Chart = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(({ className, ...props }, ref) => (
  <div className="relative" ref={ref} {...props} />
))
Chart.displayName = "Chart"

const ChartContainer = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => <div className="overflow-hidden rounded-md border" ref={ref} {...props} />,
)
ChartContainer.displayName = "ChartContainer"

const ChartTooltip = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      className="absolute z-10 rounded-md border bg-popover px-2 py-1.5 text-sm font-medium text-popover-foreground shadow-lg animate-in fade-in"
      ref={ref}
      {...props}
    />
  ),
)
ChartTooltip.displayName = "ChartTooltip"

const ChartTooltipContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => <div className="space-y-1" ref={ref} {...props} />,
)
ChartTooltipContent.displayName = "ChartTooltipContent"

const ChartLegend = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => <div className="flex items-center space-x-2" ref={ref} {...props} />,
)
ChartLegend.displayName = "ChartLegend"

const ChartLegendItem = React.forwardRef<
  HTMLDivElement,
  { name: string; color: string } & React.HTMLAttributes<HTMLDivElement>
>(({ className, name, color, ...props }, ref) => (
  <div className="flex items-center text-sm" ref={ref} {...props}>
    <svg width="12" height="12" viewBox="0 0 12 12" fill="none" className="mr-2">
      <rect width="12" height="12" fill={color} rx="6" />
    </svg>
    {name}
  </div>
))
ChartLegendItem.displayName = "ChartLegendItem"

export { Chart, ChartContainer, ChartTooltip, ChartTooltipContent, ChartLegend, ChartLegendItem }

