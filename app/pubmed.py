from fastapi import FastAPI, Query
from typing import Optional, List
from pydantic import BaseModel

from service.file import earticle_pdf_local
from service.search import esearch, einfo


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
    """
    Search PubMed for articles matching the given term.
    Returns a list of PubMed IDs along with count and retmax information.
    """
    result = esearch(term=term, retmax=retmax)
    return result


class ArticleInfoResp(BaseModel):
    url: str
    title: str
    abstract: str
    authors: List[str]
    date_revised: str
    keywords: List[str]
    pmc_id: str


@app.get("/einfo", response_model=ArticleInfoResp, operation_id="einfo_pubmed")
async def einfo_pubmed(
    pmid: str = Query(..., description="The PubMed ID to query PubMed metadata"),
):
    """
    Get metadata for a given PubMed ID.
    Returns metadata from the PubMed response.
    """
    result = einfo(pmid=pmid)
    return result


class DownloadResp(BaseModel):
    file_path: str


@app.get("/download", response_model=DownloadResp, operation_id="earticle_download")
async def earticle_download(
    pmc_id: str = Query(..., description="The PMC ID of the article"),
):
    """
    Download a PDF article from PMC and save it to the configured output path.
    Returns the path to the saved PDF file.
    """
    file_path = earticle_pdf_local(pmc_id=pmc_id)

    return {"file_path": file_path}
