from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(5, 0, -1)]),  # Рейтинг от 5 до 1
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем значение по умолчанию для поля rating
        self.fields['rating'].initial = 5
        # Делаем поле comment необязательным
        self.fields['comment'].required = False