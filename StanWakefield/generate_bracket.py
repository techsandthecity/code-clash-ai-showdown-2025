#!/usr/bin/env python3
"""
SEC Basketball Championship Bracket Generator

This script generates a visual tournament bracket showing the winners of each round.
"""

import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
from sec_tournament_predictor import SECTournamentPredictor, SEC_TEAMS, FIRST_ROUND_MATCHUPS
from sec_tournament_predictor import SECOND_ROUND_TEAMS, QUARTERFINAL_TEAMS

class BracketGenerator:
    """Generate a visual tournament bracket."""
    
    def __init__(self):
        """Initialize the bracket generator."""
        self.predictor = SECTournamentPredictor(use_fallback=True)
        self.predictor.extract_data_from_images()
        self.predictor.initialize_elo_ratings()
        
        # Set a specific random seed for reproducibility
        random.seed(42)
        
        # Tournament structure
        self.first_round_matchups = FIRST_ROUND_MATCHUPS
        self.second_round_teams = SECOND_ROUND_TEAMS
        self.quarterfinal_teams = QUARTERFINAL_TEAMS
        
        # Store the simulation results
        self.first_round_winners = []
        self.second_round_winners = []
        self.quarterfinal_winners = []
        self.semifinal_winners = []
        self.champion = None
        
        # Colors
        self.colors = {
            'background': '#f5f5f5',
            'bracket_lines': '#555555',
            'text': '#222222',
            'first_round': '#6baed6',
            'second_round': '#4292c6',
            'quarterfinals': '#2171b5',
            'semifinals': '#084594',
            'champion': '#000000',
            'highlight': '#ff7f0e'
        }
    
    def simulate_tournament(self):
        """Simulate a single tournament run."""
        # First Round
        self.first_round_winners = []
        for matchup in self.first_round_matchups:
            winner = self.predictor.simulate_game(matchup[0], matchup[1])
            self.first_round_winners.append(winner)
        
        # Second Round
        second_round_matchups = list(zip(self.first_round_winners, self.second_round_teams))
        self.second_round_winners = []
        for matchup in second_round_matchups:
            winner = self.predictor.simulate_game(matchup[0], matchup[1])
            self.second_round_winners.append(winner)
        
        # Quarterfinals
        quarterfinal_matchups = list(zip(self.second_round_winners, self.quarterfinal_teams))
        self.quarterfinal_winners = []
        for matchup in quarterfinal_matchups:
            winner = self.predictor.simulate_game(matchup[0], matchup[1])
            self.quarterfinal_winners.append(winner)
        
        # Semifinals
        self.semifinal_winners = [
            self.predictor.simulate_game(self.quarterfinal_winners[0], self.quarterfinal_winners[1]),
            self.predictor.simulate_game(self.quarterfinal_winners[2], self.quarterfinal_winners[3])
        ]
        
        # Championship
        self.champion = self.predictor.simulate_game(self.semifinal_winners[0], self.semifinal_winners[1])
        
        return {
            'first_round': list(zip([t[0] for t in self.first_round_matchups], 
                                   [t[1] for t in self.first_round_matchups], 
                                   self.first_round_winners)),
            'second_round': list(zip(self.first_round_winners, 
                                    self.second_round_teams, 
                                    self.second_round_winners)),
            'quarterfinals': list(zip(self.second_round_winners, 
                                     self.quarterfinal_teams, 
                                     self.quarterfinal_winners)),
            'semifinals': list(zip([self.quarterfinal_winners[0], self.quarterfinal_winners[2]], 
                                  [self.quarterfinal_winners[1], self.quarterfinal_winners[3]], 
                                  self.semifinal_winners)),
            'championship': (self.semifinal_winners[0], self.semifinal_winners[1], self.champion)
        }
    
    def generate_bracket_image(self, output_path='sec_bracket.png'):
        """Generate a visual tournament bracket."""
        # Simulate the tournament
        results = self.simulate_tournament()
        
        # Create the figure and axis
        fig, ax = plt.subplots(figsize=(16, 16), facecolor=self.colors['background'])
        ax.set_facecolor(self.colors['background'])
        
        # Remove axis ticks and labels
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        # Title with enhanced style
        ax.set_title('2025 SEC Basketball Championship Bracket', fontsize=24, pad=20, 
                    color='#001F5B', weight='bold')
        
        # Add subtitle with predicted champion
        champion = results['championship'][2]
        ax.text(0.5, 0.985, f"Predicted Champion: {champion}", fontsize=16, 
                ha='center', va='top', color='#D63500', weight='bold')
        
        # Draw the bracket
        self._draw_bracket(ax, results)
        
        # Add a legend
        self._add_legend(ax)
        
        # Save the image
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Bracket image saved to {output_path}")
        
        return output_path
    
    def _draw_bracket(self, ax, results):
        """Draw the tournament bracket."""
        # Layout parameters
        margin_top = 0.05
        margin_bottom = 0.05
        margin_left = 0.05
        margin_right = 0.05
        
        # Calculate heights - increased spacing between matchups
        usable_height = 1.0 - margin_top - margin_bottom
        first_round_height = usable_height * 0.5  # Increased from 0.45
        second_round_height = usable_height * 0.3  # Increased from 0.25
        quarterfinal_height = usable_height * 0.2  # Increased from 0.15
        semifinal_height = usable_height * 0.15  # Increased from 0.1
        championship_height = usable_height * 0.05
        
        # X positions for each round
        first_round_x = margin_left
        second_round_x = first_round_x + 0.15
        quarterfinal_x = second_round_x + 0.15
        semifinal_x = quarterfinal_x + 0.15
        championship_x = semifinal_x + 0.15
        champion_x = championship_x + 0.15
        
        # Draw first round (4 matchups)
        first_round_y_positions = self._get_y_positions(margin_bottom, first_round_height, 4)
        for i, (team_a, team_b, winner) in enumerate(results['first_round']):
            y = first_round_y_positions[i]
            self._draw_matchup(ax, first_round_x, y, team_a, team_b, winner, self.colors['first_round'])
        
        # Draw second round (4 matchups)
        second_round_y_positions = self._get_y_positions(margin_bottom, second_round_height, 4)
        for i, (team_a, team_b, winner) in enumerate(results['second_round']):
            y = second_round_y_positions[i]
            self._draw_matchup(ax, second_round_x, y, team_a, team_b, winner, self.colors['second_round'])
            
            # Draw connector from first round to second round
            if i < len(first_round_y_positions):
                self._draw_connector(ax, first_round_x + 0.1, first_round_y_positions[i],
                                    second_round_x, y)
        
        # Draw quarterfinals (4 matchups)
        quarterfinal_y_positions = self._get_y_positions(margin_bottom, quarterfinal_height, 4)
        for i, (team_a, team_b, winner) in enumerate(results['quarterfinals']):
            y = quarterfinal_y_positions[i]
            self._draw_matchup(ax, quarterfinal_x, y, team_a, team_b, winner, self.colors['quarterfinals'])
            
            # Draw connector from second round to quarterfinals
            if i < len(second_round_y_positions):
                self._draw_connector(ax, second_round_x + 0.1, second_round_y_positions[i],
                                    quarterfinal_x, y)
        
        # Draw semifinals (2 matchups)
        semifinal_y_positions = self._get_y_positions(margin_bottom, semifinal_height, 2)
        for i, (team_a, team_b, winner) in enumerate(results['semifinals']):
            y = semifinal_y_positions[i]
            self._draw_matchup(ax, semifinal_x, y, team_a, team_b, winner, self.colors['semifinals'])
            
            # Draw connector from quarterfinals to semifinals
            if i == 0:  # First semifinal
                self._draw_connector(ax, quarterfinal_x + 0.1, quarterfinal_y_positions[0],
                                    semifinal_x, y)
                self._draw_connector(ax, quarterfinal_x + 0.1, quarterfinal_y_positions[1],
                                    semifinal_x, y)
            else:  # Second semifinal
                self._draw_connector(ax, quarterfinal_x + 0.1, quarterfinal_y_positions[2],
                                    semifinal_x, y)
                self._draw_connector(ax, quarterfinal_x + 0.1, quarterfinal_y_positions[3],
                                    semifinal_x, y)
        
        # Draw championship
        championship_y = margin_bottom + semifinal_height / 2
        team_a, team_b, winner = results['championship']
        self._draw_matchup(ax, championship_x, championship_y, team_a, team_b, winner, self.colors['champion'])
        
        # Draw connector from semifinals to championship
        self._draw_connector(ax, semifinal_x + 0.1, semifinal_y_positions[0],
                            championship_x, championship_y)
        self._draw_connector(ax, semifinal_x + 0.1, semifinal_y_positions[1],
                            championship_x, championship_y)
        
        # Draw champion
        self._draw_champion(ax, champion_x, championship_y, winner)
    
    def _get_y_positions(self, base_y, height, num_positions):
        """Calculate Y positions for matchups."""
        positions = []
        for i in range(num_positions):
            positions.append(base_y + height * (i + 0.5) / num_positions)
        return positions
    
    def _draw_matchup(self, ax, x, y, team_a, team_b, winner, color):
        """Draw a matchup box with team names."""
        # Draw the box - increased height
        rect = patches.Rectangle((x, y - 0.04), 0.1, 0.08, 
                                linewidth=1, edgecolor=self.colors['bracket_lines'],
                                facecolor=color, alpha=0.3)
        ax.add_patch(rect)
        
        # Draw team names - increased font size and spacing
        text_color_a = self.colors['highlight'] if team_a == winner else self.colors['text']
        text_color_b = self.colors['highlight'] if team_b == winner else self.colors['text']
        
        ax.text(x + 0.005, y + 0.015, team_a, fontsize=12, 
                color=text_color_a, ha='left', va='center')
        ax.text(x + 0.005, y - 0.015, team_b, fontsize=12, 
                color=text_color_b, ha='left', va='center')
        
        # Draw horizontal line between teams
        ax.plot([x, x + 0.1], [y, y], color=self.colors['bracket_lines'], linewidth=0.5)
    
    def _draw_connector(self, ax, x1, y1, x2, y2):
        """Draw a connector line between rounds."""
        ax.plot([x1, x1 + (x2 - x1) / 2, x2], [y1, y2, y2], 
                color=self.colors['bracket_lines'], linewidth=1)
    
    def _draw_champion(self, ax, x, y, team):
        """Draw the champion with a trophy icon."""
        champion_box = patches.Rectangle((x, y - 0.05), 0.15, 0.1, 
                                        linewidth=2, edgecolor=self.colors['highlight'],
                                        facecolor=self.colors['highlight'], alpha=0.2)
        ax.add_patch(champion_box)
        
        ax.text(x + 0.075, y + 0.025, "CHAMPION", fontsize=14, 
                color=self.colors['highlight'], ha='center', va='center', weight='bold')
        ax.text(x + 0.075, y - 0.025, team, fontsize=16, 
                color=self.colors['highlight'], ha='center', va='center', weight='bold')
    
    def _add_legend(self, ax):
        """Add a legend explaining the bracket."""
        # Add round labels at the top - increased font size
        ax.text(0.12, 0.97, "First Round", fontsize=14, ha='center', va='center')
        ax.text(0.27, 0.97, "Second Round", fontsize=14, ha='center', va='center')
        ax.text(0.42, 0.97, "Quarterfinals", fontsize=14, ha='center', va='center')
        ax.text(0.57, 0.97, "Semifinals", fontsize=14, ha='center', va='center')
        ax.text(0.72, 0.97, "Championship", fontsize=14, ha='center', va='center')
        
        # Add dates - increased font size
        ax.text(0.12, 0.94, "March 12", fontsize=12, ha='center', va='center', style='italic')
        ax.text(0.27, 0.94, "March 13", fontsize=12, ha='center', va='center', style='italic')
        ax.text(0.42, 0.94, "March 14", fontsize=12, ha='center', va='center', style='italic')
        ax.text(0.57, 0.94, "March 15", fontsize=12, ha='center', va='center', style='italic')
        ax.text(0.72, 0.94, "March 16", fontsize=12, ha='center', va='center', style='italic')
        
        # Add a note about the highlighted teams being winners - increased font size
        ax.text(0.5, 0.02, "Highlighted teams advance to the next round", 
                fontsize=12, ha='center', va='center', color=self.colors['highlight'])

def main():
    """Generate a bracket image."""
    generator = BracketGenerator()
    output_path = generator.generate_bracket_image()
    
    # Try to open the image
    if os.path.exists(output_path):
        try:
            import webbrowser
            webbrowser.open(f"file://{os.path.abspath(output_path)}")
        except Exception:
            print(f"Image saved to {output_path}")

if __name__ == "__main__":
    main() 