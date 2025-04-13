from urllib.parse import ParseResult, urlparse, urljoin
import requests
from protego import Protego
import time

DEFAULT_CRAWL_DELAY = 0.1

robots_cache: dict = {}

def can_crawl(url: str):
    parsed: ParseResult = urlparse(url)
    base_url = parsed.netloc
    
    if base_url not in robots_cache:
        robots_txt = requests.get(urljoin(base_url, "/robots.txt"))
        rp = Protego.parse(robots_txt)
        robots_cache[base_url] = rp
    else:
        rp = robots_cache[base_url]
        
    wait_time = rp.crawl_delay("*") if rp.crawl_delay("*") is not None else DEFAULT_CRAWL_DELAY
    
    return rp.can_fetch(url, "*"), wait_time


last_request: dict = {}

def wait_if_needed(url: str, crawl_delay: int):
    parsed: ParseResult = urlparse(url)
    base_url = parsed.netloc
    
    if base_url in last_request:
        now = time.time()
        if now - last_request[base_url] < crawl_delay:
            time.sleep(crawl_delay - now  - last_request[base_url])
    last_request[base_url] = time.time()
