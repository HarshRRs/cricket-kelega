
import scraper
import json

def get_match_priority(match):
    score = 0
    name = match.get('name', '').lower()
    m_type = match.get('matchType', '').lower()
    status = match.get('status', '').lower()

    # 1. Premium / Scraped (Highest Priority)
    if match.get('is_premium'): score += 2000

    # 2. Status
    if 'live' in status: score += 1000
    elif 'common' in status or 'upcoming' in status: score += 200
    
    # 3. Tournaments / Keywords
    if 'world cup' in name: score += 500
    
    if 'women' in name:
        score += 500
    else:
        score += 1500 # Aggressive Men's Boost

    if 'final' in name: score += 500
    if 'semi-final' in name: score += 500

    # 4. Big Teams
    if 'india' in name or 'ind ' in name: score += 100
    if 'australia' in name or 'aus ' in name: score += 80
    if 'england' in name or 'eng ' in name: score += 80
    if 'pakistan' in name or 'pak ' in name: score += 80

    return score

print("Fetching matches...")
try:
    matches = scraper.get_cricbuzz_matches()
    with open("debug_log.txt", "w", encoding="utf-8") as f:
        f.write(f"Found {len(matches)} matches.\n\n")
        f.write("--- Match Analysis ---\n")
        for m in matches:
            score = get_match_priority(m)
            f.write(f"Name: {m.get('name')} | Status: {m.get('status')} | Score: {score}\n")
            f.write(f"   (Type: {m.get('matchType')})\n")
    print("Debug log written to debug_log.txt")
        
except Exception as e:
    print(f"Error: {e}")
