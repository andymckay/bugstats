import os
from datetime import date, datetime, timedelta
from pprint import pprint
from operator import itemgetter

import requests

try:
    import settings
except ImportError:
    settings = False

args = {
    'email1': 'wraithan@mozilla.com',
    'email1_assigned_to': 1,
    'bug_status': ('RESOLVED', 'VERIFIED', 'CLOSED'),
    'x_axis_field': 'target_milestone',
    'resolution': 'FIXED',
}

open_bugs = {
    'bug_status': ('UNCONFIRMED', 'NEW', 'ASSINGED', 'REOPENED'),
    'email1': 'wraithan@mozilla.com',
    'email1_assigned_to': 1,
    'target_milestone': '---',
    'target_milestone_type': 'not_equals'
}

if settings:
    args.update(settings.additional_filter)
elif os.getenv('BUGZILLA_FILTER', False):
    var = os.getenv('BUGZILLA_FILTER')
    auth = dict(pair.split('=') for pair in var.split(';'))
    args.update(auth)

bugzilla_url = 'https://api-dev.bugzilla.mozilla.org/latest/count'
bug_url = 'https://bugzilla.mozilla.org/show_bug.cgi?id={id}'


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


def get_bugs():
    res = requests.get(
        url='https://api-dev.bugzilla.mozilla.org/latest/bug',
        params=open_bugs
    )
    keys = ('target_milestone', 'summary', 'id', 'priority')
    bugs = [dict([(key, bug[key]) for key in keys])
            for bug in res.json()['bugs']]
    sorted_bugs = multikeysort(bugs, ('target_milestone', 'priority'))
    return {
        'bugs': sorted_bugs,
        'source': 'api'
    }


def get_stats():
    source = 'api'
    try:
        res = requests.get(url=bugzilla_url, params=args, timeout=1,
                           verify=True).json()
    except requests.Timeout:
        return {'error': 'Bugzilla timed out'}
    start = 1
    labels = [datetime.strptime(l, '%Y-%m-%d').date()
              for l in res['x_labels'][start:]]
    closed_bugs = dict(zip(labels, res['data'][start:]))

    # This code fills in all the 0 bug milestones
    today = date.today()
    i = labels[0]
    day = timedelta(days=1)
    days = 0
    while i < today:
        if i not in labels:
            if days == 7:
                closed_bugs[i] = 0
                days = 0
            days += 1
        else:
            days = 0
        i += day

    # This code calculates the ideal and average closed bugs
    data = []
    to_avg = []
    for label, count in sorted(closed_bugs.iteritems()):
        if len(to_avg) >= 4:
            to_avg.pop(0)
        to_avg.append(count)
        ideal = (4*len(to_avg))-sum(to_avg[:-1])
        if ideal > 8:
            ideal = 8
        data.append({'date': label.isoformat(),
                     'count': count,
                     'avg': sum(to_avg)/float(len(to_avg)),
                     'ideal': ideal})

    return {'stats': data, 'source': source}


if __name__ == '__main__':
    pprint(get_bugs())
    pprint(get_stats())
