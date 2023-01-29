from pickle import TRUE
from django.db import models
from core import settings
from .BaseModels import BaseModel

from rest_framework.decorators import api_view, permission_classes


class Province(BaseModel):
    class Meta:
        db_table = 'mst_provinces'


class District(BaseModel):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    class Meta:
        db_table = 'mst_districts'

    def __str__(self):
        return self.name_en


class LocalLevelType(BaseModel):
    class Meta:
        db_table = 'mst_local_level_types'


class LocalLevel(BaseModel):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    local_level_type = models.ForeignKey(
        LocalLevelType, on_delete=models.CASCADE)
    wards_count = models.IntegerField(null=True)
    gps_lat = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    gps_long = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    class Meta:
        db_table = 'mst_local_levels'


class FiscalYear(models.Model):
    code = models.CharField(max_length=7)
    from_date_bs = models.CharField(max_length=10)
    from_date_ad = models.DateField()
    to_date_bs = models.CharField(max_length=10)
    to_date_ad = models.DateField()
    display_order = models.IntegerField(null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False, null=False, blank=False)
    updated_at = models.DateTimeField(
        auto_now=True, editable=False, null=False, blank=False)

    class Meta:
        db_table = 'mst_fiscal_years'
        ordering = ['display_order']


class NepaliMonth(BaseModel):
    class Meta:
        db_table = 'mst_nepali_months'


class Gender(BaseModel):
    class Meta:
        db_table = 'mst_genders'


class AppClient(BaseModel):
    province = models.ForeignKey(
        Province, on_delete=models.CASCADE,null=True,blank=True)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE,null=True,blank=True)
    local_level = models.ForeignKey(
        LocalLevel, on_delete=models.CASCADE,null=True,blank=True)
    admin_email = models.EmailField(max_length=100)
    is_active = models.BooleanField(default=False, null=True)
    url_1 = models.CharField(max_length=100)
    url_2 = models.CharField(max_length=100)
    remarks = models.CharField(max_length=200,null=True,blank=True)

    class Meta:
        db_table = 'app_clients'

def property_image_upload_to(instance, filename):
    return 'client-%s/property_image/%s' % (instance.client.id,filename)
class Property(BaseModel):
    client = models.ForeignKey(
        AppClient, on_delete=models.CASCADE,null=True)
    parent = models.ForeignKey('self',related_name='children', related_query_name='child',on_delete=models.CASCADE,null=True,blank=True)
    province = models.ForeignKey(
        Province, on_delete=models.CASCADE,null=True,blank=True)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE,null=True,blank=True)
    local_level = models.ForeignKey(
        LocalLevel, on_delete=models.CASCADE,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    block_no = models.CharField(max_length=16,null=True,blank=True)
    floor_no = models.CharField(max_length=16,null=True,blank=True)
    flat_no = models.CharField(max_length=16,null=True,blank=True)
    room_no = models.CharField(max_length=16,null=True,blank=True)
    total_area = models.CharField(max_length=16,null=True,blank=True)
    own_porperty = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=16, decimal_places=2)
    is_active = models.BooleanField(default=True)
    photo = models.ImageField(null=True,blank=True,upload_to=property_image_upload_to,default = 'customers/nopp.jpg')
    remarks = models.CharField(max_length=200)
    class Meta:
        db_table = 'properties'

def customer_image_upload_to(instance, filename):
    return 'client-%s/customers/%s' % (instance.client.id,filename)
class Customer(BaseModel):
    client = models.ForeignKey(
        AppClient, on_delete=models.CASCADE,null=True,blank=True)
    province = models.ForeignKey(
        Province, on_delete=models.CASCADE,null=True,blank=True)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE,null=True,blank=True)
    local_level = models.ForeignKey(
        LocalLevel, on_delete=models.CASCADE,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    contact = models.CharField(max_length=10)
    secondary_contact = models.CharField(max_length=10)
    email = models.EmailField()
    photo = models.ImageField(null=True,blank=True,upload_to=customer_image_upload_to,default = 'customers/nopp.jpg')
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = 'customers'
        unique_together = ('client', 'email')
class BillingCycle(BaseModel):
    days_count = models.IntegerField()
    class Meta:
        db_table = 'billing_cycles'

def owner_image_upload_to(instance, filename):
    return 'client-%s/owners/%s' % (instance.client.id,filename)
class Owner(BaseModel):
    client = models.ForeignKey(
        AppClient, on_delete=models.CASCADE,null=True,blank=True)
    province = models.ForeignKey(
        Province, on_delete=models.CASCADE,null=True,blank=True)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE,null=True,blank=True)
    local_level = models.ForeignKey(
        LocalLevel, on_delete=models.CASCADE,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    contact = models.CharField(max_length=10)
    secondary_contact = models.CharField(max_length=10)
    email = models.EmailField()
    photo = models.ImageField(null=True,blank=True,upload_to=owner_image_upload_to,default = 'customers/nopp.jpg')
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = 'owners'
        unique_together = ('client', 'email')

def contract_file_upload_to(instance, filename):
    return 'client-%s/contracts/%s' % (instance.client.id,filename)
class Contract(BaseModel):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE,null=True,blank=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE,null=True,blank=True)
    owner = models.ForeignKey(
        Owner, on_delete=models.CASCADE,null=True,blank=True)
    billing_cycle = models.ForeignKey(
        BillingCycle, on_delete=models.CASCADE,null=True,blank=True)
    contract_file = models.FileField(null=True,blank=True,upload_to=contract_file_upload_to,default = 'customers/nopp.jpg')
    date_from = models.DateField()
    date_to = models.DateField()
    rent_amount = models.DecimalField(max_digits=16, decimal_places=2)
    increment_year = models.IntegerField()
    increment_rate = models.DecimalField(max_digits=16, decimal_places=2)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = 'contracts'

def sub_property_file_upload_to(instance, filename):
    return 'client-%s/contracts/contract-%s/%s' % (instance.client.id,instance.contract.id,filename)
class SubProperty(BaseModel):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE,null=True,blank=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE,null=True,blank=True)
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE,null=True,blank=True)
    block_no = models.CharField(max_length=16,null=True,blank=True)
    floor_no = models.CharField(max_length=16,null=True,blank=True)
    flat_no = models.CharField(max_length=16,null=True,blank=True)
    room_no = models.CharField(max_length=16,null=True,blank=True)
    total_area = models.CharField(max_length=16,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    remarks = models.CharField(max_length=200)
    file = models.FileField(null=True,blank=True,upload_to=sub_property_file_upload_to,default = 'customers/nopp.jpg')
    class Meta:
        db_table = 'sub_properties'

def end_user_image_upload_to(instance, filename):
    return 'client-%s/customers/customer-%s/end_users/%s' % (instance.client.id,instance.customer.id,filename)
class EndUser(BaseModel):
    client = models.ForeignKey(
        AppClient, on_delete=models.CASCADE,null=True,blank=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE,null=True,blank=True)
    sub_property = models.ForeignKey(
        SubProperty, on_delete=models.CASCADE,null=True,blank=True)
    province = models.ForeignKey(
        Province, on_delete=models.CASCADE,null=True,blank=True)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE,null=True,blank=True)
    local_level = models.ForeignKey(
        LocalLevel, on_delete=models.CASCADE,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    contact = models.CharField(max_length=10)
    secondary_contact = models.CharField(max_length=10)
    email = models.EmailField()
    photo = models.ImageField(null=True,blank=True,upload_to=end_user_image_upload_to,default = 'customers/nopp.jpg')
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = 'end_users'
        unique_together = ('sub_property', 'email')


def third_party_file_upload_to(instance, filename):
    return 'client-%s/contracts/contract-%s/%s' % (instance.client.id,instance.contract.id,filename)
class ThirdParty(BaseModel):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE,null=True,blank=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE,null=True,blank=True)
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE,null=True,blank=True)

    block_no = models.CharField(max_length=16,null=True,blank=True)
    floor_no = models.CharField(max_length=16,null=True,blank=True)
    flat_no = models.CharField(max_length=16,null=True,blank=True)
    room_no = models.CharField(max_length=16,null=True,blank=True)
    total_area = models.CharField(max_length=16,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    remarks = models.CharField(max_length=200)
    file = models.FileField(null=True,blank=True,upload_to=sub_property_file_upload_to,default = 'customers/nopp.jpg')
    class Meta:
        db_table = 'third_party'