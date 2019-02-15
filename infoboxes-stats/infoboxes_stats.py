"""
Given a list of wikis emits statistics regarding shared templates, their parameters
and value types

This script for each wiki:

- takes 50 most used portable infoboxes
- analyzes the names of template parameters

It also writes values.txt file with all values taken from infoboxes.
"""
import json
import logging

from collections import Counter, defaultdict

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


def get_querypage(site: Site, page: str, limit: int = 500):
    """
    :type site Site
    :type page str
    :type limit int
    :rtype: list[str]
    """
    # http://poznan.wikia.com/api.php?action=query&list=querypage&qppage=Nonportableinfoboxes
    # http://poznan.wikia.com/api.php?action=query&list=querypage&qppage=Mostlinkedtemplates
    # http://poznan.wikia.com/api.php?action=query&list=querypage&qppage=AllInfoboxes
    res = site.get(action='query', list='querypage', qppage=page, qplimit=limit)
    return [
        # (u'value', u'69'), (u'ns', 10), (u'title', u'Template:Crew TV')
        entry['title']
        for entry in res['query']['querypage']['results']
    ]


def get_portable_infobox_params(site: Site, template_name: str):
    """
    Please provide Template namespace suffix in template_name

    :type site Site
    :type template_name str
    :rtype: list[str]
    """
    logging.info('Getting "%s" infobox parameters ...', template_name)

    # http://poznan.wikia.com/api.php?action=templateparameters&titles=Szablon:Ulica_infobox&format=json
    res = site.get(action='templateparameters', titles=template_name)

    if res['pages']:
        item = next(iter(res['pages'].items()))[1]
        return item['params']

    return []


def get_articles_with_infobox(site: Site, template: str, limit: int = 500):
    """
    :type site Site
    :type template str
    :type limit int
    :rtype list[str]
    """
    # http://poznan.wikia.com/api.php?action=query&list=embeddedin&eititle=Szablon:Ulica_infobox&eilimit=500
    res = site.get(action='query', list='embeddedin', eititle=template, eilimit=limit)
    return [
        # <ei pageid="3915" ns="0" title="Czartoria" />
        entry['title']
        for entry in res['query']['embeddedin']
        if entry['ns'] == 0  # NS_MAIN only
    ]


def get_infoboxes_from_article(site: Site, title: str):
    """
    :type site Site
    :type title str
    :rtype: list[str, dict]
    """
    logger = logging.getLogger('get_infoboxes_from_article')
    logger.info('Article: %s', title)

    # https://nfs.fandom.com/wikia.php?controller=TemplatesApiController&method=getMetadata&title=Ferrari_355_F1
    res = json.loads(site.raw_call(
        http_method='GET',
        script='wikia',
        data={
            'controller': 'TemplatesApiController',
            'method': 'getMetadata',
            'title': title
        }
    ))

    return [
        # Ulica infobox -> Template:Ulica infobox
        ('Template:{}'.format(template['name']), template['parameters'])
        for template in res['templates']
        if template['type'] == 'infobox'
    ]


def get_portable_infoboxes(wikis):
    """
    :type: wikis list[str]
    :rtype: list[str]
    """
    logger = logging.getLogger('get_portable_infoboxes')

    # on how many wikis a template is used?
    global_templates = Counter()

    # how frequently is a given parameter used in this template across wikis?
    template_parameters = defaultdict(Counter)

    # raw values as we get them
    # they will be stored in "values.txt" file for further processing
    template_values = []

    for wiki_domain in wikis:
        site = get_site(wiki_domain)

        logger.info('Processing <%s> wiki', site.host[1])

        # fetch all templates as we want to get only the top templates
        templates = get_querypage(site, 'Mostlinkedtemplates')
        all_infoboxes = get_querypage(site, 'AllInfoboxes')
        non_portable = get_querypage(site, 'Nonportableinfoboxes')
        # print(all_infoboxes, non_portable)

        logger.info('%s: %d infoboxes in total (%d of them are non-portable)',
                    wiki_domain, len(all_infoboxes), len(non_portable))

        # list only portable infoboxes
        infoboxes = [
            template
            for template in templates
            if template in all_infoboxes and template not in non_portable
        ][:50]

        # process each portable infobox
        for infobox in infoboxes:
            params = get_portable_infobox_params(site, infobox)
            # print(wiki_domain, infobox, params)

            # update per template params statistics
            template_parameters[infobox].update(set(params))

            # now get article that use a given infobox
            articles = get_articles_with_infobox(site, infobox, 50)

            for article in articles:
                data = get_infoboxes_from_article(site, article)
                # print(data)

                for template_name, parameter in data:
                    # ignore data coming from other templates and infoboxes
                    if template_name != infobox:
                        continue

                    template_values += [
                        str(value).strip().replace("\n", '\\n')
                        for value in parameter.values()
                    ]

        # print(wiki_domain, "\n".join(template_values)); exit(1)

        # print(wiki_domain, infoboxes)

        for infobox in infoboxes:
            global_templates.update((infobox,))

    logger.info('%d unique template', len(global_templates.keys()))

    # get info about most common ones
    for infobox, usage_count in global_templates.most_common(25):
        logger.info('Most common parameters for %s (used on %d wikis): %s',
                    infobox, usage_count,
                    template_parameters[infobox].most_common())

    # write collected values to a file
    with open('values.txt', 'wt') as fp:
        for value in template_values:
            fp.write(value + "\n")

    logger.info('values.txt file written - %d lines', len(template_values))


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
        """.strip().split('\n')[:2]
    )

    """
    for arg, items in mapping.items():
        print('{} -> {}'.format(
            arg, items))
    """
