from django.core.exceptions import ValidationError


def validate_image_size(file):
  file_size_kb = 500

  if file.size > file_size_kb * 1024:
    raise ValidationError(f'Please keep file size under {file_size_kb}KB!')
