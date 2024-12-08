from .views import CreateDiscountCodeView, delete_all_promotion_codes, delete_all_coupons
from django.urls import path



urlpatterns = [
    # path("delete_all_promotion_codes/", delete_all_promotion_codes),
    # path("delete_all_coupons/", delete_all_coupons),
    path("create/", CreateDiscountCodeView.as_view(),)
]
