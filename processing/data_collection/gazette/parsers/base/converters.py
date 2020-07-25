from pathlib import Path
import subprocess

from lxml.etree import Element, parse, tostring


class PdfToPopplerXmlConverter:
    def convert(self, source, store_dir):
        target = Path(store_dir) / "converted_pdf_to_poppler_xml.xml"
        self._convert_pdf_to_xml(source, str(target))

        return str(target)

    def _convert_pdf_to_xml(self, source, target):
        if Path(target).exists():
            Path(target).unlink()

        command = f"pdftohtml -q -xml -i {source} {target}"
        subprocess.run(command, shell=True)


class PopplerXmlToGazetteXmlConverter:
    def __init__(self):
        self.fonts = {}

    def convert(self, source, store_dir):
        source_xml = parse(source)
        source_xml_encoding = source_xml.docinfo.encoding

        target_xml = self._transform_xml(source_xml)
        target = Path(store_dir) / "converted_poppler_xml_to_gazette_xml.xml"
        with target.open("wb") as targetfile:
            targetfile.write(self._to_text(target_xml, source_xml_encoding))

        return str(target)

    def _transform_xml(self, source):
        self._detect_fonts(source)
        transformed_texts = [self._transform_text(t) for t in source.iter("text")]

        root = Element("gazettexml")
        root.extend(transformed_texts)

        return root.getroottree()

    def _to_text(self, xml, encoding="utf-8"):
        return tostring(xml, encoding=encoding, pretty_print=True, xml_declaration=True)

    def _detect_fonts(self, tree):
        for font in tree.iter("fontspec"):
            self._register_font(font)

    def _register_font(self, font):
        self.fonts[font.get("id")] = {f"font_{k}": v for k, v in font.items()}

    def _transform_text(self, text):
        element = Element("text", attrib=self._transform_text_attrib(text))
        element.text = "".join(text.xpath(".//text()"))
        element.tail = text.tail
        return element

    def _transform_text_attrib(self, text):
        attrib = {
            **self._text_font_attrib(text),
            **self._text_page_attrib(text),
            **text.attrib,
            "bold": "true" if text.find("b") is not None else "false",
            "italic": "true" if text.find("i") is not None else "false",
        }
        del attrib["font"]
        return attrib

    def _text_font_attrib(self, text):
        return self.fonts[text.get("font")]

    def _text_page_attrib(self, text):
        page_attrib = text.getparent().attrib
        return {f"page_{k}": v for k, v in page_attrib.items()}
