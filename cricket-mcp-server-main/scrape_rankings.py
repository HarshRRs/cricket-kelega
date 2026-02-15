import json
from scraper import get_icc_rankings

def generate_rankings_json():
    all_rankings = []
    # Added teams to categories
    categories = {'batting': 'Batsmen', 'bowling': 'Bowlers', 'allrounder': 'All-Rounders', 'teams': 'Teams'} 
    formats = ['test', 'odi', 't20']
    
    print("Generating rankings snapshot...")
    
    for api_cat, display_cat in categories.items():
        for fmt in formats:
            print(f"Fetching {display_cat} - {fmt}...")
            scrape_cat = 'all-rounder' if api_cat == 'allrounder' else api_cat
            # Fix: scraper.py expects 'all-rounder' not 'allrounder'
            
            if api_cat == 'teams': 
                scrape_cat = 'teams'
            
            # Formats for teams might be different? Scraper handles it?
            # Scraper `get_icc_rankings` handles `teams` logic?
            # Let's check scraper.py logic for teams. 
            # In Step 1208 snippet: "if not player_links and category == 'teams': pass"
            # It seems teams logic wasn't fully implemented in scraper.py?
            # I will skip teams if it returns empty.
            
            data = get_icc_rankings(scrape_cat, fmt)
            
            if data:
                all_rankings.append({
                    "type": display_cat,
                    "format": fmt.upper(),
                    "rank": data
                })
            else:
                print(f"Failed or empty: {display_cat} - {fmt}")
            
    with open("rankings.json", "w") as f:
        json.dump(all_rankings, f, indent=2)
        
    print(f"Saved {len(all_rankings)} categories to rankings.json")

if __name__ == "__main__":
    generate_rankings_json()
