
from django.shortcuts import render, redirect
from foiling.models import dr_form, dr_item
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.contrib import messages
from foiling.forms import NewDrForm, NewDrItem
import json
from django.db import connection


# def dr_group(user):
#     return user.groups.filter(name='foiling').exists()

# Use the above with:
@login_required
#@user_passes_test(dr_group, login_url='acchome')
def FHomepage(request):
    if request.method == 'POST':
        form = NewDrForm(request.POST)
        if form.is_valid():
            olo = form.cleaned_data['control_no']
            form.save()
            return redirect(f'/foiling/editdr/{olo}')
        else:
            messages.warning(request, "Canceled: Control Number already exist!")

    else:
        form = NewDrForm()
    context = {
        'form':form,
        'dr_form': dr_form.objects.filter(Q(status='OPEN')| Q(status='WAITING')).order_by('control_no'),
        #'dr_form': dr_form.objects.all().order_by('control_no'),
    }
    return render(request, 'foiling/home.html', context)

def CloseDR(request, cnum):
    olo = dr_form.objects.get(control_no=cnum)
    olo.status = "CLOSED"
    olo.save()
    messages.success(request, f'{cnum}: Succesfully Closed!')
    return redirect('FHomepage')

def DeleteDR(request, cnum):
    dr_form.objects.get(control_no=cnum).delete()
    messages.info(request, f'{cnum}: Succesfully deleted!')
    return redirect('FHomepage')
    
def EditDR(request, cnum):
    if request.method == 'POST' and request.POST.get('form_ctrl') == "dr_form":
        form = NewDrForm(request.POST, instance=dr_form.objects.filter(control_no=cnum).get(control_no=cnum))
        form1 = NewDrItem()
        if form.is_valid():
            form.save()
            return redirect('FHomepage')

    elif request.method == 'POST' and request.POST.get('form_ctrl') == "dr_item":
        form1 = NewDrItem(request.POST)
        if form1.is_valid():
            cnum=form1.cleaned_data['control_noFK']
            form1.save()
            return redirect(f'/foiling/editdr/{cnum}')
    else:
        form = NewDrForm(instance=dr_form.objects.filter(control_no=cnum).get(control_no=cnum))
        form1 = NewDrItem()
    context = {
        'form'  :   form,
        'form1' :   form1,
        'items' :   dr_item.objects.filter(control_noFK=cnum).order_by('id')
    }
    return render(request, 'foiling/dr.html', context)

def DeleteITEM(request, id):
    cnum = dr_item.objects.get(id=id).control_noFK
    dr_item.objects.get(id=id).delete()
    # messages.info(request, f'{cnum}: Succesfully deleted!')
    return redirect(f'/foiling/editdr/{cnum}')
    
def EditItem(request, id):
    if request.method == 'POST':
        form1 = NewDrItem(request.POST, instance=dr_item.objects.get(id=id))
        if form1.is_valid():
            cnum=dr_item.objects.get(id=id).control_noFK
            form1.save()
            return redirect(f'/foiling/editdr/{cnum}')
    else:
        form1 = NewDrItem(instance=dr_item.objects.get(id=id))
    context = {
        'form1' :   form1,
    }
    return render(request, 'foiling/edit.html', context)

def Acchome(request):
    if request.method == 'POST':
        customerS = request.POST['customerS']
        monS = request.POST['monS']
        yearS = request.POST['yearS']
        return redirect(f'/foiling/summary/{customerS}/{monS}/{yearS}')
    return render(request, 'foiling/acchome.html')

def Summary(request, customerS, monS, yearS):
    customerS = customerS
    monS = monS
    yearS = yearS

    objs = dr_item.objects.raw(f"""
                                SELECT
                                    t.id,
                                    product_no,
                                    wos_no,
                                    quantity,
                                    cn,
                                    date_created,
                                    customer,
                                    status
                                FROM ( SELECT
                                        id,
                                        product_no,
                                        wos_no,
                                        (first_quantity + second_quantity + third_quantity + fourth_quantity + fifth_quantity) AS quantity,
                                        control_no AS cn,
                                        (select date_created from foiling_dr_form where control_no = cn limit 1) AS date_created,
                                        (select customer from foiling_dr_form where control_no = cn limit 1) AS customer,
                                        (select status from foiling_dr_form where control_no = cn limit 1) AS status
                                    FROM foiling_dr_item ) AS t
                                WHERE t.customer = '{customerS}' AND t.date_created LIKE '{yearS}-{monS}%%' ORDER BY date_created;""")
    context = {
        'items': objs,
        'customerS' :   customerS,
        'monS'  :   monS,
        'yearS' :   yearS,
    }
    return render(request, 'foiling/summary.html', context)