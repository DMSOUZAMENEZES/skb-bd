from sqlite3 import Row

from database import search_documents


def run_search(query: str, limit: int = 10) -> list[Row]:
    return search_documents(query=query, limit=limit)
