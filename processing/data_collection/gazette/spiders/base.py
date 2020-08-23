import json
import re
from datetime import date, datetime

import dateparser
from dateutil.rrule import DAILY, rrule
from fake_useragent import UserAgent
import scrapy

from gazette.items import Gazette


class BaseGazetteSpider(scrapy.Spider):
    def __init__(self, start_date=None, *args, **kwargs):
        super(BaseGazetteSpider, self).__init__(*args, **kwargs)

        if start_date is not None:
            parsed_data = dateparser.parse(start_date)
            if parsed_data is not None:
                self.start_date = parsed_data.date()


class DiarioMunicipalSigpubGazetteSpider(BaseGazetteSpider):
    custom_settings = {"USER_AGENT": UserAgent().random}

    def start_requests(self):
        yield scrapy.Request(self.CALENDAR_URL, callback=self.parse_calendar)

    def parse_calendar(self, response):
        formdata = {
            "calendar[_token]": response.xpath(
                "//input[@id='calendar__token']/@value"
            ).get()
        }
        available_dates = rrule(
            freq=DAILY, dtstart=self.FIRST_AVAILABLE_DATE, until=date.today()
        )
        for query_date in available_dates:
            formdata.update(
                {
                    "calendar[day]": str(query_date.day),
                    "calendar[month]": str(query_date.month),
                    "calendar[year]": str(query_date.year),
                }
            )
            editions = {
                "regular": self.GAZETTE_INFO_URL,
                "extra": self.EXTRA_GAZETTE_INFO_URL,
            }
            for edition_type, url in editions.items():
                yield scrapy.FormRequest(
                    url=url,
                    formdata=formdata,
                    meta={"date": query_date, "edition_type": edition_type},
                    callback=self.parse_gazette_info,
                )

    def parse_gazette_info(self, response):
        body = json.loads(response.text)
        meta = response.meta

        if "error" in body:
            self.logger.warning(
                f"{meta['edition_type'].capitalize()} Gazette not available for {meta['date'].date()}"
            )
            return

        for edicao in body["edicao"]:
            url = f"{body['url_arquivos']}{edicao['link_diario']}.pdf"
            yield Gazette(
                date=meta["date"],
                file_urls=[url],
                territory_id=self.TERRITORY_ID,
                power="executive_legislative",
                is_extra_edition=(meta["edition_type"] == "extra"),
                scraped_at=datetime.utcnow(),
            )


class FecamGazetteSpider(BaseGazetteSpider):

    URL = "https://www.diariomunicipal.sc.gov.br/site/"
    total_pages = None

    def start_requests(self):
        yield scrapy.Request(
            f"{self.URL}?q={self.FECAM_QUERY}", callback=self.parse_pagination
        )

    def parse_pagination(self, response):
        """
        This parse function is used to get all the pages available and
        return request object for each one
        """
        return [
            scrapy.Request(
                f"{self.URL}?q={self.FECAM_QUERY}&Search_page={i}", callback=self.parse
            )
            for i in range(1, self.get_last_page(response) + 1)
        ]

    def parse(self, response):
        """
        Parse each page from the gazette page.
        """
        # Get gazzete info
        documents = self.get_documents_links_date(response)
        for d in documents:
            yield self.get_gazette(d)

    def get_documents_links_date(self, response):
        """
        Method to get all the relevant documents list and their dates from the page
        """
        documents = []
        titles = response.css("div.row.no-print h4")
        for title in titles:
            title_sibling_link = title.xpath("following-sibling::a[2]")
            if "[Abrir/Salvar Original]" in title_sibling_link.xpath("./text()").get():
                link = title_sibling_link.xpath("./@href").get().strip()
            else:
                link = title.xpath("./a/@href").get().strip()
            date = (
                title.xpath("following-sibling::span[1]")
                .re_first("\d{2}/\d{2}/\d{4}")
                .strip()
            )
            documents.append((link, date))
        return documents

    @staticmethod
    def get_last_page(response):
        """
        Get the last page number available in the pages navigation menu
        """
        href = response.xpath(
            "/html/body/div[1]/div[4]/div[4]/div/div/ul/li[14]/a/@href"
        ).get()
        result = re.search("Search_page=(\d+)", href)
        if result is not None:
            return int(result.groups()[0])

    def get_gazette(self, document):
        """
        Transform the tuple returned by get_documents_links_date and returns a
        Gazette item
        """
        if document[1] is None or len(document[1]) == 0:
            raise "Missing document date"
        if document[0] is None or len(document[0]) == 0:
            raise "Missing document URL"

        return Gazette(
            date=dateparser.parse(document[1], languages=("pt",)).date(),
            file_urls=(document[0],),
            territory_id=self.TERRITORY_ID,
            scraped_at=datetime.utcnow(),
        )
