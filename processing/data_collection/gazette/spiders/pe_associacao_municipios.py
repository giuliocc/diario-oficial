from datetime import date

from gazette.spiders.base import DiarioMunicipalSigpubGazetteSpider


class PeAssociacaoMunicipiosSpider(DiarioMunicipalSigpubGazetteSpider):
    name = "pe_associacao_municipios"
    TERRITORY_ID = "2600000"

    FIRST_AVAILABLE_DATE = date(2009, 1, 1)
    CALENDAR_URL = "http://www.diariomunicipal.com.br/amupe"
    GAZETTE_INFO_URL = "http://www.diariomunicipal.com.br/amupe/materia/calendario"
    EXTRA_GAZETTE_INFO_URL = (
        "http://www.diariomunicipal.com.br/amupe/materia/calendario/extra"
    )
