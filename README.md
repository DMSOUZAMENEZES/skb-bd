# Diretrizes e Protocolos SUS

Repositório de referência rápida para organizar informações sobre **Protocolos Clínicos e Diretrizes Terapêuticas (PCDT)**, **Diretrizes Diagnósticas e Terapêuticas (DDT)**, **Diretrizes Nacionais/Brasileiras** e **Protocolos de Uso** relacionados ao Sistema Único de Saúde (SUS).

> Este material é informativo e não substitui os documentos oficiais do Ministério da Saúde, a avaliação clínica individual ou as normas vigentes publicadas em portarias.

## Estado atual

- `database.py` implementado: cria `data/skb.db` com tabela `documents` e diretórios `storage/pdf`, `storage/text`, `imports`
- `app.py` implementado: comando `init` funcional via `python app.py init`
- Comandos `sync`, `search` e `ask` ainda não implementados

## Próxima tarefa

Implementar `sync`: descobrir documentos novos na página da CONITEC, baixar PDFs e registrar na tabela `documents`.

**Blocker crítico desta etapa:** `sync` precisa estar funcional antes de qualquer trabalho em `search` ou `ask`.

## Critérios de Aceitação

### `sync`

- Descobre e baixa pelo menos 10 documentos PDF da CONITEC sem erros
- Registra cada documento na tabela `documents` com `filename` e `imported_at`
- Não duplica documentos já existentes (reexecução idempotente)
- Conclui para uma base de até 500 documentos em menos de 10 minutos

### `search`

- Retorna resultados em menos de 500 ms para uma base com até 500 documentos
- Usa SQLite FTS5 como motor de busca
- Retorna ao menos o `filename` e um trecho (`snippet`) do texto relevante por resultado

### `ask`

- Usa OpenAI API para gerar a resposta
- A resposta identifica o documento-fonte (nome do arquivo ou título)
- Responde em menos de 30 segundos para consultas de texto simples
- Retorna mensagem de erro clara quando nenhum documento relevante é encontrado

## Restrições não negociáveis

- Python 3.11+
- SQLite FTS5 nativo como motor de busca (sem dependência de banco externo)
- Agente de resposta: OpenAI API
- Extração de PDF: PyMuPDF (já em `requirements.txt`)
- Sem abstrações antecipadas — só o que tem uso imediato

## Hierarquia de dependências do MVP

```
1. Descobrir documentos   ← blocker de tudo
2. Baixar PDFs novos      ← blocker de 3–6
3. Extrair texto (PDF → txt)  ← blocker de 4–6
4. Armazenar em SQLite    ← blocker de 5–6
5. Pesquisa rápida (search)   ← blocker de 6
6. Agente de resposta (ask)   ← entregável final
```

Trabalhe sempre na menor etapa desbloqueada. Não avance para uma etapa superior sem que a anterior tenha critério de aceitação satisfeito.

## Objetivo

- Centralizar links oficiais para consulta de protocolos e diretrizes do SUS.
- Padronizar um roteiro de leitura para profissionais, gestores, pesquisadores e estudantes.
- Facilitar a triagem inicial de documentos por condição clínica, tipo de diretriz e situação de publicação.

## Fontes oficiais prioritárias

| Fonte | Quando consultar | Link |
| --- | --- | --- |
| Ministério da Saúde - PCDT | Lista alfabética de documentos publicados pelo Ministério da Saúde. | <https://www.gov.br/saude/pt-br/assuntos/pcdt> |
| Conitec - Protocolos e Diretrizes | Página institucional de PCDT, DDT, Diretrizes Nacionais/Brasileiras e Protocolos de Uso. | <https://www.gov.br/conitec/pt-br/assuntos/avaliacao-de-tecnologias-em-saude/protocolos-clinicos-e-diretrizes-terapeuticas> |
| Conitec - PCDT em elaboração | Acompanhamento de protocolos em desenvolvimento ou atualização. | <https://www.gov.br/conitec/pt-br/assuntos/avaliacao-de-tecnologias-em-saude/pcdt-em-elaboracao-1> |
| Medicamentos por CID e PCDT | Apoio para relacionar CID, medicamentos e PCDT vinculados. | <https://www.gov.br/conitec/pt-br/protocolos-clinicos-e-diretrizes-terapeuticas/medicamentos-por-cid-e-pcdt> |

## Conceitos essenciais

### PCDT

Documento técnico-científico que define critérios de diagnóstico, tratamento recomendado, medicamentos e demais orientações a serem seguidas no âmbito do SUS.

### DDT

Diretriz voltada a diagnóstico e tratamento, frequentemente utilizada em temas nos quais a linha de cuidado exige parâmetros clínicos, assistenciais e terapêuticos específicos.

### Diretrizes Nacionais/Brasileiras

Documentos orientadores de boas práticas para profissionais de saúde e gestores, aplicáveis ao setor público e privado de saúde.

### Protocolos de Uso

Documentos normativos mais específicos, usados para estabelecer critérios, parâmetros e padrões de utilização de uma tecnologia em determinada doença ou condição.

## Roteiro de consulta recomendado

1. **Identifique a condição clínica** usando o nome da doença, agravo ou CID quando disponível.
2. **Pesquise primeiro nas páginas oficiais** do Ministério da Saúde e da Conitec.
3. **Confira a data de publicação e atualização** do documento antes de utilizar a recomendação.
4. **Verifique portarias associadas**, anexos e eventuais versões resumidas ou atualizadas.
5. **Confirme a situação do protocolo** quando não houver documento publicado, consultando a página de PCDT em elaboração.
6. **Registre a fonte consultada** em materiais internos, pareceres ou fluxos assistenciais.

## Modelo para catalogação local

Use a estrutura abaixo para registrar protocolos consultados:

```markdown
## Nome da condição

- Tipo de documento: PCDT | DDT | Diretriz Nacional/Brasileira | Protocolo de Uso
- Órgão responsável: Ministério da Saúde | Conitec | outro
- Data de publicação:
- Última atualização:
- Portaria relacionada:
- Link oficial:
- Observações:
```

## Boas práticas de manutenção

- Revisar links e datas periodicamente, pois protocolos podem ser atualizados.
- Preferir sempre URLs oficiais `gov.br` ou publicações normativas vinculadas.
- Não copiar recomendações clínicas para fora de contexto; mantenha referência ao documento completo.
- Indicar claramente quando um protocolo estiver em elaboração, consulta pública ou atualização.

## Aviso de uso

Este repositório não fornece aconselhamento médico. Decisões clínicas devem ser tomadas por profissionais habilitados, com base no documento oficial vigente, nas necessidades do paciente e nas normas do SUS aplicáveis.
