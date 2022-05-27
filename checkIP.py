# выполение запроса к кш-м

import re
from IPy import IP
from pingConnect import response
from psConnect import telnetPs
from killallConnect import kill
from read_logs import telnetLog
from logs import logger


def allocation_of_an_ip_address(m_text):
    """Выделение IP адреса из сообщения"""
    ip_s = ''
    spc = re.search(r'\d', m_text)  # проверка, содержит ли текст цифры (IP адрес)
    if spc:
        spc_pos = spc.start()  # определяем позицию первой цифры
        for i in range(spc_pos, len(m_text)):
            ip_s = ip_s + str(m_text[i])  # выделяем из текста полный IP адрес
        text = ip_s
    else:
        text = 'Проверьте введенный IP'
    return text

def responce_kshm(user, key_word, mess):
    """Выполнение запроса к КШ(М)"""
    resp = ''
    IPw = allocation_of_an_ip_address(mess)
    try:
        IP(IPw)
        if key_word == 'ping':  # если требуется пропинговать
            resp = response(IPw)  # обращение к функции пингования pingConnect.py
        elif key_word == 'ps':  # если требуется проверить работу драйвера
            ch_resp = telnetPs(IPw)  # обращение к функции зароса ps psConnect.py
            if 'pipgw -f pipgw.conf' in ch_resp:
                resp = 'Драйвер запущен'
            else:
                resp = 'Драйвер не работает'
        elif key_word == 'kill':  # если требуется перезагрузить КШ(М)
            resp = kill(IPw)  # обращение к функции перезагрузки killConnect.py
        elif key_word == 'log':  # если требуется прочитать лог
            resp = telnetLog(IPw)

    except Exception as err:
        resp = "Введен неправильный IP\n" + str(err)
    resp_txt = key_word + '_' + IPw
    logger(user, resp_txt, resp)
    return resp


if __name__ == '__main__':
    user = 'probe'
    kw = 'log'
    mess = '/log 159.159.2.166'
    print(responce_kshm(user, kw, mess))