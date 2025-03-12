import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';

// Team data for the 2025 SEC Tournament based on actual bracket
const secTeams = [
  { name: "Auburn", seed: 1, offRating: 119.8, defRating: 93.2, overallEfficiency: 26.6, color: "#0C2340" },
  { name: "Florida", seed: 2, offRating: 117.5, defRating: 94.1, overallEfficiency: 23.4, color: "#0021A5" },
  { name: "Alabama", seed: 3, offRating: 118.2, defRating: 96.7, overallEfficiency: 21.5, color: "#A32136" },
  { name: "Tennessee", seed: 4, offRating: 116.5, defRating: 95.3, overallEfficiency: 21.2, color: "#FF8200" },
  { name: "Texas A&M", seed: 5, offRating: 114.8, defRating: 95.4, overallEfficiency: 19.4, color: "#500000" },
  { name: "Kentucky", seed: 6, offRating: 116.8, defRating: 98.2, overallEfficiency: 18.6, color: "#0033A0" },
  { name: "Missouri", seed: 7, offRating: 112.5, defRating: 96.4, overallEfficiency: 16.1, color: "#F1B82D" },
  { name: "Ole Miss", seed: 8, offRating: 111.3, defRating: 97.8, overallEfficiency: 13.5, color: "#14213D" },
  { name: "Arkansas", seed: 9, offRating: 110.7, defRating: 97.4, overallEfficiency: 13.3, color: "#9D2235" },
  { name: "Mississippi State", seed: 10, offRating: 108.5, defRating: 96.9, overallEfficiency: 11.6, color: "#660000" },
  { name: "Georgia", seed: 11, offRating: 107.2, defRating: 98.5, overallEfficiency: 8.7, color: "#BA0C2F" },
  { name: "Vanderbilt", seed: 12, offRating: 106.8, defRating: 98.2, overallEfficiency: 8.6, color: "#866D4B" },
  { name: "Texas", seed: 13, offRating: 106.3, defRating: 100.4, overallEfficiency: 5.9, color: "#BF5700" },
  { name: "Oklahoma", seed: 14, offRating: 105.1, defRating: 100.6, overallEfficiency: 4.5, color: "#841617" },
  { name: "LSU", seed: 15, offRating: 104.2, defRating: 101.5, overallEfficiency: 2.7, color: "#461D7C" },
  { name: "South Carolina", seed: 16, offRating: 103.7, defRating: 101.8, overallEfficiency: 1.9, color: "#73000A" }
];

// Function to simulate a single game between two teams
function simulateGame(teamA, teamB) {
  const efficiencyDiff = teamA.overallEfficiency - teamB.overallEfficiency;
  
  let teamAWinProb = 0.5 + (efficiencyDiff / 60);
  
  if (Math.abs(efficiencyDiff) < 5) {
    const seedAdvantage = (teamB.seed - teamA.seed) * 0.01;
    teamAWinProb += seedAdvantage;
  }
  
  teamAWinProb = Math.min(Math.max(teamAWinProb, 0.1), 0.9);
  
  return Math.random() < teamAWinProb ? teamA : teamB;
}

// Function to set up the initial tournament bracket
function initializeBracket() {
  return [...secTeams].sort((a, b) => a.seed - b.seed);
}

// Function to simulate the entire tournament
function simulateTournament() {
  let teams = initializeBracket();
  const rounds = ['First Round', 'Second Round', 'Quarterfinals', 'Semifinals', 'Finals'];
  const tournamentLog = [];
  
  tournamentLog.push({ round: "Tournament Start", matchups: [] });
  
  // Simulate each round
  for (let round = 0; round < rounds.length; round++) {
    const roundLog = { round: rounds[round], matchups: [] };
    const nextRoundTeams = [];
    
    // Simulate all games in the current round
    for (let i = 0; i < teams.length; i += 2) {
      // If odd number of teams, give the last team a bye
      if (i + 1 >= teams.length) {
        nextRoundTeams.push(teams[i]);
        roundLog.matchups.push({
          teamA: teams[i],
          teamB: null,
          winner: teams[i],
          isBye: true
        });
        continue;
      }
      
      const teamA = teams[i];
      const teamB = teams[i + 1];
      const winner = simulateGame(teamA, teamB);
      
      roundLog.matchups.push({
        teamA: teamA,
        teamB: teamB,
        winner: winner,
        isBye: false
      });
      
      nextRoundTeams.push(winner);
    }
    
    tournamentLog.push(roundLog);
    teams = nextRoundTeams;
  }
  
  return { champion: teams[0], log: tournamentLog };
}

// Function to run multiple simulations and find the most likely champion
function predictChampion(numSimulations = 1000) {
  const championCounts = {};
  const roundAdvances = {};
  
  // Initialize counts for all teams
  secTeams.forEach(team => {
    championCounts[team.name] = 0;
    roundAdvances[team.name] = {
      'First Round': 0,
      'Second Round': 0,
      'Quarterfinals': 0,
      'Semifinals': 0,
      'Finals': 0,
      'Champion': 0
    };
  });
  
  // Run simulations
  for (let i = 0; i < numSimulations; i++) {
    const result = simulateTournament();
    const champion = result.champion;
    championCounts[champion.name]++;
    
    // Track round advances
    result.log.forEach(round => {
      if (round.round !== "Tournament Start") {
        round.matchups.forEach(matchup => {
          if (!matchup.isBye) {
            const winnerName = matchup.winner.name;
            roundAdvances[winnerName][round.round]++;
            
            if (round.round === "Finals") {
              roundAdvances[winnerName]["Champion"]++;
            }
          }
        });
      }
    });
  }
  
  // Calculate win probabilities
  const predictions = Object.entries(championCounts).map(([name, count]) => {
    return {
      team: name,
      winCount: count,
      probability: (count / numSimulations * 100).toFixed(1),
      roundData: roundAdvances[name]
    };
  });
  
  // Sort by probability (descending)
  predictions.sort((a, b) => b.winCount - a.winCount);
  
  return predictions;
}

const SECTournamentPredictor = () => {
  const [predictions, setPredictions] = useState([]);
  const [simulationCount, setSimulationCount] = useState(1000);
  const [isLoading, setIsLoading] = useState(false);
  const [singleSimulation, setSingleSimulation] = useState(null);
  const [showSingleSim, setShowSingleSim] = useState(false);
  const [activeTeam, setActiveTeam] = useState(null);
  
  // CSS styles
  const styles = {
    container: {
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
      maxWidth: '1200px',
      margin: '0 auto',
      padding: '20px'
    },
    card: {
      backgroundColor: 'white',
      borderRadius: '8px',
      boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
      overflow: 'hidden'
    },
    header: {
      padding: '20px',
      backgroundColor: '#0033A0',
      color: 'white'
    },
    title: {
      fontSize: '2rem',
      fontWeight: 'bold',
      margin: '0 0 8px 0'
    },
    subtitle: {
      fontSize: '1rem',
      color: '#b3c6f1',
      margin: '0'
    },
    content: {
      padding: '20px'
    },
    controlRow: {
      display: 'flex',
      gap: '20px',
      marginBottom: '30px',
      flexWrap: 'wrap'
    },
    inputGroup: {
      flex: '1',
      minWidth: '300px'
    },
    label: {
      display: 'block',
      marginBottom: '8px',
      fontWeight: '500'
    },
    input: {
      width: '100%',
      padding: '10px',
      border: '1px solid #ccc',
      borderRadius: '4px',
      fontSize: '16px'
    },
    buttonGroup: {
      display: 'flex',
      gap: '10px',
      flex: '1',
      minWidth: '300px',
      alignItems: 'flex-end'
    },
    button: {
      flex: '1',
      padding: '12px',
      borderRadius: '4px',
      border: 'none',
      cursor: 'pointer',
      fontWeight: '600',
      fontSize: '14px'
    },
    primaryButton: {
      backgroundColor: '#0033A0',
      color: 'white'
    },
    secondaryButton: {
      backgroundColor: '#f0f0f0',
      color: '#333'
    },
    disabledButton: {
      opacity: '0.7',
      cursor: 'not-allowed'
    },
    section: {
      marginBottom: '40px'
    },
    sectionTitle: {
      fontSize: '1.5rem',
      fontWeight: '600',
      marginBottom: '16px'
    },
    sectionSubtitle: {
      fontSize: '0.9rem',
      color: '#666',
      marginBottom: '20px'
    },
    teamDetailTitle: {
      fontSize: '1.25rem',
      fontWeight: '600',
      marginBottom: '12px'
    },
    gridContainer: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
      gap: '16px',
      marginTop: '20px'
    },
    gridItem: {
      backgroundColor: '#f5f5f5',
      padding: '16px',
      borderRadius: '4px'
    },
    gridItemLabel: {
      fontSize: '0.85rem',
      color: '#666',
      marginBottom: '4px'
    },
    gridItemValue: {
      fontSize: '1.25rem',
      fontWeight: '600'
    },
    gridItemSubtext: {
      fontSize: '0.75rem',
      color: '#888',
      marginTop: '4px'
    },
    table: {
      width: '100%',
      borderCollapse: 'collapse',
      marginTop: '20px',
      overflow: 'hidden',
      borderRadius: '4px',
      border: '1px solid #eee'
    },
    tableHeader: {
      backgroundColor: '#f5f5f5',
      textAlign: 'left',
      fontWeight: '600'
    },
    tableHeaderCell: {
      padding: '12px 16px',
      borderBottom: '1px solid #ddd'
    },
    tableRow: {
      cursor: 'pointer',
      borderBottom: '1px solid #eee'
    },
    tableRowActive: {
      backgroundColor: '#f0f7ff'
    },
    tableCell: {
      padding: '12px 16px'
    },
    collapsibleSection: {
      marginTop: '30px'
    },
    collapsibleHeader: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      marginBottom: '16px'
    },
    closeButton: {
      padding: '4px 8px',
      backgroundColor: '#ff5252',
      color: 'white',
      border: 'none',
      borderRadius: '4px',
      cursor: 'pointer',
      fontSize: '0.85rem'
    },
    championCard: {
      padding: '16px',
      backgroundColor: '#e8f0fe',
      borderRadius: '4px',
      marginBottom: '20px'
    },
    roundContainer: {
      marginBottom: '20px',
      border: '1px solid #ddd',
      borderRadius: '4px',
      overflow: 'hidden'
    },
    roundHeader: {
      padding: '12px 16px',
      backgroundColor: '#f0f0f0',
      fontWeight: '600'
    },
    matchupContainer: {
      padding: '12px 16px',
      borderTop: '1px solid #ddd',
      display: 'flex',
      alignItems: 'center',
      flexWrap: 'wrap'
    },
    teamNameA: {
      flex: '1',
      minWidth: '200px',
      padding: '4px 0'
    },
    teamNameB: {
      flex: '1',
      minWidth: '200px',
      padding: '4px 0'
    },
    vsLabel: {
      padding: '0 16px'
    },
    winnerLabel: {
      marginLeft: '16px',
      fontSize: '0.85rem',
      padding: '2px 8px',
      borderRadius: '4px',
      backgroundColor: '#f0f0f0'
    },
    footer: {
      marginTop: '40px',
      padding: '20px 0',
      borderTop: '1px solid #eee',
      color: '#888',
      fontSize: '0.85rem'
    }
  };
  
  // Run predictions on component mount
  useEffect(() => {
    runSimulations();
  }, []);
  
  // Function to run the simulations
  const runSimulations = () => {
    setIsLoading(true);
    
    // Use setTimeout to prevent UI freezing
    setTimeout(() => {
      const predictions = predictChampion(simulationCount);
      setPredictions(predictions);
      setIsLoading(false);
    }, 100);
  };
  
  // Function to run a single simulation for demonstration
  const runSingleSimulation = () => {
    setIsLoading(true);
    
    setTimeout(() => {
      const result = simulateTournament();
      setSingleSimulation(result);
      setShowSingleSim(true);
      setIsLoading(false);
    }, 100);
  };
  
  // Data for round advancement chart
  const prepareRoundData = () => {
    if (predictions.length === 0) return [];
    
    const rounds = ["First Round", "Second Round", "Quarterfinals", "Semifinals", "Finals", "Champion"];
    const data = [];
    
    rounds.forEach(round => {
      const roundData = {
        name: round,
      };
      
      predictions.forEach(pred => {
        if (activeTeam && pred.team !== activeTeam) return;
        
        const percentage = pred.roundData && pred.roundData[round] ? 
          (pred.roundData[round] / simulationCount * 100).toFixed(1) : 0;
        
        roundData[pred.team] = parseFloat(percentage);
      });
      
      data.push(roundData);
    });
    
    return data;
  };
  
  // Get the team color by name
  const getTeamColor = (teamName) => {
    const team = secTeams.find(team => team.name === teamName);
    return team ? team.color : "#000000";
  };
  
  // Handle team selection for detailed view
  const handleTeamClick = (teamName) => {
    setActiveTeam(activeTeam === teamName ? null : teamName);
  };
  
  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.header}>
          <h1 style={styles.title}>2025 SEC Basketball Tournament Predictor</h1>
          <p style={styles.subtitle}>Based on team statistics and Monte Carlo simulation</p>
        </div>
        
        <div style={styles.content}>
          <div style={styles.controlRow}>
            <div style={styles.inputGroup}>
              <label style={styles.label}>Number of Simulations</label>
              <input
                type="number"
                min="100"
                max="10000"
                step="100"
                value={simulationCount}
                onChange={(e) => setSimulationCount(Number(e.target.value))}
                style={styles.input}
              />
            </div>
            
            <div style={styles.buttonGroup}>
              <button
                onClick={runSimulations}
                disabled={isLoading}
                style={{
                  ...styles.button,
                  ...styles.primaryButton,
                  ...(isLoading ? styles.disabledButton : {})
                }}
              >
                {isLoading ? "Running..." : "Run Predictions"}
              </button>
              
              <button
                onClick={runSingleSimulation}
                disabled={isLoading}
                style={{
                  ...styles.button,
                  ...styles.secondaryButton,
                  ...(isLoading ? styles.disabledButton : {})
                }}
              >
                Simulate One Tournament
              </button>
            </div>
          </div>
          
          {predictions.length > 0 && (
            <div style={styles.section}>
              <h2 style={styles.sectionTitle}>Championship Predictions</h2>
              <p style={styles.sectionSubtitle}>
                Based on {simulationCount.toLocaleString()} simulations. Click on a team for detailed analysis.
              </p>
              
              <div style={{ height: '400px', marginBottom: '30px' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={predictions.map(p => ({
                      team: p.team,
                      probability: parseFloat(p.probability),
                      color: getTeamColor(p.team)
                    }))}
                    margin={{ top: 5, right: 30, left: 20, bottom: 60 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="team" 
                      angle={-45} 
                      textAnchor="end" 
                      height={80} 
                      tick={{ fontSize: 12 }}
                    />
                    <YAxis label={{ value: 'Win Probability (%)', angle: -90, position: 'insideLeft' }} />
                    <Tooltip formatter={(value) => [`${value}%`, 'Chance to Win']} />
                    <Bar dataKey="probability" name="Chance to Win">
                      {predictions.map((entry, index) => (
                        <Cell 
                          key={`cell-${index}`} 
                          fill={entry.team === activeTeam ? getTeamColor(entry.team) : '#ddd'} 
                          onClick={() => handleTeamClick(entry.team)}
                          cursor="pointer"
                        />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
              
              {activeTeam && (
                <div style={{ marginTop: '30px', marginBottom: '30px' }}>
                  <h3 
                    style={{ 
                      ...styles.teamDetailTitle, 
                      color: getTeamColor(activeTeam)
                    }}
                  >
                    {activeTeam} Tournament Progression
                  </h3>
                  
                  <div style={{ height: '300px', marginBottom: '20px' }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart 
                        data={prepareRoundData()} 
                        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis label={{ value: 'Probability (%)', angle: -90, position: 'insideLeft' }} />
                        <Tooltip />
                        <Line 
                          type="monotone" 
                          dataKey={activeTeam} 
                          stroke={getTeamColor(activeTeam)} 
                          strokeWidth={3} 
                          dot={{ r: 6 }}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                  
                  <div style={styles.gridContainer}>
                    {Object.entries(predictions.find(p => p.team === activeTeam).roundData).map(([round, count]) => (
                      <div key={round} style={styles.gridItem}>
                        <div style={styles.gridItemLabel}>{round}</div>
                        <div style={styles.gridItemValue}>
                          {(count / simulationCount * 100).toFixed(1)}%
                        </div>
                        <div style={styles.gridItemSubtext}>
                          {count.toLocaleString()} of {simulationCount.toLocaleString()} simulations
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              <div style={{ marginTop: '30px' }}>
                <h3 style={styles.teamDetailTitle}>Prediction Results</h3>
                <table style={styles.table}>
                  <thead>
                    <tr style={styles.tableHeader}>
                      <th style={styles.tableHeaderCell}>Rank</th>
                      <th style={styles.tableHeaderCell}>Team</th>
                      <th style={styles.tableHeaderCell}>Seed</th>
                      <th style={styles.tableHeaderCell}>Championship Probability</th>
                      <th style={styles.tableHeaderCell}>Final Four Probability</th>
                    </tr>
                  </thead>
                  <tbody>
                    {predictions.map((pred, idx) => {
                      const team = secTeams.find(t => t.name === pred.team);
                      const finalFourProb = (pred.roundData["Semifinals"] / simulationCount * 100).toFixed(1);
                      
                      return (
                        <tr 
                          key={pred.team} 
                          style={{
                            ...styles.tableRow, 
                            ...(activeTeam === pred.team ? styles.tableRowActive : {})
                          }}
                          onClick={() => handleTeamClick(pred.team)}
                        >
                          <td style={styles.tableCell}>{idx + 1}</td>
                          <td 
                            style={{
                              ...styles.tableCell,
                              color: team.color,
                              fontWeight: 500
                            }}
                          >
                            {pred.team}
                          </td>
                          <td style={styles.tableCell}>{team.seed}</td>
                          <td style={styles.tableCell}>{pred.probability}%</td>
                          <td style={styles.tableCell}>{finalFourProb}%</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}
          
          {showSingleSim && singleSimulation && (
            <div style={styles.collapsibleSection}>
              <div style={styles.collapsibleHeader}>
                <h2 style={styles.sectionTitle}>
                  Sample Tournament Simulation
                </h2>
                <button 
                  onClick={() => setShowSingleSim(false)} 
                  style={styles.closeButton}
                >
                  Hide
                </button>
              </div>
              
              <div style={{
                ...styles.championCard,
                backgroundColor: `${getTeamColor(singleSimulation.champion.name)}20` // 20 for opacity
              }}>
                <h3 style={{
                  ...styles.teamDetailTitle,
                  color: getTeamColor(singleSimulation.champion.name),
                  margin: 0
                }}>
                  Champion: {singleSimulation.champion.name} (Seed {singleSimulation.champion.seed})
                </h3>
              </div>
              
              <div>
                {singleSimulation.log
                  .filter(round => round.round !== "Tournament Start")
                  .map((round, roundIdx) => (
                    <div key={roundIdx} style={styles.roundContainer}>
                      <div style={styles.roundHeader}>
                        {round.round}
                      </div>
                      
                      {round.matchups.map((matchup, matchIdx) => (
                        <div 
                          key={matchIdx} 
                          style={styles.matchupContainer}
                        >
                          {matchup.isBye ? (
                            <div style={styles.teamNameA}>
                              <span style={{ 
                                fontWeight: 500, 
                                color: getTeamColor(matchup.teamA.name) 
                              }}>
                                {matchup.teamA.name} (Seed {matchup.teamA.seed})
                              </span>
                              <span style={{ color: '#888', marginLeft: '8px' }}>
                                - Bye
                              </span>
                            </div>
                          ) : (
                            <>
                              <div 
                                style={{
                                  ...styles.teamNameA,
                                  fontWeight: matchup.winner.name === matchup.teamA.name ? 700 : 400,
                                  color: matchup.winner.name === matchup.teamA.name 
                                    ? getTeamColor(matchup.teamA.name) 
                                    : '#888'
                                }}
                              >
                                {matchup.teamA.name} (Seed {matchup.teamA.seed})
                              </div>
                              
                              <div style={styles.vsLabel}>vs</div>
                              
                              <div 
                                style={{
                                  ...styles.teamNameB,
                                  fontWeight: matchup.winner.name === matchup.teamB.name ? 700 : 400,
                                  color: matchup.winner.name === matchup.teamB.name 
                                    ? getTeamColor(matchup.teamB.name) 
                                    : '#888'
                                }}
                              >
                                {matchup.teamB.name} (Seed {matchup.teamB.seed})
                              </div>
                              
                              <div 
                                style={{
                                  ...styles.winnerLabel,
                                  backgroundColor: `${getTeamColor(matchup.winner.name)}20`,
                                  color: getTeamColor(matchup.winner.name)
                                }}
                              >
                                Winner: {matchup.winner.name}
                              </div>
                            </>
                          )}
                        </div>
                      ))}
                    </div>
                  ))}
              </div>
            </div>
          )}
          
          <div style={styles.footer}>
            <p>
              This predictor uses team efficiency ratings and Monte Carlo simulation to project tournament outcomes.
              Team colors and data are for demonstration purposes.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SECTournamentPredictor;