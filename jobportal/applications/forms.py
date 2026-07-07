from django import forms
from .models import Application
from django.core.exceptions import ValidationError

# Minimum and maximum upload sizes
MIN_UPLOAD_SIZE = 2 * 1024 * 1024  # 2 MB
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB

# Allowed content types for resume uploads
ALLOWED_CONTENT_TYPES = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain',
]

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['message', 'resume']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
            'resume': forms.ClearableFileInput()
        }

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if not resume:
            return resume

        content_type = getattr(resume, 'content_type', '')
        if content_type not in ALLOWED_CONTENT_TYPES:
            raise ValidationError('Unsupported file type. Allowed: PDF, DOC, DOCX, TXT.')

        if resume.size < MIN_UPLOAD_SIZE:
            raise ValidationError('File too small. Minimum size is 2 MB.')

        if resume.size > MAX_UPLOAD_SIZE:
            raise ValidationError('File too large. Maximum size is 5 MB.')

        return resume