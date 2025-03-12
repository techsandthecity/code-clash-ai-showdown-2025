#!/usr/bin/env python3
"""
Fallback data for the SEC Basketball Tournament Predictor.

This module provides manually entered statistics that can be used
if the OCR extraction from images fails or produces incomplete data.
"""

# Fallback data based on approximations of the 2024-2025 season
# These are placeholder values and would be replaced with actual statistics
# from the images in real implementation

FALLBACK_TEAM_STATS = {
    "Alabama": {
        "scoring_offense": 83.5,
        "scoring_defense": 70.1,
        "field_goal_pct": 0.465,
        "three_pt_made": 10.2,
        "three_pt_pct": 0.362,
        "free_throw_pct": 0.735,
        "rebounds": 38.2,
        "assists": 15.4,
        "blocks": 4.8,
        "turnovers": 11.9
    },
    "Arkansas": {
        "scoring_offense": 75.2,
        "scoring_defense": 74.8,
        "field_goal_pct": 0.438,
        "three_pt_made": 7.5,
        "three_pt_pct": 0.331,
        "free_throw_pct": 0.705,
        "rebounds": 36.4,
        "assists": 13.7,
        "blocks": 3.9,
        "turnovers": 12.7
    },
    "Auburn": {
        "scoring_offense": 81.5,
        "scoring_defense": 66.3,
        "field_goal_pct": 0.472,
        "three_pt_made": 8.8,
        "three_pt_pct": 0.354,
        "free_throw_pct": 0.722,
        "rebounds": 39.6,
        "assists": 16.2,
        "blocks": 5.3,
        "turnovers": 10.8
    },
    "Florida": {
        "scoring_offense": 80.3,
        "scoring_defense": 70.9,
        "field_goal_pct": 0.457,
        "three_pt_made": 8.3,
        "three_pt_pct": 0.347,
        "free_throw_pct": 0.728,
        "rebounds": 37.8,
        "assists": 14.9,
        "blocks": 4.5,
        "turnovers": 11.5
    },
    "Georgia": {
        "scoring_offense": 74.8,
        "scoring_defense": 75.4,
        "field_goal_pct": 0.432,
        "three_pt_made": 7.1,
        "three_pt_pct": 0.327,
        "free_throw_pct": 0.698,
        "rebounds": 35.9,
        "assists": 13.2,
        "blocks": 3.7,
        "turnovers": 13.1
    },
    "Kentucky": {
        "scoring_offense": 79.4,
        "scoring_defense": 72.3,
        "field_goal_pct": 0.451,
        "three_pt_made": 7.8,
        "three_pt_pct": 0.338,
        "free_throw_pct": 0.715,
        "rebounds": 37.2,
        "assists": 14.3,
        "blocks": 4.2,
        "turnovers": 12.0
    },
    "LSU": {
        "scoring_offense": 73.5,
        "scoring_defense": 74.6,
        "field_goal_pct": 0.435,
        "three_pt_made": 7.3,
        "three_pt_pct": 0.325,
        "free_throw_pct": 0.702,
        "rebounds": 36.1,
        "assists": 12.9,
        "blocks": 3.8,
        "turnovers": 13.0
    },
    "Mississippi State": {
        "scoring_offense": 72.8,
        "scoring_defense": 73.9,
        "field_goal_pct": 0.433,
        "three_pt_made": 7.0,
        "three_pt_pct": 0.322,
        "free_throw_pct": 0.695,
        "rebounds": 36.0,
        "assists": 12.7,
        "blocks": 3.6,
        "turnovers": 13.2
    },
    "Missouri": {
        "scoring_offense": 76.8,
        "scoring_defense": 73.5,
        "field_goal_pct": 0.442,
        "three_pt_made": 7.6,
        "three_pt_pct": 0.335,
        "free_throw_pct": 0.708,
        "rebounds": 36.7,
        "assists": 13.9,
        "blocks": 4.0,
        "turnovers": 12.4
    },
    "Oklahoma": {
        "scoring_offense": 72.4,
        "scoring_defense": 74.2,
        "field_goal_pct": 0.430,
        "three_pt_made": 6.9,
        "three_pt_pct": 0.320,
        "free_throw_pct": 0.692,
        "rebounds": 35.8,
        "assists": 12.5,
        "blocks": 3.5,
        "turnovers": 13.3
    },
    "Ole Miss": {
        "scoring_offense": 76.5,
        "scoring_defense": 73.1,
        "field_goal_pct": 0.440,
        "three_pt_made": 7.5,
        "three_pt_pct": 0.332,
        "free_throw_pct": 0.707,
        "rebounds": 36.6,
        "assists": 13.8,
        "blocks": 3.9,
        "turnovers": 12.5
    },
    "South Carolina": {
        "scoring_offense": 73.0,
        "scoring_defense": 74.0,
        "field_goal_pct": 0.434,
        "three_pt_made": 7.1,
        "three_pt_pct": 0.323,
        "free_throw_pct": 0.697,
        "rebounds": 36.0,
        "assists": 12.8,
        "blocks": 3.7,
        "turnovers": 13.1
    },
    "Tennessee": {
        "scoring_offense": 79.8,
        "scoring_defense": 67.5,
        "field_goal_pct": 0.455,
        "three_pt_made": 8.0,
        "three_pt_pct": 0.342,
        "free_throw_pct": 0.718,
        "rebounds": 38.5,
        "assists": 15.0,
        "blocks": 4.7,
        "turnovers": 11.2
    },
    "Texas": {
        "scoring_offense": 73.2,
        "scoring_defense": 74.1,
        "field_goal_pct": 0.435,
        "three_pt_made": 7.2,
        "three_pt_pct": 0.324,
        "free_throw_pct": 0.698,
        "rebounds": 36.2,
        "assists": 12.9,
        "blocks": 3.8,
        "turnovers": 13.0
    },
    "Texas A&M": {
        "scoring_offense": 78.5,
        "scoring_defense": 71.8,
        "field_goal_pct": 0.447,
        "three_pt_made": 7.7,
        "three_pt_pct": 0.336,
        "free_throw_pct": 0.712,
        "rebounds": 37.0,
        "assists": 14.1,
        "blocks": 4.1,
        "turnovers": 12.2
    },
    "Vanderbilt": {
        "scoring_offense": 72.6,
        "scoring_defense": 74.5,
        "field_goal_pct": 0.431,
        "three_pt_made": 7.0,
        "three_pt_pct": 0.321,
        "free_throw_pct": 0.694,
        "rebounds": 35.9,
        "assists": 12.6,
        "blocks": 3.6,
        "turnovers": 13.2
    }
} 