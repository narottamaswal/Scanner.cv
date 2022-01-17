from django.shortcuts import render
# from social.fac import detect_gun
from rest_framework.views import APIView
from django.shortcuts import render, resolve_url
from rest_framework.views import APIView
from . models import *
from rest_framework.response import Response
from django.http import HttpResponse
import json
from rest_framework.renderers import JSONRenderer
import os
# from profanity_filter import ProfanityFilter
import re
from PIL import Image
from io import BytesIO
from base64 import b64decode
import base64
from PIL import Image
from io import BytesIO
from django.http import JsonResponse
import cv2
import numpy as np
from .TestD import openCvFunction
from imutils.perspective import four_point_transform
import cv2
from pathlib import Path
import os
import mimetypes
from base64 import b64decode, b64encode
from PIL import Image
import os
import img2pdf

class PostView(APIView):   
    def post(self, request):
        print("post method")
        results = {'value':''}
        post = request.data
        #print(post)
        img_data=post['image']
        print(img_data)
        username=post['username']
        imagestr = 'data:image/png;base64,...base 64 stuff....'
        im = Image.open(BytesIO(b64decode(img_data.split(',')[1])))
        filename=username+'.'+img_data[11:14]
        img_path="D:/PROJECTS/DocumentScanner/Project/"+filename    
        im.save(img_path)
        resultFilePath = openCvFunction(img_path)   
        #print(resultFilePath)
        with open(resultFilePath, "rb") as image_file:
            data = base64.b64encode(image_file.read())
            data = data.decode('utf-8')
        #print(data,type(data))
        mime_type = "image/jpg"
        if not mime_type:
            mime_type = 'image/jpg'
        image_data = bytes('data:' + mime_type + ';base64,' +data,encoding='utf-8')
        #print(data)
        #print(image_data)
        image_data=image_data.decode("utf-8")
        return JsonResponse({'uri':image_data})

class PDFView(APIView):   
    def post(self, request):
        print("pdf method")
        results = {'value':''}
        post = request.data
        img_data=post['image']
        filename=post['filename']
        print(img_data.split(','),filename)
        im = Image.open(BytesIO(b64decode(img_data.split(',')[1])))
        #print(im)
        filename=filename+'.jpg'
        filepath="D:/PROJECTS/DocumentScanner/Project/"+filename    
        im.save(filepath)
        pdf_path = "D:/PROJECTS/DocumentScanner/Project/PDF"+filename+".pdf"
     
        # opening image
        image = Image.open(filepath)
        pdf_bytes = img2pdf.convert(image.filename)
        file = open(pdf_path, "wb")
        file.write(pdf_bytes)
        image.close()
        file.close()
        with open(pdf_path, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
            encoded_string = encoded_string.decode('utf-8')
        #print(data,type(data))
        mime_type = "application/pdf"
        if not mime_type:
            mime_type = 'application/pdf'
        pdfData = bytes('data:' + mime_type + ';base64,' +encoded_string,encoding='utf-8')
        pdfData=pdfData.decode("utf-8")
        print(pdfData)
        return JsonResponse({'uri':pdfData})

        
