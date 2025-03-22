import { OrganizerHeader } from "@/components/organizer/organizer-header"
import { OrganizerDashboard } from "@/components/organizer/organizer-dashboard"
import { AnalyticsCharts } from "@/components/organizer/analytics-charts"
import { EventIdeaGenerator } from "@/components/organizer/event-idea-generator"
import { SmartScheduler } from "@/components/organizer/smart-scheduler"
import { PricingStrategy } from "@/components/organizer/pricing-strategy"
import { OrganizerInsights } from "@/components/organizer/organizer-insights"

export default function OrganizerHome() {
  return (
    <main className="min-h-screen bg-background">
      <OrganizerHeader />
      <div className="container mx-auto px-4 py-6 max-w-7xl">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-3">
            <OrganizerDashboard />
          </div>

          <div className="md:col-span-3">
            <AnalyticsCharts />
          </div>

          <div className="md:col-span-2">
            <EventIdeaGenerator />
          </div>

          <div className="md:col-span-1">
            <div className="grid grid-cols-1 gap-6">
              <SmartScheduler />
              <PricingStrategy />
            </div>
          </div>

          <div className="md:col-span-3">
            <OrganizerInsights />
          </div>
        </div>
      </div>
    </main>
  )
}

