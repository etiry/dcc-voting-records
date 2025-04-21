def get_filename_from_url(url):
    return url.rstrip('/').split('/')[-1]
