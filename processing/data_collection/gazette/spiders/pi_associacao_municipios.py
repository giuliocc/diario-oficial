from datetime import date

from gazette.spiders.base import DiarioMunicipalSigpubGazetteSpider


class PiAssociacaoMunicipiosSpider(DiarioMunicipalSigpubGazetteSpider):
    name = "pi_associacao_municipios"
    TERRITORY_ID = "2200000"

    FIRST_AVAILABLE_DATE = date(2009, 1, 1)
    CALENDAR_URL = "http://www.diariomunicipal.com.br/appm"
    GAZETTE_INFO_URL = "http://www.diariomunicipal.com.br/appm/materia/calendario"
    EXTRA_GAZETTE_INFO_URL = (
        "http://www.diariomunicipal.com.br/appm/materia/calendario/extra"
    )
