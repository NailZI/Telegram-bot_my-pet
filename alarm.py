# Запись в log аварийного события
import datetime
import os

def alarm(mes):
    dat = datetime.date.today()
    os.chdir('E:\\AxiLogs')
    timeLog = datetime.datetime.now().strftime('%H.%M.%S')  # текущее время
    al = open(f'alarm_{dat}.txt', 'a')
    al.write(f'{timeLog}\n' + str(mes) + '\n')
    print(f'{timeLog}\n' + str(mes) + '\n')
    al.close()
