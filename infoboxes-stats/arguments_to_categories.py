"""
Produces template's named argument to article categories mapping
"""
from __future__ import print_function

import logging
import json
import re

from collections import defaultdict

from mwclient.client import Site
import requests

logging.basicConfig(level=logging.INFO)


def get_articles_from_top_categories(site, categories_limit=3, articles_limit=5):
    """
    :type site Site
    :type categories_limit int
    :type articles_limit int
    :rtype: list[str,str]
    """
    # http://muppet.sandbox-s6.wikia.com/api.php?action=query&list=querypage&qppage=Mostpopularcategories&qplimit=20
    res = site.get(action='query', list='querypage', qppage='Mostpopularcategories', qplimit=categories_limit)

    categories = [result['title'] for result in res['query']['querypage']['results']]

    for category in categories:
        # get first X pages from the category
        # http://muppet.sandbox-s6.wikia.com/api.php?action=query&list=categorymembers&cmtitle=Category:Sesame%20Street%20Episodes&cmlimit=50
        res = site.get(action='query', list='categorymembers', cmtitle='Category:{}'.format(category), cmlimit=articles_limit)

        for page in res['query']['categorymembers']:
            # we're interested in main namespace articles one
            if page['ns'] == 0:
                yield page['title'], category


def get_infobox_arguments(site, title):
    """
    :type site Site
    :type title str
    :rtype: list[str]
    """
    logger = logging.getLogger('get_infobox_arguments')
    logger.info('Article: %s', title)

    # https://nfs.sandbox-s6.fandom.com/wikia.php?controller=TemplatesApiController&method=getMetadata&title=Ferrari_355_F1
    res = json.loads(site.raw_call(
        http_method='GET',
        script='wikia',
        data={
            'controller': 'TemplatesApiController',
            'method': 'getMetadata',
            'title': title
        }
    ))

    infoboxes = [template for template in res['templates'] if template['type'] == 'infobox']
    # print(infoboxes)

    # return a set of template arguments used on a given article
    arguments = set()

    for infobox in infoboxes:
        arguments.update(infobox['parameters'].keys())

    return arguments


def arguments_to_categories(wikis, env=None, proxy=None):
    """
    :type wikis list[str]
    :type env str
    :type proxy str
    :rtype: dict
    """
    logger = logging.getLogger('arguments_to_categories')

    # apply the environment
    if env:
        wikis = [re.sub(r'\.(wikia|fandom)', '.{}.\\1'.format(env), wiki) for wiki in wikis]

    logger.info('Gathering stats for %s domains', wikis)

    # we will emit results as (template argument) => (a set of article categories where this argument is used)
    res = defaultdict(set)

    # set up connection to MediaWiki backend via our internal proxy
    pool = requests.Session()
    if proxy:
        logger.info('Using HTTP proxy: %s', proxy)
        pool.proxies = {'http': proxy}

    # gather statistics for each wiki
    for wiki in wikis:
        site = Site(host=('http', wiki), path='/', pool=pool)

        # process each article
        for article, category in get_articles_from_top_categories(site):
            # update each template argument found with a category where this article is in
            for argument in get_infobox_arguments(site, article):
                res[argument].add(category)

    return res


if __name__ == '__main__':
    mapping = arguments_to_categories(
        wikis=[
            'muppet.wikia.com',
            'nfs.fandom.com',
            'gta.wikia.com',
        ],
        env='sandbox-s6',
        proxy='border-http-s3:80'
    )

    for arg, items in mapping.items():
        print('{} -> {}'.format(
            arg, items))
