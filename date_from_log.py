# Вытаскиваем дату создания файла из полученного сообщения
import re
import datetime
import time

mydate = datetime.datetime.now() # определение текущей даты
# print(mydate.strftime("%b"))
month = ('', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')


def read_date(data, corr):
    try:
        ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
        data = ansi_escape.sub('', data)
        timest = 0
        corr_log = r'{0}.log'.format(corr)
        # нахождение в тексте file всех позиций, с которых начинается 'наименование корректора.log'
        for m in re.finditer(corr_log, data):
            simb = data[m.start()]  # определение первой позиции

            i = end_pos = 0

            while simb != '\r':  # поиск позиции, где заканчивается текст, по переводу строки
                i += 1
                simb = data[m.start() + i]
                end_pos = m.start() + i  # запись последней позиции

            if data[m.start() - 4] == ':':  # если в позиции время записаны часы и минуты
                f_hour = data[m.start() - 6:m.start() - 4]
                f_min = data[m.start() - 3:m.start() - 1]
                f_year = mydate.strftime('%Y')
            else:  # если в позиции время записан год
                f_hour = '00'
                f_min = '00'
                f_year = data[m.start() - 5:m.start() - 1]

            file_dict = {'month': data[m.start() - 13:m.start() - 10],  # запись всех значений в словарь
                         'day': data[m.start() - 9:m.start() - 7],
                         'year': f_year,
                         'hour': f_hour,
                         'min': f_min,
                         'file': data[m.start():end_pos]}

            mnth = month.index(file_dict['month'])  # перевод символов месяца в цифру
            # сборка формы "день/месяц/год час:минуты" для преобразования в timestamp
            file_date = f"{file_dict['day']}/{mnth}/{file_dict['year']} {file_dict['hour']}:{file_dict['min']}"
            timestamp = time.mktime(datetime.datetime.strptime(file_date, '%d/%m/%Y %H:%M').timetuple())  # преобразование
            time_dict = {'time_st': int(timestamp), 'file': file_dict['file']}  # сохранение значения в словарь

            if time_dict['time_st'] > timest:
                timest = time_dict['time_st']
                file_save = time_dict['file']

        return file_save

    except Exception as err:
        text = 'Ошибка определения файла\n' + str(err)
        return text


if __name__ == '__main__':
    pass
    # text = ""
    # print(read_date('ek260'))
