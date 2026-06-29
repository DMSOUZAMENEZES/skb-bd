# SKB-BD

MVP simplificado da base de conhecimento para documentos do SUS, iniciado por pasta local.

## Fluxo atual (fase inicial)

1. Inicializa SQLite (`documents`)
2. Importa PDFs de `storage/import`
3. Extrai texto para `storage/text`
4. Cadastra metadados e texto no banco
5. Pesquisa com `LIKE`

## Estrutura

- `app.py`: CLI
- `database.py`: esquema e consultas SQLite
- `importer.py`: importação de PDFs locais
- `parser.py`: extração de texto de PDFs
- `storage/import`: entrada manual de PDFs
- `storage/pdf`: PDFs normalizados por hash
- `storage/text`: textos extraídos por hash
- `storage/skb.db`: banco SQLite

## Comandos

```bash
python app.py init-db
python app.py import
python app.py search "diabetes"
```
