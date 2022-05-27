# Доступ в КШ-М посредством telnet для проверки драйвера

import telnetlib
import time


def telnetPs(ip):
    try:
        telnet = telnetlib.Telnet(ip)
        telnet.read_until(b'ksh-m login:') # проверка запроса логина
        telnet.write(b'****\n') # ввод логина
        time.sleep(2) # ожидание
        telnet.read_until(b'Password:') # проверка запроса пароля
        telnet.write(b'********\n') # ввод пароля
        time.sleep(2) # ожидание
        telnet.read_until(b'$') # проверка принятия пароля
        telnet.write(b'su\n') # ввод логина админа
        time.sleep(2)
        telnet.read_until(b'Password:') # проверка запроса пароля
        telnet.write(b'*********\n') # ввод пароля админа
        time.sleep(2)
        telnet.write(b'ps\n') # ввод команды ps
        time.sleep(25)
        all_result = telnet.read_very_eager().decode('utf-8') + '\n' + ip # чтение результата
        telnet.close()
    except Exception as err:
        all_result = f'ps driver {ip} ошибка выполнения операции\n' + str(err)
        #logger('no_user', all_result)
    return all_result

if __name__ == '__main__':
    print(telnetPs('159.159.2.166'))
