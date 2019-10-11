from django.shortcuts import render, HttpResponse,reverse,redirect,get_object_or_404
from .models import Client, ClientModelForm, ClientProduct,ClientProductForm
from django.contrib import messages
# Create your views here.

def whoami(  ):
    import sys
    return sys._getframe(1).f_code.co_name

from django import forms
class ClientFilterForm(forms.Form):
    name = forms.CharField(label='Client Name', required=False )
    country = forms.CharField(label='Country', required=False )


def client_index(request):
    client_set = request.user.client_set
    if request.method == 'POST':
        form = ClientFilterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            country = form.cleaned_data['country']
            if name:
                client_set = client_set.filter(name__icontains=name)
            if country:
                client_set = client_set.filter(country__icontains=country)
    else:
        form = ClientFilterForm()

    client_set = client_set.all()
    html = "clients/%s.html" % whoami()
    return render(request, html, {'client_set': client_set, 'filterForm': form})

def list_all_clients(request):
    if request.user.member.isManager() is False:
        return HttpResponse("WRONG!")

    client_set = Client.objects.all()
    if request.method == 'POST':
        form = ClientFilterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            country = form.cleaned_data['country']
            if name and len(name) > 0:
                client_set = Client.objects.filter(name__icontains=name).all()
            if country and len(country)>0:
                client_set = client_set.filter(country__icontains=country).all()
    else:
        form = ClientFilterForm()
    html = "clients/%s.html"%whoami()
    return render(request, html, {'client_set': client_set, 'filterForm': form})

def add_client(request):
    if request.method == "POST":
        form = ClientModelForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.user = request.user
            client.save()
            messages.success(request, "Client Added: %s "% client)
            return redirect(reverse('view_client', kwargs={'client_id': client.id}))
    else:
        form = ClientModelForm()

    html = "clients/%s.html" % whoami()
    return render(request, html, {'form': form})

def view_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    html = "clients/%s.html" % whoami()
    return render(request, html, {'client': client})

from .models import ClientContactor, ClientContactorForm
def add_contactor(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = ClientContactorForm(request.POST)
        if form.is_valid():
            contactor = form.save(commit=False)
            contactor.client = client
            contactor.save()
            messages.success(request, 'Contactor added ! ')
            return redirect(reverse('view_client',kwargs={'client_id': client.id}))
    else:
        form = ClientContactorForm()

    html = "clients/%s.html" % whoami()
    return render(request, html, {'client': client, 'form': form})

def edit_contactor(request, contactor_id):

    contactor = get_object_or_404(ClientContactor, pk=contactor_id)
    client = contactor.client

    if request.method == 'POST':
        form = ClientContactorForm(request.POST, instance=contactor)
        if form.is_valid():
            contactor = form.save()
            messages.success(request, 'Contactor updated ! ')
            return redirect(reverse('view_client',kwargs={'client_id': client.id}))
    else:
        form = ClientContactorForm(instance=contactor)

    html = "clients/%s.html" % whoami()
    return render(request, html, {'client': client, 'contactor': contactor, 'form': form})

def edit_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)

    if request.method == 'POST':
        form = ClientModelForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(request, "Client Info Updated ! ")
            return redirect(reverse('view_client', kwargs={'client_id': client.id}))
    else:
        form = ClientModelForm(instance=client)

    html = "clients/%s.html" % whoami()
    return render(request, html, {'client': client, 'form': form})

def add_clientproduct(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == "POST":
        form = ClientProductForm(request.POST)
        if form.is_valid():
            cp = form.save(commit=False)
            cp.user=request.user
            cp.client=client
            cp.save()
            messages.success(request, "Product added ! ")
            return redirect(reverse('edit_cp_info', kwargs={'cp_id':cp.id}))
    else:
        form = ClientProductForm()

    html = "clientproducts/%s.html" % whoami()
    return render(request, html, {'client': client, 'form': form})

def edit_cp_name(request, cp_id):
    cp = get_object_or_404(ClientProduct, pk=cp_id)
    client = cp.client
    if request.method == "POST":
        form = ClientProductForm(request.POST, instance=cp)
        if form.is_valid():
            cp = form.save()
            messages.success(request, "Product name updated ! ")
            return redirect(reverse('view_client', kwargs={'client_id': client.id}))
    else:
        form = ClientProductForm(instance=cp)
    html = "clientproducts/%s.html" % whoami()

    return render(request, html, {'client': client, 'cp': cp, 'form': form})

def view_cp(request, cp_id):
    cp = get_object_or_404(ClientProduct, pk=cp_id)
    client=  cp.client
    html = "clientproducts/%s.html" % whoami()
    return render(request, html, {'client': client, 'cp': cp})

def expire_cp(request, cp_id, expired):
    cp = get_object_or_404(ClientProduct, pk=cp_id)

    if expired == 0:
        # Only Manager leve can do
        if request.user.member.isManager():
            cp.expired = False
            cp.save()
            messages.success(request, 'Active Product success ! ')
            return redirect(reverse("view_client", kwargs={'client_id': cp.client.id}))
        else:
            return HttpResponse("No permission to active one expired product ! ")
    if expired == 1:
        # Own Sales can set to true
        if request.user.member.isSales():
            if request.user == cp.user or request.user.member.isManager():
                cp.expired=True
                cp.save()
                messages.success(request, 'Expired Product success ! ')
                return redirect(reverse("view_client", kwargs={'client_id': cp.client.id}))
            else:
                return HttpResponse("No Permission to expired other sales product!")
        else:
            return HttpResponse("No permission to expired product ! ")
    return HttpResponse("ERROR input! ")


from .models import CPInfo, CPInfoForm, CPINFO_DISPLAY_FIELDS
def edit_cp_info(request, cp_id):
    cp = get_object_or_404(ClientProduct, pk=cp_id)
    client = cp.client

    if request.method == 'POST':
        try:
            if cp.cpinfo:
                form = CPInfoForm(request.POST, instance=cp.cpinfo)
        except:
            form = CPInfoForm(request.POST)

        if form.is_valid():
            cp_info = form.save(commit=False)
            cp_info.user = request.user
            cp_info.cp = cp
            cp_info.save()
            messages.success(request, "CP Info Updated ! ")
            return redirect(reverse('view_client', kwargs={'client_id': client.id}))
    else:
        try:
            if cp.cpinfo:
                form = CPInfoForm(instance=cp.cpinfo)
        except:
            form = CPInfoForm()
    html = "clientproducts/%s.html" % whoami()
    return render(request, html, {'client': client, 'cp': cp, 'form': form})

from .models import ClientOrder, AddCOForm, CO_STATUS_CHOICE

class FilterOrderForm(forms.Form):
    clientname = forms.CharField(label='Client Name', required=False)
    orderID = forms.CharField(label='Order ID', required=False)
    po = forms.CharField(label='PO#', required=False)
    status = forms.CharField(label='Status', required=False)

def process_orderFilterForm(request, querySet):
    form = FilterOrderForm(request.POST)
    if form.is_valid():
        clientname = form.cleaned_data['clientname']
        orderID = form.cleaned_data['orderID']
        po = form.cleaned_data['po']
        status = form.cleaned_data['status']
        if clientname:
            querySet = querySet.filter(client__name__icontains=clientname)
        if orderID:
            querySet = querySet.filter(job_id__icontains=orderID)
        if po:
            querySet = querySet.filter(po_number__icontains=po)
        if status:
            querySet = querySet.filter(status=status)

    return (form, querySet)

def list_my_orders(request):
    order_set = request.user.clientorder_set
    if request.method == 'POST':
        (form, order_set) = process_orderFilterForm(request, order_set)
    else:
        form = FilterOrderForm()
    order_set = order_set.all()
    html = "clientorders/%s.html" % whoami()
    return render(request, html, {'order_set': order_set, 'filterForm': form})

def list_all_orders(request):
    order_set = ClientOrder.objects
    if request.method == 'POST':
        (form, order_set) = process_orderFilterForm(request, order_set)
    else:
        form = FilterOrderForm()
    order_set = order_set.all()
    html = "clientorders/%s.html" % whoami()
    return render(request, html, {'order_set':order_set, 'filterForm': form})

def list_all_order_summaryView(request):
    order_set = ClientOrder.objects
    if request.method == 'POST':
        (form, order_set) = process_orderFilterForm(request, order_set)
    else:
        form = FilterOrderForm()
    order_set = order_set.all()
    html = "clientorders/%s.html" % whoami()
    return render(request, html, {'order_set': order_set, 'filterForm': form})

def add_clientorder(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = AddCOForm(request.POST)
        if form.is_valid():
            co = form.save(commit=False)
            co.user = request.user
            co.client = client
            co.save()
            messages.success(request, 'Client Order add successful ! ')
            return redirect(reverse('view_co', kwargs={'co_id': co.id}))
    else:
        form = AddCOForm()
        form.fields['contactor'].queryset = client.clientcontactor_set.all()

    html = "clientorders/%s.html" % whoami()
    return render(request, html, {'client': client,  'form': form})

def view_co(request, co_id):
    co = get_object_or_404(ClientOrder, pk=co_id)
    html = "clientorders/%s.html" % whoami()
    return render(request, html, {'co': co,'client': co.client })

def edit_co(request, co_id):
    co = get_object_or_404(ClientOrder, pk=co_id)
    client = co.client

    if request.method == 'POST':
        form = AddCOForm(request.POST, instance=co)
        if form.is_valid():
            co = form.save(commit=False)
            co.user=request.user
            co.save()
            co.addNote(request.user, "EDIT ORDER" , co.print())
            messages.success(request, 'Client Order updated successful ! ')
            return redirect(reverse('view_co', kwargs={'co_id': co.id}))
    else:
        form = AddCOForm(instance=co)
    html = "clientorders/%s.html" % whoami()
    return render(request, html, {'client': client, 'co': co, 'form': form})

def update_co_status(request, co_id, nxt_action):
    co = get_object_or_404(ClientOrder, pk=co_id)

    if nxt_action in ['SUBMIT', "DELIVER"] and request.user.member.isSales():
        co.status = nxt_action
        co.save()
        messages.success(request, "%s order success!" % nxt_action)
        return redirect(reverse('view_co', kwargs={'co_id': co.id}))

    if nxt_action in ['APPROVE', 'DRAFT', 'CANCEL', 'COMPLETE'] and request.user.member.isManager():
        co.status = nxt_action
        co.save()
        messages.success(request, "%s order success!" % nxt_action)
        return redirect(reverse('view_co', kwargs={'co_id': co.id}))
    return HttpResponse("No Permission!")



from .models import OrderProduct, OrderProductForm

def add_cop(request, co_id):
    co = get_object_or_404(ClientOrder, pk=co_id)
    client = co.client

    if request.method == 'POST':
        form = OrderProductForm(request.POST)
        if form.is_valid():
            cop = form.save(commit=False)
            cop.user = request.user
            cop.co = co
            cop.price = cop.cp.cpinfo.price
            cop.currency = cop.cp.cpinfo.currency
            cop.save()
            messages.success(request, 'Product added into Order successful! ')
            return redirect(reverse('add_cop', kwargs={'co_id': co.id}))
    else:
        form = OrderProductForm()
        form.fields['cp'].queryset = client.clientproduct_set.filter(expired=True).all()
    html = "clientorders/%s.html" % whoami()
    return render(request, html, {'client': client, 'co': co, 'form': form})

def edit_cop(request, cop_id):
    cop = get_object_or_404(OrderProduct, pk=cop_id)
    co = cop.co
    client = co.client

    if request.method == 'POST':
        form = OrderProductForm(request.POST, instance=cop)
        if form.is_valid():
            cop = form.save(commit=False)
            cop.user = request.user
            cop.save()
            messages.success(request, 'Product updated in Order successful! ')
            return redirect(reverse('view_co', kwargs={'co_id': co.id}))
    else:
        form = OrderProductForm(instance=cop)
        form.fields['cp'].queryset = client.clientproduct_set.filter(expired=True).all()

    html = "clientorders/%s.html" % whoami()
    return render(request, html, {'client': client, 'co': co, 'form': form, 'cop': cop})