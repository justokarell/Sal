import os
import magic
from django.core.exceptions import ValidationError

def validate_is_pic(file):
    filesize= file.size
    valid_mime_types = ['image/png', 'image/jpeg']
    file_mime_type = magic.from_buffer(file.read(1024), mime=True)
    if filesize > 5242880:
        raise ValidationError("The maximum file size that can be uploaded is 5MB")
    if file_mime_type not in valid_mime_types:
        raise ValidationError('Unsupported file type. Only .png or .jpg are allowed!')
    valid_file_extensions = ['.png','.jpg', 'jpeg']
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Unacceptable file extension. Only .png or .jpg are allowed!')
    
