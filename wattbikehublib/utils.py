import re

def username_parser(url):
    regex = '^((http[s]*:\/\/)|)hub.wattbike.com\/(?P<username>[a-z\.\d]+)$'
    result = re.match(regex, url)
    if result:
        return result.groupdict()['username']
