from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Image
from .forms import ImageForm
# Create your views here.

def home(request):
    images = Image.objects.all()
    return render(request, 'core/home.html', {'images': images})

def download_image(request, id):
    try:
        image_obj = Image.objects.get(pk=id)
        image_data = image_obj.image.read()
        response = HttpResponse(image_data, content_type="image/jpeg")
        response['Content-Disposition'] = 'attachment; filename="%s"' % image_obj.image.name
        return response
    except Image.DoesNotExist:
        return HttpResponse("Image not found", status=404)

def add_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    form = ImageForm()
    return render(request, 'core/addimage.html', {'form': form})    
