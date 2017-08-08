from __future__ import unicode_literals
from django.core.exceptions import ValidationError

import os
from django.db import models

regions=(
    ('UK','UK'),
    ('England','England'),
    ('Wales	','Wales'),
    ('Scotland','Scotland')

)
# Create your models here.
import uuid
import os



def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('downloads/', filename)


class Climate(models.Model):
    region = models.CharField(max_length=8,choices=regions)
    max_temp=models.FileField(blank=True,null=True,upload_to=get_file_path,)
    min_temp=models.FileField(blank=True,null=True,upload_to=get_file_path)
    mean_temp=models.FileField(blank=True,null=True,upload_to=get_file_path)
    sunshine=models.FileField(blank=True,null=True,upload_to=get_file_path)
    rainfall=models.FileField(blank=True,null=True,upload_to=get_file_path)

    def __str__(self):
        return "region:{}".format(self.region)


    def delete(self, *args, **kwargs):
        if os.path.isfile(self.max_temp.path):
            os.remove(self.max_temp.path)
        if os.path.isfile(self.min_temp.path):
            os.remove(self.min_temp.path)
        if os.path.isfile(self.mean_temp.path):
            os.remove(self.mean_temp.path)
        if os.path.isfile(self.sunshine.path):
            os.remove(self.sunshine.path)
        if os.path.isfile(self.rainfall.path):
            os.remove(self.rainfall.path)

        super(Climate, self).delete(*args, **kwargs)

class ClimateData(models.Model):
    file_id=models.CharField(null=True,blank=True,max_length=1000000)
    Year=models.CharField(null=True,blank=True,max_length=10000)
    JAN=models.CharField(null=True,blank=True,max_length=100,default=0)
    FEB=models.CharField(null=True,blank=True,max_length=100,default=0)
    MAR=models.CharField(null=True,blank=True,max_length=100,default=0)
    APR=models.CharField(null=True,blank=True,max_length=100,default=0)
    MAY=models.CharField(null=True,blank=True,max_length=100,default=0)
    JUN=models.CharField(null=True,blank=True,max_length=100,default=0)
    JUL=models.CharField(null=True,blank=True,max_length=100,default=0)
    AUG=models.CharField(null=True,blank=True,max_length=100,default=0)
    SEP=models.CharField(null=True,blank=True,max_length=100,default=0)
    OCT=models.CharField(null=True,blank=True,max_length=100,default=0)
    NOV=models.CharField(null=True,blank=True,max_length=100,default=0)
    DEC=models.CharField(null=True,blank=True,max_length=100,default=0)
    WIN=models.CharField(null=True,blank=True,max_length=100,default=0)
    SPR=models.CharField(null=True,blank=True,max_length=100,default=0)
    SUM=models.CharField(null=True,blank=True,max_length=100,default=0)
    AUT=models.CharField(null=True,blank=True,max_length=100,default=0)
    ANN=models.CharField(null=True,blank=True,max_length=100,default=0)