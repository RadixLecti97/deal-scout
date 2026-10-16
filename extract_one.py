import os
import csv
from pathlib import Path
from typing import Literal

from anthropic import Anthropic
from pydantic import BaseModel, Field


class DealInfo(BaseModel):
    deal_type: Literal["catalog_sale", "licensing_agreement", "royalty_financing", "merger", "company_acquisition", "other"]
    seller: str = Field(description="Organization name only, written as the article writes it. No parentheses, no explanations, no legal suffixes (Inc, Ltd, LLC), never a parent company.")
    buyer: str = Field(description="Organization that ends up holding the asset, named as the article names it. Same naming rule as seller.If the article names a subsidiary as the buyer, use the subsidiary, not its parent.")
    asset: str = Field(description="For catalog deals: the artist or seller’s name plus the article’s noun (Catalog, Compositions). For company deals: the company name. For a merger: the company being absorbed. 1 to 4 words.")
    announced_date: str | None = Field(default=None, description="ISO format YYYY-MM-DD. Null if the article does not state a full date with a year.Never infer a year. A date without a year, like ‘September 7’, is null.")
    price_usd: int | None = Field(default=None, description="Total deal value in whole US dollars. Use a number only if the article states "
        "a total, or dollar amounts that clearly add up to one (cash + assumed debt + "
        "capped earn-out). Approximate amounts like 'about $1B' count as the number. "
        "Null if any part is not in dollars (for example an equity stake), if the "
        "amount is a range or a bound ('more than', 'up to'), or if it is not disclosed.")
    price_text: str | None = Field(default=None, description="The price exactly as the article words it, e.g. '~$300-400M' or 'EUR 200M'. Null if no price is given.")
    terms_summary: str = Field(description="One or two sentences on the main terms: structure, payments, closing timing")
    price_basis: Literal["stated_total", "reported", "partial", "undisclosed"] = Field(
        description="stated_total: full value stated. reported: secondhand or approximate. "
        "partial: some amounts but no single USD total. undisclosed: no dollar figure.")


client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
GUIDE = Path("LABELLING_GUIDE.md").read_text(encoding="utf-8")


def extract_deal(article_text: str) -> DealInfo:
    response = client.messages.parse(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        system=GUIDE,
        messages=[{
            "role": "user",
            "content": "Extract the deal described in the article below. "
                       "If a field isn't stated, use null.\n\n"
                       f"Article:\n{article_text}",
        }],
        output_format=DealInfo,
    )
    return response.parsed_output


rows = []
for file_path in sorted(Path("articles").glob("*.txt")):
    try:
        content = file_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, PermissionError):
        print(f"Skipped {file_path.name}: could not read")
        continue
    deal = extract_deal(content)
    rows.append({"file": file_path.name, **deal.model_dump()})
    print(f"done: {file_path.name}")

with open("results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["file", *DealInfo.model_fields])
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to results.csv")