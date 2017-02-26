from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^process$', views.process, name="process"),
	url(r'^login', views.login, name="login"),
	url(r'^register', views.do_register, name="register"),
	url(r'^success$', views.success, name="success"),
	url(r'^logout$', views.logout, name="logout"),
	url(r'^edit', views.edit, name="edit_self"),
	url(r'^edit/(?P<userid>\d+)$', views.edit, name="edit"),
	url( r'^show/(?P<userid>\d+)$', views.show, name="show" ),
	url(r'^admin', views.admin, name="admin"),
]
