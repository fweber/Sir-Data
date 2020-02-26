#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 12:12:15 2018

@author: fweber
"""

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import X5gonResource

# für import-export app
@admin.register(X5gonResource)




class ViewAdmin(ImportExportModelAdmin):
    pass
