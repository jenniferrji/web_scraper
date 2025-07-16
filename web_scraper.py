import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# This function crawls the given URL and finds links containing any of the keywords.
# It will also follow links within the Cisco domain up to the specified max_depth (how many pages to go into).
def find_training_links(url, keywords, max_depth=1):
    visited = set()  # Keeps track of visited URLs to avoid repeats
    found = set()    # Stores found training links
    def crawl(current_url, depth):
        # Stop if we've reached the max depth or if already visited this URL
        if depth > max_depth or current_url in visited:
            return
        visited.add(current_url)
        try:
            response = requests.get(current_url)
            soup = BeautifulSoup(response.text, 'lxml')
        except Exception:
            # If there is an error fetching or parsing, skip this URL
            return
        # Look at every <a> tag with an href attribute (every hyperlink with a destination)
        for a in soup.find_all('a', href=True):
            href = a['href']
            full_url = urljoin(current_url, href)  # Make absolute (complete) URL
            text = a.get_text().strip()
            href_lower = href.lower()
            text_lower = text.lower()
            # Check if any keyword is a substring of the link or its text
            for kw in keywords:
                kw_lower = kw.lower()
                if kw_lower in href_lower or kw_lower in text_lower:
                    if full_url not in found:
                        found.add(full_url)
                        print(f"{full_url} | {text}")  # Print the matching link and its text
                    break  # Stop checking more keywords for this link
            # Only follow links that stay within the Cisco domain
            parsed = urlparse(full_url)
            if "cisco.com" in parsed.netloc:
                crawl(full_url, depth + 1)
    crawl(url, 0)
    return list(found)

if __name__ == "__main__":
    # The starting Cisco training page to scrape
    url = "https://www.cisco.com/site/us/en/learn/training-certifications/training/index.html#accordion-5dd9235457-item-3265282a49"
    # Keywords to look for in links and link text (related to Cisco certifications)
    keywords = [
        "ccie", "security", "ccna", "enterprise", "labs",
        "ccnp", "data center", "cct", "routing", "switching",
        "collaboration", "clcor", "cyberops", "devnet", "ensari", "associate", "professional", "technician"
    ]
    # Find training links, crawling up to 3 pages deep
    training_links = find_training_links(url, keywords, max_depth=2)
    print("Total training links found:", len(training_links))
