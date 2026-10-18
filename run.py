"""Servidor WSGI para Windows e Linux: python run.py."""
import os

from app import app


def main():
    from waitress import serve

    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', '3030'))
    print(f'TOPPUR: http://{host}:{port}', flush=True)
    serve(app, host=host, port=port, threads=4)


if __name__ == '__main__':
    main()
