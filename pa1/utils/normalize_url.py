from urllib.parse import urlparse, urlunparse, urljoin, parse_qsl, urlencode
import posixpath

def normalize_url(url: str) -> str:
    parsed = urlparse(url)

    # minusculo
    hostname = parsed.hostname.lower() if parsed.hostname else ''

    # tirar www
    if hostname.startswith('www.'):
        hostname = hostname[4:]

    # tira barras adicionais, pontos indicando caminhos e outros
    path = posixpath.normpath(parsed.path or '/')

    if parsed.path.endswith('/') and not path.endswith('/'):
        path += '/'

    # colocar parametros na mesma ordem
    query = urlencode(sorted(parse_qsl(parsed.query)))

    # juntar partes
    normalized = urlunparse(('', hostname, path, '', query, ''))

    # remover barra no comeco
    return normalized.lstrip('/')
