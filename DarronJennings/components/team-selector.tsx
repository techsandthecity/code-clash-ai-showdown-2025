"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Slider } from "@/components/ui/slider"
import { secTeams, updateTeamStats } from "@/lib/tournament-utils"

export function TeamSelector() {
  const [teams, setTeams] = useState(secTeams)

  const handleStatChange = (teamIndex, stat, value) => {
    const updatedTeams = [...teams]
    updatedTeams[teamIndex].stats[stat] = value
    updateTeamStats(teamIndex, stat, value)
    setTeams(updatedTeams)
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Team Statistics</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-sm text-muted-foreground mb-4">
          Adjust team statistics to influence prediction outcomes. Changes will affect how the simulation predicts game
          results.
        </p>

        <div className="space-y-6 max-h-[600px] overflow-y-auto pr-2">
          {teams.map((team, index) => (
            <div key={index} className="space-y-3 pb-4 border-b last:border-0">
              <div className="flex items-center">
                <div className="w-6 h-6 flex items-center justify-center bg-muted rounded-full mr-2 text-xs">
                  {team.seed}
                </div>
                <h3 className="font-medium">{team.name}</h3>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <Label htmlFor={`${team.name}-wins`} className="text-xs">
                    Wins: {team.stats.wins}
                  </Label>
                  <Slider
                    id={`${team.name}-wins`}
                    defaultValue={[team.stats.wins]}
                    max={30}
                    step={1}
                    onValueChange={(value) => handleStatChange(index, "wins", value[0])}
                  />
                </div>
                <div>
                  <Label htmlFor={`${team.name}-losses`} className="text-xs">
                    Losses: {team.stats.losses}
                  </Label>
                  <Slider
                    id={`${team.name}-losses`}
                    defaultValue={[team.stats.losses]}
                    max={30}
                    step={1}
                    onValueChange={(value) => handleStatChange(index, "losses", value[0])}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <Label htmlFor={`${team.name}-ppg`} className="text-xs">
                    PPG: {team.stats.ppg}
                  </Label>
                  <Slider
                    id={`${team.name}-ppg`}
                    defaultValue={[team.stats.ppg]}
                    min={60}
                    max={100}
                    step={0.1}
                    onValueChange={(value) => handleStatChange(index, "ppg", value[0])}
                  />
                </div>
                <div>
                  <Label htmlFor={`${team.name}-oppg`} className="text-xs">
                    OPPG: {team.stats.oppg}
                  </Label>
                  <Slider
                    id={`${team.name}-oppg`}
                    defaultValue={[team.stats.oppg]}
                    min={60}
                    max={100}
                    step={0.1}
                    onValueChange={(value) => handleStatChange(index, "oppg", value[0])}
                  />
                </div>
              </div>

              <div>
                <Label htmlFor={`${team.name}-momentum`} className="text-xs">
                  Momentum: {team.stats.momentum}
                </Label>
                <Slider
                  id={`${team.name}-momentum`}
                  defaultValue={[team.stats.momentum]}
                  min={0}
                  max={10}
                  step={0.1}
                  onValueChange={(value) => handleStatChange(index, "momentum", value[0])}
                />
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}

