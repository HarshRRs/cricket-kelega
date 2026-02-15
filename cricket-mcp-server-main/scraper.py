import requests
from bs4 import BeautifulSoup
import re
import time

# Use mimic headers to avoid basic bot detection
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_cricbuzz_matches():
    """
    Scrapes live matches from Cricbuzz using robust link detection.
    Returns a list of dictionaries with match details.
    """
    try:
        url = "https://www.cricbuzz.com/cricket-match/live-scores"
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        matches = []
        
        # Find all match links directly
        match_links = soup.find_all("a", href=lambda href: href and "/live-cricket-scores/" in href)
        
        seen_ids = set()
        
        for link in match_links:
            try:
                href = link.get("href")
                match_match = re.search(r"/live-cricket-scores/(\d+)/", href)
                if not match_match:
                    continue
                    
                match_id = match_match.group(1)
                if match_id in seen_ids:
                    continue
                seen_ids.add(match_id)
                
                match_name = link.text.strip()
                
                # Try to find status/score by looking at specific container structure
                # Logic: Link is usually inside a header (h3/div). 
                # The status/score is usually in a sibling div or parent's sibling.
                
                status_text = ""
                score_text = ""
                
                # Attempt 1: Check standard Cricbuzz list structure
                # Link parent is usually 'cb-lv-scr-mtch-hdr' (div or h3)
                # Sibling is 'cb-scr-wll-chvrn' (div)
                
                header_container = link.parent
                match_item_container = header_container.parent
                
                # Look for score container
                score_div = match_item_container.find("div", class_="cb-scr-wll-chvrn")
                if not score_div:
                    # Fallback: Look for any text in siblings?
                    # Or try next 'div'
                    score_div = match_item_container.find_next("div", class_="cb-scr-wll-chvrn")
                
                if score_div:
                    raw_text = score_div.get_text(" ", strip=True) 
                    extracted = raw_text.split("•") 
                    if extracted:
                        status_text = extracted[-1].strip()
                        if len(extracted) > 1:
                            score_text = extracted[0].strip()
                        else:
                            score_text = raw_text
                
                # If still empty, maybe it's just "Upcoming" or link text has info?
                
                matches.append({
                    "id": match_id,
                    "name": match_name,
                    "status": status_text or "Live/Upcoming",
                    "score": score_text,
                    "source": "cricbuzz"
                })
            except Exception as e:
                continue
                
        return matches
    except Exception as e:
        print(f"Error fetching Cricbuzz matches: {e}")
        return []

def get_commentary(match_id):
    """
    Scrapes commentary for a specific match ID.
    Returns list of commentary strings.
    """
    try:
        url = f"https://www.cricbuzz.com/live-cricket-scores/{match_id}/commentary"
        response = requests.get(url, headers=HEADERS, timeout=10)
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        commentary_lines = []
        # Commentary lines are often in p.cb-com-ln (older) or div.cb-col.cb-col-100 ng-scope (angular)
        # Try finding p class="cb-com-ln"
        comm_elements = soup.find_all("p", class_="cb-com-ln")
        
        if not comm_elements:
            # Fallback selector
            comm_elements = soup.select(".cb-col.cb-col-100 .cb-com-ln")

        for el in comm_elements:
            text = el.get_text(strip=True)
            if text:
                commentary_lines.append(text)
                
        return commentary_lines[:25] # Limit to recent
    except Exception as e:
        print(f"Error fetching commentary for {match_id}: {e}")
        return [f"Could not load commentary: {str(e)}"]

if __name__ == "__main__":
    # verification
    print("Fetching matches from Cricbuzz...")
    matches = get_cricbuzz_matches()
    print(f"Found {len(matches)} matches.")
    for m in matches[:3]:
        print(f"Match: {m['name']} | ID: {m['id']} | Status: {m['status']}")
        print("Fetching commentary...")
        comm = get_commentary(m['id'])
        print(f"Commentary lines: {len(comm)}")
        if comm:
            print(f"Latest: {comm[0]}")
        print("-" * 20)
