from django.urls import path, include
from . import views
from rest_framework import routers


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'mobile_money_profile',views.MoMoViewSet)
router.register(r'bank_profile_profile',views.BankViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('verify_payment/<str:ref>', views.VerifyPayment.as_view()),
]


