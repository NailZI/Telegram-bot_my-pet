# Доступ в КШ-М посредством telnet для проверки чтения лога

import telnetlib
import time
import re
from date_from_log import read_date


def log_proc(file):
    corr = ('ek260', 'spg761', 'spg741', 'sevcd.dev1', 'ek270',
            'irvis_rs4', 'spg742.dev1', 'tc215', 'tekon17', 'ek88_Dev1',
            'tc215', 'bp97tm')
    corr_log = None
    for c in corr:
        if c in file:
            corr_log = c
    print(corr_log)
    return corr_log


def telnetLog(ip):
    try:
        all_result = f'Запрос к IP {ip} не удался'
        telnet = telnetlib.Telnet(ip)
        telnet.read_until(b'ksh-m login:')  # проверка запроса логина
        telnet.write(b'******\n')  # ввод логина
        time.sleep(2)  # ожидание
        telnet.read_until(b'Password:')  # проверка запроса пароля
        telnet.write(b'*********\n')  # ввод пароля
        time.sleep(2)  # ожидание
        telnet.read_until(b'$')  # проверка принятия пароля
        telnet.write(b'su\n')  # ввод логина админа
        time.sleep(2)
        telnet.read_until(b'Password:')  # проверка запроса пароля
        telnet.write(b'**********\n')  # ввод пароля админа
        telnet.read_until(b'#')  # проверка выполнения команды
        telnet.write(b'cd /mnt/opt/ps\n')  # переход в папку /mnt/opt/ps
        telnet.read_until(b'#')  # проверка выполнения команды
        telnet.write(b'ls -l\n')  # показать содержимое папки
        time.sleep(10)
        log_file = telnet.read_very_eager().decode('latin-1')  # чтение результата
        corr = log_proc(log_file)
        if corr == None:
            all_result = 'log файл корректора не найден'
        else:
            pass
            file_log = read_date(log_file, corr)
            resp = f'cat {file_log}\n'.encode('utf-8')  # формирование команды tail -f
            # resp = f'tail -f {file_log}\n'.encode('utf-8')  # формирование команды tail -f
            telnet.write(resp)  # отправка команды
            # print('запрос >>')
            time.sleep(30)
            # telnet.read_until(b'#')  # проверка выполнения команды
            all_result = telnet.read_very_eager().decode('latin-1')  # чтение результата
            # print('>> ответ')
        telnet.close()
        # all_result = None
        return all_result

    except Exception as err:
        all_result = f'запрос лога {ip} ошибка выполнения операции\n' + str(err)
        return all_result


if __name__ == '__main__':
    print(telnetLog('159.159.2.166'))
    print(telnetLog('159.159.5.19'))
