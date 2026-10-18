"""Importa fotos verificadas e preserva origem e atribuição de cada arquivo.

Execute na raiz do projeto. Fotos TOPPUR são do catálogo original solicitado.
Referências externas são Wikimedia Commons com licença comercial compatível.
"""
import html
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'static' / 'assets' / 'catalog'
HEADERS = {'User-Agent': 'ToppurCatalogResearch/1.0 (website reconstruction)'}

# ID do arquivo na biblioteca pública da TOPPUR; descrição exata do enquadramento.
TOPPUR = {
    'acoplamentos': (2690, 'Elemento elástico em poliuretano para acoplamento.'),
    'batentes': (2442, 'Coxim em poliuretano: referência da família de amortecimento.'),
    'calcos': (2472, 'Apoios antivibração em borracha: referência de apoio técnico.'),
    'juntas': (2433, 'Junta em borracha do catálogo TOPPUR.'),
    'polias': (2486, 'Polia em poliuretano do catálogo TOPPUR.'),
    'rolos': (2469, 'Rolos revestidos em poliuretano do catálogo TOPPUR.'),
    'tiras': (2425, 'Perfis em poliuretano: referência da linha de perfis e tiras.'),
    'vedacoes-gerais': (2459, 'Vedações em borracha do catálogo TOPPUR.'),
    'buchas-automotivas': (2677, 'Buchas em poliuretano: referência de modelos sob medida.'),
    'sedes-valvulas': (2458, 'Sedes de borracha para válvula borboleta.'),
    'valvulas': (2462, 'Inserto de válvula em poliuretano do catálogo TOPPUR.'),
    'diafragmas': (2452, 'Diafragma de embreagem em borracha do catálogo TOPPUR.'),
    'discos': (2443, 'Disco em acrílico do catálogo TOPPUR.'),
    'lencois': (2474, 'Lençóis de borracha do catálogo TOPPUR.'),
    'revestimento-rodas': (2549, 'Roda em poliuretano: referência da linha de rodas e revestimentos.'),
    'revestimento-cilindros-silos-calhas': (2516, 'Revestimento de cilindro em poliuretano do catálogo TOPPUR.'),
    'manchetas': (3140, 'Mancheta para bomba de concreto do catálogo TOPPUR.'),
}

COMMONS = {
    'arruelas': ('File:Rubber washer.jpg', 'Arruela de borracha. Imagem ilustrativa; não representa um modelo fabricado pela TOPPUR.'),
    'hidrociclones': ('File:Close up of hydrocyclones on Evowash sand washing plant (6237342892).jpg', 'Hidrociclones em aplicação industrial. Referência de aplicação, não um equipamento TOPPUR.'),
    'passa-fios': ('File:Rubbergrommets.jpg', 'Passa-fios de borracha. Imagem ilustrativa; consulte modelos e medidas.'),
    'tubos': ('File:EPDM rubber tube.jpg', 'Tubo de borracha EPDM. Imagem ilustrativa; material e dimensões sob consulta.'),
    'coifas': ('File:Achsmanschette.jpg', 'Coifa de transmissão. Imagem ilustrativa; não representa um modelo fabricado pela TOPPUR.'),
    'rotores': ('File:02 Impeller.jpg', 'Rotor flexível. Imagem ilustrativa; consulte a aplicação e o material.'),
    'defensas-portuarias': ('File:Rubber Fender in port Vado Ligure.jpg', 'Defensa de borracha em aplicação portuária. Imagem ilustrativa de aplicação.'),
}


def request_json(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=40) as response:
        return json.load(response)


def plain(value):
    return html.unescape(re.sub(r'<[^>]*>', '', value)).strip()


def download(url, slug):
    suffix = Path(urllib.parse.urlparse(url).path).suffix.lower()
    if suffix not in ('.jpg', '.jpeg', '.png', '.webp'):
        raise ValueError(f'Unsupported image: {url}')
    destination = ASSETS / (slug + suffix)
    if destination.exists() and destination.stat().st_size > 0:
        return 'catalog/' + destination.name
    with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=40) as response:
        content = response.read()
    destination.write_bytes(content)
    return 'catalog/' + destination.name


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    records = {}
    def persist():
        (ROOT / 'photo_sources.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
    for slug, (media_id, caption) in TOPPUR.items():
        media = request_json(f'https://toppur.com.br/wp-json/wp/v2/media/{media_id}')
        url = media['source_url']
        records[slug] = dict(image=download(url, slug), url=url, page=media['link'],
                             author='TOPPUR', license='Catálogo original TOPPUR', license_url='',
                             illustrative=False, caption=caption)
        print(f'TOPPUR: {slug}')
        persist()
    for slug, (title, caption) in COMMONS.items():
        query = urllib.parse.urlencode(dict(action='query', format='json', titles=title,
                                            prop='imageinfo', iiprop='url|extmetadata', iiurlwidth=1000))
        pages = request_json('https://commons.wikimedia.org/w/api.php?' + query)['query']['pages']
        info = next(iter(pages.values()))['imageinfo'][0]
        metadata = info['extmetadata']
        license_name = metadata.get('LicenseShortName', {}).get('value', '')
        if not (license_name.startswith(('CC BY', 'CC0')) or license_name == 'Public domain') or 'NC' in license_name or 'ND' in license_name:
            raise ValueError(f'License requires review for {slug}: {license_name}')
        url = info['url']
        try:
            local_image = download(url, slug)
        except urllib.error.HTTPError:
            local_image = download(info['thumburl'], slug)
        records[slug] = dict(image=local_image, url=info['url'], page=info['descriptionurl'],
                             author=plain(metadata.get('Artist', {}).get('value', 'Wikimedia Commons')),
                             license=license_name, license_url=metadata.get('LicenseUrl', {}).get('value', ''),
                             illustrative=True, caption=caption)
        print(f'Commons: {slug} ({license_name})')
        persist()
    (ROOT / 'photo_sources.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Imported {len(records)} photographs with provenance.')


if __name__ == '__main__':
    main()
