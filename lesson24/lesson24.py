"""
Отчёт о состоянии системы:
Пользователи системы: 'root', 'user1', ...
Процессов запущено: 833

Пользовательских процессов:
root: 533
user1: 231
...

Всего памяти используется: 71.3% (используем данные %MEM)
Всего CPU используется: 33.2% (используем данные %CPU)
Больше всего памяти использует: (%имя процесса, первые 20 символов если оно длиннее)
Больше всего CPU использует: (%имя процесса, первые 20 символов если оно длиннее)
"""
import datetime
from collections import defaultdict

from subprocess import (
    PIPE, Popen
)


def parse():
    with Popen(["ps", "aux"], stderr=PIPE, stdout=PIPE, encoding='utf-8') as p:
        head_line = next(p.stdout)
        head = [s.strip() for s in head_line.split(' ') if s]
        ln = len(head) - 1

        mem_ind = head.index('%MEM')
        mem_info = .0

        cpu_ind = head.index('%CPU')
        cpu_info = .0

        command_ind = head.index('COMMAND')

        users = set()
        user_proc_cnt = defaultdict(int)
        proc_cpu_cnt = defaultdict(int)
        proc_mem_cnt = defaultdict(int)

        for line in filter(lambda x: x, iter(str.strip(line) for line in p.stdout)):
            info_list = [ss for ss in line.split(' ') if ss]
            info_list = info_list[:ln] + [' '.join(info_list[ln:])]

            user = info_list[0]
            users.add(user)
            user_proc_cnt[user] += 1

            command = info_list[command_ind]
            mem_info_ = float(info_list[mem_ind])
            cpu_info_ = float(info_list[cpu_ind])

            proc_mem_cnt[command] += mem_info_
            proc_cpu_cnt[command] += cpu_info_

            mem_info += mem_info_
            cpu_info += cpu_info_

    dt = datetime.datetime.now().strftime('%d-%m-%Y-%H-%M')
    with open(dt + '-scan.txt', 'w', encoding='utf-8') as f:
        f.write('Отчёт о состоянии системы:\r\n')
        f.write('Пользователи системы: ' + ', '.join(f"'{u}'" for u in user_proc_cnt) + '\r\n')
        cnt = sum(l for l in user_proc_cnt.values())
        f.write(f'Процессов запущено: {cnt}\r\n\r\n')

        ranked_user_proc_cnt = sorted(user_proc_cnt.items(), key=lambda x: x[1], reverse=True)
        f.write('Пользовательских процессов:\r\n')
        f.write('\r\n'.join(f'{user}: {cnt}' for user, cnt in ranked_user_proc_cnt) + '\r\n\r\n')

        f.write(f'Всего памяти используется: {round(mem_info, 1)}%\r\n')
        f.write(f'Всего CPU используется: {round(cpu_info, 1)}%\r\n')

        p, cnt = list(sorted(proc_mem_cnt.items(), key=lambda x: x[1]))[-1]
        f.write(f'Больше всего памяти использует: {round(cnt, 1)}% - {p[20:]}\r\n')
        p, cnt = list(sorted(proc_cpu_cnt.items(), key=lambda x: x[1]))[-1]
        f.write(f'Больше всего CPU использует: {round(cnt, 1)}% - {p[20:]}\r\n')


if __name__ == '__main__':
    parse()
