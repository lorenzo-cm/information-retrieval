from bs4 import BeautifulSoup
from urllib.parse import ParseResult, urlparse, urljoin
import requests
import time

from src.utils.errors import NotHTMLError

# { "URL": " https :// g1. globo .com/",
# " Title ": "G1 - O portal de not´ı cias da Globo ",
# " Text ": " Deseja receber as not´ı cias mais importantes em
# ,→ tempo real ? Ative as notifica ¸c~oes do G1! Agora n~ao
# ,→ Ativar Gasto familiar Despesa ",
# " Timestamp ": 1649945049 }

def crawl(url: str, debug: bool) -> tuple[str, set[str], set[str]]:
    """Função principal de crawl
    
    A função coleta apenas HTML, de maneira a extrair o conteúdo da página e os links (referências).
    
    Os links são classificados como inlinks ou outlinks
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    if 'text/html' not in response.headers.get('Content-Type', ''):
        raise NotHTMLError(url)
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
    """Essa função realiza a extração dos links e a classificação deles em inlinks e outlinks"""
    inlinks: set = set()
    outlinks: set = set()
    
    parsed: ParseResult = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    
    for tag in soup.find_all('a', href=True):
        href: str = tag['href'] # type: ignore
        href_parsed = urlparse(href)
        
        # remover strings vazias e strings somente com / 
        # ou que comecam com # que traduziriam ambas no proprio link        
        if not href.strip() or href.strip() == '/' or href.startswith('#'):
            continue
        
        #- //meta.ai -> https://meta.ai
        if href.startswith('//'):
            href = "https:" + href
        
        # /search -> https://google.com/search
        elif href.startswith('/'):
            href = urljoin(base_url, href)
        
        # spotify:// , javascript:, mail:
        if href_parsed.scheme and href_parsed.scheme not in ['http', 'https', '', ' ']:
            continue
        
        # https://google.com
        elif href.startswith('http'):
            href_parsed = urlparse(href)
            if parsed.hostname == href_parsed.hostname:
                inlinks.add(href)
            else:
                outlinks.add(href)
        
        # search -> https://google.com/search
        else:
            href = urljoin(base_url, href)
            inlinks.add(urljoin(base_url, href))
        
    return inlinks, outlinks
        
    
if __name__ == "__main__":
    
    url = 'https://assinecoquetel.com.br/'
    html, inlinks, outlinks = crawl(url, False)
    