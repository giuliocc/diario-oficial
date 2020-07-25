from datetime import date

from gazette.spiders.base import DiarioMunicipalSigpubGazetteSpider


class PeSaoJoseDoEgitoSpider(DiarioMunicipalSigpubGazetteSpider):
    name = "pe_sao_jose_do_egito"
    parser = "gazette.parsers.pe_sao_jose_do_egito.PeSaoJoseDoEgitoParser"

    TERRITORY_ID = "2613602"

    FIRST_AVAILABLE_DATE = date(2009, 1, 1)
    CALENDAR_URL = "http://www.diariomunicipal.com.br/amupe"
    GAZETTE_INFO_URL = "http://www.diariomunicipal.com.br/amupe/materia/calendario"
    EXTRA_GAZETTE_INFO_URL = (
        "http://www.diariomunicipal.com.br/amupe/materia/calendario/extra"
    )
