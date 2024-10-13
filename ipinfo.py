from requests import get, RequestException
from argparse import ArgumentParser

# API's website: https://ip-api.com/

class IpInfoHandler:
    url = 'http://ip-api.com/json/'
    FIELDS = {
    'as'           : (2048, 'AS number and organization, separated by space (RIR). Empty for IP blocks not being announced in BGP tables.'),
    'asname'       : (4194304, 'AS name (RIR). Empty for IP blocks not being announced in BGP tables.'),
    'city'         : (16, 'City'),
    'continent'    : (1048576, 'Continent name'),
    'continentCode': (2097152, 'Two-letter continent code'),
    'country'      : (1, 'Country name'),
    'countryCode'  : (2, 'Two-letter country code ISO 3166-1 alpha-2'),
    'currency'     : (8388608, 'National currency'),
    'district'     : (524288, 'District (subdivision of city)'),
    'hosting'      : (16777216, 'Hosting, colocated or data center'),
    'isp'          : (512, 'ISP name'),
    'lat'          : (64, 'Latitude'),
    'lon'          : (128, 'Longitude'),
    'message'      : (32768, 'included only when status is failCan be one of the following: private range, reserved range, invalid query'),
    'mobile'       : (65536, 'Mobile (cellular) connection'),
    'offset'       : (33554432, 'Timezone UTC DST offset in seconds'),
    'org'          : (1024, 'Organization name'),
    'proxy'        : (131072, 'Proxy, VPN or Tor exit address'),
    'query'        : (8192, 'IP used for the query'),
    'region'       : (4, 'Region/state short code (FIPS or ISO)'),
    'regionName'   : (8, 'Region/state'),
    'reverse'      : (4096, 'Reverse DNS of the IP (can delay response)'),
    'status'       : (16384, 'success or fail'),
    'timezone'     : (256, 'Timezone (tz)'),
    'zip'          : (32, 'Zip code'),
    }
    DEFAULT_FIELDS = (
    "status",
    "message",
    "country",
    "countryCode",
    "region",
    "regionName",
    "city",
    "lat",
    "lon",
    "timezone",
    "isp",
    "org",
    "as",
    "query",
    )

    def __init__(self):
        self.DEFAULT_FIELDS_NUM = sum(self.FIELDS[value][0] for value in self.DEFAULT_FIELDS)
        self.ALL_FIELDS_NUM = sum(pair[0] for pair in self.FIELDS.values())
        self.__fields = self.DEFAULT_FIELDS_NUM
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

    def set_timeout(self, t) -> None:
        self.__timeout = t

    def get_timeout(self) -> int:
        return self.__timeout

    def set_fields(self, num) -> None:
        if num > self.ALL_FIELDS_NUM:
            raise ValueError(f"{num} too large")
        self.__fields = num

    def get_fields(self) -> int:
        return self.__fields

    def resolve_fields(self, input) -> int:
        if isinstance(input, str):
            pre_data = input.split(',')
            if len(pre_data) == 0:
                return 0
            data = list(map(lambda x: x.strip(), pre_data))
        elif isinstance(input, (list, tuple)):
            data = list(map(lambda x: x.strip(), input))
        num = 0
        for item in data:
            if item in self.FIELDS.keys():
                num += self.FIELDS[item][0]
            else:
                if item != '':
                    print(f'error: field not valid -> {item}')
        return num

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("ip", default=None, nargs="?",
                        help="IPv4 address which information you want to get "
                        "(default: yours)")
    parser.add_argument("-o", "--options", nargs=1, default=IpInfoHandler.DEFAULT_FIELDS, metavar="[option1,option2,option3,...]",
                        help="info fields you want to obtain. check documentation or API's web for all the options available (default: {})".format(','.join(IpInfoHandler.DEFAULT_FIELDS)))
    args = parser.parse_args()

    if args.ip != None and not (args.ip.count('.') == 3 and all(map(lambda x: x.isnumeric(), args.ip.split('.')))):
        parser.error("{} is not a valid IPv4 address".format(args.ip))

    ip_handler = IpInfoHandler()
    
    if args.options != IpInfoHandler.DEFAULT_FIELDS:
        ip_handler.set_fields(
            ip_handler.resolve_fields(args.options)
            )

    res = ip_handler.get_info(args.ip)

    max_key_length = max(map(len, res.keys()))

    for key, value in res.items():
        print(f'{key.ljust(max_key_length)}: {value}')