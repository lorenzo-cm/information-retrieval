import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Web crawler")

    parser.add_argument('-s', '--seeds', type=str, required=True,
                        help='Caminho para o arquivo com URLs seed')
    parser.add_argument('-n', '--limit', type=int, required=True,
                        help='Número máximo de páginas a serem rastreadas')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Ativa o modo debug')

    return parser.parse_args()
