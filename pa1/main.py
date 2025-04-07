from arg_parser import get_args

def run_crawler(seed_file, limit, debug=False):
    if debug:
        print(f"Iniciando crawler com limite de {limit} páginas...")

    # Carrega os seeds do arquivo
    with open(seed_file, 'r') as f:
        seeds = [line.strip() for line in f if line.strip()]
    
    if debug:
        print(f"Seeds carregadas: {seeds}")

    # Aqui você colocaria a lógica do crawler
    # ...

def main():
    args = get_args()

    if args.debug:
        print("Modo Debug Ativado")
        print(f"Arquivo de seeds: {args.seeds}")
        print(f"Limite de páginas: {args.limit}")

    run_crawler(seed_file=args.seeds, limit=args.limit, debug=args.debug)

if __name__ == '__main__':
    main()
