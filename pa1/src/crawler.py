
from os import error
from queue import Queue
from re import U
import threading

from langsmith import expect
from yarl import URL

from src.storage import Storage
from src.utils.crawl_url import crawl
from src.utils.politeness import can_crawl, wait_if_needed
from src.utils.normalize_url import normalize_url
from src.utils.log import error_logger, progress_logger

class Crawler:
    def __init__(self, seeds, limit, debug, threads) -> None:
        self.debug: bool = debug
        self.limit: int = limit
        
        # Set in which the url will be mark as visited
        self.visited: set = set()
        
        # Global queue and putting seeds into it
        # Nao precisa controlar com lock pq Queue é thread-safe
        self.frontier: Queue = Queue()
        self.seeds: list[str] = seeds
        
        for seed in seeds:
            self.frontier.put(seed)
            
        # Thread handling
        self.thread_count: int = threads
        
        # Count pages
        self.total_pages_crawled: int = 0
        self.lock_total_pages = threading.Lock()
        
        # Storage
        self.storage = Storage()
        self.lock_storage = threading.Lock()
        
        
    def run(self):
        threads = [threading.Thread(target=self.crawl) for _ in range(self.thread_count)]
        for t in threads: t.start()
        for t in threads: t.join()
        self.storage.close()

    def crawl(self) -> None:
        while(True):
            try:
                with self.lock_total_pages:
                    if self.total_pages_crawled >= self.limit or self.frontier.empty():
                        break

                url: str = self.frontier.get()

                if url in self.visited:
                    continue

                can, time_wait = can_crawl(url)
                if not can:
                    continue

                wait_if_needed(url, time_wait)

                html, inlinks, outlinks = crawl(url, self.debug)
                
                self.visited.add(normalize_url(url))
                
                with self.lock_storage:
                    self.storage.add(url, html)
                
                for link in outlinks:
                    self.frontier.put(link)
                    
                for link in inlinks:
                    self.frontier.put(link)

                with self.lock_total_pages:
                    self.total_pages_crawled += 1
                    if self.total_pages_crawled != 0 and self.total_pages_crawled % (self.limit//20) == 0:
                        progress_logger.info(f"PROGRESS | Count pages crawled: {self.total_pages_crawled}")
                          
            except Exception as e:
                error_logger.error(f'IGNORING ERROR | URL: {url} | Exception: {e}')
                continue 
