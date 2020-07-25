from collections import namedtuple

from lxml.etree import parse
from scrapy.utils.misc import arg_to_iter


Extraction = namedtuple("Extraction", ["name", "extractor"])
Text = namedtuple("Text", ["raw", "text"])


class BaseTextExtractor:
    def __init__(self, allow=None, cleanup=None, ignore=[]):
        self.can_allow = allow
        self.cleanup = cleanup
        self.can_ignore = ignore

    def extract(self, filepath):
        texts = self._file_to_texts(filepath)
        yield from self._extract_texts(texts)

    def text(self, filepath):
        texts = []

        for text in self.extract(filepath):
            if self.cleanup is not None:
                texts.extend(self.cleanup(text))
            else:
                texts.append(text.text)

        return texts

    def _file_to_texts(self, filepath):
        raw_texts = self._parse_file(filepath)
        for raw in raw_texts:
            yield self._raw_to_text(raw)

    def _parse_file(self, filepath):
        raise NotImplementedError("Method __parse_file must be implemented")

    def _raw_to_text(self, raw):
        raise NotImplementedError("Method _raw_to_text must be implemented")

    def _extract_texts(self, texts):
        yield from (t for t in texts if self._is_extractable(t))

    def _is_ignored(self, text):
        if self.can_ignore is None:
            return False

        return any(
            [condition_to_ignore(text) for condition_to_ignore in self.can_ignore]
        )

    def _is_allowed(self, text):
        if self.can_allow is None:
            return True

        return self.can_allow(text)

    def _is_extractable(self, text):
        return not self._is_ignored(text) and self._is_allowed(text)


class BaseMultilineTextExtractor(BaseTextExtractor):
    def __init__(self, start=None, stop=None, cleanup=None, ignore=[]):
        self.start_condition = start
        self.stop_condition = stop
        self.cleanup = cleanup
        self.can_ignore = ignore

    def _extract_texts(self, texts):
        extracted_texts = []
        has_started = False

        for text in texts:
            if self._is_ignored(text):
                continue

            if has_started:
                if self._is_stopper(text):
                    has_started = False
                else:
                    last_text = extracted_texts[-1]
                    last_text.raw.append(text.raw)
                    extracted_texts[-1] = last_text._replace(
                        text=last_text.text + text.text
                    )
                    continue

            if self._is_starter(text):
                has_started = True
                extracted_texts.append(Text(raw=[text.raw], text=text.text))

        yield from extracted_texts

    def _is_starter(self, text):
        if self.start_condition is None:
            return True

        return self.start_condition(text)

    def _is_stopper(self, text):
        if self.stop_condition is None:
            return False

        return self.stop_condition(text)


class BoundsMixin:
    def __init__(self, bounded_by, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bounder = bounded_by


class BaseBoundedTextExtractor(BoundsMixin, BaseTextExtractor):
    def extract(self, filepath):
        texts = self.bounder.extract(filepath)
        yield from self._extract_texts(texts)


class BaseBoundedMultilineTextExtractor(BoundsMixin, BaseMultilineTextExtractor):
    def extract(self, filepath):
        texts = self.bounder.extract(filepath)

        for text in texts:
            boundary_texts = (self._raw_to_text(t) for t in arg_to_iter(text.raw))
            yield from self._extract_texts(boundary_texts)


class LxmlMixin:
    def _parse_file(self, filepath):
        xml = parse(filepath)
        texts = xml.iter("text")
        return texts

    def _raw_to_text(self, raw):
        return Text(raw=raw, text=f"{raw.text}{raw.tail}")


class LxmlTextExtractor(LxmlMixin, BaseTextExtractor):
    pass


class LxmlMultilineTextExtractor(LxmlMixin, BaseMultilineTextExtractor):
    pass


class LxmlBoundedTextExtractor(LxmlMixin, BaseBoundedTextExtractor):
    pass


class LxmlBoundedMultilineTextExtractor(LxmlMixin, BaseBoundedMultilineTextExtractor):
    pass
