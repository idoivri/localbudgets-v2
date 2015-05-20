from pymongo import MongoClient
from django.http import HttpResponse
from django.shortcuts import render
import pygal



def show_graph(request, muni_name):

    client = MongoClient()
    db = client.database
    muni = db[muni_name]

    line_chart = pygal.Line()
    line_chart.title = muni_name

    lines = list(muni['2010'].find())
    lines.sort(cmp=lambda x,y: cmp(x['code'], y['code']), reverse=True)
    dots = [ int(x['amount']) for x in muni['2010'].find() ] 
    line_chart.add('2010', dots)

    lines = list(muni['2011'].find())
    lines.sort(cmp=lambda x,y: cmp(x['code'], y['code']), reverse=True)
    dots = [ int(x['amount']) for x in muni['2011'].find() ] 
    line_chart.add('2011', dots)

    return HttpResponse(line_chart.render())

def show_pie(request, muni_name, year):
    client = MongoClient()
    db = client.database
    muni = db[muni_name]
    year_dataset = muni[year]
    big_lines = list(x for x in muni[year].find() if x['code'] == '. ')

    pie_chart = pygal.Pie( label_font_size=12, major_label_font_size=2, title_font_size=5)
    pie_chart.title = muni_name + year
    for line in big_lines:
        pie_chart.add(line['name'], int(line['amount']))

    return HttpResponse(pie_chart.render())
