from datetime import date

from gazette.spiders.base import DiarioMunicipalSigpubGazetteSpider


class CeAssociacaoMunicipiosSpider(DiarioMunicipalSigpubGazetteSpider):
    name = "ce_associacao_municipios"
    TERRITORY_ID = "2300000"

    FIRST_AVAILABLE_DATE = date(2009, 1, 1)
    CALENDAR_URL = "http://www.diariomunicipal.com.br/aprece"
    GAZETTE_INFO_URL = "http://www.diariomunicipal.com.br/aprece/materia/calendario"
    EXTRA_GAZETTE_INFO_URL = (
        "http://www.diariomunicipal.com.br/aprece/materia/calendario/extra"
    )
