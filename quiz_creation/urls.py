from django.contrib import admin
from django.urls import path, include
from quiz_creation import views

urlpatterns = [
    # path('questioncreation', views.questioncreationpage),
    path('create', views.createquizpage),
    path('createquiz', views.createquiz),
    path('submitquiz', views.submitquiz),
    path('deletequiz', views.deletequiz),
    path('ajaxcheckquiz', views.ajaxcheckquiz),
    path('ajaxcheckquestionfields', views.ajaxcheckquestionfields),
    path('ajaxgetquestiontoedit', views.ajaxgetquestiontoedit),
    path('ajaxeditquestion', views.ajaxeditquestion),
    path('ajaxdeletequestion', views.ajaxdeletequestion),
    path('ajaxremovequestiontoedit', views.ajaxremovequestiontoedit),
]
