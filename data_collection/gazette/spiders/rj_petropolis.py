import datetime
import re

import dateparser
import scrapy
from dateparser.search import search_dates

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjPetropolisSpider(BaseGazetteSpider):
    name = "rj_petropolis"
    TERRITORY_ID = "3303906"
    allowed_domains = ["petropolis.rj.gov.br"]
    start_date = datetime.date(2001, 10, 2)
    start_urls = [
        "https://www.petropolis.rj.gov.br/pmp/index.php/servicos-na-web/informacoes/diario-oficial/viewcategory/3-diario-oficial.html"
    ]

    def parse(self, response):
        raw_links = response.xpath("//select[@id='cat_list']/@onchange").get()
        options = response.xpath(
            "//select[@id='cat_list']/option[contains(./text(), '\xa0')]"
        )

        for option in options:
            option_text = option.xpath("./text()").re_first(r"\w+$")
            if self._is_year(option_text):
                year = option_text
                continue
            else:
                current_month_date = f"{year} {option_text} 1"
                current_month_date = dateparser.parse(
                    current_month_date, languages=["pt"], date_formats=["%Y %B %d"]
                ).date()

                if current_month_date < self.start_date:
                    continue

            month_id = option.xpath("./@value").get()
            link = re.search(
                fr"/pmp/index.php/servicos-na-web/informacoes/diario-oficial/viewcategory/{month_id}-[a-z]+\.html",
                raw_links,
            ).group()

            yield scrapy.Request(response.urljoin(link), callback=self.parse_editions)

    def parse_editions(self, response):
        editions = response.xpath(
            "//div[contains(./text(), 'Arquivos:')]/following-sibling::table[not(contains(@class, 'jd_footer'))]"
        )

        for edition in editions:
            link = edition.xpath("./tr[1]/td/b/a/@href").get()
            title = edition.xpath("./tr[1]/td/b/a/text()").get()
            edition_number = re.match(r"\s*\d+", title)

            if not edition_number:
                continue

            description = "#".join(edition.xpath("./tr[2]//text()").getall())
            try:
                raw_date = re.search(r"\d+/[\d#]+/[\d#]+", description).group()
                raw_date = re.sub(r"[\s#]", "", raw_date)
                date = datetime.datetime.strptime(raw_date, "%d/%m/%Y").date()
            except Exception:
                date = search_dates(title, languages=["pt"])[-1][1].date()

            yield Gazette(
                date=date,
                edition_number=edition_number.group().strip(),
                file_urls=[response.urljoin(link)],
                power="executive",
            )

    def _is_year(self, text):
        return text.isdigit()
