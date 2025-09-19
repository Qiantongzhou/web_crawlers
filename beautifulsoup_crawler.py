import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
# crawler function
def crawl(start, domain_whitelist, max_pages):
    visited = set()
    queue = deque([start])

    while queue and len(visited) < max_pages:
        url = queue.popleft()
        if url in visited:
            continue
        domain = urlparse(url).netloc
        if not any(allowed in domain for allowed in domain_whitelist):
            continue



        try:
            #timeout 5 sec
            response = requests.get(url, timeout=5)
            if "text/html" not in response.headers.get("Content-Type", ""):
                continue
            raw = BeautifulSoup(response.text, "html.parser")
            #get title
            title = raw.title.string.strip() if raw.title else "No title"
            #get other info todo..

            # add to visited
            visited.add(url)
            print(f"[{len(visited)}] Title: {title}, URL: {url}")
            #find the next url
            for link in raw.find_all("a", href=True):
                next_url = urljoin(url, link["href"])
                next_domain = urlparse(next_url).netloc
                if (next_url not in visited
                        and any(allowed
                                in next_domain
                                for allowed
                                in domain_whitelist)):
                    queue.append(next_url)

        except Exception as e:
            print(f"Failed to fetch or timeout: {url}")

    return visited

##designed to crawl my own website.
if __name__ == "__main__":
    #start with main page
    start = "http://qiantongzhou.huizhoutech.top"
    #no external link
    whitelist = ["huizhoutech.top"]
    #stop when reach max page
    max_pages = 20

    crawl(start, whitelist, max_pages)

