import { UserHeader } from "@/components/user/user-header"
import { UserDashboard } from "@/components/user/user-dashboard"
import { EventRecommendations } from "@/components/user/event-recommendations"
import { SocialFriends } from "@/components/user/social-friends"
import { Gamification } from "@/components/user/gamification"
import { RecommendationMetrics } from "@/components/user/recommendation-metrics"

export default function UserHome() {
  return (
    <main className="min-h-screen bg-background">
      <UserHeader />
      <div className="container mx-auto px-4 py-6 max-w-7xl">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-3">
            <UserDashboard />
          </div>

          <div className="md:col-span-2">
            <EventRecommendations />
          </div>

          <div className="md:col-span-1">
            <div className="grid grid-cols-1 gap-6">
              <SocialFriends />
              <Gamification />
              <RecommendationMetrics />
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}

