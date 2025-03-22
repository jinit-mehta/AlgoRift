"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { useUserStore } from "@/lib/user-store"

export function SocialFriends() {
  const { friends } = useUserStore()

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>Social Network</CardTitle>
        <CardDescription>Friends attending events</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {friends.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-40 text-muted-foreground">
              <p>No friends are attending events.</p>
            </div>
          ) : (
            friends.map((friend, index) => (
              <div key={index} className="flex items-center gap-3 p-2">
                <Avatar>
                  <AvatarFallback>{friend.name[0]}</AvatarFallback>
                  {friend.avatar && <AvatarImage src={friend.avatar} alt={friend.name} />}
                </Avatar>

                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <p className="font-medium truncate">{friend.name}</p>
                    <Badge variant="outline" className="ml-2">
                      {friend.mutualEvents} events
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground truncate">Attending: {friend.attendingEvent}</p>
                </div>
              </div>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  )
}

