from queue import Queue
import random
import threading

from src.storage import Storage
from src.utils.crawl_url import crawl
from src.utils.politeness import can_crawl, wait_if_needed
from src.utils.normalize_url import normalize_url, extract_domain
from src.utils.log import error_logger, progress_logger

class Crawler:
    def __init__(self, seeds, limit, debug, threads) -> None:
        self.debug: bool = debug
        self.limit: int = limit
        
        # Set in which the url will be mark as visited
        self.visited: set = set()
        self.visited_domains: set = set()
        
        # Global queue and putting seeds into it
        # Nao precisa controlar com lock pq Queue é thread-safe
        self.frontier: Queue = Queue()
        self.new_domains_frontier: Queue = Queue()
        self.seeds: list[str] = seeds
        
        self.explore_new_domains_frontier_prob = 0.7 # must not be too low to not be visited and no too big to allow subdomain exploration
        
        for seed in seeds:
            self.new_domains_frontier.put(seed)
            
        # Thread handling
        self.thread_count: int = threads
        
        # Count pages
        self.total_pages_crawled: int = 0
        self.lock_total_pages = threading.Lock()
        
        # Storage
        self.storage = Storage()
        self.lock_storage = threading.Lock()
        
        # Seed for reproducibility
        self._set_seed()
        
        # Progress log config
        self.log_freq = self.limit//20 if self.limit>=20 else self.limit
        
    def run(self):
        threads = [threading.Thread(target=self.crawl) for _ in range(self.thread_count)]
        for t in threads: t.start()
        for t in threads: t.join()
        self.storage.close()


    def crawl(self) -> None:
        while(True):
            try:
                with self.lock_total_pages:
                    if self.total_pages_crawled >= self.limit or (self.frontier.empty() and self.new_domains_frontier.empty()):
                        break

                url: str = ''
                
                # Essa função contem o teste de probabilidade
                if self._should_explore_new_domains_and_not_empty():
                    url = self.new_domains_frontier.get()
                else:
                    url = self.frontier.get()

                if url in self.visited or url == '':
                    continue
                
                self.visited.add(normalize_url(url))
                
                can, time_wait = can_crawl(url)
                if not can:
                    continue

                wait_if_needed(url, time_wait)

                html, inlinks, outlinks = crawl(url, self.debug)
                
                with self.lock_storage:
                    self.storage.add(url, html)
                
                for link in outlinks:
                    domain: str = extract_domain(link)
                    if domain in self.visited_domains:
                        self.frontier.put(link)
                    else:
                        self.new_domains_frontier.put(link)
                        self.visited_domains.add(domain)
                    
                for link in inlinks:
                    self.frontier.put(link)

                with self.lock_total_pages:
                    self.total_pages_crawled += 1
                    if self.total_pages_crawled != 0 and self.total_pages_crawled % self.log_freq == 0:
                        progress_logger.info(f"PROGRESS | Count pages crawled: {self.total_pages_crawled} | {self.total_pages_crawled/self.limit * 100}%")
                          
            except Exception as e:
                error_logger.error(f'IGNORING ERROR | URL: {url} | Exception: {e}')
                continue 

    def _set_seed(self):
        random.seed(42)
    
    def _should_explore_new_domains_and_not_empty(self) -> bool:
        # the or makes when the main frontier is empty, it will obligatory fetch from the new domains frontier (improbable scenario)
        return not self.new_domains_frontier.empty() and (random.random() <= self.explore_new_domains_frontier_prob or self.frontier.empty())
