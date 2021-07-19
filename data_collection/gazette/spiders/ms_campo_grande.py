import re
from datetime import date, datetime

from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MsCampoGrandeSpider(BaseGazetteSpider):
    TERRITORY_ID = "5002704"
    name = "ms_campo_grande"
    allowed_domains = ["diogrande.campogrande.ms.gov.br"]
    start_date = date(1998, 1, 9)

    def start_requests(self):
        base_url = "https://diogrande.campogrande.ms.gov.br/wp-admin/admin-ajax.php?action=edicoes_json"
        initial_date = self.start_date.strftime("%d/%m/%Y")
        final_date = date.today().strftime("%d/%m/%Y")
        url = f"{base_url}&de={initial_date}&ate{final_date}&start=0"
        yield Request(url)

    def parse(self, response, sequential=0):
        for entry in response.json()["data"]:
            date = datetime.strptime(entry["dia"], "%Y-%m-%d").date()

            if date < self.start_date:
                return

            edition_number = entry["numero"]
            title = entry["desctpd"]
            is_extra = "extra" in title.lower()
            url = response.urljoin(entry["arquivo"])  # wrong url
            yield Gazette(
                file_urls=[url],
                date=date,
                edition_number=edition_number,
                is_extra_edition=is_extra,
                power="executive_legislative",
            )

        next_sequential = sequential + 10
        next_url = re.sub(r"start=(\d+)", f"start={next_sequential}", response.url)
        yield Request(next_url, cb_kwargs={"sequential": next_sequential})
