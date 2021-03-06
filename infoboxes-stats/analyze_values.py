"""
Reads values.tx file (generated by infoboxes_stats.py script)
and provides statistics about their types
"""
import json
from collections import defaultdict


def get_stats_for_values(data):
    """
    :type: data list[str]
    :rtype: dict
    """
    stats = defaultdict(int)

    for line in data:
        stats['_all'] += 1

        value = str(line.strip())

        if value == '':
            stats['empty_value'] += 1
            continue

        if value.isdigit():
            # return true if all characters in the string are digits
            # and there is at least one character, false otherwise
            stats['numeric_value'] += 1
            continue

        if value.startswith('[['):
            stats['has_link'] += 1

        if '<' in value and '>' in value:
            stats['has_html'] += 1

        if "''" in value:
            stats['has_wikitext_formatting'] += 1

        if "gallery>" in value:
            stats['has_gallery'] += 1

        if "<br" in value:
            stats['has_br_tag'] += 1

        if "\\n" in value:
            stats['is_multiline'] += 1

        if value.endswith('.png') or value.endswith('.jpg') or value.endswith('.gif'):
            # a file perhaps?
            stats['image_name'] += 1

    return stats


if __name__ == "__main__":
    with open("values.txt") as fp:
        ret = get_stats_for_values(fp)
        print(json.dumps(ret, indent=True))
