from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from .models import Account, AccountForm, AccountBalance
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from clients.models import ClientOrder, Client
from .models import Income, Transfer, IncomeForm, Outcome, OutcomeForm


# Create your views here.
def whoami(  ):
    import sys
    return sys._getframe(1).f_code.co_name

def account_index(request):
    account_set = Account.objects.all()
    html = "accounts/%s.html" % whoami()
    return render(request, html, {'account_set': account_set})

@login_required
def add_account(request):
    account_set = Account.objects.all()
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save()
            messages.success(request, 'Account added ! ')
            return redirect(reverse('account_index'))
    else:
        form = AccountForm()

    html = "accounts/%s.html" % whoami()
    return render(request, html, {'account_set': account_set, 'form': form})

@login_required
def edit_account(request, account_id):

    account_set = Account.objects.all()
    account = get_object_or_404(Account, pk=account_id)

    if request.method == "POST":
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            account = form.save()
            messages.success(request, 'Account updated ! ')
            return redirect(reverse('account_index'))
    else:
        form = AccountForm(instance=account)

    html = "accounts/%s.html" % whoami()
    print(html)
    return render(request, html, {'account_set': account_set, 'account': account, 'form': form})

def view_account(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    html = "accounts/%s.html" % whoami()
    return render(request, html, {'account': account})

from .models import Payee, PayeeForm

def payee_index(request):
    payee_set = Payee.objects.all()
    html = "accounts/%s.html" % whoami()
    return render(request, html, {'payee_set': payee_set})

@login_required
def view_payee(request, payee_id):
    payee = get_object_or_404(Payee, pk=payee_id)
    html = "accounts/%s.html" % whoami()
    return render(request, html, {'payee': payee})

@login_required
def add_payee(request):
    payee_set = Payee.objects.all()
    if request.method == "POST":
        form = PayeeForm(request.POST)
        if form.is_valid():
            account = form.save()
            messages.success(request, 'Payee added ! ')
            return redirect(reverse('payee_index'))
    else:
        form = PayeeForm()

    html = "accounts/%s.html" % whoami()
    return render(request, html, {'payee_set': payee_set, 'form': form})

@login_required
def edit_payee(request, payee_id):
    payee_set = Payee.objects.all()
    payee = get_object_or_404(Payee, pk=payee_id)

    if request.method == "POST":
        form = PayeeForm(request.POST, instance=payee)
        if form.is_valid():
            account = form.save()
            messages.success(request, 'Payee updated ! ')
            return redirect(reverse('payee_index'))
    else:
        form = PayeeForm(instance=payee)

    html = "accounts/%s.html" % whoami()
    print(html)
    return render(request, html, {'payee_set': payee_set, 'payee': payee, 'form': form})




@login_required
def list_transaction(request):
    transfer_set = Transfer.objects.all()
    html = "transactions/%s.html" % whoami()
    return render(request, html, {'transfer_set': transfer_set})

@login_required
def view_transaction(request, tran_id):
    return HttpResponse("TBD")
    html = "transactions/%s.html" % whoami()
    return render(request, html, {})

from .models import TransferForm
@login_required
def edit_transaction(request, tran_id):
    tran = get_object_or_404(Transfer, pk=tran_id)
    if request.method == "POST":
        form = TransferForm(request.POST, instance=tran)
        if form.is_valid():
            tran = form.save()
            return redirect(reverse('list_transaction'))
    else:
        form = TransferForm(instance=tran)
    html = "transactions/%s.html" % whoami()

    return render(request, html, {'tran': tran, 'form': form})

from datetime import date

@login_required
def add_income(request, co_id):
    co = get_object_or_404(ClientOrder, pk=co_id)
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            need_jiehui = False
            trueAmount = 0

            if form.cleaned_data['account'].currency != "RMB":
                need_jiehui = True
            else:
                trueAmount = form.cleaned_data['amount']
            transfer = Transfer.objects.create(
                clientorder=co,
                client=co.client,
                date=form.cleaned_data['date'],
                account=form.cleaned_data['account'],
                amount=form.cleaned_data['amount'],
                currency=form.cleaned_data['account'].currency,
                need_jiehui=need_jiehui,
                trueAmount=trueAmount,
                note = form.cleaned_data['note'],
            )
            income = Income.objects.create(transfer=transfer, payer=form.cleaned_data['payer'])
            messages.success(request, 'Income added ! ')
            return redirect(reverse('view_co', kwargs={'co_id': co.id}))
    else:
        form = IncomeForm()
        form.fields['date'].initial = date.today()

    html = "transactions/%s.html" % whoami()
    return render(request, html, {'client': co.client, 'co': co, 'form': form})



@login_required
def add_outcome(request, co_id):
    co = get_object_or_404(ClientOrder, pk=co_id)
    if request.method == "POST":
        form = OutcomeForm(request.POST)
        if form.is_valid():
            need_jiehui = False  # 支出都为RMB, 不需要结汇
            trueAmount = form.cleaned_data['amount']  # TrueAmount

            transfer = Transfer.objects.create(
                clientorder=co,
                client=co.client,
                date=form.cleaned_data['date'],
                account=form.cleaned_data['account'],
                amount=form.cleaned_data['amount'],  # 支出为负数
                currency=form.cleaned_data['account'].currency,
                need_jiehui=need_jiehui,
                trueAmount=trueAmount,
                note = form.cleaned_data['note'],
            )
            outcome = Outcome.objects.create(transfer=transfer, payee=form.cleaned_data['payee'])
            messages.success(request, 'Outcome added ! ')
            return redirect(reverse('view_co', kwargs={'co_id': co.id}))
    else:
        form = OutcomeForm()
        form.fields['date'].initial = date.today()

    html = "transactions/%s.html" % whoami()
    return render(request, html, {'client': co.client, 'co': co, 'form': form})

from django import forms

class JiehuiForm(forms.Form):
    amount = forms.DecimalField(label=u'结汇金额')
    account = forms.ModelChoiceField(queryset=Account.objects.filter(currency='RMB').all() , label='RMB Account')
    rate = forms.DecimalField(label='Rate')
    trueAmount = forms.DecimalField(label='RMB Amount')

@login_required
def jiehui_income(request, income_id):
    income = get_object_or_404(Income, pk=income_id)
    if income.transfer.need_jiehui == False or income.transfer.currency == 'RMB':
        return HttpResponse(" No need Jiehui for RMB or Jiehui Flag is False ! ")
    if request.method == 'POST':
        form = JiehuiForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['account'].addJiehuiTransfer(form.cleaned_data['rate'],
                                              form.cleaned_data['trueAmount'],
                                            income.transfer):
                messages.success(request, 'Jiehui Success!')
                return redirect(reverse('view_co', kwargs={'co_id':income.transfer.clientorder.id}))
            else:
                messages.error(request, 'Jiehui Failed ! ')
    else:
        form = JiehuiForm()
    form.fields['amount'].label=u'结汇金额(%s)'%income.transfer.currency
    form.fields['amount'].widget.attrs['readonly'] = True
    #
    form.fields['amount'].initial=income.transfer.amount

    html = "transactions/%s.html" % whoami()
    return render(request, html, {'income': income, 'form': form})
# TBD

import datetime
class AccountBalanceInitForm(forms.Form):
    balance = forms.DecimalField(label=u'Current Balance')
    date = forms.DateField(label=u'Balance Date', initial=datetime.date.today())

def init_account_balance(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    if account.accountbalance_set.all().count() > 0:
        return HttpResponse("Already initialzed! ")

    if request.method == 'POST':
        form =AccountBalanceInitForm(request.POST)
        if form.is_valid():
            balance = form.cleaned_data['balance']
            date = form.cleaned_data['date']
            ab = AccountBalance.objects.create(
                account=account,
                balance_date=date,
                parentABNode=None,
                previousBalance=0,
                activitySum=0,
                adjustBalance=balance,
                balance=balance,
                note='INIT'
            )
            messages.success(request, 'Account initialized success!')
            return redirect(reverse("view_account", kwargs={"account_id": account.id}))
    else:
        form = AccountBalanceInitForm()

    html = "accounts/%s.html" % whoami()
    return render(request, html, {'account': account, 'form': form})

import decimal
def account_duizhang(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    if request.method == "POST":
        trueBalance = decimal.Decimal(request.POST['trueBalance'])
        previousBalance = account.preBalance()
        activitySum = account.activitySum()
        parentABNode = account.accountbalance_set.last()


        adjustBalance = trueBalance - account.balance()
        import pdb
        pdb.set_trace()

        new_ab = AccountBalance.objects.create(
            account=account,
            balance_date = date.today(),
            parentABNode=parentABNode,
            previousBalance = previousBalance,
            activitySum = activitySum,
            adjustBalance= adjustBalance,
            balance = trueBalance,
            note = 'DUIZHANG'
        )

        for tran in account.duizhangList():
            tran.abnode = new_ab
            tran.save()

        messages.success(request, "Duizhang Success! ")
        return redirect(reverse('view_account', kwargs={'account_id': account.id}))

    return HttpResponse("OK")