import sqlite3
import tempfile
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from html import unescape
import re
from contextlib import closing

from app import create_app
from catalog import PRODUCTS


class SiteTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.database = str(Path(self.directory.name) / 'test.sqlite3')
        self.app = create_app({'TESTING': True, 'SECRET_KEY': 'test-key', 'DATABASE': self.database})
        self.client = self.app.test_client()

    def tearDown(self):
        self.directory.cleanup()

    def token(self):
        self.client.get('/contato')
        with self.client.session_transaction() as session:
            return session['csrf_token']

    def valid_data(self):
        return dict(csrf_token=self.token(), name='João da Silva', phone='11999999999',
                    email='joao@example.com', material='Peças em poliuretano',
                    message='Preciso de vinte buchas para equipamento industrial.')

    def test_pages_images_and_encoding(self):
        for path in ['/', '/produtos', '/segmentos', '/sobre', '/contato']:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, path)
            self.assertIn('POLIURETANO, BORRACHA E PLÁSTICOS', response.get_data(as_text=True))
        for product in PRODUCTS:
            self.assertEqual(self.client.get('/produtos/' + product['slug']).status_code, 200)
            if product['image']:
                with self.client.get('/static/assets/' + product['image']) as image:
                    self.assertEqual(image.status_code, 200)

    def test_catalog_pdf_inline_download_and_range(self):
        with self.client.get('/catalogos/concretagem') as response:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.mimetype, 'application/pdf')
            self.assertTrue(response.headers['Content-Disposition'].startswith('inline'))
            self.assertTrue(response.data.startswith(b'%PDF-'))
        with self.client.get('/catalogos/concretagem?download=1') as response:
            self.assertTrue(response.headers['Content-Disposition'].startswith('attachment'))
        with self.client.get('/catalogos/concretagem', headers={'Range': 'bytes=0-9'}) as response:
            self.assertEqual(response.status_code, 206)
            self.assertEqual(len(response.data), 10)
        for route in ['/', '/produtos', '/produtos/concretagem']:
            self.assertIn('/catalogos/concretagem', self.client.get(route).get_data(as_text=True))

    def test_search_category_and_missing(self):
        html = self.client.get('/produtos?categoria=borracha').get_data(as_text=True)
        self.assertIn('Vedações em borracha', html)
        self.assertNotIn('href="/produtos/placas-tarugos"', html)
        html = self.client.get('/produtos?q=tarugos').get_data(as_text=True)
        self.assertIn('href="/produtos/placas-tarugos"', html)
        self.assertNotIn('href="/produtos/ventosas"', html)
        self.assertIn('Nenhum produto encontrado', self.client.get('/produtos?q=inexistente').get_data(as_text=True))
        for path in ['/produtos/inexistente', '/produtos?categoria=invalida', '/inexistente']:
            self.assertEqual(self.client.get(path).status_code, 404)

    def test_expanded_catalog_lines_and_photos(self):
        self.assertEqual(len({p['slug'] for p in PRODUCTS}), len(PRODUCTS))
        required = {'acoplamentos', 'arruelas', 'batentes', 'calcos', 'coxins',
                    'gaxetas', 'hidrociclones', 'juntas', 'passa-fios', 'polias',
                    'rolos', 'sapatas', 'tubos', 'tiras', 'buchas-automotivas',
                    'coifas', 'sedes-valvulas', 'valvulas', 'diafragmas', 'discos',
                    'difusores', 'esferas', 'lencois', 'rotores', 'defensas-portuarias',
                    'revestimento-rodas', 'revestimento-cilindros-silos-calhas', 'manchetas'}
        self.assertTrue(required.issubset({p['slug'] for p in PRODUCTS}))
        html = self.client.get('/produtos?linha=automotiva').get_data(as_text=True)
        self.assertIn('href="/produtos/coifas"', html)
        self.assertNotIn('href="/produtos/arruelas"', html)
        self.assertEqual(self.client.get('/produtos?linha=invalida').status_code, 404)
        html = self.client.get('/produtos?linha=automotiva&categoria=borracha').get_data(as_text=True)
        self.assertIn('Nenhum produto encontrado', html)
        html = self.client.get('/produtos/esferas').get_data(as_text=True)
        self.assertIn('PEÇA TÉCNICA SOB CONSULTA', html)
        self.assertNotIn('assets/None', html)

    def test_researched_photos_and_attribution(self):
        from catalog import PHOTO_SOURCES
        self.assertEqual(len(PHOTO_SOURCES), 24)
        self.assertEqual(sum(bool(p['image']) for p in PRODUCTS), 38)
        for slug, photo in PHOTO_SOURCES.items():
            with self.client.get('/static/assets/' + photo['image']) as response:
                self.assertEqual(response.status_code, 200)
            html = self.client.get('/produtos/' + slug).get_data(as_text=True)
            self.assertIn(photo['page'].replace('&', '&amp;'), html)
            if photo['illustrative']:
                self.assertIn('Imagem ilustrativa', html)
                self.assertIn(photo['license'], html)

    def test_quote_saved_and_whatsapp_encoded(self):
        data = self.valid_data()
        data['message'] += '\nTeste & medidas: 20 mm.'
        response = self.client.post('/contato', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('Seu pedido foi registrado.', html)
        link = re.search(r'href="(https://wa.me/5511991632077\?[^\"]+)"', html).group(1)
        message = parse_qs(urlparse(unescape(link)).query)['text'][0]
        self.assertIn(data['message'], message)
        with closing(sqlite3.connect(self.database)) as db:
            record = db.execute('SELECT name,message FROM quotes').fetchone()
        self.assertEqual(record, (data['name'], data['message']))

    def test_validation_csrf_and_private_confirmation(self):
        self.assertEqual(self.client.post('/contato', data={}).status_code, 400)
        data = self.valid_data()
        data.update(phone='123', email='invalid', message='curto')
        self.assertEqual(self.client.post('/contato', data=data).status_code, 422)
        with closing(sqlite3.connect(self.database)) as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM quotes').fetchone()[0], 0)
        self.assertEqual(self.app.test_client().get('/orcamento/confirmacao').status_code, 302)

    def test_escaping_and_cookie_size(self):
        data = self.valid_data()
        data['name'] = '<script>alert(1)</script>'
        data['message'] = 'Descrição ' * 390
        response = self.client.post('/contato', data=data)
        self.assertLess(len(response.headers.get('Set-Cookie', '')), 1000)
        html = self.client.get('/orcamento/confirmacao').get_data(as_text=True)
        self.assertNotIn('<script>alert(1)</script>', html)
        self.assertIn('&lt;script&gt;', html)


if __name__ == '__main__':
    unittest.main()
