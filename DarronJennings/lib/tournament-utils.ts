// SEC Teams with realistic data
export const secTeams = [
  {
    name: "Alabama",
    seed: 1,
    stats: { wins: 24, losses: 7, ppg: 89.8, oppg: 78.2, momentum: 8.5 },
  },
  {
    name: "Tennessee",
    seed: 2,
    stats: { wins: 24, losses: 7, ppg: 79.6, oppg: 67.8, momentum: 8.2 },
  },
  {
    name: "Kentucky",
    seed: 3,
    stats: { wins: 23, losses: 8, ppg: 87.2, oppg: 79.1, momentum: 7.8 },
  },
  {
    name: "Auburn",
    seed: 4,
    stats: { wins: 22, losses: 9, ppg: 83.1, oppg: 72.3, momentum: 7.5 },
  },
  {
    name: "South Carolina",
    seed: 5,
    stats: { wins: 21, losses: 10, ppg: 75.4, oppg: 70.2, momentum: 7.0 },
  },
  {
    name: "Florida",
    seed: 6,
    stats: { wins: 21, losses: 10, ppg: 82.7, oppg: 77.5, momentum: 6.8 },
  },
  {
    name: "Mississippi State",
    seed: 7,
    stats: { wins: 20, losses: 11, ppg: 74.8, oppg: 71.3, momentum: 6.5 },
  },
  {
    name: "Texas A&M",
    seed: 8,
    stats: { wins: 19, losses: 12, ppg: 76.2, oppg: 73.1, momentum: 6.2 },
  },
  {
    name: "Ole Miss",
    seed: 9,
    stats: { wins: 19, losses: 12, ppg: 77.5, oppg: 74.8, momentum: 6.0 },
  },
  {
    name: "LSU",
    seed: 10,
    stats: { wins: 17, losses: 14, ppg: 78.3, oppg: 77.2, momentum: 5.5 },
  },
  {
    name: "Georgia",
    seed: 11,
    stats: { wins: 16, losses: 15, ppg: 75.9, oppg: 76.8, momentum: 5.0 },
  },
  {
    name: "Arkansas",
    seed: 12,
    stats: { wins: 15, losses: 16, ppg: 79.1, oppg: 80.2, momentum: 4.5 },
  },
  {
    name: "Missouri",
    seed: 13,
    stats: { wins: 13, losses: 18, ppg: 73.6, oppg: 78.4, momentum: 4.0 },
  },
  {
    name: "Vanderbilt",
    seed: 14,
    stats: { wins: 9, losses: 22, ppg: 71.2, oppg: 79.5, momentum: 3.5 },
  },
]

// Update team stats in the global array
export function updateTeamStats(teamIndex, stat, value) {
  secTeams[teamIndex].stats[stat] = value
}

// Predict the winner of a game based on team statistics
export function predictGame(team1, team2) {
  // If either team is not defined or doesn't have stats, return the other team
  if (!team1 || !team1.stats) return team2
  if (!team2 || !team2.stats) return team1

  // Calculate team strength based on various factors
  const team1Strength = calculateTeamStrength(team1)
  const team2Strength = calculateTeamStrength(team2)

  // Add some randomness to the prediction (upset factor)
  const upsetFactor = Math.random() * 20 - 10 // Random value between -10 and 10

  // Determine winner based on strength plus upset factor
  if (team1Strength + upsetFactor > team2Strength) {
    return team1
  } else {
    return team2
  }
}

// Calculate team strength based on various statistics
function calculateTeamStrength(team) {
  if (!team || !team.stats) return 0

  const { wins, losses, ppg, oppg, momentum } = team.stats

  // Win percentage (40% weight)
  const winPct = (wins / (wins + losses)) * 40

  // Scoring margin (30% weight)
  const scoringMargin = (ppg - oppg) * 3

  // Momentum factor (20% weight)
  const momentumFactor = momentum * 2

  // Seed advantage (10% weight)
  const seedAdvantage = (15 - team.seed) * 0.5

  return winPct + scoringMargin + momentumFactor + seedAdvantage
}

