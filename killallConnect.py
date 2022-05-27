# Соединение с КШ(М) через telnet для перезагрузки
import telnetlib
import time
from logs import logger

def kill(ip):
    try:
        telnet = telnetlib.Telnet(ip)
        telnet.read_until(b'ksh-m login:') # КШ-М готов к приему команд
        telnet.write(b'****\n') # логин входа
        time.sleep(2)
        telnet.read_until(b'Password:') # пароль входа
        telnet.write(b'*******\n')
        time.sleep(2)
        telnet.read_until(b'$')
        #print('Connect ok')
        telnet.write(b'su\n')
        time.sleep(2)
        telnet.read_until(b'Password:')
        telnet.write(b'*********\n')
        time.sleep(2)
        telnet.read_until(b'#')
        telnet.write(b'cd /mnt/opt/ps\n') # переход к папке ps
        time.sleep(2)
        telnet.write(b'rm *log*\n') # удаление логов
        time.sleep(2)
        telnet.write(b'killall pipgw\n') # остановка драйвера
        time.sleep(2)
        telnet.write(b'reboot\n') # перезагрузка
        telnet.close()
        res = f'{ip} перезагрузка выполнена успешно'
    except Exception as err:
        res = f'kill {ip} ошибка выполнения перезагрузки\n' + str(err)
        #logger('no_user', res)
    return res

if __name__ == '__main__':
    print(kill('159.159.2.174'))