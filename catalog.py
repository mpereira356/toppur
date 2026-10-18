"""Conteúdo editorial e fotos extraídos do site original da TOPPUR."""

import json
from pathlib import Path

CATEGORIES = {'poliuretano': 'Peças em poliuretano', 'borracha': 'Peças em borracha', 'revestimentos': 'Revestimentos', 'tecnicas': 'Peças em borracha e poliuretano'}

LINES = {'industriais': 'Componentes industriais', 'automotiva': 'Linha automotiva',
         'especiais': 'Peças especiais e técnicas', 'revestimentos': 'Revestimentos técnicos'}
CATALOG_SOURCE = 'https://toppur.com.br/nossos-produtos/'

PRODUCTS = [
    dict(slug='perfis-guarnicoes', name='Perfis e guarnições', category='poliuretano', image='poliuretano-pecas-001.jpeg', description='Perfis e guarnições em poliuretano PU para vedação industrial. Desenvolvemos soluções de acordo com as dimensões e necessidades técnicas da sua aplicação.'),
    dict(slug='placas-tarugos', name='Placas e tarugos', category='poliuretano', image='PLACAS-EM-POLIURETANO-05-1024x683.jpg', description='Placas e tarugos em poliuretano para projetos industriais. Consulte os formatos, medidas e durezas disponíveis para sua operação.'),
    dict(slug='rodas-rodizios', name='Rodas e rodízios', category='poliuretano', image='RODIZIOS-EM-POLIURETANO-01.jpg', description='Rodas e rodízios em poliuretano para movimentação industrial. Nossa equipe orienta a escolha de acordo com o equipamento e suas condições de uso.'),
    dict(slug='pecas-borracha', name='Peças técnicas em borracha', category='borracha', image='borracha-pecas-001.jpeg', description='Gaxetas, coxins e diafragmas para vedação, controle de fluxo e absorção de vibrações. Modelos personalizados conforme a necessidade do cliente.'),
    dict(slug='buchas-poliuretano', name='Buchas em poliuretano', category='poliuretano', image='BUCHAS-POLIURETANO-03.png', description='Buchas que combinam flexibilidade e resistência para aplicações mecânicas. Soluções sob medida para o seu equipamento.'),
    dict(slug='elementos-elasticos', name='Elementos elásticos', category='poliuretano', image='ELEMENTOS-ELASTICOS-EM-POLIURETANO-03-1024x683.png', description='Elementos elásticos em poliuretano para aplicações industriais. Consulte nossa equipe para avaliar formatos e requisitos técnicos.'),
    dict(slug='ventosas', name='Ventosas de borracha e silicone', category='borracha', image='VENTOSAS-EM-SILICONE.jpg', description='Ventosas para automação e manipulação de objetos em superfícies lisas. Consulte modelos e possibilidades de fabricação para sua aplicação.'),
    dict(slug='revestimentos-pu', name='Revestimentos em poliuretano', category='revestimentos', image='REVESTIMENTO-ROLDANA-EM-POLIURETANO-07-1024x683.png', description='Revestimentos em PU para proteção de peças contra abrasão, impacto e desgaste. A solução é avaliada conforme as condições de trabalho do equipamento.'),
    dict(slug='roletes', name='Roletes em poliuretano', category='poliuretano', image='ROLETES-EM-POLIURETANO.jpg', description='Roletes em poliuretano para aplicações industriais, incluindo o segmento frigorífico. Envie as medidas e a aplicação para avaliação técnica.'),
    dict(slug='raspadores', name='Raspadores de correia', category='poliuretano', image='RASPADORES-DE-CORREIA-EM-POLIURETANO-1.jpg', description='Raspadores em poliuretano para sistemas de correias. Consulte nossa equipe sobre o desenvolvimento da peça para sua operação.'),
    dict(slug='vedacoes', name='Vedações em borracha', category='borracha', image='VEDACOES-EM-BORRACHA.jpg', description='Vedações de borracha para equipamentos industriais. Desenvolvemos modelos conforme as condições de uso e dimensões necessárias.'),
    dict(slug='concretagem', name='Linha de concretagem', category='poliuretano', image='Concretagem-Construcao-Civil.jpg', description='Peças para concretagem e construção civil: anéis de pressão, anéis guia, cones de vedação, gaxetas, guarnições e manchetas. Consulte os modelos e materiais indicados para cada peça.'),
]

# Os termos repetidos "Coxim", "Coxins" e "Coxim de borracha" do
# original representam uma única família. Materiais não discriminados na
# fonte ficam na categoria técnica, sem inferir composição ou desempenho.
for product in PRODUCTS:
    product['line'] = ('revestimentos' if product['category'] == 'revestimentos'
                       else 'especiais' if product['slug'] == 'ventosas' else 'industriais')
    product['source'] = CATALOG_SOURCE

ADDITIONAL_PRODUCTS = [
    ('acoplamentos', 'Acoplamentos', 'industriais', 'tecnicas'),
    ('arruelas', 'Arruelas', 'industriais', 'tecnicas'),
    ('batentes', 'Batentes', 'industriais', 'tecnicas'),
    ('calcos', 'Calços', 'industriais', 'tecnicas'),
    ('coxins', 'Coxins de borracha', 'industriais', 'borracha'),
    ('gaxetas', 'Gaxetas em borracha e poliuretano', 'industriais', 'tecnicas'),
    ('hidrociclones', 'Hidrociclones', 'industriais', 'tecnicas'),
    ('juntas', 'Juntas', 'industriais', 'tecnicas'),
    ('passa-fios', 'Passa-fios', 'industriais', 'tecnicas'),
    ('polias', 'Polias', 'industriais', 'tecnicas'),
    ('rolos', 'Rolos', 'industriais', 'tecnicas'),
    ('sapatas', 'Sapatas', 'industriais', 'tecnicas'),
    ('tubos', 'Tubos', 'industriais', 'tecnicas'),
    ('tiras', 'Tiras', 'industriais', 'tecnicas'),
    ('vedacoes-gerais', 'Vedações em geral', 'industriais', 'tecnicas'),
    ('buchas-automotivas', 'Buchas automotivas', 'automotiva', 'tecnicas'),
    ('coifas', 'Coifas', 'automotiva', 'tecnicas'),
    ('sedes-valvulas', 'Sedes de válvulas', 'automotiva', 'tecnicas'),
    ('valvulas', 'Válvulas', 'automotiva', 'tecnicas'),
    ('diafragmas', 'Diafragmas', 'especiais', 'borracha'),
    ('discos', 'Discos', 'especiais', 'tecnicas'),
    ('difusores', 'Difusores', 'especiais', 'tecnicas'),
    ('esferas', 'Esferas', 'especiais', 'tecnicas'),
    ('lencois', 'Lençóis', 'especiais', 'tecnicas'),
    ('rotores', 'Rotores', 'especiais', 'tecnicas'),
    ('revestimento-rodas', 'Revestimento de rodas para empilhadeiras e carros industriais', 'revestimentos', 'revestimentos'),
    ('revestimento-cilindros-silos-calhas', 'Revestimentos de cilindros, silos e calhas', 'revestimentos', 'revestimentos'),
    ('defensas-portuarias', 'Defensas portuárias', 'revestimentos', 'tecnicas'),
    ('manchetas', 'Manchetas de poliuretano', 'industriais', 'poliuretano'),
]

for slug, name, line, category in ADDITIONAL_PRODUCTS:
    PRODUCTS.append(dict(slug=slug, name=name, line=line, category=category, image=None,
                         source=CATALOG_SOURCE,
                         description=f'{name}: item do portfólio TOPPUR. Envie desenho, amostra ou dimensões e informe a aplicação para consultar materiais, possibilidades de fabricação e orçamento.'))

next(p for p in PRODUCTS if p['slug'] == 'coxins').update(
    image='COXIM-BORRACHA.jpg',
    source='https://toppur.com.br/coxim-de-borracha/',
    description='Coxins de borracha sob medida para absorver impactos e reduzir vibrações em equipamentos. A TOPPUR apresenta modelos cilíndricos, tipo batente, automotivos e com insertos metálicos. Consulte dimensões e composição para sua aplicação.')
next(p for p in PRODUCTS if p['slug'] == 'gaxetas').update(
    image='gaxeta-em-borracha-e-poliuretano.jpg',
    source='https://toppur.com.br/gaxeta-em-borracha-e-poliuretano-vedacao-industrial/',
    description='Gaxetas de borracha e poliuretano para vedação de sistemas hidráulicos, pneumáticos e industriais. Desenvolvidas conforme dimensões, material e aplicação. Informe as condições de trabalho para avaliação técnica.')

# Origem, autoria e licença das fotos pesquisadas ficam junto do catálogo.
PHOTO_SOURCES = json.loads(Path(__file__).with_name('photo_sources.json').read_text(encoding='utf-8'))
for product in PRODUCTS:
    photo = PHOTO_SOURCES.get(product['slug'])
    if photo:
        product['image'] = photo['image']
        product['photo'] = photo

SEGMENTS = ['Concretagem e construção civil', 'Alimentos e bebidas', 'Automobilístico e off-road', 'Agrícola', 'Frigorífico', 'Ferroviário', 'Saneamento básico', 'Petróleo, gás e óleo', 'Cartonagem e embalagem', 'Revestimentos', 'Siderurgia e mineração', 'Vidreiro']
