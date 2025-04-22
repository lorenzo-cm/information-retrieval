import time
import gzip
import os
from warcio.warcwriter import WARCWriter
from io import BytesIO

class Storage:
    def __init__(self, output_dir="./data/"):
        self.output_dir = output_dir
        self.page_buffer = []
        self.file_index = 0
        os.makedirs(self.output_dir, exist_ok=True)

    def add(self, url, html):
        self.page_buffer.append({
            "url": url,
            "html": html,
            "timestamp": int(time.time())
        })
        if len(self.page_buffer) >= 1000:
            self._save_warc()

    def _save_warc(self):
        warc_path = os.path.join(self.output_dir,
                                f"corpus_{self.file_index:03}.warc.gz")

        with gzip.open(warc_path, "wb") as stream:
            writer = WARCWriter(stream, gzip=True)

            for page in self.page_buffer: 
                payload = page["html"].encode("utf-8")

                record = writer.create_warc_record(
                    uri=page["url"],
                    record_type="resource",
                    payload=BytesIO(payload),
                )
                writer.write_record(record)

        self.file_index += 1
        self.page_buffer = []

    def close(self):
        if self.page_buffer:
            self._save_warc()