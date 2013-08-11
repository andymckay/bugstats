from pprint import pprint

import requests

from .utils import multikeysort

args = {
    'bug_status': ('UNCONFIRMED', 'NEW', 'ASSINGED', 'REOPENED'),
    'email1': 'wraithan@mozilla.com',
    'email1_assigned_to': 1,
    'target_milestone': '---',
    'target_milestone_type': 'not_equals'
}


def get_bugs():
    res = requests.get(
        url='https://api-dev.bugzilla.mozilla.org/latest/bug',
        params=args
    )
    keys = ('target_milestone', 'summary', 'id', 'priority')
    bugs = [dict([(key, bug[key]) for key in keys])
            for bug in res.json()['bugs']]
    sorted_bugs = multikeysort(bugs, ('target_milestone', 'priority'))
    return {
        'bugs': sorted_bugs,
        'source': 'api'
    }

if __name__ == '__main__':
    pprint(get_bugs())
