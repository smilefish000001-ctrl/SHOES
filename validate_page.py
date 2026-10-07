from html.parser import HTMLParser
from pathlib import Path
import sys


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.in_title = False
        self.in_h1 = False
        self.title = []
        self.h1 = []
        self.articles = 0

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        if tag == "title":
            self.in_title = True
        elif tag == "h1":
            self.in_h1 = True
        elif tag == "article":
            self.articles += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "h1":
            self.in_h1 = False

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)
        if self.in_h1:
            self.h1.append(data)


page_path = Path(__file__).with_name("index.html")
source = page_path.read_text(encoding="utf-8")
parser = PageParser()
parser.feed(source)

expected = "全球鞋業與鞋機需求情報"
errors = []
if not source.lstrip().lower().startswith("<!doctype html>"):
    errors.append("missing HTML doctype")
for required in ("html", "head", "body", "main"):
    if required not in parser.tags:
        errors.append(f"missing <{required}>")
if "".join(parser.title).strip() != expected:
    errors.append("page title changed")
if "".join(parser.h1).strip() != expected:
    errors.append("visible h1 changed")
if not 5 <= parser.articles <= 8:
    errors.append(f"expected 5-8 articles, found {parser.articles}")
if "本資料整理自公開資訊" in source:
    errors.append("removed footer disclaimer returned")

if errors:
    for error in errors:
        print(f"ERROR: {error}")
    sys.exit(1)

print(f"OK: title preserved; {parser.articles} intelligence articles; standalone page structure valid")
