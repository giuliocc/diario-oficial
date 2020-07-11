from datetime import date

from gazette.spiders.base import DiarioMunicipalSigpubGazetteSpider


class RjAssociacaoMunicipiosSpider(DiarioMunicipalSigpubGazetteSpider):
    name = "rj_associacao_municipios"
    TERRITORY_ID = "3300000"

    FIRST_AVAILABLE_DATE = date(2009, 1, 1)
    CALENDAR_URL = "http://www.diariomunicipal.com.br/aemerj"
    GAZETTE_INFO_URL = "http://www.diariomunicipal.com.br/aemerj/materia/calendario"
    EXTRA_GAZETTE_INFO_URL = (
        "http://www.diariomunicipal.com.br/aemerj/materia/calendario/extra"
    )
