import os
from datetime import datetime, timedelta

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

if settings:
    args.update(settings.additional_filter)
elif os.getenv('BUGZILLA_FILTER', False):
    var = os.getenv('BUGZILLA_FILTER')
    args.update(dict(pair.split('=') for pair in var.split(';')))

bugzilla_url = 'https://api-dev.bugzilla.mozilla.org/latest/count'


def get_stats():
    source = 'api'
    res = requests.get(url=bugzilla_url, params=args).json()
    labels = [datetime.strptime(l, '%Y-%m-%d').date()
              for l in res['x_labels'][1:]]
    closed_bugs = dict(zip(labels, res['data'][1:]))
    first_label = labels[-1]
    i = labels[0]
    week = timedelta(days=7)
    while i < first_label:
        if i not in labels:
            closed_bugs[i] = 0
        i += week

    data = []
    to_avg = []
    for date, count in sorted(closed_bugs.iteritems()):
        if len(to_avg) > 5:
            to_avg.pop(0)
        to_avg.append(count)
        data.append({'date': date.isoformat(),
                     'count': count,
                     'avg': sum(to_avg)/float(len(to_avg))})

    return {'data': data, 'source': source}


if __name__ == '__main__':
    print get_stats()
