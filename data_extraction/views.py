import requests
from django.http.response import HttpResponse
from data_extraction.models import Climate,ClimateData
from urllib.request import Request,urlopen
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import re
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
import csv
import uuid


def get_file_climate_condition(urls,region):
    for url in urls:

        res = requests.get(url)
        file_temp = NamedTemporaryFile(delete=True)
        file_temp.write(res.content)

        file_temp.flush()
        climate_obj = Climate()
        climate_obj.region = region
        climate_obj.save()
        if "Tmax" in url:
            climate_obj.max_temp.save("Maxtemp", File(file_temp))
        if "Tmin" in url:
            climate_obj.min_temp.save("Min_temp", File(file_temp))
        if "Tmean" in url:
            climate_obj.mean_temp.save("Mean_temp", File(file_temp))
        if "Sunshine" in url:
            climate_obj.sunshine.save("Sunshine_temp", File(file_temp))
        if "Rainfall" in url:
            climate_obj.rainfall.save("Rainfall_temp", File(file_temp))


    return HttpResponse()


def uk_climate(regin_uk,region):

    max_temp_url = [climate_cond for climate_cond in regin_uk if "Tmax" in climate_cond ]
    min_temp_url = [climate_cond for climate_cond in regin_uk if "Tmin" in climate_cond]
    mean_temp_url = [climate_cond for climate_cond in regin_uk if "Tmean" in climate_cond]
    sunshine_url = [climate_cond for climate_cond in regin_uk if "Sunshine" in climate_cond]
    rainfall_url = [climate_cond for climate_cond in regin_uk if "Rainfall" in climate_cond]
    urls=max_temp_url+min_temp_url+mean_temp_url+sunshine_url+rainfall_url
    get_file_climate_condition(urls,region)

    return HttpResponse()


def download_files(request):

    Climate.objects.all().delete()
    url = Request("http://www.metoffice.gov.uk/climate/uk/summaries/datasets#Yearorder", headers={'User-Agent': 'Mozilla/5.0'})
    site = urlopen(url)
    html = site.read().decode('utf-8')
    links = re.findall('"((http|ftp)s?://.*?)"', html)
    OutputTuple = [(a) for a ,b in links]
    year_ordered=[url for url  in OutputTuple if "date" in url]
    regin_uk=[regin_uk for regin_uk in year_ordered if "/UK.txt" in regin_uk]
    regin_england=[regin_england for regin_england in year_ordered if "/England.txt" in regin_england]
    regin_wales=[regin_wales for regin_wales in year_ordered if "/Wales.txt" in regin_wales]
    regin_scotland=[regin_scotland for regin_scotland in year_ordered if "/Scotland.txt" in regin_scotland]
    uk_climate(regin_uk,region="UK")

    uk_climate(regin_england,region="England")
    uk_climate(regin_wales,region="Wales")
    uk_climate(regin_scotland,region="Scotland")


    return HttpResponse("Ok")

def yearwise_data(request):
    ClimateData.objects.all().delete()
    path ='/home/chandani/Desktop/data_extract/media/downloads/'
    # csv_path='/home/chandani/Desktop/data_extract/csv_files'
    # csv_file = r"NewProcessedDoc.csv"
    files = os.listdir(path)
    for file in files:
        pathIn = path + "/" + file
        id = uuid.uuid1()
        in_txt = open(pathIn, mode="r", encoding='utf-8')
        startFromLine = 9
        linesCounter = 1
        for line in in_txt:
            if linesCounter >=startFromLine :
                lis = line.split()
                for n, i in enumerate(lis):
                    if i == "---":
                        lis[n] = 0
                if len(lis)==18:
                    ClimateData.objects.get_or_create(file_id=id, Year=lis[0], JAN=lis[1], FEB=lis[2], MAR=lis[3],APR=lis[4], MAY=lis[5], JUN=lis[6],JUL=lis[7], AUG=lis[8], SEP=lis[9], OCT=lis[10], NOV=lis[11],
                                                  DEC=lis[12], WIN=lis[13], SPR=lis[14], SUM=lis[15], AUT=lis[16],ANN=lis[17]
                                                  )

                else:
                    ClimateData.objects.get_or_create(file_id=id, Year=lis[0], JAN=lis[1], FEB=lis[2], MAR=lis[3],
                                                      APR=lis[4], MAY=lis[5], JUN=lis[6], JUL=lis[7], WIN=lis[8], SPR=lis[9],
                                                      )

            linesCounter += 1

            # csv_file=csv_path+"/"+file+".csv"
        # print(csv_file)
        # in_txt=open(pathIn, mode="r",encoding='utf-8')
        # out_csv = csv.writer(open(csv_file, 'w'))
        # out_csv.writerows(csv.reader(in_txt))
    # data=ClimateData.objects.all()
    # climate_data_list={"climate_data_list":data}
    null_obj=ClimateData.objects.filter(WIN="---")
    for i in null_obj:
        i.WIN=0
        i.save()

    return HttpResponse()


def download_csv(request, queryset):

    csv_file = '/home/chandani/Desktop/data_extract/data_extraction/static/data_extraction/climate_data.csv'
    opts = queryset.model._meta

    # the csv writer
    writer = csv.writer(open(csv_file, 'w'))
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names[2:])
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names[2:] ])
    # print(csv.reader(open(csv_file,'r')))
    return csv_file

def export_csv(request,id):
    csv_file = download_csv( request, ClimateData.objects.filter(file_id=id).order_by("Year"))
    return render(request,'data_extraction/d3.html')

