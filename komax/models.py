from django.db import models
from django.utils import timezone


class dr_form(models.Model):
    date_created = models.DateField(default=timezone.now)
    control_no = models.IntegerField(unique=True)
    customer = models.CharField(max_length=50)
    line = models.CharField(max_length=50, default='LINE')
    status = models.CharField(max_length=20, default='OPEN')
    
    def __str__(self):
        return str(self.control_no)

class dr_item(models.Model):
    product_no = models.CharField(max_length=50)
    wos_no = models.CharField(max_length=50,default='')
    first_quantity = models.IntegerField(default='')
    second_quantity = models.IntegerField(default='')
    third_quantity = models.IntegerField(default='')
    fourth_quantity = models.IntegerField(default='')
    fifth_quantity = models.IntegerField(default='')
    control_noFK = models.ForeignKey(dr_form, to_field="control_no", db_column="control_no", on_delete=models.CASCADE, default='', related_name='entries')
    
    def __str__(self):
        return str(self.product_no)
    # class Meta:
    #     verbose_name_plural = "Dies"