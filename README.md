# SKB - SUS Knowledge Base

Base local pesquisavel de documentos oficiais do SUS para suporte a consulta tecnica.

## Objetivo

Construir uma base local pesquisavel de documentos oficiais (PCDT, DDT, Diretrizes e Protocolos de Uso), com sincronizacao periodica, extracao de texto e busca offline.

## Status

MVP em desenvolvimento.

## Funcionalidades do MVP

- Sincronizacao inicial de documentos (seed local e suporte a coleta HTTP simples)
- Armazenamento em SQLite
- Extracao e normalizacao basica de texto
- Pesquisa local por titulo e conteudo

## Requisitos

- Python 3.10+

## Instalacao

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Se `requirements.txt` ainda nao existir no branch, o MVP roda sem dependencias externas obrigatorias.

## Uso

```bash
python app.py sync
python app.py search "diabetes"
```

## Estrutura do Projeto

- `app.py`: CLI principal
- `database.py`: schema e operacoes SQLite
- `parser.py`: limpeza/extracao de texto
- `crawler.py`: obtencao/sincronizacao de documentos
- `search.py`: busca local
- `docs/`: documentacao de dominio (fontes e protocolos)

## Roadmap

- [x] Banco (SQLite)
- [x] Parser basico
- [x] Downloader basico
- [x] Pesquisa local
- [ ] Agente de consulta
- [ ] Relevancia avancada (ranking/FTS)
- [ ] Enriquecimento de metadados

## Documentacao de Dominio

Conteudo de fontes oficiais e classificacao de protocolos foi movido para:

- `docs/fontes-oficiais.md`
- `docs/protocolos.md`
