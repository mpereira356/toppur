# TOPPUR — Python / Flask

Site institucional com catálogo de 41 entradas, busca por produto, filtros por linha e material, páginas de segmentos e empresa, formulário com SQLite e atendimento pelo WhatsApp. Fontes, imagens e PDF ficam no próprio projeto.

## Executar no Linux — porta 3030

Pré-requisitos: Git, Python 3.10 ou superior e suporte a venv. Em Ubuntu/Debian, instale com `sudo apt install git python3 python3-venv`.

```bash
git clone https://github.com/mpereira356/toppur.git
cd toppur
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
.venv/bin/python -c "import secrets; from pathlib import Path; p=Path('.env'); p.write_text(p.read_text().replace('SECRET_KEY=', 'SECRET_KEY='+secrets.token_hex(32), 1))"
chmod 600 .env
.venv/bin/python run.py
```

Acesse **http://IP_DO_SERVIDOR:3030**. O `run.py` usa Waitress, escuta em `0.0.0.0` e mantém depuração desativada. Se houver firewall ou regra de rede no provedor, permita a porta TCP 3030 para o público desejado. Para um domínio com HTTPS, coloque o servidor atrás de um proxy reverso.

As variáveis `HOST`, `PORT` e `SECRET_KEY` são carregadas de `.env`. Variáveis já definidas no ambiente têm prioridade. Preserve a chave ao reiniciar para manter sessões válidas. Nunca envie `.env` ou a base de pedidos ao GitHub.

## Manter o site rodando como serviço no Linux

O exemplo em `deploy/toppur.service` pressupõe o projeto em `/opt/toppur` e um usuário de serviço chamado `toppur`. Após preparar o ambiente virtual e o `.env` nesse diretório:

```bash
sudo useradd --system --home-dir /opt/toppur --shell /usr/sbin/nologin toppur
sudo mkdir -p /opt/toppur/instance
sudo chown toppur:toppur /opt/toppur/instance
sudo chown root:toppur /opt/toppur/.env
sudo chmod 640 /opt/toppur/.env
sudo cp /opt/toppur/deploy/toppur.service /etc/systemd/system/toppur.service
sudo systemctl daemon-reload
sudo systemctl enable --now toppur
sudo systemctl status toppur
```

Se o usuário `toppur` já existir, pule o `useradd`. O usuário do serviço precisa conseguir ler o código, as imagens, o PDF e o ambiente virtual. Apenas `instance/` precisa ser gravável para os pedidos. Ajuste caminhos e usuário no arquivo de serviço caso seu diretório seja outro.

Para consultar logs: `sudo journalctl -u toppur -f`.

## Alternativa com Docker Compose

Com Docker e Compose instalados, clone o projeto e prepare o `.env` com a chave como acima. Em seguida:

```bash
docker compose up -d --build
docker compose logs -f web
```

O acesso também é pela porta **3030**. Os pedidos persistem no volume `toppur_data`, fora da imagem. Não execute `docker compose down -v` se quiser preservar esses dados.

## Executar no Windows

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python -c "import secrets; print(secrets.token_hex(32))"
# Cole a chave gerada em SECRET_KEY no arquivo .env.
.\.venv\Scripts\python run.py
```

Acesse **http://127.0.0.1:3030**. Para desenvolvimento local, `python app.py` também usa a porta 3030, com o servidor de desenvolvimento do Flask.

## Catálogo PDF

O arquivo fornecido `static/catalogos/TOPPUR-CONCRETAGEM.pdf` tem 16 páginas e atualização indicada em março de 2026. A imagem principal da home abre o PDF. Home, catálogo de produtos e a peça “Linha de concretagem” também dão acesso ao arquivo.

- Visualizar: `/catalogos/concretagem`
- Baixar: `/catalogos/concretagem?download=1`
- O arquivo é servido localmente, com suporte a requisições parciais para leitores de PDF.

## Atualizar no servidor

```bash
cd /opt/toppur
git pull --ff-only
.venv/bin/python -m pip install -r requirements.txt
sudo systemctl restart toppur
```

Com Docker, após `git pull --ff-only`, use `docker compose up -d --build`. Faça backup do banco antes de atualizações.

## Conteúdo e pedidos

- `catalog.py`: produtos, descrições, linhas e segmentos. `templates/`: páginas. `static/site.css`: identidade visual.
- `static/fonts/`: fontes locais e respectivas licenças. `static/assets/`: fotografias.
- `photo_sources.json`: origem e créditos das 24 fotos pesquisadas; 17 são da biblioteca TOPPUR e 7 são referências externas identificadas como ilustrativas. As páginas dos produtos exibem os créditos e as licenças dessas referências.
- 38 das 41 entradas têm fotografia. Sapatas, difusores e esferas seguem com apresentação tipográfica até haver fotos adequadas.
- O formulário valida os campos no servidor, usa proteção CSRF e salva em `instance/orcamentos.sqlite3`, criado automaticamente. Faça backup desse arquivo ou do volume Docker.
- O cliente pode encaminhar o pedido pelo WhatsApp na confirmação. O registro local não envia e-mail nem notifica automaticamente a equipe. Não há painel administrativo nem listagem pública de pedidos.
- `.env`, SQLite, caches, capturas e a versão estática antiga são ignorados pelo Git. Este repositório contém a aplicação Flask que deve ser executada no Linux.

## Verificações

```bash
.venv/bin/python -m unittest discover -s tests -v
```

Os testes verificam catálogo, páginas, busca, imagens, créditos, PDF, validação, CSRF, persistência e WhatsApp. O GitHub Actions executa esses testes em Linux a cada push e pull request.

Verificação opcional no navegador: com Playwright e Chrome disponíveis e o site rodando, execute `python tests/browser_qa.py`. Use `QA_ORIGIN` para alterar a URL; o padrão é `http://127.0.0.1:3030`. As capturas ficam em `.qa/`.
