from datetime import date

from gazette.spiders.base import DiarioMunicipalSigpubGazetteSpider


class SpAssociacaoMunicipiosSpider(DiarioMunicipalSigpubGazetteSpider):
    name = "sp_associacao_municipios"
    TERRITORY_ID = "3500000"

    FIRST_AVAILABLE_DATE = date(2009, 1, 1)
    CALENDAR_URL = "http://www.diariomunicipal.com.br/apm"
    GAZETTE_INFO_URL = "http://www.diariomunicipal.com.br/apm/materia/calendario"
    EXTRA_GAZETTE_INFO_URL = (
        "http://www.diariomunicipal.com.br/apm/materia/calendario/extra"
    )
