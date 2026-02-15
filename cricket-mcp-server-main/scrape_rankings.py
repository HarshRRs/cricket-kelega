import requests
from bs4 import BeautifulSoup
import time

def test_fetch():
    urls = [
        "https://www.cricbuzz.com/",
        "https://www.cricbuzz.com/cricket-stats/icc-rankings/men/batting"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/"
    }
    
    for url in urls:
        print(f"\nFetching {url}...")
        try:
            r = requests.get(url, headers=headers, timeout=10)
            print(f"Status: {r.status_code}")
            print(f"Content Length: {len(r.content)}")
            
            soup = BeautifulSoup(r.content, 'html.parser')
            print(f"Title: {soup.title.string.strip() if soup.title else 'No Title'}")
            
            if "rankings" in url:
                # Dump structure
                print("Looking for 'cb-rank-tbl' class...")
                rows = soup.find_all(class_="cb-rank-tbl")
                print(f"Found {len(rows)} elements with 'cb-rank-tbl'.")
                
                # Look for 'Kane Williamson'
                kw = soup.find(string=lambda t: t and "Kane Williamson" in t)
                if kw:
                    print(f"Found Kane Williamson in: {kw.parent}")
                else:
                    print("Kane Williamson NOT found.")
                    
        except Exception as e:
            print(f"Error fetching {url}: {e}")

if __name__ == "__main__":
    test_fetch()
