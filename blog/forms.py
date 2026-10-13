
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post

        fields = [
            "title",
            "content",
            "category",
            "tags",
            "status",
            "cover_image",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter post title",
                }
            ),

            "content": forms.Textarea(
                attrs={
                    "rows": 8,
                    "class": "form-control",
                    "placeholder": "Write your post content here...",
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "tags": forms.SelectMultiple(
                attrs={
                    "class": "form-select",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "cover_image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def clean_title(self):
        title = self.cleaned_data["title"]

        if len(title) < 5:
            raise forms.ValidationError(
                "Title must be at least 5 characters long."
            )

        return title

    def clean_cover_image(self):
        image = self.cleaned_data.get("cover_image")

        if image:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    "Image file too large (max 5MB)."
                )

            valid_extensions = [
                ".jpg",
                ".jpeg",
                ".png",
                ".webp",
            ]

            if not any(
                image.name.lower().endswith(ext)
                for ext in valid_extensions
            ):
                raise forms.ValidationError(
                    "Unsupported file type. Use JPG, PNG, or WEBP."
                )

        return image


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email",
            }
        )
    )

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your username",
                }
            ),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment

        fields = ["content"]

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "cols": 40,
                    "placeholder": "Write your comment here...",
                    "style": (
                        "display: block; "
                        "width: 100%; "
                        "min-height: 120px;"
                    ),
                }
            )
        }

