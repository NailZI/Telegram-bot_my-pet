import time
from pythonping import ping
from logs import logger


def response(hostname):
    try:
        m = ping(hostname, timeout=3, count=5)
        time.sleep(1)
    except Exception as err:
        m = f'ping IP {hostname} не доступен!\n' + str(err)
        #logger('no_user', m)
    return m


if __name__ == '__main__':
    host_1 = '159.159.2.166'
    host_2 = '1.1.1.2'
    # print(host_1, '\n', response(host_1))
    # print(host_2, '\n', response(host_2))
    n = str(response(host_1))
    print(type(n))
    print(n.split('\n'))
