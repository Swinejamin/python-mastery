from pprint import pprint
from colored import Fore, Back, Style


class TableFormatter:
    def __init__(self):
        self._width = 0
        self._columns = 0
        self._list_to_print = list()

    @property
    def width(self):
        return self._width

    def headings(self, headers):
        raise NotImplementedError()

    def row(self, rowdata):
        raise NotImplementedError()

    @staticmethod
    def print_line(line=""):
        print(line)

    def print(self):
        for line in self._list_to_print:
            self.print_line(line)

    def divider(self, separator="-"):
        return (
            Fore.yellow
            + Style.bold
            + "|".join(f"{separator * self._width}" for _ in range(self._columns))
            + Style.reset
        )

    def add_divider(self):
        self._list_to_print.append(self.divider())


def print_table(records, fields, formatter):
    if not isinstance(formatter, TableFormatter):
        raise TypeError(
            f"Expected a TableFormatter, received ~{type(formatter).__name__})~"
        )
    formatter.headings(fields)
    for r in records:
        rowdata = [getattr(r, fieldname) for fieldname in fields]
        formatter.row(rowdata)

    formatter.print()


class TextTableFormatter(TableFormatter):
    def headings(self, headers):
        self._columns = len(headers)
        self._width = max(self._width, *[(len(h) + 9) // 10 * 10 for h in headers])

        self.add_divider()

        self._list_to_print.append(
            Fore.white
            + Back.deep_sky_blue_3a
            + "x".join(f"{header:^{self._width}s}" for header in headers)
            + Style.reset
        )
        self.add_divider()

    def row(self, rowdata):
        self._list_to_print.append(
            "|".join(f"{cell:^{self._width}}" for cell in rowdata)
        )

    @staticmethod
    def print_line(line=""):
        print(
            f"{Fore.yellow + Style.bold}|{Style.reset}{line}{Fore.yellow + Style.bold}|{Style.reset}"
        )

    def print(self):
        self.add_divider()
        for line in self._list_to_print:
            self.print_line(line)


class CSVTableFormatter(TableFormatter):
    def headings(self, headers):
        width = max(self._width, *[(len(h) + 9) // 10 * 10 for h in headers])
        self._width = width

        self._list_to_print.append(",".join(header.upper() for header in headers))
        self._list_to_print.append("")

    def row(self, rowdata):
        self._list_to_print.append(f"{','.join(f'{cell}' for cell in rowdata)}")


def html_tag(tag, content, color="yellow", indent=0, new_line=True):
    tag_style = getattr(Fore, color) + Style.bold

    whitespace = "\n" if new_line else ""

    indent_string = "\t" * indent if new_line else ""

    tag_open = f"{whitespace}{indent_string}{tag_style}<{tag}>{Style.reset}"
    tag_close = f"{tag_style}{whitespace}{indent_string}</{tag}>{Style.reset}"
    return f"{tag_open}{content}{tag_close}"


def tr(content):
    return html_tag(tag="tr", content=content, indent=1)


class HTMLTableFormatter(TableFormatter):
    def headings(self, headers):
        self._list_to_print.append(
            tr(
                content="\n\t\t"
                + "".join(
                    html_tag(
                        tag="th",
                        content=f"{Style.bold} {header.upper()} {Style.reset}",
                        color="green",
                        new_line=False,
                    )
                    for header in headers
                ),
            )
        )

    def row(self, rowdata):
        self._list_to_print.append(
            tr(
                "\n\t\t"
                + "".join(
                    html_tag(tag="td", content=cell, new_line=False) for cell in rowdata
                )
            )
        )

    def print(self):
        table_header = html_tag(tag="thead", content=self._list_to_print[0], indent=0)

        table_body = html_tag(
            tag="tbody",
            indent=0,
            content=f'{"".join(self._list_to_print[1:])}',
        )
        print(html_tag(tag="table", content=f"{table_header}{table_body}", indent=0))


def create_formatter(name):
    if name == "text":
        formatter_cls = TextTableFormatter
    elif name == "csv":
        formatter_cls = CSVTableFormatter
    elif name == "html":
        formatter_cls = HTMLTableFormatter
    else:
        raise RuntimeError("Unknown format %s" % name)
    return formatter_cls()
