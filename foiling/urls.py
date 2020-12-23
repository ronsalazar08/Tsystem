from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.FHomepage, name='FHomepage'),
    path('deletedr/<slug:cnum>', views.DeleteDR, name='fdeletedr'),
    path('closedr/<slug:cnum>', views.CloseDR, name='fclosedr'),
    path('editdr/<slug:cnum>', views.EditDR, name='feditdr'),
    path('deleteitem/<slug:id>', views.DeleteITEM, name='fdeleteitem'),
    path('edititem/<slug:id>', views.EditItem, name='fedititem'),
    path('acchome/', views.Acchome, name='facchome'),
    path('summary/<slug:customerS>/<slug:monS>/<slug:yearS>', views.Summary, name='fsummary'),
]