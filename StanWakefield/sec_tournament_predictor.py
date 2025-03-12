#!/usr/bin/env python3
"""
SEC Basketball Championship Predictor

This program predicts the winner of the 2025 SEC Basketball Championship
using statistical data from secsports.com and an Elo rating system.
"""

import os
import numpy as np
import pandas as pd
from PIL import Image
import pytesseract
import re
import random
from tqdm import tqdm
import matplotlib.pyplot as plt
import argparse
import sys

# Import fallback data
try:
    from fallback_data import FALLBACK_TEAM_STATS
except ImportError:
    FALLBACK_TEAM_STATS = {}

# Constants
ITERATIONS = 10000
SEC_TEAMS = [
    "Alabama", "Arkansas", "Auburn", "Florida", 
    "Georgia", "Kentucky", "LSU", "Mississippi State",
    "Missouri", "Oklahoma", "Ole Miss", "South Carolina", 
    "Tennessee", "Texas", "Texas A&M", "Vanderbilt"
]

# First round matchups (March 12th)
FIRST_ROUND_MATCHUPS = [
    ("South Carolina", "Arkansas"),
    ("Texas", "Vanderbilt"),
    ("LSU", "Mississippi State"),
    ("Oklahoma", "Georgia")
]

# Teams waiting in the second round (March 13th)
SECOND_ROUND_TEAMS = ["Ole Miss", "Texas A&M", "Missouri", "Kentucky"]

# Teams waiting in the quarterfinals (March 14th)
QUARTERFINAL_TEAMS = ["Auburn", "Tennessee", "Florida", "Alabama"]

class SECTournamentPredictor:
    def __init__(self, stats_folder="stats", use_fallback=False):
        """Initialize the predictor with the path to the stats folder."""
        self.stats_folder = stats_folder
        self.use_fallback = use_fallback
        self.team_stats = {team: {} for team in SEC_TEAMS}
        self.elo_ratings = {}
        self.championship_counts = {team: 0 for team in SEC_TEAMS}
        
    def extract_data_from_images(self):
        """Extract team statistics from screenshots using OCR."""
        if self.use_fallback:
            print("Using fallback data instead of OCR extraction.")
            if not FALLBACK_TEAM_STATS:
                print("Error: Fallback data not available. Make sure fallback_data.py exists.")
                sys.exit(1)
            self.team_stats = FALLBACK_TEAM_STATS.copy()
            return self.team_stats
            
        print("Extracting data from images...")
        
        # Check if stats folder exists
        if not os.path.exists(self.stats_folder):
            print(f"Warning: Stats folder '{self.stats_folder}' not found.")
            print("Using fallback data instead.")
            if FALLBACK_TEAM_STATS:
                self.team_stats = FALLBACK_TEAM_STATS.copy()
                return self.team_stats
            else:
                print("Error: Fallback data not available. Make sure fallback_data.py exists.")
                sys.exit(1)
        
        # Process each image in the stats folder
        png_files = [f for f in os.listdir(self.stats_folder) if f.endswith(".png")]
        if not png_files:
            print(f"Warning: No PNG files found in '{self.stats_folder}' folder.")
            print("Using fallback data instead.")
            if FALLBACK_TEAM_STATS:
                self.team_stats = FALLBACK_TEAM_STATS.copy()
                return self.team_stats
            else:
                print("Error: Fallback data not available. Make sure fallback_data.py exists.")
                sys.exit(1)
        
        for filename in png_files:
            image_path = os.path.join(self.stats_folder, filename)
            self._process_image(image_path, filename)
                
        print("Data extraction complete.")
        
        # Fill in any missing values with averages or fallback data
        self._handle_missing_values()
        
        # Check if we got enough data
        stats_count = sum(len(stats) for team, stats in self.team_stats.items())
        if stats_count < len(SEC_TEAMS) * 5:  # At least 5 stats per team
            print("Warning: Not enough data extracted from images.")
            print("Using fallback data instead.")
            if FALLBACK_TEAM_STATS:
                self.team_stats = FALLBACK_TEAM_STATS.copy()
            else:
                print("Error: Fallback data not available. Make sure fallback_data.py exists.")
                sys.exit(1)
        
        return self.team_stats
    
    def _process_image(self, image_path, filename):
        """Process an individual image to extract team statistics."""
        print(f"Processing image: {filename}")
        
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            
            # Extract relevant statistics based on the filename
            if "offense-defense" in filename:
                self._parse_offense_defense_stats(text)
            elif "field-goal-percentage" in filename:
                self._parse_field_goal_stats(text)
            elif "3-point-field-goals" in filename:
                self._parse_3point_stats(text)
            elif "free-throw-percentage" in filename:
                self._parse_free_throw_stats(text)
            elif "combined-team-rebounds" in filename:
                self._parse_rebound_stats(text)
            elif "turnovers" in filename:
                self._parse_turnover_stats(text)
            elif "blocked-shots-and-assists" in filename:
                self._parse_blocks_assists_stats(text)
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    def _match_team_name(self, name):
        """Match a team name from OCR text to the official team name."""
        name = name.strip()
        
        # Direct match
        if name in SEC_TEAMS:
            return name
        
        # Handle common OCR errors or abbreviated names
        name_map = {
            "Miss": "Ole Miss",
            "Mississippi": "Ole Miss",
            "Texas AM": "Texas A&M",
            "Miss State": "Mississippi State",
            "Mississippi St": "Mississippi State",
            "Miss St": "Mississippi State",
            "Missisippi": "Mississippi State",
            "Ole Miss State": "Mississippi State",
            "Ole Miss Mississippi": "Ole Miss",
            "S Carolina": "South Carolina",
            "So Carolina": "South Carolina"
        }
        
        if name in name_map:
            return name_map[name]
        
        # Try to find closest match
        for team in SEC_TEAMS:
            if team.lower() in name.lower() or name.lower() in team.lower():
                return team
        
        return None  # No match found
    
    def _parse_offense_defense_stats(self, text):
        """Parse scoring offense and defense stats."""
        lines = text.strip().split('\n')
        
        # Regular expression to match team name and two numeric values
        pattern = r'([A-Za-z]+(?:\s+[A-Za-z&]+)*)\s+(\d+\.\d+)\s+(\d+\.\d+)'
        
        for line in lines:
            match = re.search(pattern, line)
            if match:
                team_name = match.group(1)
                offense = float(match.group(2))
                defense = float(match.group(3))
                
                team = self._match_team_name(team_name)
                if team:
                    self.team_stats[team]['scoring_offense'] = offense
                    self.team_stats[team]['scoring_defense'] = defense
    
    def _parse_field_goal_stats(self, text):
        """Parse field goal percentage stats."""
        lines = text.strip().split('\n')
        
        # Pattern to match team name and field goal percentage
        pattern = r'([A-Za-z]+(?:\s+[A-Za-z&]+)*)\s+(\d+\.\d+)'
        
        for line in lines:
            match = re.search(pattern, line)
            if match:
                team_name = match.group(1)
                fg_pct = float(match.group(2))
                
                team = self._match_team_name(team_name)
                if team:
                    self.team_stats[team]['field_goal_pct'] = fg_pct
    
    def _parse_3point_stats(self, text):
        """Parse 3-point field goal stats."""
        lines = text.strip().split('\n')
        
        # Pattern to match team name, 3-point makes per game, and percentage
        pattern = r'([A-Za-z]+(?:\s+[A-Za-z&]+)*)\s+(\d+\.\d+)\s+(\d+\.\d+)'
        
        for line in lines:
            match = re.search(pattern, line)
            if match:
                team_name = match.group(1)
                threes_made = float(match.group(2))
                three_pt_pct = float(match.group(3))
                
                team = self._match_team_name(team_name)
                if team:
                    self.team_stats[team]['three_pt_made'] = threes_made
                    self.team_stats[team]['three_pt_pct'] = three_pt_pct
    
    def _parse_free_throw_stats(self, text):
        """Parse free throw percentage stats."""
        lines = text.strip().split('\n')
        
        # Pattern to match team name and free throw percentage
        pattern = r'([A-Za-z]+(?:\s+[A-Za-z&]+)*)\s+(\d+\.\d+)'
        
        for line in lines:
            match = re.search(pattern, line)
            if match:
                team_name = match.group(1)
                ft_pct = float(match.group(2))
                
                team = self._match_team_name(team_name)
                if team:
                    self.team_stats[team]['free_throw_pct'] = ft_pct
    
    def _parse_rebound_stats(self, text):
        """Parse rebounding stats."""
        lines = text.strip().split('\n')
        
        # Pattern to match team name and rebounds per game
        pattern = r'([A-Za-z]+(?:\s+[A-Za-z&]+)*)\s+(\d+\.\d+)'
        
        for line in lines:
            match = re.search(pattern, line)
            if match:
                team_name = match.group(1)
                rebounds = float(match.group(2))
                
                team = self._match_team_name(team_name)
                if team:
                    self.team_stats[team]['rebounds'] = rebounds
    
    def _parse_turnover_stats(self, text):
        """Parse turnover stats."""
        lines = text.strip().split('\n')
        
        # Pattern to match team name and turnovers per game
        pattern = r'([A-Za-z]+(?:\s+[A-Za-z&]+)*)\s+(\d+\.\d+)'
        
        for line in lines:
            match = re.search(pattern, line)
            if match:
                team_name = match.group(1)
                turnovers = float(match.group(2))
                
                team = self._match_team_name(team_name)
                if team:
                    self.team_stats[team]['turnovers'] = turnovers
    
    def _parse_blocks_assists_stats(self, text):
        """Parse blocked shots and assists stats."""
        lines = text.strip().split('\n')
        
        # Pattern to match team name, blocks, and assists
        pattern = r'([A-Za-z]+(?:\s+[A-Za-z&]+)*)\s+(\d+\.\d+)\s+(\d+\.\d+)'
        
        for line in lines:
            match = re.search(pattern, line)
            if match:
                team_name = match.group(1)
                blocks = float(match.group(2))
                assists = float(match.group(3))
                
                team = self._match_team_name(team_name)
                if team:
                    self.team_stats[team]['blocks'] = blocks
                    self.team_stats[team]['assists'] = assists
    
    def _handle_missing_values(self):
        """Handle missing values by filling with averages."""
        stats_fields = [
            'scoring_offense', 'scoring_defense', 'field_goal_pct',
            'three_pt_made', 'three_pt_pct', 'free_throw_pct',
            'rebounds', 'turnovers', 'blocks', 'assists'
        ]
        
        # Calculate averages for each stat
        averages = {}
        for field in stats_fields:
            values = [team_stats[field] for team_stats in self.team_stats.values() 
                     if field in team_stats]
            if values:
                averages[field] = sum(values) / len(values)
            else:
                averages[field] = 0.0
        
        # Fill missing values with averages
        for team in SEC_TEAMS:
            for field in stats_fields:
                if field not in self.team_stats[team]:
                    # Try to get from fallback data first
                    if FALLBACK_TEAM_STATS and team in FALLBACK_TEAM_STATS and field in FALLBACK_TEAM_STATS[team]:
                        self.team_stats[team][field] = FALLBACK_TEAM_STATS[team][field]
                    else:
                        self.team_stats[team][field] = averages[field]
    
    def initialize_elo_ratings(self):
        """Initialize Elo ratings for each team based on their stats."""
        print("Initializing Elo ratings...")
        
        # Base Elo rating
        base_elo = 1500
        
        # Calculate initial Elo ratings based on team stats
        for team in SEC_TEAMS:
            team_stats = self.team_stats[team]
            
            # Create a composite score using a weighted formula
            offense_score = team_stats.get('scoring_offense', 0) * 3
            defense_score = -team_stats.get('scoring_defense', 0) * 2  # Lower is better
            shooting_score = (
                team_stats.get('field_goal_pct', 0) * 100 + 
                team_stats.get('three_pt_pct', 0) * 50 +
                team_stats.get('free_throw_pct', 0) * 30
            )
            efficiency_score = (
                team_stats.get('rebounds', 0) * 1.5 +
                team_stats.get('assists', 0) * 1.0 -
                team_stats.get('turnovers', 0) * 2.0 +
                team_stats.get('blocks', 0) * 1.0
            )
            
            # Calculate the final rating
            self.elo_ratings[team] = base_elo + offense_score + defense_score + shooting_score + efficiency_score
        
        # Normalize ratings to avoid extreme values
        min_rating = min(self.elo_ratings.values())
        max_rating = max(self.elo_ratings.values())
        
        for team in SEC_TEAMS:
            normalized = 1400 + (self.elo_ratings[team] - min_rating) * (600 / (max_rating - min_rating))
            self.elo_ratings[team] = normalized
        
        print("Elo ratings initialized:")
        for team, rating in sorted(self.elo_ratings.items(), key=lambda x: x[1], reverse=True):
            print(f"{team:<20}: {rating:.1f}")
        
        return self.elo_ratings
    
    def calculate_win_probability(self, team_a, team_b):
        """Calculate the probability of team_a beating team_b using Elo ratings."""
        elo_a = self.elo_ratings.get(team_a, 1500)
        elo_b = self.elo_ratings.get(team_b, 1500)
        
        # Elo formula for win probability
        exponent = (elo_b - elo_a) / 400.0
        return 1.0 / (1.0 + 10.0 ** exponent)
    
    def simulate_game(self, team_a, team_b):
        """Simulate a game between two teams and return the winner."""
        prob_a_wins = self.calculate_win_probability(team_a, team_b)
        return team_a if random.random() < prob_a_wins else team_b
    
    def simulate_tournament(self):
        """Simulate the entire SEC tournament once."""
        # First Round (March 12th) - Seeds 9-16
        first_round_winners = []
        for matchup in FIRST_ROUND_MATCHUPS:
            winner = self.simulate_game(matchup[0], matchup[1])
            first_round_winners.append(winner)
        
        # Second Round (March 13th)
        second_round_matchups = list(zip(first_round_winners, SECOND_ROUND_TEAMS))
        second_round_winners = []
        for matchup in second_round_matchups:
            winner = self.simulate_game(matchup[0], matchup[1])
            second_round_winners.append(winner)
        
        # Quarterfinals (March 14th)
        quarterfinal_matchups = list(zip(second_round_winners, QUARTERFINAL_TEAMS))
        quarterfinal_winners = []
        for matchup in quarterfinal_matchups:
            winner = self.simulate_game(matchup[0], matchup[1])
            quarterfinal_winners.append(winner)
        
        # Semifinals (March 15th)
        semifinal_1_winner = self.simulate_game(quarterfinal_winners[0], quarterfinal_winners[1])
        semifinal_2_winner = self.simulate_game(quarterfinal_winners[2], quarterfinal_winners[3])
        
        # Championship (March 16th)
        champion = self.simulate_game(semifinal_1_winner, semifinal_2_winner)
        
        return champion
    
    def run_simulation(self, iterations=ITERATIONS):
        """Run multiple iterations of tournament simulation."""
        print(f"Running {iterations} tournament simulations...")
        
        for _ in tqdm(range(iterations)):
            champion = self.simulate_tournament()
            self.championship_counts[champion] += 1
        
        print("Simulations complete.")
        return self.championship_counts
    
    def get_championship_probabilities(self):
        """Calculate championship probabilities for each team."""
        total_simulations = sum(self.championship_counts.values())
        probabilities = {team: count / total_simulations 
                        for team, count in self.championship_counts.items()}
        
        # Sort teams by probability in descending order
        sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_probs
    
    def display_results(self):
        """Display the simulation results."""
        probs = self.get_championship_probabilities()
        
        print("\n2025 SEC Basketball Championship Prediction Results:")
        print("==================================================")
        print(f"Based on {ITERATIONS} simulations\n")
        
        print("Championship Probabilities:")
        for i, (team, prob) in enumerate(probs, 1):
            print(f"{i}. {team}: {prob:.1%}")
        
        predicted_winner = probs[0][0]
        print(f"\nPredicted Champion: {predicted_winner} ({probs[0][1]:.1%})")
        
        # Create a bar chart of the results
        self._plot_results(probs)
        
    def _plot_results(self, probabilities):
        """Create and save a visualization of the results."""
        teams = [team for team, _ in probabilities]
        probs = [prob for _, prob in probabilities]
        
        plt.figure(figsize=(12, 8))
        bars = plt.bar(teams, probs)
        plt.xticks(rotation=45, ha='right')
        plt.ylabel('Championship Probability')
        plt.title('2025 SEC Basketball Championship Prediction')
        
        # Add percentage labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{height:.1%}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('sec_championship_prediction.png')
        print("Results visualization saved to 'sec_championship_prediction.png'")

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description='SEC Basketball Tournament Predictor')
    parser.add_argument('--stats', default='stats', help='Path to the folder containing stat images')
    parser.add_argument('--iterations', type=int, default=ITERATIONS, 
                        help=f'Number of simulation iterations (default: {ITERATIONS})')
    parser.add_argument('--fallback', action='store_true', 
                        help='Use fallback data instead of OCR extraction')
    args = parser.parse_args()
    
    predictor = SECTournamentPredictor(stats_folder=args.stats, use_fallback=args.fallback)
    predictor.extract_data_from_images()
    predictor.initialize_elo_ratings()
    predictor.run_simulation(iterations=args.iterations)
    predictor.display_results()

if __name__ == "__main__":
    main() 