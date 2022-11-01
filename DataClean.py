from urllib import parse

import openpyxl

workbook = openpyxl.load_workbook("./data/sports.xlsx")
print(workbook.sheetnames)

worksheet = workbook.worksheets[0]
dataset = []
column_name = []
for idx, row in enumerate(worksheet.rows):
    if idx == 0:
        for cell in row:
            column_name.append(cell.value)
    else:
        tmp = []
        for cell in row:
            tmp.append(cell.value)
        dataset.append(tmp[:])
print(f"{len(dataset)}*{len(dataset[0])}")


def get_domain(url: str):
    return parse.urlparse(url).netloc


# add site
column_name.append("site")
for i in range(len(dataset)):
    dataset[i].append(get_domain(dataset[i][1]))

print(column_name)
print(f"{len(dataset)}*{len(dataset[0])}")

dataset = sorted(dataset, key=lambda data: data[0])


# train 405-904
def get_trainset():
    trainset = dataset[404:904]

    subjective_num = 0
    objective_num = 0
    for each in trainset:
        if each[2] in ["objective", 0]:
            objective_num += 1
        elif each[2] in ["subjective", 1]:
            subjective_num += 1

    print(objective_num, subjective_num)
    return trainset

# print(set([dataset[i][2] for  i in range(len(dataset))]))

# write csv file
import csv

trainset = get_trainset()

with open("./MyData/train.csv", 'w+') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(column_name)
    writer.writerows(trainset)

with open("./MyData/test.csv", 'w+') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(column_name)
    writer.writerows(dataset[:404] + dataset[904:])

with open("./MyData/all.csv", 'w+') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(column_name)
    writer.writerows(dataset)
