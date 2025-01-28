from django import forms # type: ignore
from .models import Tour, Day, Inclusive, NotInclusive, Icon, Review, WhyWe,\
                    Client, ImageForGalery, ImageForDescription, Faq, OneFaq,\
                    FaqTour, MyContacts, Lifehack, CardForLifehack, Certificate, \
                    Communication, Payment
from ckeditor.widgets import CKEditorWidget # type: ignore
from django.forms.widgets import NumberInput, TextInput, EmailInput # type: ignore
from django.contrib.auth.forms import AuthenticationForm # type: ignore
from multiupload.fields import MultiFileField # type: ignore

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Ім'я користувача")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ('title', 'title1', 'dateStart', 'dateEnd', 'seats',
                  'description', 'faq', 'descriptionPdf',
                  'priceAdult', 'priceChild', 'pricePensioner',
                  'dateBeforeAdult', 'priceAdultBefore', 'dateBeforeChild', 'priceChildBefore',
                  'isActive', 'isOutside', 'isOneDay', 'isPartner',
                  'background1', 'background2', 'background3')
        widgets = {
            'isActive': forms.CheckboxInput(),
            'isOutside': forms.CheckboxInput(),
            'isOneDay': forms.CheckboxInput(),
            'dateStart': forms.SelectDateWidget(empty_label=("Рік", "Місяць", "День")),
            'dateEnd': forms.SelectDateWidget(empty_label=("Рік", "Місяць", "День")),
            'dateBeforeAdult': forms.SelectDateWidget(empty_label=("Рік", "Місяць", "День")),
            'dateBeforeChild': forms.SelectDateWidget(empty_label=("Рік", "Місяць", "День")),
            'description': CKEditorWidget(),
        }
        
class Background1Form(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ('background1',)
        
class Background2Form(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ('background2',)
        
class Background3Form(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ('background3',)
        
class TitlteForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ('title',)
        
class Titlte1Form(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ('title1', 'seats')
        
class DateStartForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ('dateStart',)
        widgets = {
            'dateStart': forms.SelectDateWidget(empty_label=("Рік", "Місяць", "День")),
        }
        
class DateEndForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ('dateEnd',)
        widgets = {
            'dateEnd': forms.SelectDateWidget(empty_label=("Рік", "Місяць", "День")),
        }
        
class DescriptionForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ('description',)
        widgets = {
            'description': CKEditorWidget(),
        }
        
class DescriptionPdfForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ('descriptionPdf',)
        
class PriceAdultForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ('priceAdult', 'dateBeforeAdult', 'priceAdultBefore', 'currency')
        widgets = {
                'dateBeforeAdult': forms.SelectDateWidget(empty_label=("Рік", "Місяць", "День")),
            }
        
class PriceChildForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ('priceChild', 'dateBeforeChild', 'priceChildBefore', 'currency')
        widgets = {
                'dateBeforeChild': forms.SelectDateWidget(empty_label=("Рік", "Місяць", "День")),
            }
        
class PricePensionerForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ('pricePensioner', 'currency')
    
class DayForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = ('number', 'title', 'description')
        widgets = {
            'description': CKEditorWidget(),
        }
        
class MyContactsForm(forms.ModelForm):
    class Meta:
        model = MyContacts
        fields = ('phone', 'insta', 'viber', 'whatsapp', 'telegram', 'telegramChannel',
                  'aboutme1', 'aboutme2', 'aboutme3',
                  'photo1', 'photo2', 'photo3', 'photo4')
        widgets = {
            'aboutme1': CKEditorWidget(),
            'aboutme2': CKEditorWidget(),
            'aboutme3': CKEditorWidget(),
        }
        
class InclusiveForm(forms.ModelForm):
    class Meta:
        model = Inclusive
        fields = ('title', 'description', 'icon')
        
class NotInclusiveForm(forms.ModelForm):
    class Meta:
        model = NotInclusive
        fields = ('title', 'description', 'price', 'icon')
        widgets = {
            'description': CKEditorWidget(),
        }
        
class WhyWeForm(forms.ModelForm):
    class Meta:
        model = WhyWe
        fields = ('title', 'description', 'icon')
        
class IconForm(forms.ModelForm):
    class Meta:
        model = Icon
        fields = ('title', 'icon')
        
class ReviewTitleForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('name', 'review', 'tour')
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('name', 'review')
        
class ClientForm(forms.ModelForm):
    payment = communication = forms.ModelChoiceField(
        queryset=Payment.objects.all(),
        empty_label=None,
        label="Оберіть відсоток передплати"
    )
    communication = forms.ModelChoiceField(
        queryset=Communication.objects.all(),
        empty_label=None,
        label="Куди Вам дзвонити / писати?"
    )
    class Meta:
        model = Client
        fields = ('name', 'phone', 'amount', 'children', 'payment', 'communication', 'notes')
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Петро Петренко'}),
            'phone': TextInput(attrs={'placeholder': '0681435268'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'amount': NumberInput(attrs={'step': 1, 'min': 0, 'max': 100}),
            'children': NumberInput(attrs={'step': 1, 'min': 0, 'max': 100}),
        }
        
class CertificateForm(forms.ModelForm):
    communication = forms.ModelChoiceField(
        queryset=Communication.objects.all(),
        empty_label=None,  # Убирает пустой вариант
        label="Куди Вам дзвонити / писати?"
    )
    class Meta:
        model = Certificate
        fields = ('name', 'phone', 'phoneFor', 'amount', 'email', 'communication')
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Петро Петренко'}),
            'phone': TextInput(attrs={'placeholder': '0681435268'}),
            'phoneFor': TextInput(attrs={'placeholder': '0681435268'}),
            'email': EmailInput(attrs={'placeholder': 'heleena_trip@ukr.net'}),
            'amount': NumberInput(attrs={'step': 1, 'min': 0, 'max': 999999999}),
        }      
        
class DashboardForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('prepayment', 'notes')
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'prepayment': forms.NumberInput(attrs={'step': 1, 'min': 0})
        }
        
class DashCertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ('amount', 'valid_until')
        widgets = {
            'valid_until': forms.SelectDateWidget(empty_label=("Рік", "Місяць", "День")),
            'amount': forms.NumberInput(attrs={'step': 1, 'min': 0})
        }
        
        def __init__(self, *args, **kwargs):
            super(DashCertificateForm, self).__init__(*args, **kwargs)
            # Задаем начальное значение для valid_until, если оно есть в объекте instance
            if self.instance and self.instance.valid_until:
                self.fields['valid_until'].initial = self.instance.valid_until
        
class CodeSearchForm(forms.Form):
    code = forms.DecimalField(max_digits=9, decimal_places=0, label="Введіть код сертифіката")
        
class ImageForGaleryForm(forms.ModelForm):
    class Meta:
        model = ImageForGalery
        fields = ['image']
        
class ImageForDescriptionForm(forms.ModelForm):
    class Meta:
        model = ImageForDescription
        fields = ['image']
        
class MultiImageForm(forms.Form):
    images = MultiFileField(min_num=1, max_num=30, max_file_size=1920*1080*5)
    
class FaqForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields = ('title',)
        
class OneFaqForm(forms.ModelForm):
    class Meta:
        model = OneFaq
        fields = ('question', 'answer')
        widgets = {
            'answer': CKEditorWidget(),
        }
        
class FaqTourForm(forms.ModelForm):
    class Meta:
        model = FaqTour
        fields = ('faq',)
        
class LifehackForm(forms.ModelForm):
    class Meta:
        model = Lifehack
        fields = ('name',)
        
class CardForLifehackForm(forms.ModelForm):
    class Meta:
        model = CardForLifehack
        fields = ['image']