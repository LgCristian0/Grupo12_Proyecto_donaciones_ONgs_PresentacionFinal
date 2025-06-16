from django import forms
from django.contrib.auth.models import User
from .models import ONG, Donante, Donacion , Campaña


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  
        help_texts = {
            'username': '',  
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ONGForm(forms.ModelForm):
    class Meta:
        model = ONG
        fields = ['descripcion', 'direccion']
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,            
                'style': 'resize: vertical; max-height: 150px;' 
            }),
            
        }

    def __init__(self, *args, **kwargs):
        super(ONGForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



class DonanteForm(forms.ModelForm):
    class Meta:
        model = Donante
        fields = ['telefono']  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'





class DonacionForm(forms.ModelForm):
    class Meta:
        model = Donacion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

       
        self.fields['donante'].disabled = True






class CampañaForm(forms.ModelForm):
    class Meta:
        model = Campaña
        fields = ['ong', 'nombre', 'meta', 'descripcion', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control descripcion-textarea',
                'rows': 3,
            }),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if not isinstance(field.widget, forms.Textarea):  # ya tiene clase
                field.widget.attrs['class'] = 'form-control'

        if user and hasattr(user, 'ong') and not user.is_superuser:
            self.fields['ong'].initial = user.ong
            self.fields['ong'].disabled = True
        elif user and user.is_superuser:
            self.fields['ong'].queryset = ONG.objects.all()


