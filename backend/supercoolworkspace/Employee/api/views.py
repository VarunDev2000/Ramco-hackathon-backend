#----------------------------------------------------------------------------
import numpy as np
import argparse
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import time
import datetime
import pandas
import sys
import random

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#----------------------------------------------------------------------------

from rest_framework import viewsets,permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import Employee_serializer

from Employee.models import Employee


class EmployeeViewSet(viewsets.ModelViewSet):

    serializer_class = Employee_serializer
    
    def get_queryset(self):
        return Employee.objects.all()
    def perform_create(self,serializer):
        serializer.save()


class call_model(APIView):

    def get(self,request):
        
        train_dir = "ML/data/train"
        val_dir = "ML/data/test"

        num_train = 28709
        num_val = 7178
        batch_size = 64
        num_epoch = 50

        train_datagen = ImageDataGenerator(rescale=1./255)
        val_datagen = ImageDataGenerator(rescale=1./255)

        train_generator = train_datagen.flow_from_directory(
                train_dir,
                target_size=(48,48),
                batch_size=batch_size,
                color_mode="grayscale",
                class_mode='categorical')

        validation_generator = val_datagen.flow_from_directory(
                val_dir,
                target_size=(48,48),
                batch_size=batch_size,
                color_mode="grayscale",
                class_mode='categorical')

        
        model = Sequential()

        model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
        model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Flatten())
        model.add(Dense(1024, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(7, activation='softmax'))


        model.load_weights('ML/model.h5')

        cv2.ocl.setUseOpenCL(False)

        emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
        emotion_percent = {"Angry":0,"Disgusted":0,"Fearful":0,"Happy":0,"Neutral":0,"Sad":0,"Surprised":0}

        cap = cv2.VideoCapture(0)
        start = time.time()
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            facecasc = cv2.CascadeClassifier('ML/haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = facecasc.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
                prediction = model.predict(cropped_img)
                maxindex = int(np.argmax(prediction))
                cv2.putText(frame, emotion_dict[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                emotion_percent[emotion_dict[maxindex]]+=1
            #cv2.imshow('Video', cv2.resize(frame,(1600,960),interpolation = cv2.INTER_CUBIC))

            if time.time() - start > 5:
                break
        cap.release()
        cv2.destroyAllWindows()
        del emotion_percent["Surprised"]
        del emotion_percent["Fearful"]
        # final_emotion = {}
        # percent = 0
        # for values in emotion_percent.values():
        #     percent = percent + values
        # for key in emotion_percent:
        #     if (percent != 0):
        #         emotion_percent[key] = (emotion_percent[key]* 100)/percent 

        obj_create = Employee.objects.create(Angry = emotion_percent["Angry"],Disgusted = emotion_percent['Disgusted'],
        Happy = emotion_percent['Happy'],Neutral = emotion_percent['Neutral'],Sad = emotion_percent['Sad'],Timestamp = datetime.date.today())
        obj_create.save()

        return Response(emotion_percent, status=status.HTTP_200_OK)


class open_music(APIView):

    def get(self,request):
        actions = {}
        emotions = ["Angry", "Happy", "Sad", "Neutral"]
        df = pandas.read_excel("EmotionLinks.xlsx") 
        actions["Angry"] = [x for x in df.angry.dropna()] 
        actions["Happy"] = [x for x in df.happy.dropna()]
        actions["Sad"] = [x for x in df.sad.dropna()]
        actions["Neutral"] = [x for x in df.neutral.dropna()]

        def open_stuff(filename): 
            if sys.platform == "win32":
                os.startfile(filename)
            else:
                opener ="open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, filename])
        
        latest = Employee.objects.order_by('-id')[0]

        maxi = 0
        emotion = ""

        e = {'Happy':latest.Happy,'Sad':latest.Sad,'Angry':latest.Angry,'Neutral':latest.Neutral}

        for key,value in e.items():
            if value>maxi:
                maxi = value
                emotion = key

        count = 0

        for key,value in e.items():
            if value==maxi:
                count = count + 1
        
        if(count>=2):
            emotion = ""

        if emotion != "":
            actionlist = [x for x in actions[emotion]]
            random.shuffle(actionlist)
            open_stuff(actionlist[0])
        
        emotion_percent = {}
        return Response(emotion_percent, status=status.HTTP_200_OK)





