
from queue import Queue
import threading

class Crawler:
    def __init__(self, seeds, storage, limit, debug) -> None:
        
        self.storage = storage
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
        self.thread_count: int = 4
        
        # Count pages
        self.total_pages_crawled: int = 0
        self.lock_total_pages = threading.Lock()
        
        
        
    
    def start(self):
        threads = [threading.Thread(target=self.crawl) for _ in range(self.thread_count)]

    def crawl(self) -> None:
        while(True):
            with self.lock_total_pages:
                if self.total_pages_crawled >= self.limit or self.frontier.empty():
                    break
            
            url: str = self.frontier.get()
            
            # Separated vector to prioritize out links intead of in links
            # A Priority Queue would be very slow
            out_links: list[str]  =  []
            in_links:  list[str]  =  []
            
            
            
            
            
            
            
    