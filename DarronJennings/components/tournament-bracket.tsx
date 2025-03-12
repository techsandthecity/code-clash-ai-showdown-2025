"use client"

import { useState, useEffect } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useToast } from "@/hooks/use-toast"
import { secTeams, predictGame } from "@/lib/tournament-utils"

export function TournamentBracket() {
  const { toast } = useToast()
  const [bracket, setBracket] = useState<any>(null)
  const [isSimulating, setIsSimulating] = useState(false)

  useEffect(() => {
    // Initialize the bracket with the SEC tournament structure
    initializeBracket()
  }, [])

  const initializeBracket = () => {
    // SEC Tournament has 14 teams, with top 4 getting double-byes and 5-10 getting single-byes
    const newBracket = {
      rounds: [
        {
          name: "First Round",
          games: [
            { id: 1, team1: secTeams[10], team2: secTeams[13], winner: null },
            { id: 2, team1: secTeams[11], team2: secTeams[12], winner: null },
          ],
        },
        {
          name: "Second Round",
          games: [
            { id: 3, team1: secTeams[8], team2: { name: "Winner Game 1", seed: null, stats: null }, winner: null },
            { id: 4, team1: secTeams[5], team2: secTeams[9], winner: null },
            { id: 5, team1: secTeams[7], team2: { name: "Winner Game 2", seed: null, stats: null }, winner: null },
            { id: 6, team1: secTeams[6], team2: secTeams[10], winner: null },
          ],
        },
        {
          name: "Quarterfinals",
          games: [
            { id: 7, team1: secTeams[0], team2: { name: "Winner Game 3", seed: null, stats: null }, winner: null },
            { id: 8, team1: secTeams[1], team2: { name: "Winner Game 4", seed: null, stats: null }, winner: null },
            { id: 9, team1: secTeams[2], team2: { name: "Winner Game 5", seed: null, stats: null }, winner: null },
            { id: 10, team1: secTeams[3], team2: { name: "Winner Game 6", seed: null, stats: null }, winner: null },
          ],
        },
        {
          name: "Semifinals",
          games: [
            {
              id: 11,
              team1: { name: "Winner Game 7", seed: null, stats: null },
              team2: { name: "Winner Game 8", seed: null, stats: null },
              winner: null,
            },
            {
              id: 12,
              team1: { name: "Winner Game 9", seed: null, stats: null },
              team2: { name: "Winner Game 10", seed: null, stats: null },
              winner: null,
            },
          ],
        },
        {
          name: "Championship",
          games: [
            {
              id: 13,
              team1: { name: "Winner Game 11", seed: null, stats: null },
              team2: { name: "Winner Game 12", seed: null, stats: null },
              winner: null,
            },
          ],
        },
      ],
    }

    setBracket(newBracket)
  }

  const simulateTournament = () => {
    setIsSimulating(true)

    // Create a copy of the bracket to modify
    const newBracket = JSON.parse(JSON.stringify(bracket))

    // Simulate first round
    newBracket.rounds[0].games.forEach((game) => {
      game.winner = predictGame(game.team1, game.team2)
    })

    // Update second round with winners
    newBracket.rounds[1].games[0].team2 = newBracket.rounds[0].games[0].winner
    newBracket.rounds[1].games[2].team2 = newBracket.rounds[0].games[1].winner

    // Simulate second round
    newBracket.rounds[1].games.forEach((game) => {
      game.winner = predictGame(game.team1, game.team2)
    })

    // Update quarterfinals with winners
    newBracket.rounds[2].games[0].team2 = newBracket.rounds[1].games[0].winner
    newBracket.rounds[2].games[1].team2 = newBracket.rounds[1].games[1].winner
    newBracket.rounds[2].games[2].team2 = newBracket.rounds[1].games[2].winner
    newBracket.rounds[2].games[3].team2 = newBracket.rounds[1].games[3].winner

    // Simulate quarterfinals
    newBracket.rounds[2].games.forEach((game) => {
      game.winner = predictGame(game.team1, game.team2)
    })

    // Update semifinals with winners
    newBracket.rounds[3].games[0].team1 = newBracket.rounds[2].games[0].winner
    newBracket.rounds[3].games[0].team2 = newBracket.rounds[2].games[1].winner
    newBracket.rounds[3].games[1].team1 = newBracket.rounds[2].games[2].winner
    newBracket.rounds[3].games[1].team2 = newBracket.rounds[2].games[3].winner

    // Simulate semifinals
    newBracket.rounds[3].games.forEach((game) => {
      game.winner = predictGame(game.team1, game.team2)
    })

    // Update championship with winners
    newBracket.rounds[4].games[0].team1 = newBracket.rounds[3].games[0].winner
    newBracket.rounds[4].games[0].team2 = newBracket.rounds[3].games[1].winner

    // Simulate championship
    newBracket.rounds[4].games[0].winner = predictGame(
      newBracket.rounds[4].games[0].team1,
      newBracket.rounds[4].games[0].team2,
    )

    // Update the bracket state
    setBracket(newBracket)
    setIsSimulating(false)

    toast({
      title: "Tournament Simulated",
      description: `Champion: ${newBracket.rounds[4].games[0].winner.name}`,
    })
  }

  const resetBracket = () => {
    initializeBracket()
    toast({
      title: "Tournament Reset",
      description: "The bracket has been reset to its initial state.",
    })
  }

  if (!bracket) {
    return <div className="flex justify-center items-center h-64">Loading bracket...</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Tournament Bracket</h2>
        <div className="space-x-2">
          <Button onClick={simulateTournament} disabled={isSimulating} variant="default">
            {isSimulating ? "Simulating..." : "Simulate Tournament"}
          </Button>
          <Button onClick={resetBracket} variant="outline">
            Reset
          </Button>
        </div>
      </div>

      <Tabs defaultValue="bracket" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="bracket">Bracket View</TabsTrigger>
          <TabsTrigger value="rounds">Rounds View</TabsTrigger>
        </TabsList>

        <TabsContent value="bracket" className="pt-4">
          <div className="overflow-x-auto">
            <div className="flex min-w-[1000px]">
              {bracket.rounds.map((round, roundIndex) => (
                <div key={roundIndex} className="flex-1">
                  <h3 className="text-center font-semibold mb-4">{round.name}</h3>
                  <div className="space-y-8 flex flex-col justify-around h-full">
                    {round.games.map((game, gameIndex) => (
                      <Card key={game.id} className={`mx-2 ${game.winner ? "border-primary" : ""}`}>
                        <CardContent className="p-3">
                          <div className="space-y-2">
                            <TeamDisplay team={game.team1} isWinner={game.winner?.name === game.team1.name} />
                            <div className="text-center text-xs">vs</div>
                            <TeamDisplay team={game.team2} isWinner={game.winner?.name === game.team2.name} />
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </TabsContent>

        <TabsContent value="rounds" className="pt-4 space-y-6">
          {bracket.rounds.map((round, roundIndex) => (
            <div key={roundIndex}>
              <h3 className="text-xl font-semibold mb-3">{round.name}</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {round.games.map((game) => (
                  <Card key={game.id} className={`${game.winner ? "border-primary" : ""}`}>
                    <CardContent className="p-4">
                      <div className="flex justify-between items-center">
                        <div className="space-y-3 w-full">
                          <TeamDisplay team={game.team1} isWinner={game.winner?.name === game.team1.name} showStats />
                          <div className="text-center text-sm font-medium">vs</div>
                          <TeamDisplay team={game.team2} isWinner={game.winner?.name === game.team2.name} showStats />

                          {game.winner && (
                            <div className="mt-3 pt-3 border-t">
                              <p className="text-center font-medium">
                                Winner: <span className="text-primary">{game.winner.name}</span>
                              </p>
                            </div>
                          )}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          ))}
        </TabsContent>
      </Tabs>
    </div>
  )
}

function TeamDisplay({ team, isWinner = false, showStats = false }) {
  if (!team || !team.name) return <div className="h-6">TBD</div>

  return (
    <div className={`flex items-center ${isWinner ? "font-bold text-primary" : ""}`}>
      <div className="w-6 h-6 flex items-center justify-center bg-muted rounded-full mr-2 text-xs">
        {team.seed || "-"}
      </div>
      <div className="flex-1">
        <div className="flex justify-between">
          <span>{team.name}</span>
          {team.stats && showStats && (
            <span className="text-xs text-muted-foreground">
              {team.stats.wins}-{team.stats.losses}
            </span>
          )}
        </div>
        {team.stats && showStats && (
          <div className="text-xs text-muted-foreground mt-1">
            PPG: {team.stats.ppg} | OPP: {team.stats.oppg}
          </div>
        )}
      </div>
    </div>
  )
}

