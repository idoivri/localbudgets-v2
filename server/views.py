from pymongo import MongoClient
from django.shortcuts import render
from upload.utils import Dataset

def show_table(request, muni_name,year):
    client = MongoClient()
    db = client.database
    muni = Dataset(muni_name,year)
    lines = []
    for line in muni.find():
        lines.append(line)

    return render(request, 'simple_table.html', {'query_results':lines} )
