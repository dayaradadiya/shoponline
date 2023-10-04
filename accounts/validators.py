from django.core.exceptions import ValidationError
import os
import magic
from django.core.exceptions import ValidationError

def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg','.png','.jpeg']

    if ext.lower() not in valid_extensions :
        raise ValidationError('Unsupported file extension. Allowed extensions: '+str(valid_extensions))
    

def validate_file_mimetype(file):
    accept = ['image/jpg','image/jpeg','image/png']
    file_mime_type = magic.from_buffer(file.read(1024),mime=True)
    print(file_mime_type)
    if file_mime_type not in accept:
        raise ValidationError("Unsupported file type, allowed file types are :jpg,jpeg,png. ")
    
def file_size(value):
    filesize=value.size
    if filesize > 10000000:
        raise ValidationError("Maximum size is 10 mb")

