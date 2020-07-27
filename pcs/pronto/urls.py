from django.conf.urls import url

from . import views

app_name = 'pronto'
urlpatterns = [
    url(r'^index$', views.index, name='index'),

    url(r'^update_pronto$', views.update_pronto, name='update_pronto'),
    url(r'^create_or_update_pronto$', views.create_or_update_pronto, name='create_or_update_pronto'),

    url(r"^render_pronto_statics$", views.render_pronto_statics, name="render_pronto_statics"),
    url(r"^render_pronto_charting$", views.render_pronto_charting, name="render_pronto_charting"),

    url(r"^get_pronto_woh$", views.get_pronto_woh, name="get_pronto_woh"),
    url(r'^get_pronto_all$', views.get_pronto_all, name='get_pronto_all'),
    url(r"^get_pronto_top$", views.get_pronto_top, name="get_pronto_top"),
    url(r"^get_pronto_time$", views.get_pronto_time, name="get_pronto_time"),
    url(r"^get_pronto_ratio$", views.get_pronto_ratio, name="get_pronto_ratio"),
    url(r"^get_pronto_report$", views.get_pronto_report, name="get_pronto_report"),
    url(r"^get_pronto_charting$", views.get_pronto_charting, name="get_pronto_charting"),
    url(r"^get_pronto_charting_day$", views.get_pronto_charting_day, name="get_pronto_charting_day"),
    url(r"^get_pronto_priority$", views.get_pronto_priority, name="get_pronto_priority"),
    url(r"^get_pronto_not_done$", views.get_pronto_not_done, name="get_pronto_not_done"),
    url(r"^delete_pronto$", views.delete_pronto, name="delete_pronto$"),
]
