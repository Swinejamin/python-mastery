def print_line(line):
    print("|" + line + "|")


def print_divider(width, columns, separator="-"):
    print("|" + (separator * width + "|") * columns)


def print_table(table, headers):
    list_to_print = list()

    width = max((len(h) + 9) // 10 * 10 for h in headers)

    for row in table:
        attributes = [getattr(row, header) for header in headers]

        for attribute in attributes:
            try:
                width = max(width, len(attribute))

            except TypeError as e:
                continue

        list_to_print.append(
            f"|{'|'.join(f'{getattr(row, header):^{width}}' for header in headers)}|"
        )

    print(width)

    print_divider(width=width, columns=len(headers))
    print("|" + "x".join(f"{header:^{width}s}" for header in headers) + "|")
    print_divider(width=width, columns=len(headers))

    for line in list_to_print:
        print(line)

    print_divider(width=width, columns=len(headers))
