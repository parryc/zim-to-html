from urllib.parse import urlparse, parse_qs


def to_css(filename):
    url = f'https://{filename}'
    parsed_url = urlparse(url)
    unique_name = parse_qs(parsed_url.query)["modules"][0]
    unique_name = unique_name.replace("|", "_")
    unique_name = unique_name.replace(",", "_")
    return f'{unique_name}.css'
