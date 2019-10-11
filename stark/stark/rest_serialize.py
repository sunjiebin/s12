#!/usr/bin/env python3
# Auther: sunjb


from rest_framework import serializers
from Sansa import models
# Serializers define the API representation.
class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Asset    #要暴露出去的表
        depth = 2
        fields = ['sn', 'name','manufactory', 'id', 'asset_type']   #要提供哪些字段出去

class ManufactorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Manufactory    #要暴露出去的表
        fields = ['manufactory', 'support_num', 'id', ]   #要提供哪些字段出去


