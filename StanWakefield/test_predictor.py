#!/usr/bin/env python3
"""
Test script for the SEC Tournament Predictor.

This script tests the core functionality of the SEC Tournament Predictor
without running the full simulation.
"""

import os
from sec_tournament_predictor import SECTournamentPredictor, SEC_TEAMS

def test_data_extraction():
    """Test the data extraction from images."""
    print("Testing data extraction...")
    
    predictor = SECTournamentPredictor()
    
    # Check if stats folder exists
    if not os.path.exists("stats"):
        print("Warning: 'stats' folder not found. Create it and add stat images.")
        return False
    
    # Check if there are PNG files in the stats folder
    png_files = [f for f in os.listdir("stats") if f.endswith(".png")]
    if not png_files:
        print("Warning: No PNG files found in the 'stats' folder.")
        return False
    
    # Test extraction
    team_stats = predictor.extract_data_from_images()
    
    # Check if stats were extracted for each team
    stats_count = sum(len(stats) for stats in team_stats.values())
    print(f"Extracted {stats_count} total statistics for {len(team_stats)} teams.")
    
    return stats_count > 0

def test_elo_rating_initialization():
    """Test the initialization of Elo ratings."""
    print("\nTesting Elo rating initialization...")
    
    predictor = SECTournamentPredictor()
    predictor.extract_data_from_images()
    
    # Initialize Elo ratings
    elo_ratings = predictor.initialize_elo_ratings()
    
    # Check if all teams have Elo ratings
    missing_ratings = [team for team in SEC_TEAMS if team not in elo_ratings]
    
    if missing_ratings:
        print(f"Warning: Missing Elo ratings for: {', '.join(missing_ratings)}")
        return False
    
    # Check if Elo ratings are within a reasonable range
    for team, rating in elo_ratings.items():
        if rating < 1000 or rating > 2500:
            print(f"Warning: Unreasonable Elo rating for {team}: {rating}")
            return False
    
    return True

def test_game_simulation():
    """Test the game simulation functionality."""
    print("\nTesting game simulation...")
    
    predictor = SECTournamentPredictor()
    predictor.extract_data_from_images()
    predictor.initialize_elo_ratings()
    
    # Test simulating a sample game
    team_a = "Tennessee"
    team_b = "Georgia"
    
    print(f"Simulating a test game: {team_a} vs {team_b}")
    # Test win probability calculation
    prob_a_wins = predictor.calculate_win_probability(team_a, team_b)
    print(f"Probability of {team_a} winning: {prob_a_wins:.2%}")
    
    # Run multiple simulations to check consistency
    wins_a = 0
    trials = 1000
    
    for _ in range(trials):
        winner = predictor.simulate_game(team_a, team_b)
        if winner == team_a:
            wins_a += 1
    
    empirical_prob = wins_a / trials
    print(f"Empirical probability from {trials} simulations: {empirical_prob:.2%}")
    
    # Check if empirical probability is close to calculated probability
    if abs(empirical_prob - prob_a_wins) > 0.1:
        print("Warning: Large difference between calculated and empirical probabilities.")
        return False
    
    return True

def test_tournament_simulation():
    """Test a single tournament simulation."""
    print("\nTesting tournament simulation...")
    
    predictor = SECTournamentPredictor()
    predictor.extract_data_from_images()
    predictor.initialize_elo_ratings()
    
    # Simulate a single tournament
    champion = predictor.simulate_tournament()
    print(f"Simulated tournament champion: {champion}")
    
    return champion in SEC_TEAMS

def main():
    """Run all tests."""
    print("SEC Tournament Predictor Test Suite")
    print("==================================")
    
    tests = [
        test_data_extraction,
        test_elo_rating_initialization,
        test_game_simulation,
        test_tournament_simulation
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\nTest Results Summary:")
    print("====================")
    for i, (test, result) in enumerate(zip(tests, results), 1):
        print(f"{i}. {test.__name__}: {'PASS' if result else 'FAIL'}")
    
    overall = all(results)
    print(f"\nOverall Test Result: {'PASS' if overall else 'FAIL'}")
    
    return overall

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 