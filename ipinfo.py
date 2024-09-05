from requests import get, RequestException
from argparse import ArgumentParser

# API's website: https://ip-api.com/

def ip_info(ip:str=None, timeout:int=10) -> dict:
    url = 'http://ip-api.com/json/'
    params = {'fields': 66846719} # = ALL. For more options refer to the API's website: https://ip-api.com/
    try:
        response = get(url+(ip if ip and isinstance(ip, str) else ''), params=params, timeout=timeout)
        if 'application/json' in response.headers['Content-Type']:
            return response.json()
    except RequestException:
        pass
    return {'error': 'check your internet access or firewall settings'}

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("ip", default=None, nargs="?", action="store",
                        help="IPv4 address which information you want to get "
                        "(default: yours)")
    args = parser.parse_args()

    if args.ip != None and not (args.ip.count('.') == 3 and all(map(lambda x: x.isnumeric(), args.ip.split('.')))):
        parser.error("{} is not a valid IPv4 address".format(args.ip))

    res = ip_info(args.ip)

    max_key_length = max(map(len, res.keys()))

    for key, value in res.items():
        print(f'{key.ljust(max_key_length)}: {value}')