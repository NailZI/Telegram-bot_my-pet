# Логирование запросов

import datetime
import os

def logger(user, inquiry, data):
    date = datetime.date.today() # текущая дата
    os.chdir('E:\\AxiLogs')
    logFile = open(f'log {date}.txt', 'a')
    inquiry = str(inquiry)
    data_s = str(data).split('\r\n')
    timeLog = datetime.datetime.now().strftime('%H.%M.%S') # текущее время
    logFile.write(f'{timeLog} ID: {user}\nзапрос: {inquiry}\nответ: {data_s}\n\n')
    logFile.close()

if __name__ == '__main__':
    pass