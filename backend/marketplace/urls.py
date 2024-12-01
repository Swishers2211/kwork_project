from django.urls import path

from marketplace.views import (
    DetailMainCategoryAPIView,
    MainCategoryAPIView,
    DetailAdditionalCategoryAPIView,
    DetailSubCategoryAPIView,
    MyAdsAPIView,
    CreateMyAdAPIView,
)

app_name = 'marketplace'

urlpatterns = [
    path('create_my_ad/', CreateMyAdAPIView.as_view(),),
    path('my_ads/', MyAdsAPIView.as_view(),),
    path('detail_subcategory/<int:subcategory_id>/', DetailSubCategoryAPIView.as_view(),),
    path('detail_additional_category/<int:additional_category_id>/', DetailAdditionalCategoryAPIView.as_view(),),
    path('main_categories/', MainCategoryAPIView.as_view(),),
    path('detail_main_category/<int:main_category_id>/', DetailMainCategoryAPIView.as_view(),),
]
