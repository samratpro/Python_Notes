# URL Mapping in App URL file----------------------
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('purchase-credits/', views.purchase_credits, name='purchase_credits'),
    path('paddle_webhook/', views.PaddleCheckoutView.as_view(), name='paddle_webhook'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
