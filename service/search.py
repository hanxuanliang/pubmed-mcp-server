import requests
from lxml import etree

from service import build_pubmed_search_url, BASE_META_URL


def esearch(term: str, retmax: int = 20) -> dict:
    """Search PubMed for a given term and return the parsed result.

    Args:
        term (str): The search term.
        retmax (int, optional): Maximum number of results to return. Defaults to 20.

    Returns:
        dict: Contains total, page_size and id_list from the PubMed response.
    """
    url = build_pubmed_search_url(term, retmax=retmax)
    response = requests.get(url)
    response.raise_for_status()
    return parse_esearch_resp(response.text)


def einfo(pmid: str) -> dict:
    """Get metadata for a given PubMed ID.

    Args:
        pmid (str): The PubMed ID.

    Returns:
        dict: Contains metadata from the PubMed response.
    """
    response = requests.get(BASE_META_URL.format(pmid=pmid))
    response.raise_for_status()

    xml_dict = parse_einfo_resp(response.text)
    return {"url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}", **xml_dict}


def parse_esearch_resp(xml_str: str) -> dict:
    root = etree.fromstring(xml_str.encode("utf-8"))

    count = int(root.findtext("Count", "0"))
    retmax = int(root.findtext("RetMax", "0"))
    id_list = [id_elem.text for id_elem in root.findall("IdList/Id")]

    return {"total": count, "page_size": retmax, "id_list": id_list}


def parse_einfo_resp(xml_str: str) -> dict:
    """Parse the XML response from PubMed einfo API.

    Example XML structure:
    <DateRevised>
        <Year>2025</Year>
        <Month>03</Month>
        <Day>19</Day>
    </DateRevised>

    <ArticleTitle>...</ArticleTitle>
    <Abstract><AbstractText>...</AbstractText></Abstract>
    <AuthorList CompleteYN="Y"><Author>...</Author></AuthorList>
    """
    root = etree.fromstring(xml_str.encode("utf-8"))

    # Extract title and abstract using itertext() to get all nested text content
    title_elem = root.find(".//ArticleTitle")
    title = (
        " ".join("".join(title_elem.itertext()).split())
        if title_elem is not None
        else "No title available"
    )

    abstract_elem = root.find(".//AbstractText")
    abstract = (
        " ".join("".join(abstract_elem.itertext()).split())
        if abstract_elem is not None
        else "No abstract available"
    )

    date_revised = ""
    date_elem = root.find(".//DateRevised")
    if date_elem is not None:
        date_info = {
            "year": date_elem.findtext("Year"),
            "month": date_elem.findtext("Month"),
            "day": date_elem.findtext("Day"),
        }
        date_revised = f"{date_info['year']}-{date_info['month']}-{date_info['day']}"

    # Process authors with more details
    author_elems = root.findall(".//Author")
    authors = [
        f"{author.findtext('LastName', '')} {author.findtext('ForeName', '')}".strip()
        for author in author_elems
    ]

    # Extract keywords
    keywords = [keyword.text for keyword in root.findall(".//Keyword") if keyword.text]

    return {
        "title": title,
        "abstract": abstract,
        "authors": authors,
        "date_revised": date_revised,
        "keywords": keywords,
    }


if __name__ == "__main__":
    print(einfo("40094832"))
