from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass(frozen=True)
class Source:
    name: str
    url: str
    document_type: str


OFFICIAL_SOURCES = [
    Source("CONITEC", "https://www.gov.br/conitec/pt-br", "Diretriz"),
    Source("BVSMS", "https://bvsms.saude.gov.br/", "PCDT"),
]


def _seed_documents() -> list[dict[str, Any]]:
    today = date.today().isoformat()
    return [
        {
            "source_url": "seed://pcdt-diabetes",
            "title": "PCDT Diabetes Mellitus Tipo 2",
            "document_type": "PCDT",
            "published_at": today,
            "content": "Manejo clinico do diabetes mellitus tipo 2 no SUS com foco em tratamento e monitoramento.",
        },
        {
            "source_url": "seed://ddt-hipertensao",
            "title": "DDT Hipertensao Arterial Sistemica",
            "document_type": "DDT",
            "published_at": today,
            "content": "Diretriz diagnostica e terapeutica para hipertensao arterial no contexto da atencao primaria.",
        },
    ]


def sync_documents() -> list[dict[str, Any]]:
    # MVP: retorna seeds locais para garantir fluxo funcional mesmo sem conectividade externa.
    return _seed_documents()
