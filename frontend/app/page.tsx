import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import Link from "next/link"

export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-50">
      <div className="container max-w-6xl px-4">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold tracking-tight text-primary mb-4">Organizer Intelligence System</h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            A comprehensive platform for event discovery, planning, and analytics
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle>User Interface</CardTitle>
              <CardDescription>Discover events, connect with friends, and earn rewards</CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="list-disc list-inside space-y-2 text-muted-foreground">
                <li>Personalized event recommendations</li>
                <li>See which friends are attending events</li>
                <li>Earn badges and points for participation</li>
                <li>Voice search for quick event discovery</li>
                <li>Dynamic pricing based on demand</li>
              </ul>
            </CardContent>
            <CardFooter>
              <Link href="/user" className="w-full">
                <Button className="w-full" size="lg">
                  Enter User Interface
                </Button>
              </Link>
            </CardFooter>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle>Organizer Interface</CardTitle>
              <CardDescription>Analytics, insights, and tools for event planning</CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="list-disc list-inside space-y-2 text-muted-foreground">
                <li>Comprehensive event analytics</li>
                <li>AI-generated event ideas</li>
                <li>Smart scheduling recommendations</li>
                <li>Optimized pricing strategies</li>
                <li>Performance insights and metrics</li>
              </ul>
            </CardContent>
            <CardFooter>
              <Link href="/organizer" className="w-full">
                <Button className="w-full" size="lg" variant="secondary">
                  Enter Organizer Interface
                </Button>
              </Link>
            </CardFooter>
          </Card>
        </div>
      </div>
    </div>
  )
}

