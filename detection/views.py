from django.shortcuts import render
from django.conf import settings
from .image_upload import ImageUploadForm

# from .detect_covid_h5 import detect_covid
from .detect_covid_tflite import detect_covid

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                uploaded_image = form.save()
                image_path = settings.MEDIA_ROOT + '/' + str(uploaded_image.image)
                results = detect_covid(image_path)
                return render(request, 'result.html', {'results': results})
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