from datetime import date

from gazette.spiders.base import DiarioMunicipalSigpubGazetteSpider


class BaAssociacaoMunicipiosSpider(DiarioMunicipalSigpubGazetteSpider):
    name = "ba_associacao_municipios"
    TERRITORY_ID = "2900000"

    FIRST_AVAILABLE_DATE = date(2009, 1, 1)
    CALENDAR_URL = "http://www.diariomunicipal.com.br/amurc"
    GAZETTE_INFO_URL = "http://www.diariomunicipal.com.br/amurc/materia/calendario"
    EXTRA_GAZETTE_INFO_URL = (
        "http://www.diariomunicipal.com.br/amurc/materia/calendario/extra"
    )
