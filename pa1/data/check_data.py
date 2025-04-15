import gzip
from warcio.archiveiterator import ArchiveIterator

warc_file_path = './data/corpus_009.warc.gz'

count = 0

with gzip.open(warc_file_path, 'rb') as stream:
    for record in ArchiveIterator(stream):
        count += 1
        url = record.rec_headers.get_header('WARC-Target-URI')
        payload = record.content_stream().read()
        html = payload.decode('utf-8')

        print(f"URL: {url}")
        print(f"HTML (primeiros 300 caracteres):\n{html[:300]}")
        print("="*80)

print(f"Count docs: {count}")