from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Photo
from django.contrib.auth.decorators import login_required
from .forms import PhotoUploadForm

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def photo_list(request):
    # Lekérjük az aktuális rendezést és az irányt az URL-ből
    sort_by = request.GET.get('sort', 'title')
    
    # Lekérjük a fotókat
    photos = Photo.objects.all().order_by(sort_by)
    
    # Meghatározzuk a következő dátum-rendezési irányt a gombhoz
    # Ha most legújabb van elöl (-upload_date), akkor a következő a legrégebbi lesz (upload_date)
    if sort_by == '-upload_date':
        next_date_sort = 'upload_date'
    else:
        next_date_sort = '-upload_date'
        
    context = {
        'photos': photos,
        'next_date_sort': next_date_sort,
        'current_sort': sort_by
    }
    
    return render(request, 'photos/list.html', context)

@login_required
def photo_upload(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user  # Assign the logged-in user
            photo.save()
            return redirect('photo_list')
    else:
        form = PhotoUploadForm()
    return render(request, 'photos/upload.html', {'form': form})

@login_required
def photo_delete(request, pk):
    # Only the owner can delete
    photo = get_object_or_404(Photo, pk=pk, user=request.user)
    
    if request.method == 'POST':
        photo.delete()
        # Optionally delete the file from disk too (advanced)
    return redirect('photo_list')