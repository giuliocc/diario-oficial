from datetime import date

from gazette.spiders.base import DiarioMunicipalSigpubGazetteSpider


class SpMonteAltoSpider(DiarioMunicipalSigpubGazetteSpider):
    name = "sp_monte_alto"
    TERRITORY_ID = "3531308"

    FIRST_AVAILABLE_DATE = date(2009, 1, 1)
    CALENDAR_URL = "http://www.diariomunicipal.com.br/pmmasp"
    GAZETTE_INFO_URL = "http://www.diariomunicipal.com.br/pmmasp/materia/calendario"
    EXTRA_GAZETTE_INFO_URL = (
        "http://www.diariomunicipal.com.br/pmmasp/materia/calendario/extra"
    )
