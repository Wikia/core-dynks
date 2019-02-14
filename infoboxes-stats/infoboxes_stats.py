"""
Given a list of wikis emits statistics regarding shared templates, their parameters
and value types
"""
from __future__ import print_function

import logging

from collections import Counter

from mwclient.client import Site
import requests

logging.basicConfig(level=logging.INFO)


# set up shared HTTP client
pool = requests.Session()
pool.proxies = {'http': 'border-http-s3:80'}


def get_site(wiki_domain: str):
    """
    :type wiki_domain str
    :rtype: Site
    """
    return Site(host=('http', wiki_domain), path='/', pool=pool)


def get_querypage(site: Site, page: str):
    """
    :type site Site
    :type page str
    :rtype: list[str]
    """
    # http://poznan.wikia.com/api.php?action=query&list=querypage&qppage=Nonportableinfoboxes
    # http://poznan.wikia.com/api.php?action=query&list=querypage&qppage=Mostlinkedtemplates
    res = site.get(action='query', list='querypage', qppage=page, qplimit=500)
    return [
        # (u'value', u'69'), (u'ns', 10), (u'title', u'Template:Crew TV')
        entry['title']
        for entry in res['query']['querypage']['results']
    ]


def get_portable_infoboxes(wikis):
    """
    :type: wikis list[str]
    :rtype: list[str]
    """
    logger = logging.getLogger('get_portable_infoboxes')

    global_templates = Counter()

    for wiki_domain in wikis:
        site = get_site(wiki_domain)

        logger.info('Processing <%s> wiki', site.host[1])

        all_infoboxes = get_querypage(site, 'AllInfoboxes')
        non_portable = get_querypage(site, 'Nonportableinfoboxes')
        # print(all_infoboxes, non_portable)

        logger.info('%s: %d infoboxes in total (%d of them are non-portable)',
                    wiki_domain, len(all_infoboxes), len(non_portable))

        # list only portable infoboxes
        infoboxes = [
            template
            for template in all_infoboxes
            if template not in non_portable
        ]

        # print(wiki_domain, infoboxes)

        for infobox in infoboxes:
            global_templates.update((infobox,))

    logger.info('%d unique template', len(global_templates.keys()))
    logger.info(global_templates.most_common(10))


if __name__ == '__main__':
    mapping = get_portable_infoboxes(
        wikis="""
villains.fandom.com
walkingdead.fandom.com
memory-alpha.fandom.com
powerrangers.fandom.com
steven-universe.fandom.com
ttte.fandom.com
spongebob.fandom.com
supernatural.fandom.com
muppet.fandom.com
tardis.fandom.com
vampirediaries.fandom.com
hero.fandom.com
        """.strip().split('\n')
    )

    """
    for arg, items in mapping.items():
        print('{} -> {}'.format(
            arg, items))
    """
