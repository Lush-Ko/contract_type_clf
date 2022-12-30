from django.urls import path
from . import views

urlpatterns = [
    path('', views.predicter_home, name='predicter_home'),
    path('alldoc', views.all_doc, name='all_doc'),
    path('<int:pk>', views.DocumentsDetailView.as_view(), name='result-answer'),
    path('<int:pk>#pdf', views.DocumentsDetailViewPDF.as_view(), name='result-answer-pdf'),
    path('<int:pk>#html', views.DocumentsDetailViewHTML.as_view(), name='result-answer-html'),
    path('<int:pk>#origin', views.DocumentsDetailViewOrigin.as_view(), name='result-answer-origin')
]