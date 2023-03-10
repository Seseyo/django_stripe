from django.urls import re_path, path
from . import views


urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^items/$', views.ItemListView.as_view(), name='items'),
    re_path(r'^item/(?P<pk>\d+)$', views.item_detail_view, name='item-detail'),
    re_path(r'^config/$', views.stripe_config),
    re_path(r'^buy/(?P<pk>\d+)$', views.create_checkout_session),
    re_path(r'^success/$', views.SuccessView.as_view(), name='success'),
    re_path(r'^cancelled/$', views.CancelledView.as_view(), name='cancelled'),
    re_path(r'^webhook/$', views.stripe_webhook)

]
