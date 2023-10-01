import os
import pickle
from django.shortcuts import redirect, render
import numpy as np
from .form import UploadModelForm,Upload_infoimg_Form
from .models import Photo,Info_img
#from PIL import Image, ImageFont, ImageDraw
#import keras
import cv2
from t_photo_upload.settings import MEDIA_ROOT
from keras.applications import VGG19, vgg19
from keras.applications.vgg19 import preprocess_input
import numpy as np
import shutil
import keras.saving.saved_model.model_serialization
from keras.utils import pad_sequences
import pyrebase

# Create your views here.

os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

config={
    'apiKey': "AIzaSyABMUGF474vTh53FNQPEh10NqFaKmo7QBs",
    'authDomain': "djangofirebase-152de.firebaseapp.com",
    'databaseURL': "https://djangofirebase-152de-default-rtdb.firebaseio.com",
    'projectId': "djangofirebase-152de",
    'storageBucket': "djangofirebase-152de.appspot.com",
    'messagingSenderId': "300566598104",
    'appId': "1:300566598104:web:d33aa6fd3513c49e1de2ad"
}
firebase = pyrebase.initialize_app(config)
database = firebase.database()

def index(request):
    all_infodata = database.child('Info').get()
    all_introdata = database.child('Intro').get()
    infodatas=[]
    for infodata in all_infodata.each():
        data=[infodata.key()]
        for keys in infodata.val().keys():
            data.append(infodata.val()[keys])
        infodatas.append(data)

    introdatas=[]
    for introdata in all_introdata.each():
        data=[introdata.key()]
        for keys in introdata.val().keys():
            data.append(introdata.val()[keys])
        introdatas.append(data)

    return render(request, 'index.html',{"introdatas":introdatas,"infodatas":infodatas})

def image_detection(request):
    photos = Photo.objects.all()  #查詢所有資料
    form = UploadModelForm()
    if request.method == "POST":
        form = UploadModelForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['image']
            file_path=MEDIA_ROOT+"/image/"+file.name
            if os.path.exists(MEDIA_ROOT+"/image/"):
                shutil.rmtree(MEDIA_ROOT+"/image/")

            photos.delete()
            form.save()

            f = open(file_path, "rb")
            img=cv2.imdecode(np.fromfile(f, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            f.close()

            # 自訂模型
            #flowers=["Narcissus" , "Snowdrop" , "LilyValley" , "Bluebell" , "Crocus" , "Iris" ,
            #        "Tigerlily" , "Daffodil" , "Fritillary" , "Sunflower" , "Daisy"  , "ColtsFoot" ,
            #        "Dandelion" , "Cowslip" , "Buttercup" , "Windflower" , "Pansy"]

            x=cv2.resize(img, (224,224), interpolation=cv2.INTER_LINEAR)
            x=cv2.cvtColor(x, cv2.COLOR_BGR2RGB)
            x=np.expand_dims(x, axis=0)
            x=preprocess_input(x)
            model=VGG19(weights='imagenet', include_top=True)
            out=model.predict(x)
            results=vgg19.decode_predictions(out, top=3)
            name=results[0][0][1]
            score=results[0][0][2]

            # 自訂模型
            #model=keras.models.load_model(MEDIA_ROOT+"/AI_models/flower_17_model")
            #idx=out[0].argmax()
            #score=out[0][idx]
            #name=flowers[idx]

            txt=f'名稱:{name}\n\n信心度:{score*100:.2f}%'

            photo=Photo.objects.get(image="image/"+file.name)
            photo.pre_value=txt
            photo.save()

            return redirect('/t_photo_app/image_detection')

    context = {'photos': photos,
               'form': form,
               }
    return render(request, 'image_detection.html', context)

def emotion(request):
    if request.method == "POST":
        def getLabel(score):
            label="中立的"
            if score <= 0.4:
                label="負面的"
            elif score >= 0.7:
                label="正向的"
            return label

        with open(MEDIA_ROOT+"/AI_models/emotion/eng_dictionary.pkl",'rb') as file:
            tok=pickle.load(file)

        model=keras.models.load_model(MEDIA_ROOT+"/AI_models/emotion/sentiment_model")
        text=request.POST["sentences"]
        x_test=pad_sequences(tok.texts_to_sequences([text]), maxlen=300)
        score=model.predict([x_test])[0]
        label=getLabel(score)
        context = {
            "label": label,
            "sentences":text
            }
        return render(request, 'emotion.html', context)

    return render(request, 'emotion.html')

def info(request):
    all_infodata = database.child('Info').get()
    infodatas=[]
    for infodata in all_infodata.each():
        data=[infodata.key()]
        for keys in infodata.val().keys():
            data.append(infodata.val()[keys])
        infodatas.append(data)
    return render(request, 'info.html',{"infodatas":infodatas})

def intro(request):
    all_introdata = database.child('Intro').get()
    introdatas=[]
    for introdata in all_introdata.each():
        data=[introdata.key()]
        for keys in introdata.val().keys():
            data.append(introdata.val()[keys])
        introdatas.append(data)
    return render(request, 'intro.html',{"introdatas":introdatas})

def contact(request):
    return render(request, 'contact.html')

def manage_login(request):
    if request.method == "POST":
        login_mid=request.POST["mid"]
        login_mpw=request.POST["mpw"]
        request.session['input_mid']=login_mid
        request.session['input_mpw']=login_mpw

        mid=database.child("Manager").child("mid").get().val()
        mpw=database.child("Manager").child("mpw").get().val()
        if login_mid == mid and login_mpw == mpw:
            return redirect ("/t_photo_app/manage_data")
        else:
            return redirect ("/t_photo_app/manage_login")
    if request.method == "GET":
        if request.session.has_key('input_mid'):
            mid=request.session['input_mid']
            mpw=request.session['input_mpw']
            message="帳號或密碼錯誤，請重新輸入"
        else:
            mid=""
            mpw=""
            message=""
        content={'input_mid':mid,'input_mpw':mpw,'message':message}
        return render(request, 'manage_login.html', content)

def manage_logout(request):
    del request.session['input_mid']
    del request.session['input_mpw']
    return redirect ("/t_photo_app/manage_login")

def manage_data(request):
    if request.session.has_key('input_mid'):
        login_mid=request.session['input_mid']
        login_mpw=request.session['input_mpw']
        mid=database.child("Manager").child("mid").get().val()
        mpw=database.child("Manager").child("mpw").get().val()
        if login_mid == mid and login_mpw == mpw:

            all_infodata = database.child('Info').get()
            infodatas=[]
            for infodata in all_infodata.each():
                data=[infodata.key()]
                for keys in infodata.val().keys():
                    data.append(infodata.val()[keys])
                infodatas.append(data)

            all_introdata = database.child('Intro').get()
            introdatas=[]
            for introdata in all_introdata.each():
                data=[introdata.key()]
                for keys in introdata.val().keys():
                    data.append(introdata.val()[keys])
                introdatas.append(data)

            form = Upload_infoimg_Form()
            return render(request, 'manage_data.html',{"introdatas":introdatas,"infodatas":infodatas,'form': form})
        else:
            return redirect ("/t_photo_app/manage_login")
    else:
        return redirect ("/t_photo_app/manage_login")

def infodata_add(request):
    if request.method == "POST":
        num=str(len(database.child("Info").get().each())+1)
        data={
                "btn":"info-btn-"+num,
                "content":"",
                "img":"",
                "title":"",
            }
        database.child("Info").child("info-items-"+num).set(data)
    return redirect("/t_photo_app/manage_data")

def infodata_edit(request):
    if request.method == "POST":
        file = request.FILES['image']
        file_path="info_image/"+file.name
        try:
            infoimg=Info_img.objects.get(image=file_path)
        except:
            form = Upload_infoimg_Form(request.POST, request.FILES)
            if form.is_valid():
                form.save()
        data={
            "Info/"+request.POST["Info-items"]:{
                "btn":request.POST["btn"],
                "content":request.POST["content"],
                "img":file_path,
                "title":request.POST["title"],
                }
            }
        database.update(data)
    return redirect("/t_photo_app/manage_data")

def infodata_delete(request):
    if request.method == "POST":
        database.child("Info").child(request.POST["Info-items"]).remove()
    return redirect("/t_photo_app/manage_data")

def introdata_add(request):
    if request.method == "POST":
        num=str(len(database.child("Intro").get().each())+1)
        data={
            "Intro/intro-items-"+num:{
                "btn":"intro-btn-"+num,
                "content":"",
                "img":"",
                "title":"",
                }
            }
        database.update(data)
    return redirect("/t_photo_app/manage_data")

def introdata_edit(request):
    if request.method == "POST":
        data={
            "Intro/"+request.POST["Intro-items"]:{
                "btn":request.POST["btn"],
                "content-0":request.POST["content-0"],
                "content-1":request.POST["content-1"],
                "content-2":request.POST["content-2"],
                "content-3":request.POST["content-3"],
                "title":request.POST["title"],
                }
            }
        database.update(data)
    return redirect("/t_photo_app/manage_data")

def introdata_delete(request):
    if request.method == "POST":
        database.child("Intro").child(request.POST["Intro-items"]).remove()
    return redirect("/t_photo_app/manage_data")

