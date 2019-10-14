from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.conf import settings
# Create your models here.
from django.db.models import Sum, Avg


SOURCE_CHOICE = (
    ('ALIBABA', "Alibaba"),
    ('EMAIL', "EMAIL"),
    ('OTHER', "OTHER"),
)

class Client(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Name', max_length=100, unique=True)
    country=models.CharField(verbose_name='Country', max_length=50)
    source = models.CharField(max_length=10,
                              verbose_name='Source',
                              choices=SOURCE_CHOICE,
                              default='OTHER')
    created_date = models.DateField(auto_now_add=True,
                                        verbose_name='Create Date')
    def __str__(self):
        return self.name


class ClientModelForm(forms.ModelForm):
    class Meta:
        model= Client
        fields= ['name', 'country', 'source']


class ClientContactor(models.Model):
    client = models.ForeignKey(Client,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Contactor Name(*)')
    position = models.CharField(max_length=100, verbose_name='Position(*)')
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    wechat = models.CharField(max_length=100, blank=True, null=True, verbose_name="Wechat")
    skype = models.CharField(max_length=100, blank=True, null=True, verbose_name="skype")
    tel = models.CharField(max_length=100, blank=True, null=True, verbose_name='Tel')
    note = models.TextField(verbose_name='Note', blank=True, null=True)

    def __str__(self):
        return self.name

class ClientContactorForm(forms.ModelForm):
    class Meta:
        model= ClientContactor
        fields= ['name', 'position', 'email', 'wechat', 'skype', 'tel', 'note']

PRICE_TERM_CHOICE=(
    ('FOB', 'FOB'),
    ('EXW', 'EXW'),
    ('ST','Tax + Shipping'),
    ('S', 'Shipping Only(No Tax)'),
    ('T', 'Tax(No Shipping')
)


CP_TYPE_CHOICE = (
    ('PRODUCT', u'产品'),
    ('SHIPPING', u'运费'),
    ('MOLD', u'磨具'),
)

class ClientProduct(models.Model):
    """ Price: Trade Currency, not for finance clearance
        PriceRMB: Finance Clearance Term
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client,
                               on_delete=models.CASCADE)
    type = models.CharField(verbose_name=u'类目', max_length=20, choices=CP_TYPE_CHOICE, default='PRODUCT')
    name = models.CharField(verbose_name='Product Name', max_length=100)
    created_date = models.DateField(auto_now_add=True, verbose_name="Created Date")
    expired = models.BooleanField(default=False, verbose_name='Expired Product')

    def __str__(self):
        if self.expired:
            return "*EXPIRED*%s"%self.name
        return self.name

class ClientProductForm(forms.ModelForm):
    class Meta:
        model = ClientProduct
        fields=['type', 'name']

class CPInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    cp = models.OneToOneField(ClientProduct, on_delete=models.CASCADE,
                           verbose_name='Product')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='created_time')

    price = models.DecimalField(decimal_places=3, max_digits=6, verbose_name='Price')
    currency = models.CharField(max_length=5, choices=settings.CURRENCE_CHOICE, default='USD')

    priceTerm = models.CharField(max_length=5, choices=PRICE_TERM_CHOICE,
                                 verbose_name='Price Term',
                                 default='FOB')
    priceRMB = models.DecimalField(decimal_places=3, max_digits=6, verbose_name=u'Price(RMB)')

    cost = models.DecimalField(decimal_places=3, max_digits=6, default=0, verbose_name='Cost(RMB)')

    unit_size = models.CharField(max_length=50, verbose_name='Unit Size', help_text='L*W*H(cm)', blank=True, null=True)
    unit_weight = models.DecimalField(max_digits=10, decimal_places=3,
                                      verbose_name="Unit Weight(g)",
                                      help_text='',
                                      blank=True, null=True)
    material = models.CharField(max_length=50, verbose_name='Material', blank=True, null=True)

    carton_size = models.CharField(max_length=50,
                                   verbose_name='Carton Size',
                                   help_text='L*W*H(cm)',
                                   blank=True,
                                   null=True)
    qty_carton = models.PositiveIntegerField(verbose_name="Units Per Carton",
                                             default=0)
    carton_nw = models.DecimalField(max_digits=5, decimal_places=3,
                                    verbose_name="Carton N.W.(KG)",
                                    blank=True,
                                    null=True)
    carton_gw = models.DecimalField(max_digits=5, decimal_places=3,
                                    verbose_name="Carton G.W.(KG)",
                                    blank=True,
                                    null=True)
    note = models.TextField(verbose_name='Note', blank=True, null=True)

    def __str__(self):
        return "INFO: %s" % self.cp


CPINFO_DISPLAY_FIELDS= ['price', 'currency', 'priceTerm', 'note', 'priceRMB', 'cost',
                        'unit_size', 'unit_weight', 'material',
                        'carton_size', 'qty_carton', 'carton_nw', 'carton_gw', 'note']

class CPInfoForm(forms.ModelForm):
    class Meta:
        model= CPInfo
        fields = CPINFO_DISPLAY_FIELDS

    def hideFields(self, cp):
        displayFields = ['price', 'currency', 'note']
        if cp.type in ['MOLD', 'SHIPPING']:
            for fld in CPINFO_DISPLAY_FIELDS:
                if fld not in displayFields:
                    self.fields[fld].widget = forms.HiddenInput()


def cpcost_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'cp/{0}/cost/{1}'.format(instance.cp.id, filename)


CO_TYPE_CHOICE = (
    ('Sample', 'Sample'),
    ('Order', 'Order'),
)


CO_STATUS_CHOICE = (
    # Sales can update
    ('DRAFT', 'DRAFT'),
    ('SUBMIT', 'SUBMIT'),
    ('DELIVER', 'DELIVER'),
    # Manager can update
    ('APPROVE', "APPROVE"),
    ('COMPLETE', 'COMPLETE'),
    ('CANCEL', 'CANCEL'),

)

class ClientOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Created User')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Client')
    job_id = models.CharField(max_length=20, unique=True, verbose_name='Job_ID(Unique)')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Created Time')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='Updated Time')
    archive = models.BooleanField(default = False, verbose_name='Archived')
    order_type = models.CharField(max_length=10, default='Order', choices=CO_TYPE_CHOICE, verbose_name='Type')
    po_number = models.CharField(max_length=50, default='N/A', verbose_name='PO')
    totalAmount = models.DecimalField(max_digits=10, decimal_places=3, default=0, verbose_name='Total Amount')
    currency = models.CharField(max_length=5, choices=settings.CURRENCE_CHOICE, default='USD', verbose_name='Currency')
    deliveryDate = models.DateField(default='2099-01-01', verbose_name='Delivery Date')
    contactor = models.ForeignKey(ClientContactor, on_delete=models.CASCADE, verbose_name='Client Contactor')
    status = models.CharField(max_length=10, choices=CO_STATUS_CHOICE, default='DRAFT')

    def editable(self):
        if self.status == 'DRAFT':
            return True
        return False

    def salesNextAction(self):
        if self.status == 'DRAFT':
            # Check
            if self.orderproduct_set.count() == 0 :
                return None
            return ["SUBMIT"]
        if self.status == 'APPROVE':
            return ['DELIVER']
        return None
    def mgrNextAction(self):
        if self.status == 'SUBMIT':
            return ['APPROVE', 'DRAFT']
        if self.status == 'APPROVE':
            return ['CANCEL']
        if self.status == 'DELIVER':
            if self.cosummary.needJiehuiQty > 0 :
                print("Jiehui > 0 ")
                return None
            return ['COMPLETE']
        return None

    def __str__(self):
        return self.job_id

    def print(self):
        return "user(%s)- COID(%s)-Archieve(%s)-Contactor(%s)-OrderType(%s)-PO(%s)-TM(%s)-CUR(%s)-DDate(%s)" % \
               (self.user, self.id, self.archive, self.contactor, self.order_type, self.po_number,
                self.totalAmount, self.currency, self.deliveryDate)

    def addNote(self, user, title, note):
        print("TBD")
        self.clientorderlog_set.create(user=user, title=title, note=note)

    def copTotalQty(self):
        if self.orderproduct_set.count() > 0:
            return self.orderproduct_set.all().aggregate(sum=Sum('qty'))['sum']
        return 0

    def copTotalSubTotal(self):
        if self.orderproduct_set.count() > 0:
            return self.orderproduct_set.all().aggregate(sum=Sum('subtotal'))['sum']
        return 0

    def incomeTransferSet(self):
        return self.transfer_set.filter(income__isnull=False)

    def outcomeTransferSet(self):
        return self.transfer_set.filter(outcome__isnull=False)


from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save



class AddCOForm(forms.ModelForm):
    class Meta:
        model = ClientOrder
        fields = ['job_id', 'contactor', 'order_type',
                  'po_number', 'totalAmount', 'currency', 'deliveryDate' ]

class ClientOrderLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Created User')
    co = models.ForeignKey(ClientOrder, on_delete=models.CASCADE, verbose_name="Client Order")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Created Time')
    title = models.CharField(max_length=100,  verbose_name='Title')
    note = models.TextField(verbose_name='Note', default="", blank=True)

    def __str__(self):
        return "%s : %s "%(self.title, self.note)

class OrderProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Created User')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Updated Time')
    co = models.ForeignKey(ClientOrder, on_delete=models.CASCADE, verbose_name='ClientOrder')
    cp = models.ForeignKey(ClientProduct, on_delete=models.CASCADE, verbose_name='Client Product')
    qty = models.PositiveIntegerField(verbose_name='Qty', default=0)
    price = models.DecimalField(decimal_places=3, max_digits=6, verbose_name='Price')
    currency = models.CharField(max_length=5, choices=settings.CURRENCE_CHOICE, default='USD')
    subtotal = models.DecimalField(decimal_places=3, max_digits=10, verbose_name='Sub-Total')
    note = models.CharField(max_length=100, verbose_name='Note', blank=True, default='')

    def __str__(self):
        return "OP(%s)-User(%s)-CP(%s)-Qty(%s)-Price(%s)-Currency(%s)-Subtotal(%s)-note(%s)"% \
        (self.id, self.user, self.cp, self.qty, self.price, self.currency, self.subtotal, self.note)

@receiver(pre_save, sender=OrderProduct)
def orderproduct_update_subtotal(instance, **kwargs):
    instance.subtotal = instance.qty*instance.price

class OrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = ['cp', 'qty', 'note' ]

