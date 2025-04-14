import pytest
from unittest.mock import patch, MagicMock

from service import build_pubmed_search_url, BASE_URL
from service.search import esearch, parse_esearch_resp


def test_build_pubmed_search_url_basic():
    """Test basic search URL construction with minimal parameters."""
    url = build_pubmed_search_url(term="test query")
    assert "db=pubmed" in url
    assert "term=test+query" in url
    assert "retmode=xml" in url
    assert "retmax=20" in url
    assert url.startswith(BASE_URL)


def test_build_pubmed_search_url_all_params():
    """Test URL construction with all parameters."""
    url = build_pubmed_search_url(
        term="test",
        retstart=10,
        retmax=50,
        rettype="uilist",
        retmode="json",
        sort="pub_date",
        field="title",
        datetype="pdat",
        reldate=30,
        mindate="2023/01/01",
        maxdate="2023/12/31"
    )

    assert "db=pubmed" in url
    assert "term=test" in url
    assert "retstart=10" in url
    assert "retmax=50" in url
    assert "rettype=uilist" in url
    assert "retmode=json" in url
    assert "sort=pub_date" in url
    assert "field=title" in url
    assert "datetype=pdat" in url
    assert "reldate=30" in url
    assert "mindate=2023%2F01%2F01" in url
    assert "maxdate=2023%2F12%2F31" in url


def test_build_pubmed_search_url_special_characters():
    """Test URL encoding of special characters in search term."""
    url = build_pubmed_search_url(term="woody plant AND sucrose")
    assert "term=woody+plant+AND+sucrose" in url


def test_build_pubmed_search_url_date_validation():
    """Test that providing only one date parameter doesn't include either in URL."""
    url = build_pubmed_search_url(term="test", mindate="2023/01/01")
    assert "mindate" not in url
    assert "maxdate" not in url

    url = build_pubmed_search_url(term="test", maxdate="2023/12/31")
    assert "mindate" not in url
    assert "maxdate" not in url


@pytest.mark.parametrize("sort_option", ["pub_date", "Author", "JournalName", "relevance"])
def test_build_pubmed_search_url_sort_options(sort_option):
    """Test all valid sort options."""
    url = build_pubmed_search_url(term="test", sort=sort_option)
    assert f"sort={sort_option}" in url


@pytest.mark.parametrize("retmode", ["xml", "json"])
def test_build_pubmed_search_url_retmode_options(retmode):
    """Test all valid retmode options."""
    url = build_pubmed_search_url(term="test", retmode=retmode)
    assert f"retmode={retmode}" in url


def test_build_pubmed_search_url_retmax_limit():
    """Test with maximum retmax value."""
    url = build_pubmed_search_url(term="test", retmax=10000)
    assert "retmax=10000" in url


@patch('requests.get')
def test_esearch(mock_get):
    """Test the esearch function."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.text = '<eSearchResult><Count>10</Count><RetMax>10</RetMax><IdList><Id>12345</Id></IdList></eSearchResult>'
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    # Call the function
    result = esearch(term="test query", retmax=10)

    # Assertions
    mock_get.assert_called_once()
    assert "test+query" in mock_get.call_args[0][0]
    assert "retmax=10" in mock_get.call_args[0][0]
    assert result == {"count": 10, "retmax": 10, "id_list": ["12345"]}


def test_parse_esearch_resp():
    """Test the parse_esearch_resp function."""
    # Sample XML response
    xml_str = '''
    <eSearchResult>
        <Count>5</Count>
        <RetMax>3</RetMax>
        <IdList>
            <Id>12345</Id>
            <Id>67890</Id>
            <Id>54321</Id>
        </IdList>
    </eSearchResult>
    '''

    # Parse the response
    result = parse_esearch_resp(xml_str)

    # Assertions
    assert result["count"] == 5
    assert result["retmax"] == 3
    assert result["id_list"] == ["12345", "67890", "54321"]
