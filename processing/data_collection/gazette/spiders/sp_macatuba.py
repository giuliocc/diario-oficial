from datetime import date

from gazette.spiders.base import DiarioMunicipalSigpubGazetteSpider


class SpMacatubaSpider(DiarioMunicipalSigpubGazetteSpider):
    name = "sp_macatuba"
    TERRITORY_ID = "3528007"

    FIRST_AVAILABLE_DATE = date(2009, 1, 1)
    CALENDAR_URL = "http://www.diariomunicipal.com.br/macatuba"
    GAZETTE_INFO_URL = "http://www.diariomunicipal.com.br/macatuba/materia/calendario"
    EXTRA_GAZETTE_INFO_URL = (
        "http://www.diariomunicipal.com.br/macatuba/materia/calendario/extra"
    )
