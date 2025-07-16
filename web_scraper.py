import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

#Function will find training links on given website based on keywords inputted to a certain max_depth.
def find_training_links(url, keywords, max_depth=1):
    visited = set()  # URLs already visited
    found = set()    # Training links found
    def crawl(current_url, depth):
        if depth > max_depth or current_url in visited:
            return
        visited.add(current_url)
        try:
            response = requests.get(current_url)
            soup = BeautifulSoup(response.text, 'lxml')
        except Exception:
            print(f"Could not find {current_url}")
            return

        # Look at every hyperlink with a destination
        for a in soup.find_all('a', href=True):
            href = a['href']
            full_url = urljoin(current_url, href) 
            text = a.get_text().strip()
            href_lower = href.lower()
            text_lower = text.lower()

            # Check if keyword is a substring of link or text
            for kw in keywords:
                kw_lower = kw.lower()
                if kw_lower in href_lower or kw_lower in text_lower:
                    if full_url not in found:
                        found.add(full_url)
                        print(f"{full_url} | {text}")  
                    break  

            # Follow links in set domain
            parsed = urlparse(full_url)
            if "cisco.com" in parsed.netloc: # CHANGE HERE TO CORRECT DOMAIN
                crawl(full_url, depth + 1)
    crawl(url, 0)
    return list(found)

if __name__ == "__main__":
    # CHANGE URL TO DESIRED PAGE
    url = "https://www.cisco.com/site/us/en/learn/training-certifications/training/index.html#accordion-5dd9235457-item-3265282a49"
    # CHANGE KEYWORDS 
    keywords = [
        "ccie", "security", "ccna", "enterprise", "labs",
        "ccnp", "data center", "cct", "routing", "switching",
        "collaboration", "clcor", "cyberops", "devnet", "ensari", "associate", "professional", "technician"
    ]

    training_links = find_training_links(url, keywords, max_depth=2) # CHANGE MAX DEPTH TO DESIRED
    print("Total training links found:", len(training_links))
