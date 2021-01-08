from django import forms
from komax.models import dr_form, dr_item
from django.utils.translation import ugettext_lazy as _


class NewDrForm(forms.ModelForm):
    customerCHOICES=[('HONDA','HONDA'),
                     ('IMV','IMV'),
                     ('GM','GM'),
                     ('OUTLANDER','OUTLANDER'),
                     ('CHRYSLER','CHRYSLER')]

    statusCHOICES=[('OPEN','OPEN'),
                   ('WAITING','WAITING'),
                   ('CLOSED','CLOSED')]
    

    customer = forms.ChoiceField(choices=customerCHOICES, required=True)
    status = forms.ChoiceField(choices=statusCHOICES, required=False)
    class Meta:
        model=dr_form
        fields = ['date_created', 'control_no', 'customer', 'line','status']

class NewDrItem(forms.ModelForm):
    control_noFK= forms.CharField(widget = forms.HiddenInput(), required=False)
    second_quantity = forms.IntegerField(widget = forms.HiddenInput(), initial=0, label="2ND")
    third_quantity = forms.IntegerField(widget = forms.HiddenInput(), initial=0, label="3RD")
    fourth_quantity = forms.IntegerField(widget = forms.HiddenInput(), initial=0, label="4TH")
    fifth_quantity = forms.IntegerField(widget = forms.HiddenInput(), initial=0, label="5TH")
    class Meta:
        model=dr_item
        fields = ['product_no', 'wos_no', 'first_quantity', 'second_quantity', 'third_quantity', 'fourth_quantity', 'fifth_quantity']
        # fields = ['product_no', 'wos_no', 'first_quantity', 'second_quantity', 'third_quantity', 'fourth_quantity', 'fifth_quantity', 'control_noFK']
        # raw_id_fields = ['control_noFK',]

        labels = {
            'first_quantity': _('1ST'),
            'second_quantity': _('2ND'),
            'third_quantity': _('3RD'),
            'fourth_quantity': _('4TH'),
            'fifth_quantity': _('5TH'),
            # 'control_noFK': _('Control no'),
        }
        # widgets = {
        #     'control_no': forms.TextInput(attrs={'disabled': True}),
        # }









