from django import forms
from .models import UploadedImage

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ('image', )
        
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if not image.content_type.startswith('image/'):
                raise ValidationError('Only image files are allowed.')
        return image
