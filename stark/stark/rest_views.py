#!/usr/bin/env python3
# Auther: sunjb

from rest_framework import viewsets
from Sansa import models
from stark.rest_serialize import AssetSerializer
from stark.rest_serialize import ManufactorySerializer
# ViewSets define the view behavior.
class AssetViewSet(viewsets.ModelViewSet):
    queryset = models.Asset.objects.all()   #先把表里面的数据全读取出来
    serializer_class = AssetSerializer  #交给AssetSerializer去对数据序列化

class ManufactoryViewSet(viewsets.ModelViewSet):
    queryset = models.Manufactory.objects.all()
    serializer_class = ManufactorySerializer