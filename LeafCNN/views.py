from django.shortcuts import render
from joblib import load
import numpy as np
import tensorflow as tf
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User,auth
from django.shortcuts import render, redirect   
from datetime import datetime
from LeafCNN.models import Contact

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
 
        # Authenticate user
        user = auth.authenticate(username=username, password=password)
 
        if user is not None:
            # User authenticated, log them in
            auth.login(request, user)
            return redirect('mainpage.html')  # Redirect to home page after successful login
        else:
            # Invalid login, show error message
            return render(request, 'login.html', {'error': 'Invalid email or password'})
 
    return render(request, 'login.html')
 
def Register(request):
    if request.method == 'POST':
        # Extract form data
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_repeat = request.POST['password_repeat']
 
        # Validate form data
        if not (username and email and password and password_repeat):
            # Handle validation error, e.g., return an error message to the template
            return render(request, 'signup.html', {'error': 'All fields are required'})
 
        if password != password_repeat:
            # Handle password mismatch error, e.g., return an error message to the template
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
 
        # Create and save the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        print('User created')
        return redirect('mainpage.html')
    else:
        return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('home.html')  # Redirect to the login page after logout


# from django.http import HttpResponse

model=load('./savedModels/savedModels.joblib')



# Create your views here.
def Welcome(request):
    return render(request,'home.html')


def Mainpage(request):
    return render(request,'mainpage.html')

def Contact(request):
        if request.method == 'POST':
        # Extract form data
            name = request.POST['name']
            email = request.POST['email']
            message=request.POST['message']
            return redirect('home.html')
        
        else:
            return render(request, 'contact.html')

def Predictor(request):
    if request.method == "POST":
        file = request.FILES["imageFile"]
        file_name=default_storage.save(file.name,file)
        file_url=default_storage.path(file_name)
        class_names = ['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']
        img = tf.keras.preprocessing.image.load_img(file_url, target_size=(256,256))
        inputimg_array = tf.keras.preprocessing.image.img_to_array(img)
        inputimg_array=inputimg_array/255
        print(inputimg_array.shape)
        img1=inputimg_array.reshape((1,256,256,3))
        print(img1.shape)
        inputimg_pred = model.predict(img1)
        pred_label = class_names[np.argmax(inputimg_pred)]
        print(pred_label)
    else:
        # This handles GET requests or any other request method
        print('No image file provided in the request')

    return render(request, 'results.html', {'prediction':pred_label})