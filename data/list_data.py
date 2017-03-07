import os
from os.path import isfile, join

mypath = os.path.dirname(os.path.abspath(__file__))
# assert False
# mypath = '/home/oferfrid/PycharmProjects/localbudgets/data/'

with file(os.path.join(mypath ,'all_data.csv'),'w') as fi:
    for d in os.listdir(mypath):
        if os.path.isdir(join(mypath, d)):
            for f in os.listdir(d):
                if os.path.isfile(join(d, f)):
                    fi.write("{}\t{}\n".format(d,f.split(".")[0]))
