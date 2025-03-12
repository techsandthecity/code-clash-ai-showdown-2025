import { TournamentBracket } from "@/components/tournament-bracket"
import { TeamSelector } from "@/components/team-selector"

export default function Home() {
  return (
    <div className="container mx-auto py-8 px-4">
      <h1 className="text-4xl font-bold text-center mb-8">SEC Basketball Tournament Predictor</h1>
      <p className="text-center mb-8 text-muted-foreground max-w-2xl mx-auto">
        Predict the outcomes of the SEC Basketball Tournament. Select teams and see how the tournament might unfold
        based on team statistics and performance.
      </p>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <div className="lg:col-span-1">
          <TeamSelector />
        </div>
        <div className="lg:col-span-3">
          <TournamentBracket />
        </div>
      </div>
    </div>
  )
}

