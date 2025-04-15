from queue import Queue
from bs4 import BeautifulSoup, Tag
from urllib.parse import ParseResult, urlparse, urljoin
import requests
import time

from src.utils.normalize_url import normalize_url

# { "URL": " https :// g1. globo .com/",
# " Title ": "G1 - O portal de not´ı cias da Globo ",
# " Text ": " Deseja receber as not´ı cias mais importantes em
# ,→ tempo real ? Ative as notifica ¸c~oes do G1! Agora n~ao
# ,→ Ativar Gasto familiar Despesa ",
# " Timestamp ": 1649945049 }

def crawl(url: str, debug: bool) -> tuple[str, set[str], set[str]]:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    if 'text/html' not in response.headers.get('Content-Type', ''):
        raise ValueError(f'text/html not found in response: {response.headers}')
    html = response.text
    
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    text = soup.get_text(separator=' ')
    words = text.split()
    timestamp = int(time.time())
    
    if debug:
        print({
            "URL": url,
            "Title": title,
            "Text": ' '.join(words[:20]),
            "Timestamp": timestamp, 
        })

    inlinks, outlinks = _extract_links(soup, url)
    
    return html, inlinks, outlinks


def _extract_links(soup: BeautifulSoup, url: str) -> tuple[set[str], set[str]]:
    inlinks: set = set()
    outlinks: set = set()
    
    parsed: ParseResult = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    
    for tag in soup.find_all('a', href=True):
        href: str = tag['href'] # type: ignore
        
        if href.startswith(('mailto:', 'javascript:', '#', 'tel:')):
            continue
        
        if href.strip() == '/':
            continue
        
        elif(href.startswith('/')):
            inlinks.add(urljoin(base_url, href))
            
        else:
            if normalize_url(url) in normalize_url(href):
                inlinks.add(href)
            else:
                outlinks.add(href)
            
    return inlinks, outlinks
        
    
if __name__ == "__main__":
    url = 'https://ciano.io'
    html, inlinks, outlinks = crawl(url, True)
