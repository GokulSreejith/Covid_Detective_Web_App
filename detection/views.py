from django.shortcuts import render, redirect
from django.http import JsonResponse 
from django.conf import settings
from .image_upload import ImageUploadForm
import requests

from .detect_covid_h5 import detect_covid
# from .detect_covid_tflite import detect_covid

def get_csrf_token():
    response = requests.get("http://localhost:5000/csrf_token/")
    csrf_token = response.cookies['csrftoken']
    return csrf_token

def generate_response(success, message, result):
    response = {
        "success": success,
        "message": message,
        "data": result
    }
    return response

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                uploaded_image = form.save()
                image_path = settings.MEDIA_ROOT + '/' + str(uploaded_image.image)
                results = detect_covid(image_path)
                return render(request, 'result.html', {'results': results["index"] })
        except Exception as e:
            print(e)
            # Handle the error
            error_message = str(e)  # Convert the error to a string
            return render(request, 'error.html', {'error_message': error_message})
    else:
        try:
            form = ImageUploadForm()
            return render(request, 'upload.html', {'form': form})
        except Exception as e:
            print(e)
            # Handle the error
            error_message = str(e)  # Convert the error to a string
            return render(request, 'error.html', {'error_message': error_message})

def check_covid_api(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                uploaded_image = form.save()
                image_path = settings.MEDIA_ROOT + '/' + str(uploaded_image.image)
                results = detect_covid(image_path)
                return JsonResponse(generate_response(True, "Check Covid Success", results), status=200, safe=False)
        except Exception as e:
            print("kjiuu")
            # Handle the error
            error_message = str(e)  # Convert the error to a string
            return JsonResponse(generate_response(False, error_message, None), status=500, safe=False)
    else:
        return redirect("/")