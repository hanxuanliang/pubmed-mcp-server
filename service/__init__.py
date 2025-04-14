import urllib.parse
from typing import Optional, Literal

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
BASE_META_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&retmode=xml"


def build_pubmed_search_url(
    term: str,
    retstart: Optional[int] = None,
    retmax: Optional[int] = 20,  # Default is 20, PubMed max is 10000
    rettype: Optional[Literal["uilist", "count"]] = None,
    retmode: Optional[Literal["xml", "json"]] = "xml",
    sort: Optional[Literal["pub_date", "Author", "JournalName", "relevance"]] = None,
    field: Optional[str] = None,
    datetype: Optional[Literal["mdat", "pdat", "edat"]] = None,
    reldate: Optional[int] = None,
    mindate: Optional[str] = None,  # Format: YYYY/MM/DD, YYYY/MM, YYYY
    maxdate: Optional[str] = None,  # Format: YYYY/MM/DD, YYYY/MM, YYYY
) -> str:
    """
    Constructs a URL for the NCBI ESearch utility (primarily for PubMed).

    Args:
        term: The search query string.
        retstart: Index of the first UID to retrieve (default: 0).
        retmax: Maximum number of UIDs to retrieve (default: 20, PubMed max: 10000).
        rettype: Retrieval type ('uilist' or 'count').
        retmode: Retrieval mode ('xml' or 'json', default: 'xml').
        sort: Sort order for UIDs ('pub_date', 'Author', 'JournalName', 'relevance').
        field: Limit search to a specific field (e.g., 'title').
        datetype: Type of date for filtering ('mdat', 'pdat', 'edat').
        reldate: Filter results published within the last 'reldate' days.
        mindate: Start date for filtering (YYYY/MM/DD, YYYY/MM, YYYY). Requires maxdate.
        maxdate: End date for filtering (YYYY/MM/DD, YYYY/MM, YYYY). Requires mindate.

    Returns:
        The constructed ESearch URL string.
    """
    params = {
        "db": "pubmed",
        "term": term,
        "retmode": retmode,
        "retmax": retmax,
    }

    if retstart is not None:
        params["retstart"] = retstart
    if rettype is not None:
        params["rettype"] = rettype
    if sort is not None:
        params["sort"] = sort
    if field is not None:
        params["field"] = field
    if datetype is not None:
        params["datetype"] = datetype
    if reldate is not None:
        params["reldate"] = reldate
    if mindate is not None and maxdate is not None:
        params["mindate"] = mindate
        params["maxdate"] = maxdate
    elif mindate is not None or maxdate is not None:
        print(
            "Warning: Both mindate and maxdate must be provided for date range filtering."
        )

    filtered_params = {k: v for k, v in params.items() if v is not None}

    query_string = urllib.parse.urlencode(filtered_params)
    return f"{BASE_URL}?{query_string}"
