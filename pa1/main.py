from src.utils.parse_args import get_args
from src.crawler import Crawler

def run_crawler(seed_file, limit, debug, threads=48):
    with open(seed_file, 'r') as f:
        seeds = [line.strip() for line in f if line.strip()]
    crawler = Crawler(seeds, limit, debug, threads)
    crawler.run()

def main():
    args = get_args()
    
    print(f"Seeds file: {args.seeds}, limit: {args.limit}, debug: {args.debug}\n")

    run_crawler(seed_file=args.seeds, limit=args.limit, debug=args.debug)

if __name__ == '__main__':
    main()
