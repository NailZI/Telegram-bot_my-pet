# Обработка данных, полученных из КШ(М)

def log_proc(file):
    corr = ('ek260', 'spg761')
    corr_log = None
    log_file = None

    for c in corr:
        if c in file:
            corr_log = c
    print(corr_log)

    for i in range(1, 11):
        if f'{corr_log}.log' in file:
            log_file = f'{corr_log}.log'
        if f'{corr_log}.log.{i}' in file:
            log_file = f'{corr_log}.log.{i}'

    return log_file


if __name__ == '__main__':
    pass