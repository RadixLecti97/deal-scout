import os
from anthropic import Anthropic
from typing import Literal
from pydantic import BaseModel, Field
# ...


class DealInfo(BaseModel):
    deal_type:Literal["catalog_sale","licensing_agreement","royalty_financing","other"]
    seller:str
    buyer:str
    asset:str
    announced_date:str = Field(description="ISO format YYYY-MM-DD")
    price_usd:int | None = None
    terms_summary:str



client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

response = client.messages.parse(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": """
    Extract the deal described in the article below. If a field isn't stated, use null (price) or "not stated". Article:
Skip to content
Concord Logo
About
Label Group
Music Publishing
Theatricals
Originals
News
Licensing
Careers
Contact

Search & Filter
BMG and Concord Combine to Create World’s Leading Independent Music Company
Image
April 28, 2026
BMG and Concord Combine to Create World’s Leading Independent Music Company

Creates global platform to deliver superior service to artists, songwriters, and partners
Unlocks meaningful value through greater scale and strong cash flow, enabling continued investment in music rights, creative talent, and technology
Bob Valentine to serve as CEO and Thomas Coesfeld as Chairman of the combined company, with global headquarters in Nashville and European Headquarters in Berlin
Combined company to be named BMG with divisions “BMG Publishing” and “Concord Records”
 

Berlin and Nashville, April 28, 2026 – BMG and Concord today announced a definitive agreement to combine their businesses, creating the leading independent music company in the world. Operating under the BMG name, the combined company will bring together two highly complementary businesses to establish a scaled, global company delivering superior service to artists, songwriters, and partners – firmly grounded in an independent, artist-first model.

The combination comes amid significant transformation in the global music market, where scale, global reach, and technology investment are increasingly critical to remain competitive. Together, BMG and Concord will form a fully integrated global music company spanning music publishing, recorded music, theatrical rights, and digital distribution. This increased scale will enable deeper investment in creativity, next-generation technology, and world-class talent, and will preserve the entrepreneurial approach that artists, songwriters, and playwrights value.

In fast-growing markets, where music consumption continues to evolve, the unified company will be well positioned to expand its presence, deepen artist and songwriter partnerships, and capture new revenue streams across platforms and formats. It is expected to generate significant cash flow to reinvest in the business and fuel growth. This includes a mid-term ambition to achieve $1.2 billion in EBITDA, building from a pro forma EBITDA base of more than $730 million in 2026, driven through organic growth, M&A, and synergies.

“We believe this is a truly one-of-a-kind opportunity to bring together two world-class teams and rosters at the right moment, as scale in rights ownership becomes increasingly critical to long-term growth,” said Thomas Coesfeld, Chief Executive Officer of BMG and designated Chairman of the combined company. “This transaction accelerates our successful BMG Next strategy by enabling a more ambitious and sustained approach to investing in artists and songwriters, as well as in rights, technology, AI tools, and the talent shaping the industry. As one unified business, we will further deepen our position as a preferred global partner to artists, songwriters, and platforms, combining scale with the agility and independence they value. We look forward to this next chapter and to the opportunities it creates for artists, songwriters, and partners.”

“We are excited to begin working together to build something truly exceptional,” said Bob Valentine, Chief Executive Officer of Concord and designated CEO of the combined company. “Both companies were founded to support great artistry and with a deep sense of responsibility to the performers, songwriters, and playwrights we serve. We share a philosophy grounded in artist development, strategic long-term management of IP, and operational discipline. Our greater scale will allow us to invest more in creative talent, global reach, accretive acquisition opportunities, and technology, while preserving the nimble, entrepreneurial spirit that artists and songwriters value most. This is not about replicating the major label model; it’s about using scale to strengthen independence. Together, we will build a company that gives artists more reach and more flexibility – all designed to support their distinct visions.”

Collectively, the companies have invested billions of dollars in music rights and built one of the most diverse and culturally significant rosters in the industry, spanning artists, songwriters, and works from Jelly Roll, Paul Simon, Lainey Wilson, will.i.am, Jason Aldean, Tina Turner, Diane Warren, and Jean-Michel Jarre, to Creedence Clearwater Revival, Daddy Yankee, Denzel Curry, Hamilton, Phil Collins, R.E.M., and The Sound of Music.

Both businesses have delivered strong financial performance, with significant EBITDA growth and consistent cash generation in recent years. Since 2021, as part of its Boost investments program, BMG has invested more than $1.5 billion in music rights acquisitions and an equal amount in signings, licenses, and technology. BMG has doubled its operating EBITDA and delivered best-in-class profitability under its BMG Next strategy. Concord brings a similarly disciplined approach, investing more than $3 billion since 2020 across publishing, recorded music, theatrical rights, and distribution, and supporting more than 125,000 artists and songwriters around the world.

The Combined Company

Upon closing, Valentine will serve as CEO of the combined company, with Coesfeld serving as Chairman. As previously announced, Coesfeld will assume the role of CEO of Bertelsmann, effective January 1, 2027. A joint management team drawn from both companies will lead the business. The newly formed company’s global headquarters will be in Nashville, with Berlin serving as its European headquarters. Its publishing division will be named BMG Publishing, and its recorded music division will be called Concord Records.

The combined company will be owned approximately 67% by Bertelsmann and approximately 33% by affiliates of Great Mountain Partners. Affiliates of Great Mountain Partners will also receive a one-time cash payment of $1.16 billion. Bertelsmann will continue to support BMG’s growth trajectory in the dynamic and fast-growing global music market.

The transaction is subject to customary closing conditions including regulatory approvals and is expected to close in the second half of 2026. Terms of the transaction were not disclosed.

Davis Polk & Wardwell LLP and ArentFox Schiff have served as legal counsel to BMG. J.P. Morgan is serving as financial advisor to Concord and Latham and Watkins LLP and Reed Smith LLP are serving as legal counsel. Alston & Bird LLP is advising Great Mountain Partners.

 

About BMG

Founded in 2008, BMG reimagined the relationship between music companies, songwriters, and artists by offering fairer contracts, greater creative freedom, and unparalleled transparency in royalties and licensing. Now the fourth-largest music company in the world, BMG combines human creativity with cutting-edge technology to connect music with global audiences. With 16 offices across 13 key markets, BMG represents more than three million songs and recordings, including some of the most iconic catalogs and works from leading artists and songwriters, including will.i.am, Jean-Michel Jarre, Tina Turner, Jason Aldean, Jelly Roll, Paul Simon, and many more. BMG is wholly owned and privately held by the international media, services, and education company Bertelsmann.

About Concord

Concord is the world’s leading independent music company. The Company supports more than 125,000 artists and songwriters whose works are licensed, marketed, and performed globally. Concord’s growing catalog of 1.3 million songs, compositions, sound recordings, films, plays, and musicals is one of the most impactful and culturally relevant collections of creative rights in history.

Concord is headquartered in Nashville with additional offices in Los Angeles, New York, London, Berlin, Melbourne, and Miami.

Contact
Nashville
(opens in a new tab)
Los Angeles
(opens in a new tab)
New York
(opens in a new tab)
London
(opens in a new tab)
Berlin
(opens in a new tab)
Melbourne
(opens in a new tab)
Miami
(opens in a new tab)
Socials
Linkedin
(opens in a new tab)
Facebook
(opens in a new tab)
Instagram
(opens in a new tab)
X
(opens in a new tab)

Royalty Portal
Privacy Policy
Cookie Policy
Terms
Accessibility Statement
Declaration of Rights Reservation
© 2026 Concord
"""}],
output_format = DealInfo,
)

print(response.parsed_output.model_dump_json(indent=2))