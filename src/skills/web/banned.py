from urllib.parse import urlparse

import config


def is_website_banned(url: str) -> bool:
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    for banned_domain in config.BANNED_DOMAINS:
        if domain.endswith(banned_domain):
            return True

    return False
