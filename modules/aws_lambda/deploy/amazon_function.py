import urllib.request

import coinmarketcap

print('Loading function')


def dotabuff(request):
    base_url = 'https://www.dotabuff.com/heroes/lanes?lane='
    base_url += request
    print(base_url)
    return base_url


def coin_market(request):
    api = coinmarketcap.Market()
    return api.ticker(request)


def lambda_handler(event, context):
    print("service = " + event['site'])
    print("request = " + event['lookup'])

    if event['site'] == "dotabuff":
        url = dotabuff(event['lookup'])
        page = fetch_page(url)
        return {
            'message': page
        }
    elif event['site'] == "crypto":
        info = coin_market(event['lookup'])
        return {
            'message': info
        }


def fetch_page(url):
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    page = urllib.request.urlopen(req)
    return page.read().decode('utf-8')