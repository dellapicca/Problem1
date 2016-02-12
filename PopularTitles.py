import os
import pandas as pd
import numpy as np
import csv
import json


#######################################
def list_text_files(root):
    """List all text files below a root directory."""
    for dirpath, dirname, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith('.json'):
                yield os.path.join(dirpath, filename)

def load_file(path,lis):
    """Load a file into the database."""
    with open(path) as fp:
        for line in fp:
            lis.append(json.loads(line))
    return lis
######################################

######################################
lis=[]
for file in list_text_files('/home/luis/Desktop/Projects/problem1_data/library_data/checkouts'):
    load_file(file,lis)
    
checkouts = pd.DataFrame(lis)
checkouts['period']=checkouts['date'].map(lambda x: pd.Period(x,'M'))



books=pd.read_csv('/home/luis/Desktop/Projects/problem1_data/library_data/books.csv',
header=None,
names=['catalog_number','ISBN','title',
'author_1','author_2','author_3','author_4','loan_period'])

checkouts['title']=checkouts['catalog_number'].map(lambda x: books['title'][int(np.where(books['catalog_number']==int(x))[0])])
#tengo que usar 'int(x)' porque el formato es distinoto en los json que en el csv para el numero de catalogo
#checkouts['date'] = pd.to_datetime(checkouts['date'],format="%m/%d/%Y")
######################################

######################################
#print('give me an initial date (format=month/year)')
#data1 = input()
#print('give me a final date (format=month/year)')
#data2 = input()
date1 = '04/2013'  #pd.to_datetime('1/2013',format="%m/%Y")
date2 = '05/2015'
date1 = pd.Period(date1,'M')
date2 = pd.Period(date2,'M')
######################################


Relevant_checkouts = checkouts[checkouts['period']>=date1][checkouts['period']<=date2]
Top_Ten={}
for i in range((date2-date1)):
    Top_Ten[str(date1+i)] = []
    Top_Ten[str(date1+i)].append(str(date1+i))
    for j in range(10):
        Top_Ten[str(date1+i)].append('"' + checkouts[checkouts['period'] == (date1 + i)]['title'].value_counts()[0:10].index[j] + '"'
        + ':' + str(checkouts[checkouts['period'] == (date1 + i)]['title'].value_counts()[0:10][j]))
    
with open('Top_Ten.csv', 'w', newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in range((date2-date1)):
        filewriter.writerow(Top_Ten[str(date1+i)])                            
        #filewriter.writerow([str(date1+i), dict(Top_Ten[str(date1+i)])])                    


