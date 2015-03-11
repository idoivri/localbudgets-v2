from pymongo import MongoClient
from django.shortcuts import render


def show_table(request, muni_name,year):
    client = MongoClient()
    db = client.database
    muni = db[muni_name]
    year_dataset = muni[year]
    lines = []
    for line in year_dataset.find():
        lines.append(line)

    return render(request, 'simple_table.html', {'query_results':lines} )
