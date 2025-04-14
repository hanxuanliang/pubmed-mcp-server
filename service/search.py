import requests
from lxml import etree

from service import build_pubmed_search_url


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


def parse_esearch_resp(xml_str: str) -> dict:
    """Parse PubMed ESearch XML response.

    Returns:
        dict: Contains total, page_size and id_list
    """
    root = etree.fromstring(xml_str.encode("utf-8"))

    count = int(root.findtext("Count", "0"))
    retmax = int(root.findtext("RetMax", "0"))
    id_list = [id_elem.text for id_elem in root.findall("IdList/Id")]

    return {"total": count, "page_size": retmax, "id_list": id_list}
