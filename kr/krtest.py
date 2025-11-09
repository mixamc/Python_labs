data = list()
write_data = {}

with open('input.txt','r',encoding='UTF-8') as file:
    rows = file.readline()
    for row in range(int(rows)):

        data = file.readline().split()
        data[1] = data[1][3:]

        if data[0] in write_data:
            if data[1] in write_data[data[0]]:
                write_data[data[0]][data[1]] += int(data[2])
                write_data[data[0]]['all_call_time'] += int(data[2])
            else:
                write_data[data[0]][data[1]] = int(data[2])
                write_data[data[0]]['all_call_time'] += int(data[2])
        else:
            write_data[data[0]] = {}
            write_data[data[0]]['all_call_time'] = int(data[2])
            write_data[data[0]][data[1]] = int(data[2])

max_elem = max([[int(item['all_call_time']), num]  for num, item in write_data.items()])

with open('output.txt', 'w',encoding='UTF-8') as file:
    number = max_elem[1]
    max_month = max([elem, date[:2]] for date, elem in write_data[number].items() if date !='all_call_time')
    file.write(f'{number} {int(max_month[1])}')
