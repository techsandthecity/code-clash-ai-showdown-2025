const fs = require("fs");
const csv = require("csv-parse/sync");

function generateSpread() {
  return Math.round((Math.random() * 14 + 1) * 10) / 10;
}

function updateTournament(csvFile) {
  const fileContent = fs.readFileSync(csvFile, "utf-8");
  const records = csv.parse(fileContent, { columns: true });
  const results = {};

  records.forEach((game) => {
    const gameNum = parseInt(game["Game Number"]);
    const team1 = game["Team 1"];
    const team2 = game["Team 2"];

    // First round games
    if (team1?.includes("No.") && team2?.includes("No.")) {
      const spread = generateSpread();
      const winner = Math.random() < 0.5 ? team1 : team2;
      results[gameNum] = { winner, spread };
    }
    // Subsequent rounds
    else {
      if (!team1 || !team2 || team1.includes("WG") || team2.includes("WG")) {
        const team1Actual = team1?.includes("WG")
          ? results[parseInt(team1.slice(2))]?.winner
          : team1;
        const team2Actual = team2?.includes("WG")
          ? results[parseInt(team2.slice(2))]?.winner
          : team2;

        if (team1Actual && team2Actual) {
          const spread = generateSpread();
          const winner = Math.random() < 0.5 ? team1Actual : team2Actual;
          results[gameNum] = { winner, spread };
        }
      }
    }
  });

  return results;
}

function displayResults(results) {
  console.log("\nTournament Results:");
  console.log("-".repeat(50));
  Object.entries(results).forEach(([gameNum, result]) => {
    console.log(`Game ${gameNum}:`);
    console.log(`Winner: ${result.winner}`);
    console.log(`Spread: ${result.spread} points`);
    console.log("-".repeat(50));
  });
}

const csvFile = "2025_sec_tournament_bracket.csv";
const results = updateTournament(csvFile);
displayResults(results);
