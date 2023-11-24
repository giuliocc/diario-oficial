import datetime

import dateparser
import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class ToPortoNacionalSpider(BaseGazetteSpider):
    TERRITORY_ID = "1718204"
    name = "to_porto_nacional"
    allowed_domains = ["diariooficial.portonacional.to.gov.br"]
    start_date = datetime.date(2021, 2, 25)
    start_urls = ["https://diariooficial.portonacional.to.gov.br/edicoes"]

    def parse(self, response, page=0):
        gazettes = response.xpath("//section//table//tr")
        for gazette in gazettes:
            raw_date = "".join(gazette.xpath("./td[1]/text()").getall()).strip()
            date = dateparser.parse(raw_date, languages=["pt"]).date()

            if self.end_date < date:
                continue
            if self.start_date > date:
                return

            url = gazette.xpath(".//a/@href").get()
            title = gazette.xpath("./td[1]/strong/text()")
            is_extra_edition = "suplemento" in title.get().lower()
            edition_number = title.re_first(r"EDIÇÃO Nº (\d+)")

            yield Gazette(
                file_urls=[url],
                date=date,
                is_extra_edition=is_extra_edition,
                edition_number=edition_number,
                power="executive_legislative",
            )

        has_next_page = response.xpath("//a[@class='page-link'][@rel='next']")
        if has_next_page:
            next_page = page + 1
            yield scrapy.Request(
                url=f"{self.start_urls[0]}?page={next_page}",
                cb_kwargs={"page": next_page},
            )
