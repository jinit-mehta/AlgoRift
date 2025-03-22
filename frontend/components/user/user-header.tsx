"use client"

import { RefreshCw, Mic, MicOff, Home } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useEffect } from "react"
import { useVoiceSearch } from "@/hooks/use-voice-search"
import { useUserStore } from "@/lib/user-store"
import Link from "next/link"

export function UserHeader() {
  const { searchQuery, setSearchQuery, refreshData, isLoading } = useUserStore()
  const { isListening, toggleListening, transcript, hasVoiceSupport } = useVoiceSearch()

  useEffect(() => {
    if (transcript) {
      setSearchQuery(transcript)
    }
  }, [transcript, setSearchQuery])

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
          <h1 className="text-xl font-bold tracking-tight">Event Discovery</h1>
        </div>

        <div className="flex items-center gap-4">
          <div className="relative w-full max-w-sm">
            <Input
              type="text"
              placeholder="Search events..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pr-10"
            />
            {hasVoiceSupport && (
              <Button variant="ghost" size="icon" className="absolute right-0 top-0" onClick={toggleListening}>
                {isListening ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
                <span className="sr-only">{isListening ? "Stop voice search" : "Start voice search"}</span>
              </Button>
            )}
          </div>

          <Button variant="outline" size="icon" onClick={refreshData} disabled={isLoading}>
            <RefreshCw className={`h-4 w-4 ${isLoading ? "animate-spin" : ""}`} />
            <span className="sr-only">Refresh data</span>
          </Button>
        </div>
      </div>
    </header>
  )
}

