# { "URL": " https :// g1. globo .com/",
# " Title ": "G1 - O portal de not´ı cias da Globo ",
# " Text ": " Deseja receber as not´ı cias mais importantes em
# ,→ tempo real ? Ative as notifica ¸c~oes do G1! Agora n~ao
# ,→ Ativar Gasto familiar Despesa ",
# " Timestamp ": 1649945049 }
import threading

class Crawler:
    def __init__(self):
        self.visited = set()
        
        self.thread_count = 4
    
    def start(self):
        threads = [threading.Thread(target=self.crawl) for _ in range(self.thread_count)]

    def crawl(self):
        pass