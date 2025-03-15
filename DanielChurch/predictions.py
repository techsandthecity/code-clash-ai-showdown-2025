import os
import openai
import pandas as pd
import random
from typing import List, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# SEC Mascots dictionary for easy lookup
SEC_MASCOTS = {
    "Alabama": "Crimson Tide (Elephant)",
    "Arkansas": "Razorbacks (Wild Hog)",
    "Auburn": "Tigers (War Eagle)",
    "Florida": "Gators",
    "Georgia": "Bulldogs",
    "Kentucky": "Wildcats",
    "LSU": "Tigers",
    "Mississippi State": "Bulldogs",
    "Missouri": "Tigers",
    "Ole Miss": "Rebels (Bear)",
    "South Carolina": "Gamecocks",
    "Tennessee": "Volunteers (Smokey the Hound)",
    "Texas A&M": "Aggies (Rough Collie)",
    "Vanderbilt": "Commodores (Anchor)"
}

def flip_coin(team1: str, team2: str) -> str:
    """
    Randomly choose between two teams to break a tie.
    """
    winner = random.choice([team1, team2])
    print(f"🎲 Tie breaker - Coin flip: {winner} wins!")
    return winner

def get_battle_winner(team1: str, team2: str) -> str:
    """
    Use OpenAI API to determine which mascot would win in a fight.
    If the response isn't clearly one of the two schools, use a coin flip.
    """
    mascot1 = SEC_MASCOTS[team1]
    mascot2 = SEC_MASCOTS[team2]
    
    prompt = f"""In a hypothetical battle between {mascot1} (from {team1}) and {mascot2} (from {team2}), 
    which would win in a fight? Consider the natural abilities, size, and strength of each mascot. 
    Respond with ONLY the name of the winner's school: {team1} or {team2}."""

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a battle analysis expert determining the winner of mascot fights."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50
    )
    
    result = response.choices[0].message.content.strip()
    
    # If the response isn't exactly one of the team names, it's considered a tie
    if result not in [team1, team2]:
        print(f"⚔️ Battle resulted in a tie between {team1} and {team2}!")
        return flip_coin(team1, team2)
    
    return result

def update_bracket(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process each round of the tournament and update the bracket.
    """
    max_round = df['Round'].max()
    
    for current_round in range(1, max_round + 1):
        round_games = df[df['Round'] == current_round]
        
        for _, game in round_games.iterrows():
            # Skip if we've already processed this game
            if pd.notna(game['Winner']):
                continue
                
            # Skip if we don't have both teams yet
            if pd.isna(game['Team1']) or pd.isna(game['Team2']):
                continue
                
            # Print the matchup
            print(f"\nRound {current_round}, Game {game['Game']}:")
            print(f"{game['Team1']} ({SEC_MASCOTS[game['Team1']]}) vs {game['Team2']} ({SEC_MASCOTS[game['Team2']]})")
            
            # Get the winner
            winner = get_battle_winner(game['Team1'], game['Team2'])
            
            # Update the winner in the dataframe
            df.loc[(df['Round'] == current_round) & (df['Game'] == game['Game']), 'Winner'] = winner
            
            # Update the next round's matchup
            if current_round < max_round:
                next_game = (game['Game'] - 1) // 2 + len(df[df['Round'] == 1]) + 1
                next_position = 'Team1' if game['Game'] % 2 == 1 else 'Team2'
                df.loc[(df['Game'] == next_game), next_position] = winner
            
            # Print the final result
            print(f"Winner: {winner} ({SEC_MASCOTS[winner]})")
            print("-" * 50)
            
    return df

def run_tournament():
    """
    Run the tournament using the bracket CSV file.
    """
    # Read the bracket
    df = pd.read_csv('2025_sec_tournament_bracket.csv')
    
    print("SEC Mascot Battle Tournament")
    print("=" * 50)
    
    # Update the bracket
    df = update_bracket(df)
    
    # Save the updated bracket
    df.to_csv('2025_sec_tournament_bracket.csv', index=False)
    
    # Print the champion
    if pd.notna(df.loc[df['Round'] == df['Round'].max(), 'Winner'].iloc[0]):
        champion = df.loc[df['Round'] == df['Round'].max(), 'Winner'].iloc[0]
        print(f"\n🏆 Tournament Champion 🏆")
        print(f"{champion} ({SEC_MASCOTS[champion]})")

if __name__ == "__main__":
    # Set random seed for reproducibility of coin flips
    random.seed(2025)
    run_tournament()