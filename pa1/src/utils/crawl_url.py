from bs4 import BeautifulSoup, Tag
import requests
import time
import re

# { "URL": " https :// g1. globo .com/",
# " Title ": "G1 - O portal de not´ı cias da Globo ",
# " Text ": " Deseja receber as not´ı cias mais importantes em
# ,→ tempo real ? Ative as notifica ¸c~oes do G1! Agora n~ao
# ,→ Ativar Gasto familiar Despesa ",
# " Timestamp ": 1649945049 }

def crawl(url: str, debug: bool):
    try:
        response = requests.get(url, timeout=5)
        if 'text/html' not in response.headers.get('Content-Type', ''):
            return ''
        html = response.text
    except Exception as e:
        return ''
    
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
        
    _extract_links(soup)

def _extract_links(soup: BeautifulSoup):
    inlinks: set = set()
    outlinks: set = set()
    for tag in soup.find_all('a', href=True):
        print(tag['href'])
        href = tag['href']
        
        if href.startswith(('mailto:', 'javascript:', '#')):
            continue
        
        
        
    
if __name__ == "__main__":
    crawl("https://g1.globo.com/", True)
