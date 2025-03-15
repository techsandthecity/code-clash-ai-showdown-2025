import requests
import pandas as pd
from datetime import datetime

# SEC Schools as of 2025 realignment
SEC_SCHOOLS = {
    'Alabama': 333,
    'Arkansas': 8,
    'Auburn': 2,
    'Florida': 57,
    'Georgia': 61,
    'Kentucky': 96,
    'LSU': 99,
    'Mississippi State': 344,
    'Missouri': 142,
    'Oklahoma': 201,    # New addition
    'Ole Miss': 145,
    'South Carolina': 2579,
    'Tennessee': 2633,
    'Texas': 251,       # New addition
    'Texas A&M': 245,
    'Vanderbilt': 238
}

def get_team_stats(team_id):
    """
    Fetch team statistics from ESPN API
    """
    # Using the seasons endpoint to get current season records
    base_url = f"http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/{team_id}/schedule"
    
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        data = response.json()
        
        # Get overall record from the events data
        events = data.get('events', [])
        wins = 0
        losses = 0
        
        for event in events:
            if event.get('completed', False):
                competitions = event.get('competitions', [])
                if competitions:
                    for team in competitions[0].get('competitors', []):
                        if str(team.get('id')) == str(team_id):
                            if team.get('winner', False):
                                wins += 1
                            else:
                                losses += 1
        
        return {'wins': wins, 'losses': losses}
    
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def main():
    all_teams_data = []
    
    for school, team_id in SEC_SCHOOLS.items():
        print(f"Fetching data for {school}...")
        team_data = get_team_stats(team_id)
        
        if team_data:
            team_stats = {
                'School': school,
                'Team ID': team_id,
                'Conference': 'SEC',
                'Wins': team_data.get('team', {}).get('record', {}).get('items', [{}])[0].get('stats', [{}])[0].get('value', 0),
                'Losses': team_data.get('team', {}).get('record', {}).get('items', [{}])[0].get('stats', [{}])[1].get('value', 0),
                'Last Updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            all_teams_data.append(team_stats)
    
    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(all_teams_data)
    print("\nCurrent SEC Basketball Records:")
    print(df.to_string(index=False))
    df.to_csv('sec_basketball_stats.csv', index=False)
    print("\nData has been saved to 'sec_basketball_stats.csv'")

if __name__ == "__main__":
    main()