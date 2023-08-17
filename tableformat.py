from pprint import pprint


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

    def print_divider(self, separator="-"):
        print(f"|{f'{separator * self._width}|' * self._columns}")

    def add_divider(self, separator="-"):
        self._list_to_print.append(
            "|".join(f"{separator * self._width}" for _ in range(self._columns))
        )


def print_table(records, fields, formatter):
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
            "x".join(f"{header:^{self._width}s}" for header in headers)
        )
        self.add_divider()

    def row(self, rowdata):
        self._list_to_print.append(
            "|".join(f"{cell:^{self._width}}" for cell in rowdata)
        )

    @staticmethod
    def print_line(line=""):
        print(f"|{line}|")

    def print(self):
        for line in self._list_to_print:
            self.print_line(line)

        self.print_divider()


class CSVTableFormatter(TableFormatter):
    def headings(self, headers):
        width = max(self._width, *[(len(h) + 9) // 10 * 10 for h in headers])
        self._width = width

        self._list_to_print.append(",".join(header.upper() for header in headers))
        self._list_to_print.append("")

    def row(self, rowdata):
        self._list_to_print.append(f"{','.join(f'{cell}' for cell in rowdata)}")


class HTMLTableFormatter(TableFormatter):
    def tr(self, content):
        self._list_to_print.append(f"\t\t<tr> {content} </tr>")

    def headings(self, headers):
        self._list_to_print.append("<table>\n\t<thead>")
        self.tr(" ".join(f"<th> {header} </th>" for header in headers))
        self._list_to_print.append("\t</thead>\n\t<tbody>")

    def row(self, rowdata):
        self.tr("".join(f"<td>  {row}  </td>" for row in rowdata))

    def print(self):
        self._list_to_print.append(f"\t</tbody>\n</table>")

        super().print()


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
