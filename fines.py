import os
import pandas as pd
import numpy as np
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

lis=[]
for file in list_text_files('/home/luis/Desktop/Projects/problem1_data/library_data/checkouts'):
    load_file(file,lis)
checkouts = pd.DataFrame(lis)
checkouts['date'] = pd.to_datetime(checkouts['date'],format="%m/%d/%Y")

lis=[]
for file in list_text_files('/home/luis/Desktop/Projects/problem1_data/library_data/checkins'):
    load_file(file,lis)
checkins = pd.DataFrame(lis)
checkins['date'] = pd.to_datetime(checkins['date'],format="%Y-%m-%d")  #2013-04-16

books=pd.read_csv('/home/luis/Desktop/Projects/problem1_data/library_data/books.csv',
header=None,
names=['catalog_number','ISBN','title',
'author_1','author_2','author_3','author_4','loan_period'])

checkouts['loan_period']=checkouts['catalog_number'].map(lambda x: books['loan_period'][int(np.where(books['catalog_number']==int(x))[0])])
del books

fines={}
for i in range(len(checkouts)):
    date_checkout = checkouts.ix[i]['date']
    catalog_number_checkout = checkouts.ix[i]['catalog_number']
    patron_number_checkout = checkouts.ix[i]['patron_number']
    loan_period = checkouts.ix[i]['loan_period']
    if len(checkins[checkins['catalog_number']==catalog_number_checkout])>=1:
        ix = checkins[checkins['catalog_number']==catalog_number_checkout].index[0]
        date_checkin = checkins.ix[ix]['date']
        damage = checkins.ix[ix]['is_damaged']
        checkins = checkins.drop(ix)
        checkouts = checkouts.drop(i)
    else:
        date_checkin = pd.Timestamp.now()
    fines[catalog_number_checkout] = fines.get(catalog_number_checkout,0) + max(((date_checkin - date_checkout).days - loan_period),0)*5 + 30*damage 
    
import csv
writer = csv.writer(open('fines.csv', 'w'))
for key, value in fines.items():
   writer.writerow([key, value])
