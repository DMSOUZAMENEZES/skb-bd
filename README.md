# skb-bd

## Comandos

```bash
python app.py init
python app.py import imports/
```

## Importacao local de PDFs

O comando `python app.py import imports/`:

1. Calcula o SHA-256 de cada PDF.
2. Copia os arquivos para `storage/pdf/`.
3. Registra os metadados na tabela `documents` do SQLite.
