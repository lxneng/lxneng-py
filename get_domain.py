def domain(url):
    """
    Returns the domain of a URL e.g. http://www.lxneng.com/ > lxneng.com
    """
    rv = urlparse.urlparse(url).netloc
    if rv.startswith("www."):
        rv = rv[4:]
    return rv