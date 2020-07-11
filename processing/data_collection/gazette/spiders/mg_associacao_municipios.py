from datetime import date

from gazette.spiders.base import DiarioMunicipalSigpubGazetteSpider


class MgAssociacaoMunicipiosSpider(DiarioMunicipalSigpubGazetteSpider):
    name = "mg_associacao_municipios"
    TERRITORY_ID = "3100000"

    FIRST_AVAILABLE_DATE = date(2009, 1, 1)
    CALENDAR_URL = "http://www.diariomunicipal.com.br/amm-mg"
    GAZETTE_INFO_URL = "http://www.diariomunicipal.com.br/amm-mg/materia/calendario"
    EXTRA_GAZETTE_INFO_URL = (
        "http://www.diariomunicipal.com.br/amm-mg/materia/calendario/extra"
    )
