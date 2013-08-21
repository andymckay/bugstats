import requests


repos = [
    {
        'owner': 'mozilla',
        'repo': 'zamboni'
    }, {
        'owner': 'mozilla',
        'repo': 'webpay'
    }, {
        'owner': 'mozilla',
        'repo': 'solitude'
    }
]
url = 'https://api.github.com/repos/{owner}/{repo}/pulls'


def get_prs():
    aggregate = []
    for repo in repos:
        pr_data = {
            'name': '{owner}/{repo}'.format(**repo),
            'prs': []
        }
        aggregate.append(pr_data)
        res = requests.get(url.format(**repo)).json()
        for raw_pr in res:
            pr = {
                'title': raw_pr['title'],
                'url': raw_pr['html_url'],
                'number': raw_pr['number']
            }
            pr_data['prs'].append(pr)
    return aggregate
