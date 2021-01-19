
from django.shortcuts import render, redirect
from komax.models import dr_form, dr_item
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.contrib import messages
from komax.forms import NewDrForm, NewDrItem
import json
from django.db import connection


def check_group(request):
    if request.user.groups.filter(name='komax').exists():
        return redirect('KHomepage')
    elif request.user.groups.filter(name='foiling').exists():
        return redirect('FHomepage')
    else:
        return redirect('acchome')

def autho(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponse(json.dumps('loggedIn'), content_type="application/json")
    else: 
        return HttpResponseRedirect('/login/')

def Logout(request):
    return render(request, 'komax/logout.html')

# def dr_group(user):
#     return user.groups.filter(name='komax').exists()

# Use the above with:
@login_required
#@user_passes_test(dr_group, login_url='acchome')
def KHomepage(request):
    if request.method == 'POST':
        if request.POST.get('form_ctrl') == "new_dr":
            form = NewDrForm(request.POST)
            if form.is_valid():
                olo = form.cleaned_data['control_no']
                form.save()
                return redirect(f'/komax/editdr/{olo}')
            else:
                messages.warning(request, "Canceled: Control Number already exist!")
        if request.POST.get('form_ctrl') == "rename_dr":
            form = NewDrForm(request.POST)
            if form.is_valid():
                olo = form.cleaned_data['control_no']
                form.save()
                old_dr = request.POST.get('old_dr')
                new_dr = request.POST.get('control_no')
                n_dr = dr_form.objects.get(control_no=new_dr)
                o_dr_items = dr_item.objects.filter(control_noFK=old_dr)
                o_dr_items.update(control_noFK=n_dr)
                dr_form.objects.get(control_no=old_dr).delete()
                return redirect(f'/komax/editdr/{olo}')
            else:
                messages.warning(request, "Canceled: Control Number already exist!")
    else:
        form = NewDrForm()
    context = {
        'form':form,
        'dr_form': dr_form.objects.filter(Q(status='OPEN')| Q(status='WAITING')).order_by('control_no'),
        #'dr_form': dr_form.objects.all().order_by('control_no'),
    }
    return render(request, 'komax/home.html', context)

def CloseDR(request, cnum):
    try:
        olo = dr_form.objects.get(control_no=cnum)
        olo.status = "CLOSED"
        olo.save()
        messages.success(request, f'{cnum}: Succesfully Closed!')
    except:
        messages.success(request, f'DR already Closed by another User!')
    return redirect('KHomepage')

def DeleteDR(request, cnum):
    try:
        dr_form.objects.get(control_no=cnum).delete()
        messages.info(request, f'{cnum}: Succesfully deleted!')
    except:
        messages.info(request, f'DR already Deleted by another User!')
    return redirect('KHomepage')
    
def EditDR(request, cnum):
    if request.method == 'POST':
        if request.POST.get('form_ctrl') == "dr_form":
            form = NewDrForm(request.POST, instance=dr_form.objects.get(control_no=cnum))
            # form = NewDrForm(request.POST, instance=dr_form.objects.filter(control_no=cnum).get(control_no=cnum))
            form1 = NewDrItem()
            if form.is_valid():
                form.save()
                return redirect('KHomepage')

        elif request.POST.get('form_ctrl') == "dr_item":
            form = NewDrForm(instance=dr_form.objects.get(control_no=cnum))
            form1 = NewDrItem(request.POST)
            new_form1 = form1.save(commit=False)
            new_form1.control_noFK = dr_form.objects.get(control_no=cnum)
            if form1.is_valid():
                # cnum=form1.cleaned_data['control_noFK']
                form1.save()
                return redirect(f'/komax/editdr/{cnum}')
    else:
        try:
            form = NewDrForm(instance=dr_form.objects.get(control_no=cnum))
            # form = NewDrForm(instance=dr_form.objects.filter(control_no=cnum).get(control_no=cnum))
            form1 = NewDrItem()
        except:
            return redirect('KHomepage')

    if request.user.username == 'komaxa':
        signed_by = "JOSIE AUTOS"
    elif request.user.username == 'komaxb':
        signed_by = "GLORIA PASTOR"
    context = {
        'form'  :   form,
        'form1' :   form1,
        'items' :   dr_item.objects.filter(control_noFK=cnum).order_by('id'),
        'signed_by' : signed_by
    }
    return render(request, 'komax/dr.html', context)

def DeleteITEM(request, id):
    cnum = dr_item.objects.get(id=id).control_noFK
    dr_item.objects.get(id=id).delete()
    # messages.info(request, f'{cnum}: Succesfully deleted!')
    return redirect(f'/komax/editdr/{cnum}')
    
def EditItem(request, id):
    if request.method == 'POST':
        form1 = NewDrItem(request.POST, instance=dr_item.objects.get(id=id))
        cnum = dr_item.objects.get(id=id)
        print(cnum.control_noFK)
        new_form1 = form1.save(commit=False)
        new_form1.control_noFK = dr_form.objects.get(control_no=f'{cnum.control_noFK}')
        if form1.is_valid():
            cnum=dr_item.objects.get(id=id).control_noFK
            form1.save()
            return redirect(f'/komax/editdr/{cnum}')
    else:
        form1 = NewDrItem(instance=dr_item.objects.get(id=id))
    context = {
        'form1' :   form1,
    }
    return render(request, 'komax/edit.html', context)

def Acchome(request):
    if request.method == 'POST':
        customerS = request.POST['customerS']
        monS = request.POST['monS']
        yearS = request.POST['yearS']
        return redirect(f'/komax/summary/{customerS}/{monS}/{yearS}')
    return render(request, 'komax/acchome.html')

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
                                        (select date_created from komax_dr_form where control_no = cn limit 1) AS date_created,
                                        (select customer from komax_dr_form where control_no = cn limit 1) AS customer,
                                        (select status from komax_dr_form where control_no = cn limit 1) AS status
                                    FROM komax_dr_item ) AS t
                                WHERE t.customer = '{customerS}' AND t.date_created LIKE '{yearS}-{monS}%%' ORDER BY cn, date_created;""")
    context = {
        'items': objs,
        'customerS' :   customerS,
        'monS'  :   monS,
        'yearS' :   yearS,
    }
    return render(request, 'komax/summary.html', context)