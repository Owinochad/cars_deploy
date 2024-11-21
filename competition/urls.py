from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),

    #admin urls
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'), 
    path('listUsers/', views.listUser, name='listUsers'),

    #admin car competition urls        
    path('editCompetition/<int:pk>/', views.editCompetition, name='editCompetition'),
    path('deleteCompetition/<int:pk>/', views.deleteCompetition, name='deleteCompetition'),
    path('deleteImage/<int:pk>/', views.deleteImage, name='deleteImage'),
    path('listCompetitions/', views.listCompetitions, name='listCompetitions'),
    path('createCompetition/', views.create_competition, name='createCompetition'),
    path('delete-images-competition/<int:competition_id>/', views.delete_images_compe, name='delete_images_competition'),  

    #admin holiday competition urls
    path('editholidayCompetition/<int:pk>/', views.editholidayCompetition, name='editholidayCompetition'),
    path('deleteholidayCompetition/<int:pk>/', views.deleteholidayCompetition, name='deleteholidayCompetition'),
    path('deleteholidayImage/<int:pk>/', views.deleteholidayImage, name='deleteholidayImage'),
    path('listHolidayCompetitions/', views.listHolidayCompetitions, name='listHolidayCompetitions'),
    path('createholiCompetition/', views.create_holiday_competition, name='createholiCompetition'),
    path('delete-images-holiday/<int:competition_id>/', views.delete_images_holi, name='delete_images_holiday'),

    #admin electronics competition urls   
    

    
    #user urls
    path('view_wallet/', views.wallet, name='view_wallet'),

    # car competition urls
    path('competitions/', views.competitions, name='competitions'),    
    path('competition/<int:competition_id>/', views.competition_details, name='competition'),
    path('competition/<int:id>/add_to_basket/', views.add_to_basket, name='add_to_basket'),

    #basket urls    
    path('update-basket/', views.update_basket, name='update_basket'),
    path('basket/', views.view_basket, name='view_basket'),
    path('remove_from_basket/<int:item_id>/', views.remove_from_basket, name='remove_from_basket'),

    #checkout urls
    path('check_out/', views.check_out, name = 'check_out'),
    path('stk/', views.stk, name="stk"),
    path('DPO/', views.DPO_payment, name="DPO"),    
    path('base/', views.base, name='base'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_failed/', views.payment_failure, name='payment_failure'),

    #other urls 
    path('test/', views.test, name='test'),   
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('cookie_policy/', views.cookie_policy, name='cookie_policy'),
    path('how_it_works/', views.how_it_works, name='how_it_works'),
    path('ticket/', views.create_ticket, name='ticket'),        
    path('search_competitions/', views.search_competitions, name='search_competitions'),

    #electronics urls
    path('electronics/<int:electronics_competition_id>/', views.electronics_competition_details, name='electronics'), 
    path('electronics_competitions/', views.electronics_competitions, name='electronics_competitions'), 

    # holiday urls
    path('holicompetitions/', views.holidaycompetitions, name='holicompetitions'),
    path('holicompetition/<int:holicompetition_id>/', views.holicompetition_details, name='holicompetition'), 
    path('holicompetition/<int:id>/add_to_baskety/', views.add_to_baskety, name='add_to_baskety'),

 ]