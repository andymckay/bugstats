import os
from datetime import date, datetime, timedelta
from pprint import pprint

import requests

try:
    import settings
except ImportError:
    settings = False


bugzilla_url = 'https://api-dev.bugzilla.mozilla.org/latest/count'
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
    args.update(dict(pair.split('=')
                for pair in os.getenv('BUGZILLA_FILTER').split(';')))


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
    pprint(get_stats())
