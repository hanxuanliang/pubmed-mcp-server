from pathlib import Path
import requests

from service import BASE_PDF_URL, HEADERS
from core.config import get_settings


def earticle_pdf(pmc_id: str) -> bytes:
    """Download a PDF article from PMC and save it to the configured output path.

    Args:
        pmc_id (str): The PMC ID of the article.

    Returns:
        str: The path to the saved PDF file.
    """
    response = requests.get(BASE_PDF_URL.format(pmc_id=pmc_id), headers=HEADERS)
    response.raise_for_status()
    return response.content


def earticle_pdf_local(pmc_id: str, download_path: str = None) -> str:
    """Download a PDF article from PMC and save it to the configured output path.

    Args:
        pmc_id (str): The PMC ID of the article.
        download_path (str, optional): Custom download path to save the file. Defaults to None.

    Returns:
        str: The path to the saved PDF file.
    """
    filename = f"{pmc_id}.pdf"

    if download_path is None:
        settings = get_settings()
        output_file = Path(settings.download_path) / filename
    else:
        output_file = Path(download_path) / filename

    output_file.parent.mkdir(parents=True, exist_ok=True)

    content = earticle_pdf(pmc_id)
    with open(output_file, "wb") as f:
        f.write(content)

    return str(output_file)


if __name__ == "__main__":
    print(earticle_pdf("PMC11901808"))
