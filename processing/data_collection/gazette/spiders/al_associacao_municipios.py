from datetime import date

from gazette.spiders.base import DiarioMunicipalSigpubGazetteSpider


class AlAssociacaoMunicipiosSpider(DiarioMunicipalSigpubGazetteSpider):
    name = "al_associacao_municipios"
    TERRITORY_ID = "2700000"

    FIRST_AVAILABLE_DATE = date(2009, 1, 1)
    CALENDAR_URL = "http://www.diariomunicipal.com.br/ama"
    GAZETTE_INFO_URL = "http://www.diariomunicipal.com.br/ama/materia/calendario"
    EXTRA_GAZETTE_INFO_URL = (
        "http://www.diariomunicipal.com.br/ama/materia/calendario/extra"
    )
