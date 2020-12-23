from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.KHomepage, name='KHomepage'),
    path('deletedr/<slug:cnum>', views.DeleteDR, name='kdeletedr'),
    path('closedr/<slug:cnum>', views.CloseDR, name='kclosedr'),
    path('editdr/<slug:cnum>', views.EditDR, name='keditdr'),
    path('deleteitem/<slug:id>', views.DeleteITEM, name='kdeleteitem'),
    path('edititem/<slug:id>', views.EditItem, name='kedititem'),
    path('acchome/', views.Acchome, name='kacchome'),
    path('summary/<slug:customerS>/<slug:monS>/<slug:yearS>', views.Summary, name='ksummary'),
]