import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Calendar, Clock, MapPin, Users, DollarSign, Navigation } from "lucide-react"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import type { Event } from "@/lib/types"

interface EventCardProps {
  event: Event
  isNearby?: boolean
}

export function EventCard({ event, isNearby = false }: EventCardProps) {
  return (
    <Card className={`overflow-hidden ${isNearby ? "border-primary border-2" : ""}`}>
      <CardHeader className="p-0">
        <div className="relative h-40 w-full bg-muted">
          {event.image ? (
            <img src={event.image || "/placeholder.svg"} alt={event.name} className="h-full w-full object-cover" />
          ) : (
            <div className="flex h-full w-full items-center justify-center bg-gradient-to-br from-blue-500/20 to-purple-500/20">
              <span className="text-xl font-medium text-muted-foreground">{event.name}</span>
            </div>
          )}
          <Badge className="absolute top-2 right-2">{event.category}</Badge>
          {isNearby && (
            <Badge className="absolute top-2 left-2 bg-primary" variant="default">
              <Navigation className="h-3 w-3 mr-1" />
              Nearby
            </Badge>
          )}
        </div>
      </CardHeader>
      <CardContent className="p-4">
        <div className="space-y-3">
          <h3 className="font-semibold text-lg">{event.name}</h3>

          <div className="flex items-center text-sm text-muted-foreground">
            <Calendar className="mr-2 h-4 w-4" />
            <span>{event.date}</span>
          </div>

          <div className="flex items-center text-sm text-muted-foreground">
            <Clock className="mr-2 h-4 w-4" />
            <span>{event.time}</span>
          </div>

          <div className="flex items-center text-sm text-muted-foreground">
            <MapPin className="mr-2 h-4 w-4" />
            <span>{event.location}</span>
          </div>

          <div className="flex items-center text-sm">
            <DollarSign className="mr-2 h-4 w-4" />
            <span className="font-medium">
              {event.pricing.type}: ${event.pricing.price}
            </span>
          </div>

          {event.friendsAttending.length > 0 && (
            <div className="flex items-center gap-2">
              <Users className="h-4 w-4 text-muted-foreground" />
              <div className="flex -space-x-2">
                <TooltipProvider>
                  {event.friendsAttending.slice(0, 3).map((friend, index) => (
                    <Tooltip key={index}>
                      <TooltipTrigger asChild>
                        <Avatar className="h-6 w-6 border-2 border-background">
                          <AvatarFallback>{friend.name[0]}</AvatarFallback>
                          {friend.avatar && <AvatarImage src={friend.avatar} alt={friend.name} />}
                        </Avatar>
                      </TooltipTrigger>
                      <TooltipContent>
                        <p>{friend.name}</p>
                      </TooltipContent>
                    </Tooltip>
                  ))}
                </TooltipProvider>

                {event.friendsAttending.length > 3 && (
                  <Avatar className="h-6 w-6 border-2 border-background">
                    <AvatarFallback>+{event.friendsAttending.length - 3}</AvatarFallback>
                  </Avatar>
                )}
              </div>
              <span className="text-sm text-muted-foreground">
                {event.friendsAttending.length} {event.friendsAttending.length === 1 ? "friend" : "friends"} attending
              </span>
            </div>
          )}
        </div>
      </CardContent>
      <CardFooter className="p-4 pt-0">
        <Button className="w-full">Book Now</Button>
      </CardFooter>
    </Card>
  )
}

