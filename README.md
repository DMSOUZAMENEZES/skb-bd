# SKB-BD

MVP simplificado da base de conhecimento para documentos do SUS, iniciado por pasta local.

## Fluxo atual (fase inicial)

1. Inicializa SQLite (`documents`)
2. Importa PDFs de `storage/import`
3. Extrai texto para `storage/text`
4. Cadastra metadados e texto no banco
5. Pesquisa com `LIKE`

## Fluxo atual (próximo item)

6. Descobre URLs de PDFs da CONITEC (sem download automático)

## Estrutura

- `app.py`: CLI
- `database.py`: esquema e consultas SQLite
- `crawler.py`: descoberta de links PDF da CONITEC
- `importer.py`: importação de PDFs locais
- `parser.py`: extração de texto de PDFs
- `storage/import`: entrada manual de PDFs
- `storage/pdf`: PDFs normalizados por hash
- `storage/text`: textos extraídos por hash
- `storage/skb.db`: banco SQLite
- `storage/crawl/conitec_pdfs.txt`: manifesto de URLs PDF descobertas

## Comandos

```bash
python app.py init-db
python app.py import
python app.py search "diabetes"
python app.py crawl-conitec
```
