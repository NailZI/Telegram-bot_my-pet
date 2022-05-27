# поиск данных из файла journal_741.xlsx (копия журнала)

import pandas
import os
import bot_conf
from logs import logger

# чтение данных из excel
os.chdir(bot_conf.folder_test)
excel_data = pandas.read_excel('journal_741.xlsx', sheet_name='list', usecols=['ID', 'IP', 'KSHM',
                                        'Object'])
journ_dict_list = excel_data.to_dict('records')


# поиск по тексту
def find_text(user, text='default'):
    answ = ''
    for i in range(len(journ_dict_list)):
        d = str(journ_dict_list[i]['Object'])
        if text.lower() in d.lower():
            if answ == 'Текст не найден\n':  # очистка переменной перед записью в нее найденного значения
                answ = '\n'
            id = 'id: ' + str(int(journ_dict_list[i]['ID']))
            kshm = 'kshm: ' + str(journ_dict_list[i]['KSHM'])
            ip = 'ip: ' + str(journ_dict_list[i]['IP'])
            answ = answ + d + '\n' + id + '\n' + kshm + '\n' + ip + '\n\n'
        elif not answ:
            answ = 'Текст не найден\n'
    #if len(answ) > 4096:  # проверка на превышение количества знаков в сообщении
    #    answ = 'Некорректный запрос, попробуйте сформулировать по другому.\n'
    logger(user, text, answ)
    return answ

# поиск по номеру ID
def find_id(user, id='0'):
    answ = ''
    for i in range(len(journ_dict_list)):
        d = str(journ_dict_list[i]['ID'])
        if id.strip() == d:
            answ = 'ID: ' + d + ' >> ' + str(journ_dict_list[i]['Object']) + '\nip: ' + str(journ_dict_list[i]['IP'])
        elif not answ:
            answ = f'ID: {id} не найден.'
    logger(user, id, answ)
    return answ

# поиск по номеру КШ(М)
def find_kshm(user, kshm='0'):
    answ = ''
    for i in range(len(journ_dict_list)):
        d = str(journ_dict_list[i]['KSHM'])
        if kshm.strip() in d:
            if answ == f'КШ(М): {kshm} не найден.':
                answ = '\n'
            answ = answ + str(journ_dict_list[i]['Object']) \
                   + '\nid: ' + str(journ_dict_list[i]['ID']) \
                   + '\nkshm: ' + d \
                   + '\nip: ' + str(journ_dict_list[i]['IP']) + '\n\n'
        elif not answ:
            answ = f'КШ(М): {kshm} не найден.'
    #if len(answ) > 4096:  # проверка на превышение количества знаков в сообщении
    #    answ = 'Некорректный запрос, попробуйте сформулировать по другому.\n'
    logger(user, kshm, answ)
    return answ


if __name__ == '__main__':
#    find_text('Производственная база')
#    print(find_text('производственная база'))
#    print(find_text('kkk'))
#    print(find_id('70'))
#    print(find_id('2228'))
#   print(find_kshm('2228'))
    print(find_kshm('user', '333'))