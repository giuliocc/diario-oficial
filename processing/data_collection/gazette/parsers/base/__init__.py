import json
from pathlib import Path

from .converters import PdfToPopplerXmlConverter, PopplerXmlToGazetteXmlConverter
from .extractors import Extraction, LxmlMultilineTextExtractor


class BaseParser:
    converters = []
    extractions = []

    def __init__(self, store_dir):
        self.store_dir = Path(store_dir)
        self.store_dir.mkdir(parents=True, exist_ok=True)

    def parse(self, source_filepath):
        self._extract(self._convert(source_filepath))

    def _convert(self, source_filepath):
        converted_filepath = source_filepath

        for converter in self.converters:
            converted_filepath = converter.convert(
                converted_filepath, str(self.store_dir)
            )

        return converted_filepath

    def _extract(self, source_filepath):
        extractions = {
            name: extractor.text(source_filepath)
            for name, extractor in self.extractions
        }

        with (self.store_dir / "extracted_data.json").open("w") as extractions_file:
            json.dump(extractions, extractions_file, indent=4, sort_keys=True)


class BaseTextPdfParser(BaseParser):
    converters = [PdfToPopplerXmlConverter(), PopplerXmlToGazetteXmlConverter()]
    extractions = [Extraction(name="text", extractor=LxmlMultilineTextExtractor())]
