from requests import get, RequestException
from sys import argv

# API's website: https://ip-api.com/

def ip_info(ip:str=None) -> dict:
    url = 'http://ip-api.com/json/'
    params = {'fields': 66846719} # = ALL. For more options refer to the API's website: https://ip-api.com/
    try:
        response = get(url+(ip if ip else ''), params=params, timeout=10)
        if 'application/json' in response.headers['Content-Type']:
            return response.json()
    except RequestException:
        pass
    return {'Error': 'Compruebe su conexión'}

def show_help():
    print('Ingresar como parámetro a continuación del script la IP cuya información desea saber. Ej: ip_info 168.230.13.21')

if __name__ == '__main__':
    show_help_ = 1
    if len(argv) == 1:
        ip=None
        show_help_ = 0
    elif len(argv) == 2:
        if argv[1].count('.') == 3:
            if all([i.isnumeric() for i in argv[1].split('.')]):
                ip = argv[1]
                show_help_ = 0
    if show_help_:
        show_help()
        exit(1)
    res = ip_info(ip)
    for i in res.keys():
        print(f'{i}: {res[i]}')