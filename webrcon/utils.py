from collections import namedtuple
import re

re_pseudo_tsv = re.compile(r'([a-zA-Z]+)([ ]+(?![a-zA-Z]))?')


# noinspection PyArgumentList
def parse_pseudotsv(data):
    table = '\n'.join(data.split('\n\n')[1:]).split('\n')
    column_widths = {}
    matches = re_pseudo_tsv.finditer(table[0])
    for match in matches:
        column_widths[match.group(1)] = match.span()
    items = []
    item = namedtuple('TSVItem', ' '.join(column_widths.keys()))
    for row in table[1:]:
        if row == '':
            break
        item_values = []
        for span in column_widths.values():
            val = row[span[0]:span[1]].strip()
            if val.startswith('"') and val.endswith('"'):
                val = val[1:len(val) - 1]
            if val == '':
                val = False
            elif val == 'x':
                val = True
            item_values.append(val)
        items.append(item(*item_values))
    return items
