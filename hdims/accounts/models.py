from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.
import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

class Account(models.Model):
    name = models.CharField(max_length=100, verbose_name='Account Name')
    currency = models.CharField(max_length=5,
                                choices=settings.CURRENCE_CHOICE,
                                default='USD',
                                verbose_name='Currency')
    note = models.TextField(verbose_name='Note')

    def __str__(self):
        return "%s(%s)"%(self.name, self.currency)

    def duizhangList(self):
        return self.transfer_set.filter(abnode=None).all()

    def activitySum(self):
        if self.transfer_set.filter(abnode=None).count() > 0:
            return self.transfer_set.filter(abnode=None).all().aggregate(sum=Sum('amount'))['sum']
        return 0

    def preBalance(self):
        if self.accountbalance_set.count() > 0:
            return self.accountbalance_set.last().balance
        return 0

    def balance(self):
        return self.preBalance()+self.activitySum()


    def addJiehuiTransfer(self, rate, amount, transfer):
        try:
            # 结汇账户里， 加一笔RMB结汇
            jiehui_tran = self.transfer_set.create(
                date = datetime.date.today(),
                amount = amount,
                currency='RMB',
                type='JIEHUI',
                trueAmount=amount,
                note="Transfer ID(%s) JIEHUI, %s(%s)"%(transfer.id, transfer.amount, transfer.currency)
            )
            # 美金账户里， 加一笔USD支出
            transfer.need_jiehui = False
            transfer.trueAmount = amount
            transfer.save()

            print(" \n\n PASS Check 1 \n\n ")

            jiehui_outcome = Transfer.objects.create(
                account=transfer.account,
                date=datetime.date.today(),
                amount=0-transfer.amount,
                currency=transfer.currency,
                type='JIEHUI',
                trueAmount=0,
                note="Transfer ID(%s) JIEHUI, %s(%s)" % (transfer.id, transfer.amount, transfer.currency)
            )
            print(" \n\n PASS Check 2 \n\n ")

        except:
            return False
        return True

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields= ['name', 'currency', 'note']


class AccountBalance(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Account')
    updated_time = models.DateTimeField(auto_now=True)
    balance_date = models.DateField(verbose_name="Balance Date", default=datetime.date.today())
    parentABNode = models.ForeignKey('self', on_delete=models.CASCADE,  blank=True, null=True,
                                     related_name='nextBalance', verbose_name='Parent Account Balance')
    previousBalance = models.DecimalField(verbose_name="Previous Balance", max_digits=10, decimal_places=2, default=0)
    activitySum = models.DecimalField(verbose_name="Activity Sum", max_digits=10, decimal_places=2, default=0)
    adjustBalance = models.DecimalField(verbose_name="Adjust Balance", max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(verbose_name="Balance", max_digits=10, decimal_places=2, default=0)
    # Previous Blanace + activyt Sum + adjust = Balance
    note = models.TextField(verbose_name='Note', blank=True, null=True)

PAYEE_TYPE = (
    ('CORP', 'Corporation'),
    ('Private', 'Private'),
)

class Payee(models.Model):
    name = models.CharField(max_length=100, verbose_name='Account Name')
    currency = models.CharField(max_length=5,
                                choices=settings.CURRENCE_CHOICE,
                                default='RMB',
                                verbose_name='Currency')
    type = models.CharField(max_length=10, choices=PAYEE_TYPE, default="CORP", verbose_name='Payee Type')
    note = models.TextField(verbose_name='Note')

    def __str__(self):
        return self.name

class PayeeForm(forms.ModelForm):
    class Meta:
        model = Payee
        fields= ['name', 'currency', 'type', 'note']

from clients.models import ClientOrder, Client, OrderProduct

class OrderPL(models.Model):
    co = models.OneToOneField(ClientOrder, on_delete=models.CASCADE, verbose_name='Order')
    orderTotalAmount = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Order Amount')
    productTotalAmount = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Product Total Amount')

TRANSFER_TYPE_CHOICE=(
    ('IO', u'收支'),
    ('JIEHUI', u'结汇'),
    ('BALANCE', u'平账'),
)

class Transfer(models.Model):
    updated_time = models.DateTimeField(auto_now=True)
    clientorder = models.ForeignKey(ClientOrder, on_delete=models.CASCADE, verbose_name='Order', null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Client', null=True, blank=True)

    date = models.DateField(verbose_name='Date', auto_now=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Account' )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount')
    currency = models.CharField(max_length=5,
                                choices=settings.CURRENCE_CHOICE,
                                default='USD',
                                verbose_name='Currency')
    note = models.TextField(verbose_name='Note')

    need_jiehui = models.BooleanField(default=False, verbose_name='Jiehui')
    trueAmount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='True Amount', default=0)
    type = models.CharField(max_length=10, verbose_name='Type', default='IO')
    abnode = models.ForeignKey(AccountBalance, on_delete=models.CASCADE, verbose_name='Account Balance Node', null=True, blank=True)

class CoSummary(models.Model):
    updated_time = models.DateTimeField(auto_now=True, verbose_name='Updated Time')
    co = models.OneToOneField(ClientOrder, on_delete=models.CASCADE, verbose_name='Client Order')
    orderAmount = models.DecimalField(verbose_name='Order Amount ', max_digits=10, decimal_places=2, default=0)
    orderCurrency = models.CharField(verbose_name='Order Currency', max_length=10, choices=settings.CURRENCE_CHOICE)
    cpAmount = models.DecimalField(verbose_name='OrderItem Total', max_digits=10, decimal_places=2, default=0)
    incomeTotal = models.DecimalField(verbose_name='Income Total', max_digits=10, decimal_places=2, default=0)
    unpaidTotal = models.DecimalField(verbose_name='Unpaid Total', max_digits=10, decimal_places=2, default=0)
    rmbIncomeTotal = models.DecimalField(verbose_name=u'人民币总收款', max_digits=10, decimal_places=2, default=0)
    rmbOutcomeTotal =  models.DecimalField(verbose_name=u'人民币总付款', max_digits=10, decimal_places=2, default=0)
    rmbProfit = models.DecimalField(verbose_name=u'人民币净利润', max_digits=10, decimal_places=2, default=0)
    rmbProfitRatio = models.DecimalField(verbose_name=u'利润率', max_digits=10, decimal_places=2, default=0)
    needJiehuiQty = models.PositiveIntegerField(verbose_name='TBD Jiehui', default=0)

    def warningList(self):
        warningList = []
        if self.co.orderproduct_set.count() == 0:
            warningList.append(u'订单里没有任何产品加入！')
        if self.orderAmount <= 0 :
            warningList.append(u'订单金额小于0！')
        if self.orderAmount != self.cpAmount:
            warningList.append(u'订单金额和产品总金额不符合！')
        if self.needJiehuiQty > 0:
            warningList.append(u'订单有尚未结汇的收款！')
        if self.rmbProfit <= 0:
            warningList.append(u'订单没有利润！')

        return warningList

from django.db.models import Sum, Avg
@receiver(post_save, sender=ClientOrder)
def clientorder_post_save_action(instance, created, **kwargs):
    try:
        instance.cosummary.orderAmount = instance.totalAmount
        instance.cosummary.orderCurrency = instance.currency
        instance.cosummary.save()
    except:
        CoSummary.objects.create(co=instance,
                                     orderAmount=instance.totalAmount,
                                     orderCurrency = instance.currency
                                     )

@receiver(post_save, sender=OrderProduct)
def orderproduct_post_save_action(instance, created, **kwargs):
    co = instance.co
    cosummary = co.cosummary
    total = co.orderproduct_set.all().aggregate(sum=Sum('subtotal'))
    cosummary.cpAmount =total['sum']
    cosummary.save()

@receiver(post_save, sender=Transfer)
def update_clientorder_financeinfo(instance, created, **kwargs):
    # cofinanceInfo must exist
    try:
        if instance.clientorder is not None:
            co = instance.clientorder
            cos = co.cosummary
            incomeTotal = co.transfer_set.filter(amount__gt=0).all().aggregate(sum=Sum('amount'))
            rmbIncomeTotal = co.transfer_set.filter(trueAmount__gt=0).all().aggregate(sum=Sum('trueAmount'))
            rmbOutcomeTotal = co.transfer_set.filter(trueAmount__lt=0).all().aggregate(sum=Sum('trueAmount'))
            rmbProfit = co.transfer_set.all().aggregate(sum=Sum('trueAmount'))
            rmbProfitRatio = 0


            if rmbIncomeTotal['sum'] is not None and rmbIncomeTotal['sum'] != 0:
                rmbProfitRatio =rmbProfit['sum'] /rmbIncomeTotal['sum']
            needJiehuiQty = co.transfer_set.filter(need_jiehui=True).count()

            if incomeTotal['sum'] is not None:
                cos.incomeTotal=incomeTotal['sum']
                cos.unpaidTotal = cos.orderAmount - cos.incomeTotal

            if rmbIncomeTotal['sum'] is not None:
                cos.rmbIncomeTotal=rmbIncomeTotal['sum']

            if rmbOutcomeTotal['sum'] is not None:
                cos.rmbOutcomeTotal=rmbOutcomeTotal['sum']
            if rmbProfit['sum'] is not None:
                cos.rmbProfit=rmbProfit['sum']
            cos.rmbProfitRatio = rmbProfitRatio
            if needJiehuiQty is not None:
                cos.needJiehuiQty=needJiehuiQty
            cos.save()
            print("Save OK")
            # Not I/O Transaction
    except:
        # Co summary not updated
        print("ERROR! ")


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields= '__all__'

class Income(models.Model):
    transfer = models.OneToOneField(Transfer, on_delete=models.CASCADE, verbose_name='Transfer')
    payer = models.CharField(max_length=100, verbose_name='Payer Name')

class IncomeForm(forms.Form):
    date = forms.DateField(label='Date')
    account = forms.ModelChoiceField(queryset=Account.objects.all(), label='Account')
    amount = forms.DecimalField(label='Amount')
    payer = forms.CharField(max_length=100, label='Payer')
    note = forms.CharField(max_length=1000, widget=forms.TextInput(), label='Note')


class Outcome(models.Model):
    transfer = models.OneToOneField(Transfer, on_delete=models.CASCADE, verbose_name='Transfer')
    payee = models.ForeignKey(Payee,on_delete=models.CASCADE, verbose_name='Payee')


class OutcomeForm(forms.Form):
    date = forms.DateField(label='Date')
    account = forms.ModelChoiceField(queryset=Account.objects.filter(currency='RMB'), label='RMB Account')
    amount = forms.DecimalField(label='Amount')
    payee = forms.ModelChoiceField(queryset=Payee.objects.all(), label='Payee')
    note = forms.CharField(max_length=1000, widget=forms.TextInput(), label='Note')

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount > 0:
            raise forms.ValidationError("Payment need < 0 ! ")
        return amount


