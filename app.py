import os
import re
import secrets
import sqlite3
from contextlib import closing
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode

from flask import Flask, abort, redirect, render_template, request, session, url_for, send_from_directory
from dotenv import load_dotenv

from catalog import CATEGORIES, LINES, PRODUCTS, SEGMENTS

load_dotenv(Path(__file__).with_name('.env'))


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or secrets.token_hex(32),
        DATABASE=str(Path(app.instance_path) / 'orcamentos.sqlite3'),
        MAX_CONTENT_LENGTH=32 * 1024,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
    )
    if test_config:
        app.config.update(test_config)
    Path(app.instance_path).mkdir(exist_ok=True)
    with closing(sqlite3.connect(app.config['DATABASE'])) as db:
        db.execute('''CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY, created_at TEXT NOT NULL,
            name TEXT NOT NULL, phone TEXT NOT NULL, email TEXT,
            material TEXT NOT NULL, message TEXT NOT NULL)''')

    @app.context_processor
    def shared():
        session.setdefault('csrf_token', secrets.token_urlsafe(32))
        return dict(categories=CATEGORIES, lines=LINES, segments=SEGMENTS,
                    year=datetime.now().year, csrf_token=session['csrf_token'])

    @app.get('/')
    def home():
        return render_template('home.html', products=PRODUCTS[:4], title='Precisão que move a indústria')

    @app.get('/catalogos/concretagem')
    def catalog_pdf():
        return send_from_directory(
            Path(app.static_folder) / 'catalogos', 'TOPPUR-CONCRETAGEM.pdf',
            mimetype='application/pdf', as_attachment=request.args.get('download') == '1',
            download_name='TOPPUR-CONCRETAGEM.pdf', conditional=True,
        )

    @app.get('/produtos')
    def products():
        category = request.args.get('categoria', '')
        line = request.args.get('linha', '')
        query = request.args.get('q', '').strip()[:100]
        if category and category not in CATEGORIES:
            abort(404)
        if line and line not in LINES:
            abort(404)
        items = [p for p in PRODUCTS if (not category or p['category'] == category)
                 and (not line or p['line'] == line)
                 and (not query or query.casefold() in (p['name'] + ' ' + p['description']).casefold())]
        return render_template('products.html', products=items, category=category, line=line, query=query,
                               title='Nossos produtos')

    @app.get('/produtos/<slug>')
    def product(slug):
        item = next((p for p in PRODUCTS if p['slug'] == slug), None)
        if not item:
            abort(404)
        related = [p for p in PRODUCTS if p['line'] == item['line'] and p != item][:3]
        return render_template('product.html', product=item, products=related, title=item['name'])

    @app.get('/segmentos')
    def segments():
        return render_template('segments.html', title='Segmentos industriais')

    @app.get('/sobre')
    def about():
        return render_template('about.html', title='Sobre a TOPPUR')

    @app.route('/contato', methods=['GET', 'POST'])
    def contact():
        values = request.form if request.method == 'POST' else request.args
        errors = []
        if request.method == 'POST':
            token = request.form.get('csrf_token', '')
            if not token or not secrets.compare_digest(token, session.get('csrf_token', '')):
                abort(400, description='Atualize a página e tente novamente.')
            data = {key: request.form.get(key, '').strip() for key in ('name', 'phone', 'email', 'material', 'message')}
            if not 2 <= len(data['name']) <= 120:
                errors.append('Informe seu nome, entre 2 e 120 caracteres.')
            if not 10 <= len(re.sub(r'\D', '', data['phone'])) <= 13 or len(data['phone']) > 30:
                errors.append('Informe um telefone válido com DDD.')
            if data['email'] and (len(data['email']) > 254 or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', data['email'])):
                errors.append('Informe um e-mail válido.')
            if data['material'] not in CATEGORIES.values() and data['material'] != 'Projeto sob medida':
                errors.append('Selecione uma solução válida.')
            if not 10 <= len(data['message']) <= 4000:
                errors.append('Descreva sua necessidade usando entre 10 e 4.000 caracteres.')
            if not errors:
                with closing(sqlite3.connect(app.config['DATABASE'])) as db:
                    cursor = db.execute('INSERT INTO quotes (created_at,name,phone,email,material,message) VALUES (?,?,?,?,?,?)',
                        (datetime.now().isoformat(), *(data[k] for k in ('name', 'phone', 'email', 'material', 'message'))))
                    quote_id = cursor.lastrowid
                    db.commit()
                session['quote_id'] = quote_id
                return redirect(url_for('confirmation'), code=303)
        return render_template('contact.html', title='Contato e orçamento', values=values, errors=errors), (422 if errors else 200)

    @app.get('/orcamento/confirmacao')
    def confirmation():
        quote_id = session.get('quote_id')
        if not quote_id:
            return redirect(url_for('contact'))
        with closing(sqlite3.connect(app.config['DATABASE'])) as db:
            db.row_factory = sqlite3.Row
            row = db.execute('SELECT * FROM quotes WHERE id = ?', (quote_id,)).fetchone()
        if row is None:
            return redirect(url_for('contact'))
        quote = dict(row)
        message = (f"Olá, TOPPUR! Solicitação #{quote['id']}\nNome: {quote['name']}\n"
                   f"Telefone: {quote['phone']}\nE-mail: {quote['email']}\n"
                   f"Solução: {quote['material']}\n\n{quote['message']}")
        return render_template('confirmation.html', title='Solicitação registrada', quote=quote,
                               whatsapp='https://wa.me/5511991632077?' + urlencode({'text': message}))

    @app.errorhandler(404)
    @app.errorhandler(400)
    @app.errorhandler(413)
    def error(error):
        return render_template('error.html', title='Página indisponível', error=error), error.code

    @app.after_request
    def headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        return response

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host=os.environ.get('HOST', '127.0.0.1'), port=int(os.environ.get('PORT', 3030)), debug=False)
