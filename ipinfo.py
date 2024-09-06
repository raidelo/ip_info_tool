from requests import get, RequestException
from argparse import ArgumentParser

# API's website: https://ip-api.com/

class IpInfoHandler:
    url = 'http://ip-api.com/json/'

    def __init__(self):
        self.__fields = 66846719 # = ALL. For more options refer to the API's website: https://ip-api.com/
        self.__timeout = 10

    def get_info(self, ip:str=None) -> dict:
        url = self.url + ip if ip and isinstance(ip, str) else self.url + ''
        params = {'fields': self.__fields}
        try:
            response = get(url,
                           params=params,
                           timeout=self.__timeout,
                           )
            if 'application/json' in response.headers['Content-Type']:
                json = response.json()
                return json if len(json) != 0 else {'content': 'empty'}
            else:
                return {'content': 'invalid'}
        except RequestException:
            return {'error': 'check your internet access or firewall settings'}
        return {'error': 'unknown error'}

    def set_timeout(self, t) -> None:
        self.__timeout = t

    def get_timeout(self) -> int:
        return self.__timeout

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("ip", default=None, nargs="?", action="store",
                        help="IPv4 address which information you want to get "
                        "(default: yours)")
    args = parser.parse_args()

    if args.ip != None and not (args.ip.count('.') == 3 and all(map(lambda x: x.isnumeric(), args.ip.split('.')))):
        parser.error("{} is not a valid IPv4 address".format(args.ip))

    ip_handler = IpInfoHandler()
    res = ip_handler.get_info(args.ip)

    max_key_length = max(map(len, res.keys()))

    for key, value in res.items():
        print(f'{key.ljust(max_key_length)}: {value}')