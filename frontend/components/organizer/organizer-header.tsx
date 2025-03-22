"use client"

import { RefreshCw, Home } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useOrganizerStore } from "@/lib/organizer-store"
import Link from "next/link"

export function OrganizerHeader() {
  const { refreshData, isLoading } = useOrganizerStore()

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between px-4 max-w-7xl mx-auto">
        <div className="flex items-center gap-2">
          <Link href="/">
            <Button variant="ghost" size="icon">
              <Home className="h-5 w-5" />
              <span className="sr-only">Home</span>
            </Button>
          </Link>
          <h1 className="text-xl font-bold tracking-tight">Organizer Intelligence</h1>
        </div>

        <div className="flex items-center gap-4">
          <Button variant="outline" onClick={refreshData} disabled={isLoading}>
            <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? "animate-spin" : ""}`} />
            Refresh Data
          </Button>
        </div>
      </div>
    </header>
  )
}

