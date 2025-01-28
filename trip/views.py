import os
import random
from django.shortcuts import get_object_or_404, render, redirect # type: ignore
from django.http import FileResponse, Http404 # type: ignore
from django.urls import reverse # type: ignore
from .forms import TourForm, DayForm, InclusiveForm, NotInclusiveForm, Titlte1Form, TitlteForm,\
    DateStartForm, DateEndForm, DescriptionForm, PriceAdultForm, PriceChildForm, PricePensionerForm,\
    Background1Form, Background2Form, Background3Form, IconForm, \
    ReviewTitleForm, ReviewForm, WhyWeForm, ClientForm, UserLoginForm, \
    ImageForGaleryForm, MultiImageForm, FaqForm, FaqTourForm, OneFaqForm, \
    LifehackForm, CardForLifehackForm, DashboardForm, CertificateForm, \
    DashCertificateForm, MyContactsForm, CodeSearchForm, DescriptionPdfForm
from .models import Tour, Day, Inclusive, NotInclusive, Icon, Review, WhyWe, Client, ImageForGalery, ImageForDescription,\
    Faq, FaqTour, OneFaq, Lifehack, CardForLifehack, Certificate, MyContacts
from django.contrib.auth import login, logout # type: ignore
from datetime import date
from dateutil.relativedelta import relativedelta # type: ignore
from django.core.mail import send_mail # type: ignore
from django.contrib.sites.models import Site # type: ignore
from django.core.files.storage import default_storage # type: ignore


today = date.today()

# current_site = Site.objects.get_current()
# domain = current_site.domain
# main_page = f"http://{domain}/"  # Генерация URL главной страницы
# dash_certificates_url = f"http://{domain}{reverse('dash_certificate')}"
# dashboard_url = f"http://{domain}{reverse('dashboard')}"

## Форма входа

def user_login(request):
    pagetitle = "Увійдіть в обліковий запис"
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('administrator')
    else:
        form = UserLoginForm()
    return render(request, 'trip/user_login.html', {'form': form, 'pagetitle': pagetitle})

def user_logout(request):
    logout(request)
    return redirect('administrator')


## Титульные страницы

def index(request):
    pagetitle = 'Heleena_trip'
    tours = Tour.objects.filter(isActive=True)[:4]
    why_we = WhyWe.objects.all()
    contacts = MyContacts.objects.all()[0]
    reviews = Review.objects.filter(tour__isActive=True)[0:6]
    images = ImageForGalery.objects.order_by('?')[:10]
    if request.method == 'POST':
        form = CertificateForm(request.POST)
        if form.is_valid():
            certificate = Certificate.objects.create(**form.cleaned_data)
            certificate.valid_until = certificate.created_at + relativedelta(months=3)
            certificate.save()
            
            content = f"Для клієнта: {form.cleaned_data['name']} \n \
                        Телефон: {form.cleaned_data['phoneFor']} \n \
                        замовлено сертифікат на суму: {form.cleaned_data['amount']} \n \
                        телефон замовника: {form.cleaned_data['phone']}"
            send_mail('Новий клієнт', content, 'heleena_trip@ukr.net', ['alexoseu@ukr.net'], fail_silently=False)
            
            return redirect('thank_you_certificate', certificate.pk)
    else:
        form = CertificateForm()
    return render(request, 'trip/index.html', 
                  {'tours': tours, 'form': form,  'reviews': reviews, 'why_we': why_we, 
                   'images': images, 'contacts': contacts, 'today': today, 'pagetitle': pagetitle})
    
def administrator(request):
    pagetitle = 'Heleena_trip'
    tours = Tour.objects.all()
    why_we = WhyWe.objects.all()
    contacts = MyContacts.objects.all()[0]
    reviews = Review.objects.all()[0:6]
    images = ImageForGalery.objects.order_by('?')[:10]
    if request.method == 'POST':
        form = CertificateForm(request.POST)
        if form.is_valid():
            certificate = Certificate.objects.create(**form.cleaned_data)
            certificate.valid_until = certificate.created_at + relativedelta(months=3)
            certificate.save()
            
            content = f"Для клієнта: {form.cleaned_data['name']} \n \
                        Телефон: {form.cleaned_data['phoneFor']} \n \
                        замовлено сертифікат на суму: {form.cleaned_data['amount']} \n \
                        телефон замовника: {form.cleaned_data['phone']}"
            send_mail('Новий сертифікат', content, 'heleena_trip@ukr.net', ['alexoseu@ukr.net'], fail_silently=False)
            
            return redirect('thank_you_certificate', certificate.pk)
    else:
        form = CertificateForm()
    return render(request, 'trip/administrator.html', 
                  {'tours': tours, 'form': form, 'reviews': reviews, 'why_we': why_we, 
                   'images': images, 'contacts': contacts, 'today': today, 'pagetitle': pagetitle})

def dashboard(request, tour_id=None):
    return dashboard_general(request, False, tour_id)

def dashboard_deleted(request, tour_id=None):
    return dashboard_general(request, True, tour_id)

def dashboard_general(request, isDeleted, tour_id=None):
    tours = Tour.objects.all()
    pagetitle = 'Робота з клієнтами'
    if tour_id:
        tour = get_object_or_404(Tour, id=tour_id)
        clients = Client.objects.filter(deleted=isDeleted, tour=tour)
    else:
        clients = Client.objects.filter(deleted=isDeleted)
    client_forms = {client.id: DashboardForm(instance=client) for client in clients}
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        client = get_object_or_404(Client, id=client_id)
        form = DashboardForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = DashboardForm()
    context = {"clients": clients, "form": form, 'client_forms': client_forms, 'pagetitle': pagetitle, 'tours': tours}
    return render(request, 'trip/dashboard.html', context)

def dash_certificates(request, certificate_id=None):
    return dash_certificates_general(request, False, certificate_id)

def dash_certificates_completed(request, certificate_id=None):
    return dash_certificates_general(request, True, certificate_id)

def dash_certificates_general(request, completed, certificate_id=None):
    pagetitle = 'Робота з сертифікатами'
    form1 = CodeSearchForm()
    if certificate_id:
        certificates = Certificate.objects.filter(id=certificate_id)
    else:
        certificates = Certificate.objects.filter(completed=completed)
    certificate_forms = {certificate.id: DashCertificateForm(instance=certificate) for certificate in certificates}
    if request.method == 'POST':
        form1 = CodeSearchForm(request.POST)
        if form1.is_valid():
            code = form1.cleaned_data['code']
            certificate = Certificate.objects.filter(code=code).first()
            if certificate:
                return redirect("dash_certificates_one", certificate.pk)
            else:
                return redirect("dash_certificates")
        certificate_id = request.POST.get('certificate_id')
        certificate = get_object_or_404(Certificate, id=certificate_id)
        form = DashCertificateForm(request.POST, instance=certificate)
        if form.is_valid():
            form.save()
            return redirect("dash_certificates")
    else:
        form = DashCertificateForm()
        form1 = CodeSearchForm()
    context = {"certificates": certificates, "form": form, "form1": form1, 
               'certificate_forms': certificate_forms, 'pagetitle': pagetitle}
    return render(request, 'trip/dash_certificates.html', context)
    
def all_reviews(request):
    pagetitle = 'Відгуки наших клієнтів'
    reviews = Review.objects.all()
    return render(request, 'trip/all_reviews.html', {'reviews': reviews, 'pagetitle': pagetitle})

def all_faqs(request):
    pagetitle = 'Найбільш популярні питання'
    faqs = Faq.objects.all()
    return render(request, 'trip/all_faqs.html', {'faqs': faqs, 'pagetitle': pagetitle})

def galery(request):
    pagetitle = 'Наші фотозвіти'
    tours = Tour.objects.filter(isActive=True)
    view_tours = [i for i in tours if (len(i.galeryImages.all()) > 0)]
    return render(request, 'trip/galery.html', 
                  {'tours': tours, 'view_tours': view_tours, 'pagetitle': pagetitle})

def documents(request):
    pagetitle = 'Перелік необхідних документів'
    return render(request, 'trip/documents.html', {'pagetitle': pagetitle})

def how_to_apply(request):
    return render(request, 'trip/how_to_apply.html', {})

def contacts(request):
    pagetitle = 'Мої контакти'
    return render(request, 'trip/contacts.html', {'pagetitle': pagetitle})

def about_me(request):
    pagetitle = 'Про мене'
    return render(request, 'trip/about_me.html', {'pagetitle': pagetitle})

def extras(request):
    pagetitle = 'Додаткові послуги'
    return render(request, 'trip/extras.html', {'pagetitle': pagetitle})

def useful(request):
    pagetitle = 'Корисна інформація'
    return render(request, 'trip/useful.html', {'pagetitle': pagetitle})

def lifehacks(request):
    pagetitle = 'Туристичні лайфхаки'
    lifehacks = Lifehack.objects.all()
    return render(request, 'trip/lifehacks.html', {'lifehacks': lifehacks, 'pagetitle': pagetitle})

def lifehack(request, lifehack_id):
    lifehack = get_object_or_404(Lifehack, id=lifehack_id)
    pagetitle = 'Лайфхак' + str(lifehack.name)
    return render(request, 'trip/lifehack.html', {'lifehack': lifehack, 'pagetitle': pagetitle})

def certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)
    pagetitle = 'Сертифікат'
    return render(request, 'trip/thank_you_certificate.html', {'certificate': certificate, 'pagetitle': pagetitle})


## Страницы с турами

def tour(request, tour_id):
    clients = Client.objects.all()
    tour = get_object_or_404(Tour, id=tour_id)
    pagetitle = tour.title1
    images = ImageForDescription.objects.filter(tour=tour)
    days = Day.objects.filter(tour=tour)
    cards = Inclusive.objects.filter(tour=tour)
    reviews = Review.objects.filter(tour=tour)[0:4]
    not_cards = NotInclusive.objects.filter(tour=tour)
    faqs = FaqTour.objects.filter(tour=tour)
    ifDateAdult = tour.dateBeforeAdult > today if tour.dateBeforeAdult else False
    ifDateChild = tour.dateBeforeChild > today if tour.dateBeforeChild else False
    if tour.priceAdult:
        priceAdult = int(tour.priceAdultBefore if ifDateAdult else tour.priceAdult)
    else:
        priceAdult = 0
    if tour.priceChild:
        priceChild = int(tour.priceChildBefore if ifDateChild else tour.priceChild)
    else:
        priceChild = 0
    upcoming_tours = [i for i in Tour.objects.all() if (i.isActive == True and i.pk != tour.pk and i.dateStart != None and i.dateStart > today)][0:3]
    if request.method == 'POST':
        form1 = ReviewForm(request.POST)
        form2 = ClientForm(request.POST)
        if form1.is_valid():
            review = Review.objects.create(**form1.cleaned_data)
            review.tour = tour
            review.save()
            return redirect('tour', tour.pk)
        if form2.is_valid():
            client = Client.objects.create(**form2.cleaned_data)
            client.tour = tour
            client.date = tour.dateStart
            client.value = ((client.amount - client.children) * priceAdult + client.children * priceChild) if priceChild > 0 else (client.amount * priceAdult)
            client.save()
            content = f"Клієнт: {form2.cleaned_data['name']} \n \
                        Телефон: {form2.cleaned_data['phone']} \n \
                        Забронював тур: {tour.title1}"
            send_mail('Новий клієнт', content, 'heleena_trip@ukr.net', ['alexoseu@ukr.net'], fail_silently=False)
            return redirect('thank_you_tour', tour.pk)
    else:
        form1 = ReviewForm()
        form2 = ClientForm()
    return render(request, 'trip/tour.html', 
                  {'tour': tour, 'days': days, 'cards': cards, 'not_cards': not_cards, 'images': images, 
                   'upcoming_tours': upcoming_tours, 'reviews': reviews, 'form1': form1, 'form2': form2,
                   'faqs': faqs, 'ifDateAdult': ifDateAdult, 'ifDateChild': ifDateChild, 'today': today,
                   'pagetitle': pagetitle})
    
def edit_tour(request, tour_id):
    clients = Client.objects.all()
    tour = get_object_or_404(Tour, id=tour_id)
    pagetitle = tour.title1
    images = ImageForDescription.objects.filter(tour=tour)
    days = Day.objects.filter(tour=tour)
    cards = Inclusive.objects.filter(tour=tour)
    reviews = Review.objects.filter(tour=tour)[0:4]
    not_cards = NotInclusive.objects.filter(tour=tour)
    faqs = FaqTour.objects.filter(tour=tour)
    ifDateAdult = tour.dateBeforeAdult > today if tour.dateBeforeAdult else False
    ifDateChild = tour.dateBeforeChild > today if tour.dateBeforeChild else False
    if tour.priceAdult:
        priceAdult = int(tour.priceAdultBefore if ifDateAdult else tour.priceAdult)
    else:
        priceAdult = 0
    if tour.priceChild:
        priceChild = int(tour.priceChildBefore if ifDateChild else tour.priceChild)
    else:
        priceChild = 0
    upcoming_tours = [i for i in Tour.objects.all() if (i.isActive == True and i.pk != tour.pk and i.dateStart != None and i.dateStart > today)][0:3]
    if request.method == 'POST':
        form1 = ReviewForm(request.POST)
        form2 = ClientForm(request.POST)
        if form1.is_valid():
            review = Review.objects.create(**form1.cleaned_data)
            review.tour = tour
            review.save()
            return redirect('tour', tour.pk)
        if form2.is_valid():
            client = Client.objects.create(**form2.cleaned_data)
            client.tour = tour
            client.date = tour.dateStart
            client.value = ((client.amount - client.children) * priceAdult + client.children * priceChild) if priceChild > 0 else (client.amount * priceAdult)
            client.save()
            content = f"Клієнт: {form2.cleaned_data['name']} \n \
                        Телефон: {form2.cleaned_data['phone']} \n \
                        Забронював тур: {tour.title1}"
            send_mail('Новий клієнт', content, 'heleena_trip@ukr.net', ['alexoseu@ukr.net'], fail_silently=False)
            return redirect('thank_you_tour', tour.pk)
    else:
        form1 = ReviewForm()
        form2 = ClientForm()
    return render(request, 'trip/edit_tour.html', 
                  {'tour': tour,'days': days, 'cards': cards, 'not_cards': not_cards, 'images': images,
                   'upcoming_tours': upcoming_tours, 'reviews': reviews, 'faqs': faqs, 
                   'form1': form1, 'form2': form2, 'ifDateAdult': ifDateAdult, 'ifDateChild': ifDateChild, 
                   'pagetitle': pagetitle})
    
def thank_you_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    pagetitle = 'Дякуємо, що обрали нас!'
    return render(request, 'trip/thank_you_tour.html', {'tour': tour, 'pagetitle': pagetitle})

def thank_you_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)
    pagetitle = 'Дякуємо за придбання сертифікату'
    return render(request, 'trip/thank_you_certificate.html', {'certificate': certificate, 'pagetitle': pagetitle})
    
def tour_galery(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    pagetitle = 'Фотозвіт:' + str(tour.title)
    return render(request, 'trip/tour_galery.html', {'tour': tour, 'pagetitle': pagetitle})

def all_tours(request):
    tours = Tour.objects.filter(isActive=True)
    pagetitle = 'Всі поїздки з Heleena_trip'
    return render(request, 'trip/all_tours.html', {'tours': tours, 'today': today, 'pagetitle': pagetitle})

def open_pdf(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    # Проверяем, есть ли файл PDF
    if not tour.descriptionPdf:
        raise Http404("PDF-файл не найден")
    # Возвращаем PDF-файл для отображения в браузере
    response = FileResponse(tour.descriptionPdf.open('rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{tour.descriptionPdf.name}"'
    return response
    
    

## Создаем новые объекты автоматически

def create_tour(request):
    tour = Tour.objects.create(
        title = 'new_tour',
        title1 = 'Название тура',
        dateStart = today,
        dateEnd = today,
        
        priceAdult = 2000,
        priceChild = 2000,
        pricePensioner = 2000,
        dateBeforeAdult = None,
        dateBeforeChild = None,
        priceAdultBefore = 1000,
        priceChildBefore = 1000,
        
        description = 'Полное описание тура',
        
        isActive = True,
        isOutside = True,
        isOneDay = False,
        isPartner = False,
        
        background1 = 'photos/default_image.jpg',
        background2 = 'photos/default_image.jpg',
        background3 = 'photos/default_image.jpg'
    )
    return redirect('edit_tour', tour.pk)


## Создаем новые объекты вручную

def new_tour(request):
    pagetitle = 'Створення нового туру'
    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TourForm()
    return render(request, 'trip/change_obj.html', {'form': form, 'pagetitle': pagetitle})

def new_day(request, tour_id):
    pagetitle = 'Створення дня програми'
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = DayForm(request.POST)
        if form.is_valid():
            day = Day.objects.create(**form.cleaned_data)
            day.tour = tour
            day.save()
            return redirect('edit_tour', tour.pk)
    else:
        form = DayForm()
    return render(request, 'trip/change_obj.html', {'form': form, 'pagetitle': pagetitle})

def new_faq(request):
    pagetitle = 'Новий блок питань FAQ'
    if request.method == 'POST':
        form = FaqForm(request.POST, request.FILES)
        if form.is_valid():
            faq = Faq.objects.create(**form.cleaned_data)
            return redirect('all_faqs')
    else:
        form = FaqForm()
    return render(request, 'trip/change_obj.html', {'form': form, 'pagetitle': pagetitle})

def new_tour_faq(request, tour_id):
    pagetitle = 'Обрати блок питань FAQ'
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = FaqTourForm(request.POST)
        if form.is_valid():
            tourFaq = FaqTour.objects.create(**form.cleaned_data)
            tourFaq.tour = tour
            tourFaq.save()
            return redirect('edit_tour', tour.pk)
    else:
        form = FaqTourForm()
    return render(request, 'trip/change_obj.html', {'form': form, 'pagetitle': pagetitle})

def new_one_faq(request, faq_id):
    pagetitle = 'Нове питання FAQ'
    faq = get_object_or_404(Faq, id=faq_id)
    if request.method == 'POST':
        form = OneFaqForm(request.POST, request.FILES)
        if form.is_valid():
            oneFaq = OneFaq.objects.create(**form.cleaned_data)
            oneFaq.faq = faq
            oneFaq.save()
            return redirect('all_faqs')
    else:
        form = OneFaqForm()
    return render(request, 'trip/change_obj.html', {'form': form, 'pagetitle': pagetitle})

def new_icon(request, tour_id):
    pagetitle = 'Додати нову іконку'
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = IconForm(request.POST, request.FILES)
        if form.is_valid():
            icon = Icon.objects.create(**form.cleaned_data)
            return redirect('edit_tour', tour.pk)
    else:
        form = IconForm()
    return render(request, 'trip/change_obj.html', {'form': form, 'pagetitle': pagetitle})

def new_icon_admin(request):
    pagetitle = 'Додати нову іконку'
    if request.method == 'POST':
        form = IconForm(request.POST, request.FILES)
        if form.is_valid():
            icon = Icon.objects.create(**form.cleaned_data)
            return redirect('administrator')
    else:
        form = IconForm()
    return render(request, 'trip/change_obj.html', {'form': form, 'pagetitle': pagetitle})

def new_inclusive(request, tour_id):
    pagetitle = 'Додати картку Включено'
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = InclusiveForm(request.POST)
        if form.is_valid():
            card = Inclusive.objects.create(**form.cleaned_data)
            card.tour = tour
            card.save()
            return redirect('edit_tour', tour.pk)
    else:
        form = InclusiveForm()
    return render(request, 'trip/change_obj.html', {'form': form, 'pagetitle': pagetitle})

def new_not_inclusive(request, tour_id):
    pagetitle = 'Додати картку Не включено'
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = NotInclusiveForm(request.POST)
        if form.is_valid():
            card = NotInclusive.objects.create(**form.cleaned_data)
            card.tour = tour
            card.save()
            return redirect('edit_tour', tour.pk)
    else:
        form = NotInclusiveForm()
    return render(request, 'trip/change_obj.html', {'form': form, 'pagetitle': pagetitle})

def new_why_we(request):
    if request.method == 'POST':
        form = WhyWeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('administrator')
    else:
        form = WhyWeForm()
    return render(request, 'trip/change_obj.html', {'form': form})

def new_review_title(request):
    if request.method == 'POST':
        form = ReviewTitleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReviewTitleForm()
    return render(request, 'trip/change_obj.html', {'form': form})

def new_review(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = Review.objects.create(**form.cleaned_data)
            review.tour = tour
            review.save()
            return redirect('tour', tour.pk)
    else:
        form = ReviewForm()
    return render(request, 'trip/change_obj.html', {"form" : form})

def upload_galery_images(request, tour_id):
    tour = Tour.objects.get(pk=tour_id)
    pagetitle = 'Завантажити фотозвіти для туру:' + tour.title
    if request.method == 'POST':
        form = MultiImageForm(request.POST, request.FILES)
        if form.is_valid():
            for old_image in tour.galeryImages.all(): 
                if old_image.image: 
                    if default_storage.exists(old_image.image.path): 
                        default_storage.delete(old_image.image.path)
                old_image.delete() 

            for image in form.cleaned_data['images']:
                ImageForGalery.objects.create(tour=tour, image=image)
            return redirect('tour_galery', tour.pk)
    else:
        form = MultiImageForm()
    return render(request, 'trip/upload_galery_images.html', {'tour': tour, 'form': form, 'pagetitle': pagetitle})

def upload_description_images(request, tour_id):
    tour = Tour.objects.get(pk=tour_id)
    pagetitle = 'Завантажити фотоопис для туру:' + tour.title
    if request.method == 'POST':
        form = MultiImageForm(request.POST, request.FILES)
        if form.is_valid():
            for old_image in tour.descriptionImages.all(): 
                if old_image.image: 
                    if default_storage.exists(old_image.image.path): 
                        default_storage.delete(old_image.image.path)
                old_image.delete() 
            for image in form.cleaned_data['images']:
                ImageForDescription.objects.create(tour=tour, image=image)
            return redirect('edit_tour', tour.pk)
    else:
        form = MultiImageForm()
    return render(request, 'trip/upload_galery_images.html', {'tour': tour, 'form': form, 'pagetitle': pagetitle})

def upload_lifehack_images(request, lifehack_id):
    lifehack = Lifehack.objects.get(pk=lifehack_id)
    pagetitle = 'Завантажити картки для лайфхаку'
    if request.method == 'POST':
        form = MultiImageForm(request.POST, request.FILES)
        if form.is_valid():
            for old_image in lifehack.cards.all(): 
                if old_image.image: 
                    if default_storage.exists(old_image.image.path): 
                        default_storage.delete(old_image.image.path)
                old_image.delete() 

            for image in form.cleaned_data['images']:
                CardForLifehack.objects.create(lifehack=lifehack, image=image)
            return redirect('lifehack', lifehack.pk)
    else:
        form = MultiImageForm()
    return render(request, 'trip/upload_galery_images.html', {'lifehack': lifehack, 'form': form, 'pagetitle': pagetitle})

def new_lifehack(request):
    pagetitle = 'Створити новий лайфхак'
    if request.method == 'POST':
        form = LifehackForm(request.POST, request.FILES)
        if form.is_valid():
            lifehack = Lifehack.objects.create(**form.cleaned_data)
            return redirect('lifehacks')
    else:
        form = LifehackForm()
    return render(request, 'trip/change_obj.html', {'form': form, 'pagetitle': pagetitle})

def new_card_for_lifehack(request, lifehack_id):
    lifehack = get_object_or_404(Lifehack, id=lifehack_id)
    if request.method == 'POST':
        form = CardForLifehackForm(request.POST, request.FILES)
        if form.is_valid():
            card = CardForLifehack.objects.create(**form.cleaned_data)
            card.lifehack = lifehack
            card.save()
            return redirect('lifehacks')
    else:
        form = CardForLifehackForm()
    return render(request, 'trip/change_obj.html', {"form" : form})



## Редактируем объекты комплексно

def change_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    pagetitle = 'Редагувати тур:' + tour.title
    try:
        old_description_path = tour.descriptionPdf.path
    except:
        old_description_path = None
    old_image_path1 = tour.background1.path
    old_image_path2 = tour.background2.path
    old_image_path3 = tour.background3.path
    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES, instance=tour)
        if form.is_valid():
            new_description = form.cleaned_data['descriptionPdf']
            new_background1 = form.cleaned_data['background1']
            new_background2 = form.cleaned_data['background2']
            new_background3 = form.cleaned_data['background3']
            form.save()   
            if old_description_path:
                if tour.descriptionPdf and tour.descriptionPdf != new_description:  # Проверяем, есть ли старое изображение и оно не совпадает с новым
                    os.remove(old_description_path)  # Удаляем старое изображение из файловой системы 
            if tour.background1 and tour.background1 != new_background1:  # Проверяем, есть ли старое изображение и оно не совпадает с новым
                if os.path.basename(old_image_path1) != 'default_image.jpg':
                    os.remove(old_image_path1)  # Удаляем старое изображение из файловой системы
            if tour.background2 and tour.background2 != new_background2:  # Проверяем, есть ли старое изображение и оно не совпадает с новым
                if os.path.basename(old_image_path2) != 'default_image.jpg':
                    os.remove(old_image_path2)  # Удаляем старое изображение из файловой системы
            if tour.background3 and tour.background3 != new_background3:  # Проверяем, есть ли старое изображение и оно не совпадает с новым
                if os.path.basename(old_image_path3) != 'default_image.jpg':
                    os.remove(old_image_path3)  # Удаляем старое изображение из файловой системы        
            return redirect('edit_tour', tour.pk)
    else:
        form = TourForm(instance=tour)
    return render(request, 'trip/change_obj.html', {'form': form, 'tour': tour, 'pagetitle': pagetitle})

def change_day(request, day_id):
    pagetitle = 'Редагувати день'
    day = get_object_or_404(Day, id=day_id)
    tour = day.tour
    if request.method == 'POST':
        form = DayForm(request.POST, request.FILES, instance=day)
        if form.is_valid():
            form.save()            
            return redirect('change_day', day.pk)
    else:
        form = DayForm(instance=day)
    return render(request, 'trip/change_day.html', {'form': form, 'day': day, 'tour': tour, 'pagetitle': pagetitle})

def change_faq(request, faq_id):
    pagetitle = 'Редагувати FAQ'
    faq = get_object_or_404(Faq, id=faq_id)
    if request.method == 'POST':
        form = FaqForm(request.POST, request.FILES, instance=faq)
        if form.is_valid():
            form.save()            
            return redirect('all_faqs')
    else:
        form = FaqForm(instance=faq)
    return render(request, 'trip/change_obj.html', {'form': form, 'faq': faq, 'pagetitle': pagetitle})

def change_one_faq(request, faq_id):
    pagetitle = 'Редагувати FAQ'
    faq = get_object_or_404(OneFaq, id=faq_id)
    if request.method == 'POST':
        form = OneFaqForm(request.POST, request.FILES, instance=faq)
        if form.is_valid():
            form.save()            
            return redirect('all_faqs')
    else:
        form = OneFaqForm(instance=faq)
    return render(request, 'trip/change_obj.html', {'form': form, 'faq': faq, 'pagetitle': pagetitle})

def change_inclusive(request, card_id):
    pagetitle = 'Редагувати картку'
    card = get_object_or_404(Inclusive, id=card_id)
    tour = card.tour
    if request.method == 'POST':
        form = InclusiveForm(request.POST, instance=card)
        if form.is_valid():
            form.save()            
            return redirect('edit_tour', tour.pk)
    else:
        form = InclusiveForm(instance=card)
    return render(request, 'trip/change_obj.html', {'form': form, 'card': card, 'pagetitle': pagetitle})

def change_not_inclusive(request, card_id):
    pagetitle = 'Редагувати картку'
    card = get_object_or_404(NotInclusive, id=card_id)
    tour = card.tour
    if request.method == 'POST':
        form = NotInclusiveForm(request.POST, instance=card)
        if form.is_valid():
            form.save()            
            return redirect('edit_tour', tour.pk)
    else:
        form = NotInclusiveForm(instance=card)
    return render(request, 'trip/change_obj.html', {'form': form, 'card': card, 'pagetitle': pagetitle})

def change_why_we(request, card_id):
    pagetitle = 'Редагувати картку'
    card = get_object_or_404(WhyWe, id=card_id)
    if request.method == 'POST':
        form = WhyWeForm(request.POST, instance=card)
        if form.is_valid():
            form.save()            
            return redirect('administrator')
    else:
        form = WhyWeForm(instance=card)
    return render(request, 'trip/change_obj.html', {'form': form, 'card': card})

def change_about_me(request):
    pagetitle = 'Редагувати мої дані'
    about_me = get_object_or_404(MyContacts, id=1)
    old_image_path1 = about_me.photo1.path
    old_image_path2 = about_me.photo2.path
    old_image_path3 = about_me.photo3.path
    old_image_path4 = about_me.photo4.path
    if request.method == 'POST':
        form = MyContactsForm(request.POST, request.FILES, instance=about_me)
        if form.is_valid():
            new_photo1 = form.cleaned_data['photo1']
            new_photo2 = form.cleaned_data['photo2']
            new_photo3 = form.cleaned_data['photo3']
            new_photo4 = form.cleaned_data['photo4']
            form.save()
            if about_me.photo1 and about_me.photo1 != new_photo1:  # Проверяем, есть ли старое изображение и оно не совпадает с новым
                if os.path.basename(old_image_path1) != 'default_image.jpg':
                    os.remove(old_image_path1)  # Удаляем старое изображение из файловой системы
            if about_me.photo2 and about_me.photo2 != new_photo2:  # Проверяем, есть ли старое изображение и оно не совпадает с новым
                if os.path.basename(old_image_path2) != 'default_image.jpg':
                    os.remove(old_image_path2)  # Удаляем старое изображение из файловой системы
            if about_me.photo1 and about_me.photo3 != new_photo3:  # Проверяем, есть ли старое изображение и оно не совпадает с новым
                if os.path.basename(old_image_path3) != 'default_image.jpg':
                    os.remove(old_image_path3)  # Удаляем старое изображение из файловой системы
            if about_me.photo1 and about_me.photo4 != new_photo4:  # Проверяем, есть ли старое изображение и оно не совпадает с новым
                if os.path.basename(old_image_path4) != 'default_image.jpg':
                    os.remove(old_image_path4)  # Удаляем старое изображение из файловой системы
            return redirect('about_me')
    else:
        form = MyContactsForm(instance=about_me)
    return render(request, 'trip/change_about_me.html', {'form': form, 'about_me': about_me, 'pagetitle': pagetitle})



## Редактируем отдельные элементы тура

def change_background1(request, tour_id):
    pagetitle = 'Змінити головне зображення'
    tour = get_object_or_404(Tour, id=tour_id)
    old_image_path = tour.background1.path
    if request.method == 'POST':
        form = Background1Form(request.POST, request.FILES, instance=tour)
        if form.is_valid():
            new_background = form.cleaned_data['background1']
            form.save()    
            if tour.background1 and tour.background1 != new_background:  # Проверяем, есть ли старое изображение и оно не совпадает с новым
                if os.path.basename(old_image_path) != 'default_image.jpg':
                    os.remove(old_image_path)  # Удаляем старое изображение из файловой системы        
            return redirect('edit_tour', tour.pk)
    else:
        form = Background1Form(instance=tour)
    return render(request, 'trip/change_obj.html', {'form': form, 'tour': tour, 'pagetitle': pagetitle})

def change_background2(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    old_image_path = tour.background2.path
    if request.method == 'POST':
        form = Background2Form(request.POST, request.FILES, instance=tour)
        if form.is_valid():
            new_background = form.cleaned_data['background2']
            form.save()
            if tour.background2 and tour.background2 != new_background:  # Проверяем, есть ли старое изображение и оно не совпадает с новым
                if os.path.basename(old_image_path) != 'default_image.jpg':
                    os.remove(old_image_path)  # Удаляем старое изображение из файловой системы
            return redirect('edit_tour', tour.pk)
    else:
        form = Background2Form(instance=tour)
    return render(request, 'trip/change_obj.html', {'form': form, 'tour': tour})

def change_background3(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    old_image_path = tour.background3.path
    if request.method == 'POST':
        form = Background3Form(request.POST, request.FILES, instance=tour)
        if form.is_valid():
            new_background = form.cleaned_data['background3']
            form.save() 
            if tour.background3 and tour.background3 != new_background:  # Проверяем, есть ли старое изображение и оно не совпадает с новым
                if os.path.basename(old_image_path) != 'default_image.jpg':
                    os.remove(old_image_path)  # Удаляем старое изображение из файловой системы
            return redirect('edit_tour', tour.pk)
    else:
        form = Background3Form(instance=tour)
    return render(request, 'trip/change_obj.html', {'form': form, 'tour': tour})

def change_description_pdf(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    try:
        old_description_path = tour.descriptionPdf.path
    except:
        old_description_path = None
    if request.method == 'POST':
        form = DescriptionPdfForm(request.POST, request.FILES, instance=tour)
        if form.is_valid():
            new_description = form.cleaned_data['descriptionPdf']
            form.save() 
            if old_description_path:
                if tour.descriptionPdf and tour.descriptionPdf != new_description:  # Проверяем, есть ли старое изображение и оно не совпадает с новым
                    os.remove(old_description_path)  # Удаляем старое изображение из файловой системы
            return redirect('edit_tour', tour.pk)
    else:
        form = DescriptionPdfForm(instance=tour)
    return render(request, 'trip/change_obj.html', {'form': form, 'tour': tour})

def change_first_title(request, tour_id):
    pagetitle = 'Редагувати назву'
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = Titlte1Form(request.POST, instance=tour)
        if form.is_valid():
            form.save()            
            return redirect('edit_tour', tour.pk)
    else:
        form = Titlte1Form(instance=tour)
    return render(request, 'trip/change_obj.html', {'form': form, 'tour': tour, 'pagetitle': pagetitle})

def change_title(request, tour_id):
    pagetitle = 'Редагувати коротку назву'
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = TitlteForm(request.POST, instance=tour)
        if form.is_valid():
            form.save()            
            return redirect('edit_tour', tour.pk)
    else:
        form = TitlteForm(instance=tour)
    return render(request, 'trip/change_obj.html', {'form': form, 'tour': tour, 'pagetitle': pagetitle})

def change_date_start(request, tour_id):
    pagetitle = 'Редагувати дату початку'
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = DateStartForm(request.POST, instance=tour)
        if form.is_valid():
            form.save()            
            return redirect('edit_tour', tour.pk)
    else:
        form = DateStartForm(instance=tour)
    return render(request, 'trip/change_obj.html', {'form': form, 'tour': tour, 'pagetitle': pagetitle})

def change_date_end(request, tour_id):
    pagetitle = 'Редагувати дату закінчення'
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = DateEndForm(request.POST, instance=tour)
        if form.is_valid():
            form.save()            
            return redirect('edit_tour', tour.pk)
    else:
        form = DateEndForm(instance=tour)
    return render(request, 'trip/change_obj.html', {'form': form, 'tour': tour, 'pagetitle': pagetitle})

def change_description(request, tour_id):
    pagetitle = 'Редагувати опис туру'
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = DescriptionForm(request.POST, instance=tour)
        if form.is_valid():
            form.save()            
            return redirect('edit_tour', tour.pk)
    else:
        form = DescriptionForm(instance=tour)
    return render(request, 'trip/change_obj.html', {'form': form, 'tour': tour, 'pagetitle': pagetitle})

def change_price_adult(request, tour_id):
    pagetitle = 'Редагувати ціну для дорослих'
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = PriceAdultForm(request.POST, instance=tour)
        if form.is_valid():
            form.save()            
            return redirect('edit_tour', tour.pk)
    else:
        form = PriceAdultForm(instance=tour)
    return render(request, 'trip/change_obj.html', {'form': form, 'tour': tour, 'pagetitle': pagetitle})

def change_price_child(request, tour_id):
    pagetitle = 'Редагувати ціну для дітей'
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = PriceChildForm(request.POST, instance=tour)
        if form.is_valid():
            form.save()            
            return redirect('edit_tour', tour.pk)
    else:
        form = PriceChildForm(instance=tour)
    return render(request, 'trip/change_obj.html', {'form': form, 'tour': tour, 'today': today, 'pagetitle': pagetitle})

def change_price_pensioner(request, tour_id):
    pagetitle = 'Редагувати ціну для пільговиків'
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = PricePensionerForm(request.POST, instance=tour)
        if form.is_valid():
            form.save()            
            return redirect('edit_tour', tour.pk)
    else:
        form = PricePensionerForm(instance=tour)
    return render(request, 'trip/change_obj.html', {'form': form, 'tour': tour, 'pagetitle': pagetitle})


## Манипулируем объектами

def activate_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if tour.isActive:
        tour.isActive = False
    else:
        tour.isActive = True
    tour.save()
    return redirect('administrator')

def relocate_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if tour.isOutside:
        tour.isOutside = False
    else:
        tour.isOutside = True
    tour.save()
    return redirect('edit_tour', tour.pk)

def short_long_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if tour.isOneDay:
        tour.isOneDay = False
    else:
        tour.isOneDay = True
    tour.save()
    return redirect('edit_tour', tour.pk)

def partner_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if tour.isPartner:
        tour.isPartner = False
    else:
        tour.isPartner = True
    tour.save()
    return redirect('edit_tour', tour.pk)

def approve_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    tour = client.tour
    if client.approved:
        client.approved = False
        tour.seats = tour.seats + client.amount
    else:
        client.approved = True
        if client.tour.seats > 0: 
            tour.seats = tour.seats - client.amount
    client.save()
    tour.save()
    return redirect('dashboard')

def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if client.deleted:
        client.deleted = False
    else:
        if client.approved:
            client.approved = False
            client.tour.seats = client.tour.seats + client.amount
            client.tour.save()
        client.deleted = True
    client.save()
    return redirect('dashboard')

def approve_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)
    if certificate.approved:
        certificate.approved = False
        certificate.code = 0
    else:
        certificate.approved = True
        while True:
            unique_code = random.randint(10000000, 99999999)
            if not Certificate.objects.filter(code=unique_code).exists():
                certificate.code = unique_code
                break
    certificate.save()
    return redirect('dash_certificates')

def complete_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)
    if certificate.completed:
        certificate.completed = False
    else:
        certificate.completed = True
    certificate.save()
    return redirect('dash_certificates')


## Удаляем объекты

def delete_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    for i in tour.days.all():
        delete_day(request, i.pk)
    delete_tour_galery(request, tour_id)
    background1_path = tour.background1.path
    background2_path = tour.background2.path
    background3_path = tour.background3.path
    tour.delete()
    if os.path.basename(background1_path) != 'default_image.jpg':
        os.remove(background1_path)
    if os.path.basename(background2_path) != 'default_image.jpg':
        os.remove(background2_path)
    if os.path.basename(background3_path) != 'default_image.jpg':
        os.remove(background3_path)
    return redirect('administrator')

def delete_day(request, day_id):
    day = get_object_or_404(Day, id=day_id)
    tour = day.tour
    day.delete()
    return redirect('edit_tour', tour.pk)

def delete_inclusive(request, card_id):
    card = get_object_or_404(Inclusive, id=card_id)
    tour = card.tour
    card.delete()
    return redirect('edit_tour', tour.pk)

def delete_not_inclusive(request, card_id):
    card = get_object_or_404(NotInclusive, id=card_id)
    tour = card.tour
    card.delete()
    return redirect('edit_tour', tour.pk)

def delete_why_we(request, card_id):
    card = get_object_or_404(WhyWe, id=card_id)
    card.delete()
    return redirect('administrator')

def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.delete()           
    return redirect('all_reviews')

def delete_tour_galery(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    for i in tour.galeryImages.all():
        old_image_path = i.image.path
        i.delete()
        os.remove(old_image_path)
    return redirect('galery')

def delete_tour_faq(request, tour_faq_id):
    tourFaq = get_object_or_404(FaqTour, id=tour_faq_id)
    tour = tourFaq.tour
    tourFaq.delete()
    return redirect('edit_tour', tour.pk)

def delete_one_faq(request, one_faq_id):
    oneFaq = get_object_or_404(OneFaq, id=one_faq_id)
    oneFaq.delete()           
    return redirect('all_faqs')

def delete_faq(request, faq_id):
    faq = get_object_or_404(Faq, id=faq_id)
    faq.delete()           
    return redirect('all_faqs')

def delete_card_for_lifehack(request, card_id):
    card = get_object_or_404(CardForLifehack, id=card_id)
    image_path = card.image.path
    card.delete()
    os.remove(image_path)
    return redirect('lifehacks')

def delete_lifehack(request, lifehack_id):
    lifehack = get_object_or_404(Lifehack, id=lifehack_id)
    for card in lifehack.cards.all():
        delete_card_for_lifehack(request, card.pk)
    lifehack.delete()
    return redirect('lifehacks')