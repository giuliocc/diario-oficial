from datetime import date

from gazette.spiders.base import DiarioMunicipalSigpubGazetteSpider


class RnAssociacaoMunicipiosSpider(DiarioMunicipalSigpubGazetteSpider):
    name = "rn_associacao_municipios"
    TERRITORY_ID = "2400000"

    FIRST_AVAILABLE_DATE = date(2009, 1, 1)
    CALENDAR_URL = "http://www.diariomunicipal.com.br/femurn"
    GAZETTE_INFO_URL = "http://www.diariomunicipal.com.br/femurn/materia/calendario"
    EXTRA_GAZETTE_INFO_URL = (
        "http://www.diariomunicipal.com.br/femurn/materia/calendario/extra"
    )
