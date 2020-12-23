from django.shortcuts import render, redirect

# Create your views here.
def Acchome(request):
    if request.method == 'POST':
        dept = request.POST['dept']
        if dept == "KOMAX":
            return redirect(f'kacchome')
        elif dept == "FOILING":
            return redirect(f'facchome')
    return render(request, 'acct/acchome.html')