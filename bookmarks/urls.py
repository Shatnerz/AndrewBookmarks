from django.conf.urls import url

from . import views
  
urlpatterns = [
    # Browsing
    url(r'^$', views.MainPage.as_view()),
    url(r'^user/(\w+)/$', views.user_page),
    url(r'^search/$', views.search_page),
    # Session management
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', views.logout_page),
    url(r'^register/$', views.register_page),
    url(r'^register/success/$', views.RegisterSuccessPage.as_view()),
    # Account management
    url(r'^save/$', views.bookmark_save_page),
    url(r'^delete/$', views.bookmark_delete_page),
]
