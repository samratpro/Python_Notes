from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),   
    path('alldata', views.alldata, name='alldata'),
    path('single_data/<data_id>', views.single_data, name='single_data'),   # ```data_id``` should be pass in views function's argument
    path('update_data/<data_id>', views.update_data, name='update_data'),   # ```data_id``` should be pass in views function's argument
    path('delete_data/<data_id>', views.delete_data, name='delete_data'),   # ```data_id``` should be pass in views function's argument
]
