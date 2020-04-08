import glob
import errno
import csv

path = 'C:/Users/Alex Vasiliadis/Desktop/Semantic Similarity Python/Dataset Preparation/*.txt'
files = glob.glob(path)
csvFile = open('C:/Users/Alex Vasiliadis/Desktop/Semantic Similarity Python/Dataset Preparation/Results.csv', 'a', newline='')
row = ['Entity1', 'Relation', 'Entity2', 'Weight']
writer = csv.writer(csvFile)
writer.writerow(row)

for name in files:
    try:
        with open(name) as f:
            for line in f.readlines():
                list_helper = []
                weight = 1
                list_final = []
                if len(line.split(' ')) > 1:
                    list_helper = line.split(' ')
                    for i in list_helper[2:]:
                        final_value = list_helper[0] + ' ' + list_helper[1].replace(':', '').replace('dbpedia/genus', 'OtherProperty') \
                                + ' ' + i.replace(',', '').replace('.', '').replace('\n', '') + ' ' + str(weight)
                        list_final = final_value.split(' ')
                        writer.writerow(list_final)
                        weight = weight + 1
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise\

