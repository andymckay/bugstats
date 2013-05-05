from datetime import datetime, timedelta

import requests

try:
    import settings
except ImportError:
    pass

args = {
    'email1': 'wraithan@mozilla.com',
    'email1_assigned_to': 1,
    'bug_status': ('RESOLVED', 'VERIFIED', 'CLOSED'),
    'x_axis_field': 'target_milestone',
    'resolution': 'FIXED',
}

if settings:
    args.update(settings.additional_filter)

bugzilla_url = 'https://api-dev.bugzilla.mozilla.org/latest/count'


def get_stats():
    res = requests.get(url=bugzilla_url, params=args).json()
    labels = [datetime.strptime(l, '%Y-%m-%d').date()
              for l in res['x_labels'][1:]]
    data = res['data'][1:]
    closed_bugs = dict(zip(labels, data))
    first_label = labels[-1]
    i = labels[0]
    week = timedelta(days=7)
    while i < first_label:
        if i not in labels:
            closed_bugs[i] = 0
        i += week

    keys = []
    values = []
    for key in sorted(closed_bugs.iterkeys()):
        keys.append(key.isoformat())
        values.append(closed_bugs[key])

    return {'dates': keys, 'count': values}


if __name__ == '__main__':
    print get_stats()
