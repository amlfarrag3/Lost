from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('reports/', views.report_list, name='report-list'),
    path("advanced-search/", views.advanced_search, name="advanced-search"),
    path("missing/add/", views.add_missing_with_report, name="add-missing-person"), 
      #api-views
    path("api/advanced-search/", views.advanced_search_api, name="api-advanced-search"),
      # Authentication
    path('login/', auth_views.LoginView.as_view(template_name="finder/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('signup/', views.signup, name="signup"),

]
