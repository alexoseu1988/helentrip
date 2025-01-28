from django.urls import path # type: ignore
from .views import *

urlpatterns = [
    
    ## Логин, Логаут
    path('user_login', user_login, name='user_login'),
    path('user_logout', user_logout, name='user_logout'),
    
    ## Титульные страницы
    path('', index, name='home'),
    path('administrator', administrator, name='administrator'),
    path('dashboard', dashboard, name='dashboard'),
    path('dashboard_general', dashboard_general, name='dashboard_general'),
    path('dashboard_deleted', dashboard_deleted, name='dashboard_deleted'),
    path('dashboard_by_tour/<int:tour_id>/', dashboard, name='dashboard_by_tour'),
    path('dash_certificates', dash_certificates, name='dash_certificates'),
    path('dash_certificates_general', dash_certificates_general, name='dash_certificates_general'),
    path('dash_certificates_completed', dash_certificates_completed, name='dash_certificates_completed'),
    path('dash_certificates_one/<int:certificate_id>/', dash_certificates, name='dash_certificates_one'),
    path('all_reviews', all_reviews, name='all_reviews'),
    path('galery', galery, name='galery'),
    path('documents', documents, name='documents'),
    path('how_to_apply', how_to_apply, name='how_to_apply'),
    path('contacts', contacts, name='contacts'),
    path('all_faqs', all_faqs, name='all_faqs'),
    path('about_me', about_me, name='about_me'),
    path('extras', extras, name='extras'),
    path('lifehacks', lifehacks, name='lifehacks'),
    path('lifehack/<int:lifehack_id>/', lifehack, name='lifehack'),
    path('certificate/<int:certificate_id>/', certificate, name='certificate'),
    path('useful', useful, name='useful'),
    
    ## Страницы с турами
    path('tour/<int:tour_id>/', tour, name='tour'),
    path('edit_tour/<int:tour_id>/', edit_tour, name='edit_tour'),
    path('thank_you_tour/<int:tour_id>/', thank_you_tour, name='thank_you_tour'),
    path('thank_you_certificate/<int:certificate_id>/', thank_you_certificate, name='thank_you_certificate'),
    path('tour_galery/<int:tour_id>/', tour_galery, name='tour_galery'),
    path('all_tours', all_tours, name='all_tours'),
    path('tour_pdf/<int:tour_id>/pdf/', open_pdf, name='open_pdf'),
    
    ## Создаем новые объекты автоматически
    path('create_tour', create_tour, name='create_tour'),
    
    ## Создаем новые объекты вручную
    path('new_tour', new_tour, name='new_tour'),
    path('new_day/<int:tour_id>/', new_day, name='new_day'),
    path('new_icon_admin', new_icon_admin, name='new_icon_admin'),
    path('new_icon/<int:tour_id>/', new_icon, name='new_icon'),
    path('new_inclusive/<int:tour_id>/', new_inclusive, name='new_inclusive'),
    path('new_not_inclusive/<int:tour_id>/', new_not_inclusive, name='new_not_inclusive'),
    path('new_why_we', new_why_we, name='new_why_we'),
    path('new_review_title', new_review_title, name='new_review_title'),
    path('new_review/<int:tour_id>/', new_review, name='new_review'),
    path('upload_galery_images/<int:tour_id>/', upload_galery_images, name='upload_galery_images'),
    path('upload_lifehack_images/<int:lifehack_id>/', upload_lifehack_images, name='upload_lifehack_images'),
    path('upload_description_images/<int:tour_id>/', upload_description_images, name='upload_description_images'),
    path('new_faq', new_faq, name='new_faq'),
    path('new_tour_faq/<int:tour_id>/', new_tour_faq, name='new_tour_faq'),
    path('new_one_faq/<int:faq_id>/', new_one_faq, name='new_one_faq'),
    path('new_lifehack', new_lifehack, name='new_lifehack'),
    path('new_card_for_lifehack/<int:lifehack_id>/', new_card_for_lifehack, name='new_card_for_lifehack'),
    
    ## Редактируем объекты комплексно
    path('change_tour/<int:tour_id>/', change_tour, name='change_tour'),
    path('change_day/<int:day_id>/', change_day, name='change_day'),
    path('change_inclusive/<int:card_id>/', change_inclusive, name='change_inclusive'),
    path('change_not_inclusive/<int:card_id>/', change_not_inclusive, name='change_not_inclusive'),
    path('change_why_we/<int:card_id>/', change_why_we, name='change_why_we'),
    path('change_about_me', change_about_me, name='change_about_me'),
    path('change_faq/<int:faq_id>/', change_faq, name='change_faq'),
    path('change_one_faq/<int:faq_id>/', change_one_faq, name='change_one_faq'),
    
    ## Редактируем отдельные элементы тура
    path('change_title/<int:tour_id>/', change_title, name='change_title'),
    path('change_first_title/<int:tour_id>/', change_first_title, name='change_first_title'),
    path('change_date_start/<int:tour_id>/', change_date_start, name='change_date_start'),
    path('change_date_end/<int:tour_id>/', change_date_end, name='change_date_end'),
    path('change_description/<int:tour_id>/', change_description, name='change_description'),
    path('change_price_adult/<int:tour_id>/', change_price_adult, name='change_price_adult'),
    path('change_price_child/<int:tour_id>/', change_price_child, name='change_price_child'),
    path('change_price_pensioner/<int:tour_id>/', change_price_pensioner, name='change_price_pensioner'),
    path('change_background1/<int:tour_id>/', change_background1, name='change_background1'),
    path('change_background2/<int:tour_id>/', change_background2, name='change_background2'),
    path('change_background3/<int:tour_id>/', change_background3, name='change_background3'),
    path('change_description_pdf/<int:tour_id>/', change_description_pdf, name='change_description_pdf'),
    
    ## Манипулируем объектами
    path('activate_tour/<int:tour_id>/', activate_tour, name='activate_tour'),
    path('relocate_tour/<int:tour_id>/', relocate_tour, name='relocate_tour'),
    path('short_long_tour/<int:tour_id>/', short_long_tour, name='short_long_tour'),
    path('partner_tour/<int:tour_id>/', partner_tour, name='partner_tour'),
    path('approve_client/<int:client_id>/', approve_client, name='approve_client'),
    path('delete_client/<int:client_id>/', delete_client, name='delete_client'),
    path('approve_certificate/<int:certificate_id>/', approve_certificate, name='approve_certificate'),
    path('complete_certificate/<int:certificate_id>/', complete_certificate, name='complete_certificate'),
    
    ## Удаляем объекты
    path('delete_tour/<int:tour_id>/', delete_tour, name='delete_tour'),
    path('delete_day/<int:day_id>/', delete_day, name='delete_day'),
    path('delete_inclusive/<int:card_id>/', delete_inclusive, name='delete_inclusive'),
    path('delete_not_inclusive/<int:card_id>/', delete_not_inclusive, name='delete_not_inclusive'),
    path('delete_why_we/<int:card_id>/', delete_why_we, name='delete_why_we'),
    path('delete_review/<int:review_id>/', delete_review, name='delete_review'),
    path('delete_tour_galery/<int:tour_id>/', delete_tour_galery, name='delete_tour_galery'),
    path('delete_faq/<int:faq_id>/', delete_faq, name='delete_faq'),
    path('delete_tour_faq/<int:tour_faq_id>/', delete_tour_faq, name='delete_tour_faq'),
    path('delete_one_faq/<int:one_faq_id>/', delete_one_faq, name='delete_one_faq'),
    path('delete_card_for_lifehack/<int:card_id>/', delete_card_for_lifehack, name='delete_card_for_lifehack'),
    path('delete_lifehack/<int:lifehack_id>/', delete_lifehack, name='delete_lifehack'),
    
]
