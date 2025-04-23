from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
import posixpath

from src.utils.errors import MissingHostnameError

def normalize_url(url: str) -> str:
    """Normaliza a url para um formato padrão"""
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


# Identificação das TLDs para parsing
ccTLDs = {
    'br', 'uk', 'jp', 'fr', 'de', 'us', 'au', 'cn', 'in', 'it',
    'es', 'ru', 'ca', 'kr', 'mx', 'za', 'nl', 'ar', 'pl', 'nz',
    'se', 'ch', 'pt', 'gr', 'tr', 'no', 'be', 'fi', 'ie'
}

def extract_domain(url: str) -> str:
    """Extrair somente o domínio principal sem o subdomínio"""
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname

    if hostname is None:
        raise MissingHostnameError(url)

    parts = hostname.lower().split('.')

    if len(parts) < 2:
        return hostname

    if parts[-1] in ccTLDs and len(parts) >= 3:
        return '.'.join(parts[-3:])
    else:
        return '.'.join(parts[-2:])


if __name__ == "__main__":
    print(normalize_url("https://www.api.ciano.io/?id=10&ad=True"), normalize_url("https://ciano.io/olha-aqui/?ad=True&id=10&"))
    print(extract_domain("https://www.redetv.uol.com.br/"))