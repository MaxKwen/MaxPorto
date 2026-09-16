from django.forms import ModelForm, Textarea, TextInput, URLInput

from main.models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "title_id",
            "description_id",
            "category",
            "project_url",
            "thumbnail",
            "is_featured",
        ]
        labels = {
            "title": "Nama Proyek (Inggris)",
            "description": "Deskripsi Proyek (Inggris)",
            "title_id": "Nama Proyek (Indonesia)",
            "description_id": "Deskripsi Proyek (Indonesia)",
            "category": "Kategori",
            "project_url": "URL Proyek",
            "thumbnail": "URL Gambar Proyek",
            "is_featured": "Proyek Unggulan",
        }
        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan proyekmu dalam bahasa Inggris",
                    "rows": 4,
                }
            ),
            "title_id": TextInput(
                attrs={
                    "placeholder": "Website Portofolio",
                    "maxlength": 255,
                }
            ),
            "description_id": Textarea(
                attrs={
                    "placeholder": "Ceritakan proyekmu dalam bahasa Indonesia",
                    "rows": 4,
                }
            ),
            "category": TextInput(
                attrs={
                    "placeholder": "Backend, IoT, Data Science",
                    "maxlength": 100,
                }
            ),
            "project_url": URLInput(
                attrs={"placeholder": "https://github.com/username/project"}
            ),
            "thumbnail": URLInput(
                attrs={"placeholder": "https://example.com/project.png"}
            ),
        }
