from django.forms import IntegerField, ModelForm, NumberInput, Textarea, TextInput, URLInput

from main.models import Achievement, Experience, Project


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


class ExperienceForm(ModelForm):
    start_year = IntegerField(
        label="Tahun Mulai",
        min_value=1900,
        max_value=2100,
        widget=NumberInput(attrs={"min": 1900, "max": 2100}),
    )
    end_year = IntegerField(
        label="Tahun Selesai",
        min_value=1900,
        max_value=2100,
        required=False,
        widget=NumberInput(attrs={"min": 1900, "max": 2100}),
    )

    class Meta:
        model = Experience
        fields = [
            "title",
            "title_id",
            "organization",
            "organization_id",
            "description",
            "description_id",
            "category",
            "start_year",
            "end_year",
        ]
        labels = {
            "title": "Posisi (Inggris)",
            "title_id": "Posisi (Indonesia)",
            "organization": "Organisasi (Inggris)",
            "organization_id": "Organisasi (Indonesia)",
            "description": "Deskripsi (Inggris)",
            "description_id": "Deskripsi (Indonesia)",
            "category": "Kategori",
            "start_year": "Tahun Mulai",
            "end_year": "Tahun Selesai",
        }
        widgets = {
            "title": TextInput(attrs={"placeholder": "Teaching Assistant"}),
            "title_id": TextInput(attrs={"placeholder": "Asisten Pengajar"}),
            "organization": TextInput(
                attrs={"placeholder": "University of Indonesia"}
            ),
            "organization_id": TextInput(
                attrs={"placeholder": "Universitas Indonesia"}
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Describe the role in English",
                    "rows": 4,
                }
            ),
            "description_id": Textarea(
                attrs={
                    "placeholder": "Jelaskan peran dalam bahasa Indonesia",
                    "rows": 4,
                }
            ),
            "category": TextInput(attrs={"placeholder": "Teaching, Organization"}),
            "start_year": NumberInput(attrs={"min": 1900, "max": 2100}),
            "end_year": NumberInput(attrs={"min": 1900, "max": 2100}),
        }


class AchievementForm(ModelForm):
    year = IntegerField(
        label="Tahun",
        min_value=1900,
        max_value=2100,
        required=False,
        widget=NumberInput(attrs={"min": 1900, "max": 2100}),
    )

    class Meta:
        model = Achievement
        fields = [
            "title",
            "title_id",
            "result",
            "result_id",
            "category",
            "year",
            "display_order",
        ]
        labels = {
            "title": "Prestasi (Inggris)",
            "title_id": "Prestasi (Indonesia)",
            "result": "Hasil (Inggris)",
            "result_id": "Hasil (Indonesia)",
            "category": "Kategori",
            "year": "Tahun",
            "display_order": "Urutan Tampilan",
        }
        widgets = {
            "title": TextInput(attrs={"placeholder": "OSN Informatics"}),
            "title_id": TextInput(attrs={"placeholder": "Informatika OSN"}),
            "result": TextInput(attrs={"placeholder": "National finalist"}),
            "result_id": TextInput(attrs={"placeholder": "Finalis nasional"}),
            "category": TextInput(attrs={"placeholder": "Competition, Certification"}),
            "year": NumberInput(attrs={"min": 1900, "max": 2100}),
            "display_order": NumberInput(attrs={"min": 0}),
        }
