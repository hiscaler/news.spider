# encoding=utf-8
import requests


def post_urls(urls, language='en-US'):
    for url in urls:
        post_url(url, language)


def post_url(url, language='en-US'):
    print("URL: %s" % url, end=' ')

    response = requests.post('http://localhost:8002/index.php/api/post/url/create', data={"language": language, "url": url})
    if response.ok:
        body = response.json()
        if body['success']:
            print("Success")
        else:
            print("Failed: %s" % body['error']['message'])
    else:
        print(response.text)

    print('-' * 120)
