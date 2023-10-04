'''

Category

'''



from csv import DictReader
from itertools import groupby
from pprint import pprint
import json
import csv
import re
import os.path
import pandas as pd

# upload file from local

# df = pd.read_csv(r"C:\Users\kumar\projects\ShopOnline\database_dump\category2.csv")
file_path = 'C:/Users/kumar/projects/ShopOnline/database_dump/'

#     name_of_file = input("sample_category_2")

filename = os.path.join(file_path + "category.csv")   

df = pd.read_csv(filename)


# chnage the data types of columns
# df.fillna(-999999, inplace=True)
# df = df.convert_dtypes()
# df = df.replace(-999999, None)
# df['pk'] = df['pk'].astype(int)
# df['main_category'] = df['main_category'].astype(int)

# load file into os.path(jupyter notebook file path)
df.to_csv('data.csv')


with open('data.csv') as csvfile:
    r = DictReader(csvfile, skipinitialspace=True)
    
    
    data = [dict(d) for d in r]

    groups = []
    uniquekeys = []

    for k, g in groupby(data, lambda r: (r['model'], r['pk'])):
        groups.append({
            "model": k[0],
            "pk": k[1],
            "fields": [{k:v for k, v in d.items() if k not in ['model','pk','']} for d in list(g)]
        })
        uniquekeys.append(k)
    records = dict(data = groups)    

    jstr = json.dumps(groups, indent=4)
    jstr = jstr.replace("[","")
    jstr = jstr.replace("]","")
    jstr = jstr.replace(".0","")
    jstr = "[" + jstr + "]"
#     print(str)
#     jsonFile = open("data.json", "w")
#     jsonFile.write(str)
#     jsonFile.close()
#     str1 = str.split(".0").join(" ")

    

    save_path = 'C:/Users/kumar/projects/ShopOnline/fixtures/'

#     name_of_file = input("sample_category_2")

    completeName = os.path.join(save_path + "sample_category_2.json")         

    file1 = open(completeName, "w")

    file1.write(jstr)
    file1.close()

#    python manage.py loaddata C:/Users/kumar/projects/ShopOnline/fixtures/category_2.json 

# python manage.py loaddata C:/Users/kumar/projects/ShopOnline/fixtures/sub_category_2.json

'''

sub Category

'''
from csv import DictReader
from itertools import groupby
from pprint import pprint
import json
import csv
import re
import os.path
import pandas as pd

# upload file from local

# df = pd.read_csv(r"C:\Users\kumar\projects\ShopOnline\database_dump\category2.csv")
file_path = 'C:/Users/kumar/projects/ShopOnline/database_dump/'

#     name_of_file = input("sample_category_2")

filename = os.path.join(file_path + "sub_category.csv")   

df = pd.read_csv(filename)


# chnage the data types of columns
# df.fillna(-999999, inplace=True)
# df = df.convert_dtypes()
# df = df.replace(-999999, None)
# df['pk'] = df['pk'].astype(int)
# df['main_category'] = df['main_category'].astype(int)

# load file into os.path(jupyter notebook file path)
df.to_csv('data.csv')


with open('data.csv') as csvfile:
    r = DictReader(csvfile, skipinitialspace=True)
    
    
    data = [dict(d) for d in r]

    groups = []
    uniquekeys = []

    for k, g in groupby(data, lambda r: (r['model'], r['pk'])):
        groups.append({
            "model": k[0],
            "pk": k[1],
            "fields": [{k:v for k, v in d.items() if k not in ['model','pk','']} for d in list(g)]
        })
        uniquekeys.append(k)
    records = dict(data = groups)    

    jstr = json.dumps(groups, indent=4)
    jstr = jstr.replace("[","")
    jstr = jstr.replace("]","")
    jstr = jstr.replace(".0","")
    jstr = "[" + jstr + "]"
#     print(str)
#     jsonFile = open("data.json", "w")
#     jsonFile.write(str)
#     jsonFile.close()
#     str1 = str.split(".0").join(" ")

    

    save_path = 'C:/Users/kumar/projects/ShopOnline/fixtures/'

#     name_of_file = input("sample_category_2")

    completeName = os.path.join(save_path + "sample_sub_category_2.json")         

    file1 = open(completeName, "w")

    file1.write(jstr)
    file1.close()

'''

fourth level Category

'''


from csv import DictReader
from itertools import groupby
from pprint import pprint
import json
import csv
import re
import os.path
import pandas as pd

# upload file from local

# df = pd.read_csv(r"C:\Users\kumar\projects\ShopOnline\database_dump\category2.csv")
file_path = 'C:/Users/kumar/projects/ShopOnline/database_dump/'

#     name_of_file = input("sample_category_2")

filename = os.path.join(file_path + "fourth_level_category.csv")   

df = pd.read_csv(filename)


# chnage the data types of columns
# df.fillna(-999999, inplace=True)
# df = df.convert_dtypes()
# df = df.replace(-999999, None)
# df['pk'] = df['pk'].astype(int)
# df['main_category'] = df['main_category'].astype(int)

# load file into os.path(jupyter notebook file path)
df.to_csv('data.csv')


with open('data.csv') as csvfile:
    r = DictReader(csvfile, skipinitialspace=True)
    
    
    data = [dict(d) for d in r]

    groups = []
    uniquekeys = []

    for k, g in groupby(data, lambda r: (r['model'], r['pk'])):
        groups.append({
            "model": k[0],
            "pk": k[1],
            "fields": [{k:v for k, v in d.items() if k not in ['model','pk','']} for d in list(g)]
        })
        uniquekeys.append(k)
    records = dict(data = groups)    

    jstr = json.dumps(groups, indent=4)
    jstr = jstr.replace("[","")
    jstr = jstr.replace("]","")
    jstr = jstr.replace(".0","")
    jstr = "[" + jstr + "]"
#     print(str)
#     jsonFile = open("data.json", "w")
#     jsonFile.write(str)
#     jsonFile.close()
#     str1 = str.split(".0").join(" ")

    

    save_path = 'C:/Users/kumar/projects/ShopOnline/fixtures/'

#     name_of_file = input("sample_category_2")

    completeName = os.path.join(save_path + "sample_fourth_level_category_2.json")         

    file1 = open(completeName, "w")

    file1.write(jstr)
    file1.close()