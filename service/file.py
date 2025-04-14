from pathlib import Path
import requests

from service import BASE_PDF_URL, HEADERS
from core.config import get_settings


def earticle_pdf(pmc_id: str) -> str:
    """Download a PDF article from PMC and save it to the configured output path.

    Args:
        pmc_id (str): The PMC ID of the article.

    Returns:
        str: The path to the saved PDF file.
    """
    settings = get_settings()
    response = requests.get(BASE_PDF_URL.format(pmc_id=pmc_id), headers=HEADERS)
    response.raise_for_status()

    output_file = Path(settings.pdf_output_path) / f"{pmc_id}.pdf"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "wb") as f:
        f.write(response.content)

    return str(output_file)


if __name__ == "__main__":
    print(earticle_pdf("PMC11901808"))
