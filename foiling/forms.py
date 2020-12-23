from django import forms
from .models import dr_form, dr_item
from django.utils.translation import ugettext_lazy as _


class NewDrForm(forms.ModelForm):
    customerCHOICES=[('GM','GM'),
                     ('P552(14405-DOOR)','P552(14405-DOOR)'),
                     ('P552(14405-FRAME)','P552(14405-FRAME)'),
                     ('P552(14401-IP)','P552(14401-IP)'),
                     ('V363N','V363N')]

    statusCHOICES=[('OPEN','OPEN'),
                   ('WAITING','WAITING'),
                   ('CLOSED','CLOSED')]
    

    customer = forms.ChoiceField(choices=customerCHOICES, required=True)
    status = forms.ChoiceField(choices=statusCHOICES, required=False)
    class Meta:
        model=dr_form
        fields = ['date_created', 'control_no', 'customer', 'line','status']

class NewDrItem(forms.ModelForm):
    # control_noFK= forms.CharField()
    class Meta:
        model=dr_item
        fields = ['product_no', 'wos_no', 'first_quantity', 'second_quantity', 'third_quantity', 'fourth_quantity', 'fifth_quantity', 'control_noFK']
        labels = {
            'product_no': _('MOSF'),
            'wos_no': _('NO.'),
            'first_quantity': _('1ST'),
            'second_quantity': _('2ND'),
            'third_quantity': _('3RD'),
            'fourth_quantity': _('4TH'),
            'fifth_quantity': _('5TH'),
            'control_noFK': _('Control no'),
        }
        # widgets = {
        #     'control_no': forms.TextInput(attrs={'disabled': True}),
        # }









