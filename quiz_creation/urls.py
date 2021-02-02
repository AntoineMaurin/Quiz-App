from django.contrib import admin
from django.urls import path, include
from quiz_creation import views

urlpatterns = [
    path('questioncreation', views.questioncreationpage),
    path('create', views.createquizpage),
    path('addquestion', views.addquestion),
    path('submitquiz', views.submitquiz),
    path('deletequestion/<int:index>', views.deletequestion),
    path('editquestion/<int:index>', views.editquestion),
    path('deletequiz', views.deletequiz),
    path('ajaxgetanswers', views.ajaxgetanswers),
    path('ajaxcheckfields', views.ajaxcheckfields),
]
