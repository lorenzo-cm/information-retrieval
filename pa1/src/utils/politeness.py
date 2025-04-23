from urllib.parse import ParseResult, urlparse, urljoin
import requests
from protego import Protego
import time

DEFAULT_CRAWL_DELAY = 0.1

robots_cache: dict = {}

def can_crawl(url: str) -> tuple[bool, float]:
    """Verifica se a página pode ser coletada e qual o tempo que devo esperar para coletá-la novamente"""
    parsed: ParseResult = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    
    # print(f"can crawl: {url}, urlJoin: {urljoin(base_url, "/robots.txt")}")
    
    if base_url not in robots_cache:
        response = requests.get(urljoin(base_url, "/robots.txt"), timeout=10)
        if 400 <= response.status_code < 600:
            return True, DEFAULT_CRAWL_DELAY
        # response.raise_for_status() # vou assumir que se n tem 'e valido
        robots_txt = response.text
        rp = Protego.parse(robots_txt)
        robots_cache[base_url] = rp
    else:
        rp = robots_cache[base_url]
        
    wait_time = rp.crawl_delay("*") if rp.crawl_delay("*") is not None else DEFAULT_CRAWL_DELAY
    
    return rp.can_fetch(url, "*"), wait_time


last_request: dict = {}

def wait_if_needed(url: str, crawl_delay: float):
    """Verifica se é necessário esperar antes de enviar uma nova requisição, caso precise, então a função espera"""
    parsed: ParseResult = urlparse(url)
    base_url = parsed.netloc
    
    if base_url in last_request:
        now = time.time()
        elapsed = now - last_request[base_url]
        if elapsed < crawl_delay:
            time.sleep(max(0, crawl_delay - elapsed)) # max 0 to avoid negative sleep time
    last_request[base_url] = time.time()


if __name__ == "__main__":
    url = "https://grupoglobo.globo.com/"
    print(can_crawl(url))