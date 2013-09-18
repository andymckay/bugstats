from operator import itemgetter
from urllib import urlencode

def multikeysort(items, columns):
    comparers = [((itemgetter(col[1:].strip()), -1)
                 if col.startswith('-')
                 else (itemgetter(col.strip()), 1))
                 for col in columns]

    def comparer(left, right):
        for fn, mult in comparers:
            result = cmp(fn(left), fn(right))
            if result:
                return mult * result
        else:
            return 0
    return sorted(items, cmp=comparer)


def encode(dictionary):
    items = []
    for key, value in dictionary.iteritems():
        if key == 'email1_assigned_to':
            key = 'emailassigned_to1'
        if type(value) == tuple:
            for v in value:
                items.append((key, v))
            continue
        items.append((key, value))
    return urlencode(sorted(items))
