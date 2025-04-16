class BaseCrawlerError(Exception):
    def __init__(self, message="Crawler error"):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"
    
class NotHTMLError(BaseCrawlerError):
    def __init__(self, url, message="Content is not valid HTML"):
        self.url = url
        full_message = f"{message}: {url}"
        super().__init__(full_message)

class MissingHostnameError(BaseCrawlerError):
    def __init__(self, url, message="Hostname is None for URL"):
        self.url = url
        full_message = f"{message}: {url}"
        super().__init__(full_message)
