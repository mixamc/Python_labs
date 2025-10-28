data = list()
write_data = []
with open('input.txt','r',encoding='UTF-8') as file:
    temp = file.readlines()
    for i in range(1,len(temp)):
        information = temp[i].split()
        data.append(information[0:1] + information[2:])

max_dates = [i[-1].split('.') for i in data]
final_date = (sorted(max_dates, key = lambda elem:(elem[-1],elem[-2],elem[-3])))[0]

with open('output.txt','w',encoding='utf-8') as wrt:
    for item in data:
        if item[-1].split('.')[:-1] == final_date[:-1]:
            write_data.append([item[0], item[1]])
            wrt.write(f'{item[0]} {item[1]}')
            wrt.write(f'\n')