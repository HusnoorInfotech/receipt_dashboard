from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("export_data/",views.export_receipts_to_excel, name="export_excel"),
    path("form/",views.showform,name="show_forms"),
    path("submitform/",views.submitform, name="submitform"),
    path("receipt/<int:receipt_no>/",views.printform,name="printreceipt"),
]