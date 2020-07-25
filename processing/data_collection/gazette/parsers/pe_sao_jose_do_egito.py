import re

from gazette.parsers.base import BaseTextPdfParser
from gazette.parsers.base.extractors import (
    Extraction,
    LxmlBoundedMultilineTextExtractor,
    LxmlBoundedTextExtractor,
    LxmlMultilineTextExtractor,
    Text,
)


def is_bold(text):
    return text.raw.get("bold") == "true"


def is_italic(text):
    return text.raw.get("italic") == "true"


def concatenate_with_next(text):
    _text = text.raw
    next_text = _text.getnext()
    return (
        f"{_text.text}{_text.tail}{next_text.text}{next_text.tail}"
        if next_text is not None
        else f"{_text.text}{_text.tail}"
    )


def contains_section_title_with_city_name(text):
    pattern = re.compile(
        """ESTADO\s+DE\s+PERNAMBUCO\s+
        .*?(MUNICÍPIO|PREFEITURA\s+MUNICIPAL).*?
        SÃO\s+JOSÉ\s+DO\s+EGITO""",
        re.DOTALL | re.VERBOSE,
    )
    _text = concatenate_with_next(text)
    return re.search(pattern, _text) is not None


def contains_section_title_without_city_name(text):
    pattern = re.compile(
        """ESTADO\s+DE\s+PERNAMBUCO\s+
        .*?(MUNICÍPIO|PREFEITURA\s+MUNICIPAL).*?
        (?!SÃO\s+JOSÉ\s+DO\s+EGITO)""",
        re.DOTALL | re.VERBOSE,
    )
    _text = concatenate_with_next(text)
    return re.search(pattern, _text) is not None


def contains_header_pattern(text):
    return (
        re.search(
            "Diário\s+Oficial\s+dos\s+Municípios\s+do\s+Estado\s+de\s+Pernambuco",
            text.text,
            re.IGNORECASE,
        )
        is not None
    )


def contains_footer_pattern(text):
    return re.search("www\.diariomunicipal\.com\.br/amupe\s+\d+", text.text) is not None


def city_section_start_condition(text):
    return (
        contains_section_title_with_city_name(text)
        and is_bold(text)
        and not is_italic(text)
    )


def city_section_stop_condition(text):
    return (
        contains_section_title_without_city_name(text)
        and is_bold(text)
        and not is_italic(text)
    )


def is_header(text):
    return contains_header_pattern(text) and not is_bold(text) and not is_italic(text)


def is_footer(text):
    return contains_footer_pattern(text) and not is_bold(text) and not is_italic(text)


text_extractor = LxmlMultilineTextExtractor(
    start=city_section_start_condition,
    stop=city_section_stop_condition,
    ignore=[is_header, is_footer],
)


def contains_cnpj_pattern(text):
    return re.search("\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}", text.text) is not None


def get_cnpjs(text):
    return re.findall("\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}", text.text)


cnpjs_extractor = LxmlBoundedTextExtractor(
    bounded_by=text_extractor,
    allow=contains_cnpj_pattern,
    cleanup=get_cnpjs,
    ignore=[is_header, is_footer],
)


def contains_subsection_ending(text):
    pattern = re.compile("Código\s+Identificador\s*:\s*[A-Z\d]+")
    return re.search(pattern, text.text) is not None


def subsection_start_condition(text):
    return is_bold(text) and not is_italic(text)


def subsection_stop_condition(text):
    previous_element = text.raw.getprevious()

    if previous_element is None:
        return False

    previous_text = Text(
        raw=previous_element, text=f"{previous_element.text}{previous_element.tail}"
    )

    return (
        contains_subsection_ending(previous_text)
        and is_bold(previous_text)
        and not is_italic(previous_text)
    )


subsection_extractor = LxmlBoundedMultilineTextExtractor(
    bounded_by=text_extractor,
    start=subsection_start_condition,
    stop=subsection_stop_condition,
    ignore=[is_header, is_footer],
)


def contains_bidding_exemption_pattern(text):
    return (
        re.search("(licitação|licitatório)", text.text, re.IGNORECASE) is not None
        and re.search("(inexigibilidade|dispensa)", text.text, re.IGNORECASE)
        is not None
    )


bidding_exemptions_extractor = LxmlBoundedTextExtractor(
    bounded_by=subsection_extractor,
    allow=contains_bidding_exemption_pattern,
    ignore=[is_header, is_footer],
)


class PeSaoJoseDoEgitoParser(BaseTextPdfParser):
    extractions = [
        Extraction(name="text", extractor=text_extractor),
        Extraction(name="cnpjs", extractor=cnpjs_extractor),
        Extraction(name="subsections", extractor=subsection_extractor),
        Extraction(name="bidding_exemptions", extractor=bidding_exemptions_extractor),
    ]
