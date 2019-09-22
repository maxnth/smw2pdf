from lxml import etree
import pdfkit
import regex as re


class Page:
    def __init__(self, title, text, attributes):
        self.title = title
        self.text = text
        self.attributes = attributes

    def create_table(self):
        template_name = list(self.attributes.keys())[0]
        table_string = "<caption>{template_name}</caption>".format(template_name=template_name)
        for attr_name, attr_val in self.attributes[template_name].items():
            table_string += "<tr><th>{name}</th><td>{value}</td></tr>".format(name=attr_name, value=attr_val)
        return table_string


class Parser:
    def __init__(self, file, out, out_format, style):
        self.ns_dict = {'mw': 'http://www.mediawiki.org/xml/export-0.10/'}
        self.file = file
        self.out = out
        self.out_format = out_format
        self.style = style

        self.tree = None
        self.attributes = set()
        self.pages = list()

        self.parse_file()
        self.get_pages()

    def parse_file(self):
        try:
            self.tree = etree.parse(self.file)
        except etree.ParseError as e:
            raise e

    def get_pages(self):
        print("Parsing pages...")

        pages = self.tree.xpath("//mw:page", namespaces=self.ns_dict)

        for page in pages:
            title = "".join(page.xpath("./mw:title/text()", namespaces=self.ns_dict))
            text = "\n".join(page.xpath("./mw:revision/mw:text/text()", namespaces=self.ns_dict))

            reg = re.compile("(?:{{){1}(?P<name>.+\n)?(?P<attributes>(?:\|?.*\n)+)(?:}}\n){1}(?P<free_text>(?:.*\n)*.*)?")
            hits = reg.match(text)

            if hits:
                form_name = hits.group("name")

                form_attributes = hits.group("attributes").replace("\n", "")
                attributes = dict()

                for attr in form_attributes[1:].split("|"):
                    attr = attr.split("=")
                    attributes[attr[0]] = attr[1]

                free_text = hits.group("free_text")
                free_text = re.sub("(?:===){1}(.+)(?:===){1}", r"<h3>\1</h3>", free_text)

                self.pages.append(Page(title, free_text, {form_name: attributes}))
            else:
                continue

    def build_result(self):
        print("Building output...")

        html_str = """<!doctype html><html lang="de"><head><meta charset="utf-8">
            <style>{style}</style><title>{target}</title></head><body><h1>{title}</h1>""".format(
                target=self.out, style=self.read_css(), title=self.out)
        for page in self.pages:
            html_str += """<div class='page'><hr><h2>{title}</h2><table class='attributes'>{attributes}</table>
                    <div class='freetext'>{freetext}</div></div>""".format(title=page.title,
                                                                           attributes=page.create_table(),
                                                                           freetext=page.text)
        html_str += """</body></html>"""

        return html_str

    def export(self):
        print("Writing output...")

        out_str = self.build_result()

        if "html" in self.out_format:
            with open(".".join([self.out, "html"]), 'w') as output:
                output.write(out_str)

        if "pdf" in self.out_format:
            pdfkit.from_string(out_str, ".".join([self.out, "pdf"]))

    def read_css(self):
        with open(self.style, 'r') as style_file:
            return style_file.read()

