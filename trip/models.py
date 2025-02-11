from django.db import models # type: ignore

# Create your models here.
from django.db import models # type: ignore
from django.utils.text import slugify # type: ignore
from django.db.models.functions import Coalesce # type: ignore
from datetime import date
from django.db.models import F, Case, When, Value # type: ignore
from django.core.validators import MinValueValidator, MaxValueValidator # type: ignore

class Tour(models.Model):
    title = models.CharField(null=True, max_length=50, verbose_name="Коротка назва")
    title1 = models.CharField(null=True, max_length=50, verbose_name="Назва 1 строка")
    dateStart = models.DateField(null=True, verbose_name="Дата початку туру")
    dateEnd = models.DateField(null=True, blank=True, verbose_name="Дата закінчення туру")
    seats = models.DecimalField(null=True, default=0, max_digits=9, decimal_places=0, verbose_name="Кількість місць")
    
    description = models.TextField(max_length=1000, verbose_name="Опис для 2 секції")
    faq = models.ForeignKey('Faq', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Часті питання")
    descriptionPdf = models.FileField(null=True, blank=True, upload_to="pdfs/", verbose_name="Опис у форматі PDF")
    
    currency = models.ForeignKey('Currency', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Валюта")
    
    priceAdult = models.CharField(null=True, blank=True, max_length=15, verbose_name="Ціна для дорослих")
    priceChild = models.CharField(null=True, blank=True, max_length=15, verbose_name="Ціна для дітей")
    pricePensioner = models.CharField(null=True, blank=True, max_length=15, verbose_name="Ціна для пільговиків")
    dateBeforeAdult = models.DateField(null=True, blank=True, verbose_name="Дата, до якої діє скидка дорослим")
    dateBeforeChild = models.DateField(null=True, blank=True, verbose_name="Дата, до якої діє скидка дітям")
    priceAdultBefore = models.CharField(null=True, blank=True, max_length=15, verbose_name="Ціна для дорослих зі скидкою")
    priceChildBefore = models.CharField(null=True, blank=True, max_length=15, verbose_name="Ціна для дітей зі скидкою")
    
    isActive = models.BooleanField(null=True, default=True, verbose_name="Діючий тур")
    isOutside = models.BooleanField(null=True,default=True, verbose_name="Закордонний тур")
    isOneDay = models.BooleanField(null=True,default=False, verbose_name="Поїздка вихідного дня")
    isPartner = models.BooleanField(null=True,default=False, verbose_name="Поїздка від партнерів")
    
    background1 = models.ImageField(null=True, upload_to="photos/", verbose_name="Фон банера")
    background2 = models.ImageField(null=True, upload_to="photos/", verbose_name="Фон вартості")
    background3 = models.ImageField(null=True, upload_to="photos/", verbose_name="Фон інших турів")
    
    ##slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Tour, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.title1
        
    class Meta:
        ordering = [
            Case(
                When(dateStart=None, then=Value(1)),
                When(dateStart__lt=date.today(), then=Value(2)),
                default=Value(0),
                output_field=models.IntegerField()
            ),
            'dateStart',
        ]
        
class Currency(models.Model):
    currency = models.CharField(null=True, max_length=15, verbose_name="Валюта")
    
    def __str__(self):
        return (str(self.currency))
    
class Communication(models.Model):
    communication = models.CharField(null=True, max_length=20, verbose_name="Куди Вам дзвонити / писати?")
    
    def __str__(self):
        return (str(self.communication))
        
class FaqTour(models.Model):
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, null=True, verbose_name="Тур", related_name="faqs")
    faq = models.ForeignKey('Faq', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Питання")
        
class Faq(models.Model):
    title = models.CharField(null=True, max_length=150, verbose_name="Часті питання")
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
        
class OneFaq(models.Model):
    faq = models.ForeignKey('Faq', on_delete=models.CASCADE, null=True, verbose_name="Одне питання", related_name="questions")
    question = models.CharField(null=True, max_length=150, verbose_name="Текст питання")
    answer = models.TextField(null=True, max_length=3000, verbose_name="Текст відповіді")
        
class ImageForGalery(models.Model):
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, null=True, verbose_name="Тур", related_name="galeryImages")
    image = models.ImageField(null=True, upload_to='photos/galery', verbose_name="Зображення дня")
    
class ImageForDescription(models.Model):
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, null=True, verbose_name="Тур", related_name="descriptionImages")
    image = models.ImageField(null=True, upload_to='photos/description', verbose_name="Зображення дня")
    
class Day(models.Model):
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, null=True, verbose_name="Тур", related_name="days")
    number = models.CharField(null=True, max_length=7, verbose_name="Номер дня (днів)")
    title = models.CharField(null=True, blank=True, max_length=150, verbose_name="Назва дня")
    description = models.TextField(null=True, max_length=1500, verbose_name="Опис дня")
    
    class Meta:
        ordering = ['number']
    
class WhyWe(models.Model):
    title = models.CharField(null=True, max_length=50, verbose_name="Чому ми")
    description = models.TextField(null=True, max_length=1000, verbose_name="Подробно, чому ми")
    icon = models.ForeignKey('Icon', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Іконка")
    
class Inclusive(models.Model):
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, null=True, verbose_name="Тур")
    title = models.CharField(null=True, max_length=50, verbose_name="Що включено у вартість")
    description = models.TextField(null=True, max_length=1000, verbose_name="Подробний опис")
    icon = models.ForeignKey('Icon', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Іконка")
    
class NotInclusive(models.Model):
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, null=True, verbose_name="Тур")
    title = models.CharField(null=True, max_length=50, verbose_name="Що входить у вартість")
    description = models.TextField(null=True, max_length=1000, verbose_name="Подробний опис")
    icon = models.ForeignKey('Icon', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Іконка")
    price = models.CharField(null=True, blank=True, max_length=15, verbose_name="Ціна додаткової послуги")
    
class Icon(models.Model):
    title = models.CharField(null=True, max_length=50, verbose_name="Опис зображення")
    icon = models.FileField(null=True, upload_to='photos/icons', verbose_name="Іконка")
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
    
class Review(models.Model):
    name = models.CharField(null=True, max_length=50, verbose_name="Ім'я, Прізвище")
    review = models.TextField(null=True, max_length=1000, verbose_name="Зміст відгуку")
    date = models.DateTimeField(null=True, auto_now_add=True)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, null=True, verbose_name="Поїздка, про яку ви хочете залишити відгук")
    
    class Meta:
        ordering = ['-date']
        
class Client(models.Model):
    name = models.CharField(null=True, max_length=100, verbose_name="Ім'я, Прізвище")
    phone = models.CharField(null=True, max_length=20, verbose_name="Номер телефону")
    amount = models.DecimalField(null=True, default=1, max_digits=3, decimal_places=0, verbose_name="Кількість осіб")
    children = models.DecimalField(null=True, default=0, max_digits=3, decimal_places=0, verbose_name="в т.ч. дітей")
    payment = models.ForeignKey('Payment', on_delete=models.PROTECT, null=True, verbose_name="Оберіть відсоток передплати")
    value = models.DecimalField(null=True, default=0, max_digits=9, decimal_places=0, verbose_name="Повна вартість туру")
    prepayment = models.DecimalField(null=True, default=0, max_digits=9, decimal_places=0, verbose_name="Розмір передплати")
    notes = models.TextField(null=True, blank=True, max_length=1000, verbose_name="Примітки")
    approved = models.BooleanField(default=False, verbose_name="Схвалено")
    deleted = models.BooleanField(default=False, verbose_name="Видалено")
    tour = models.ForeignKey('Tour', on_delete=models.PROTECT, null=True, verbose_name="Подорож", related_name="clients")
    date = models.DateField(null=True, verbose_name="Дата початку туру")
    communication = models.ForeignKey('Communication', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Куди Вам дзвонити / писати?")
    
    class Meta:
        ordering = ['-id']
    
class Certificate(models.Model):
    name = models.CharField(null=True, max_length=50, verbose_name="Ім'я та Прізвище, для кого подарунок")
    phone = models.CharField(null=True, max_length=20, verbose_name="Ваш номер телефону")
    phoneFor = models.CharField(null=True, max_length=20, verbose_name="Номер телефону, для кого сертифікат")
    amount = models.DecimalField(null=True, default=0, max_digits=9, decimal_places=0, verbose_name="Сума подарунку у грн", validators=[MinValueValidator(0), MaxValueValidator(999999999)])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата замовлення")
    valid_until = models.DateTimeField(null=True, verbose_name="Сертифікат дійсний до")
    code = models.DecimalField(null=True, default=0, max_digits=9, decimal_places=0, verbose_name="Унікальний код сертифіката")
    email = models.EmailField(max_length=254, blank=True, null=True, verbose_name="Електронна пошта")
    approved = models.BooleanField(default=False, verbose_name="Схвалено")
    completed = models.BooleanField(default=False, verbose_name="Відпрацьовано")
    communication = models.ForeignKey('Communication', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Куди Вам дзвонити / писати?")
    
    class Meta:
        ordering = ['-id']
        
class Extra(models.Model):
    name = models.CharField(null=True, max_length=50, verbose_name="Ім'я та Прізвище, для кого подарунок")
    phone = models.CharField(null=True, max_length=20, verbose_name="Ваш номер телефону")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата замовлення")
    completed = models.BooleanField(default=False, verbose_name="Відпрацьовано")
    extraType = models.ForeignKey('ExtraType', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Тип додаткової послуги", related_name="extraTypes")
    communication = models.ForeignKey('Communication', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Куди Вам дзвонити / писати?")
    
    class Meta:
        ordering = ['-id']
    
class Payment(models.Model):
    percent = models.DecimalField(null=True, default=50, max_digits=3, decimal_places=0, verbose_name="% передплати")
    
    def __str__(self):
        return (str(self.percent) + '%')
    
class ExtraType(models.Model):
    type = models.CharField(null=True, max_length=50, verbose_name="Тип додаткової послуги")
    
    def __str__(self):
        return (self.type)
    
class MyContacts(models.Model):
    phone = models.CharField(null=True, max_length=50, verbose_name="Номер телефону")
    insta = models.CharField(null=True, max_length=50, verbose_name="Інстаграм")
    viber = models.CharField(null=True, max_length=50, verbose_name="Вайбер")
    whatsapp = models.CharField(null=True, max_length=50, verbose_name="Ватсап")
    telegram = models.CharField(null=True, max_length=50, verbose_name="Телеграм")
    telegramChannel = models.CharField(null=True, max_length=500, verbose_name="Телеграм канал")
    
    aboutme1 = models.TextField(null=True, max_length=1000, verbose_name="Про мене 1")
    aboutme2 = models.TextField(null=True, max_length=1000, verbose_name="Про мене 2")
    aboutme3 = models.TextField(null=True, max_length=1000, verbose_name="Про мене 3")
    
    photo1 = models.ImageField(null=True, upload_to="photos/", verbose_name="Моє фото 1")
    photo2 = models.ImageField(null=True, upload_to="photos/", verbose_name="Моє фото 2")
    photo3 = models.ImageField(null=True, upload_to="photos/", verbose_name="Моє фото 3")
    photo4 = models.ImageField(null=True, upload_to="photos/", verbose_name="Моє фото 4")
    
    titleIndex = models.CharField(null=True, max_length=100, verbose_name="Title для домашньої сторінки")
    titleReviews = models.CharField(null=True, max_length=100, verbose_name="Title для сторінки відгуків")
    titleFAQ = models.CharField(null=True, max_length=100, verbose_name="Для всіх FAQ")
    titleGalery = models.CharField(null=True, max_length=100, verbose_name="Title для галереї")
    titleDocuments = models.CharField(null=True, max_length=100, verbose_name="Title для документів")
    titleAboutMe = models.CharField(null=True, max_length=100, verbose_name="Title для сторінки Про мене")
    titleExtras = models.CharField(null=True, max_length=100, verbose_name="Title для додаткових послуг")
    titleUseful = models.CharField(null=True, max_length=100, verbose_name="Title для сторінки з корисним")
    titleLifehacks = models.CharField(null=True, max_length=100, verbose_name="Title для сторінки з лайфхаками")
    titleAnswers = models.CharField(null=True, max_length=100, verbose_name="Title для сторінки з відповідями")
    
class Lifehack(models.Model):
    name = models.CharField(null=True, max_length=50, verbose_name="Назва лайфхаку")
    
class CardForLifehack(models.Model):
    lifehack = models.ForeignKey('Lifehack', on_delete=models.CASCADE, null=True, verbose_name="Лайфхак", related_name="cards")
    image = models.ImageField(null=True, upload_to='photos/lifehacks', verbose_name="Зображення лайфхаку")