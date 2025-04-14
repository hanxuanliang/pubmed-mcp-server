from fastapi import FastAPI, Query
from typing import Optional, List
from pydantic import BaseModel

from service.search import esearch


app = FastAPI(
    title="pubmed fetch API",
    description="pubmed fetch API",
    version="0.1.0",
)


class SearchTermResp(BaseModel):
    total: int
    page_size: int
    id_list: List[str]


@app.get("/search", response_model=SearchTermResp, operation_id="search_pubmed")
async def search_pubmed(
    term: str = Query(..., description="The search term to query PubMed"),
    retmax: Optional[int] = Query(
        20, description="Maximum number of results to return (default: 20)"
    ),
):
    """Search PubMed for articles matching the given term.

    Returns a list of PubMed IDs along with count and retmax information.
    """
    result = esearch(term=term, retmax=retmax)
    return result
