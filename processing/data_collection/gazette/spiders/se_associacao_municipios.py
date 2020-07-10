from datetime import date

from gazette.spiders.base import DiarioMunicipalSigpubGazetteSpider


class SeAssociacaoMunicipiosSpider(DiarioMunicipalSigpubGazetteSpider):
    name = "se_associacao_municipios"
    TERRITORY_ID = "2800000"

    FIRST_AVAILABLE_DATE = date(2009, 1, 1)
    CALENDAR_URL = "http://www.diariomunicipal.com.br/sergipe"
    GAZETTE_INFO_URL = "http://www.diariomunicipal.com.br/sergipe/materia/calendario"
    EXTRA_GAZETTE_INFO_URL = (
        "http://www.diariomunicipal.com.br/sergipe/materia/calendario/extra"
    )
