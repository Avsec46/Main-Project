from django_filters import rest_framework as filters
from django_filters.filters import ModelChoiceFilter
from django.forms.widgets import TextInput
from .models import *
from .forms import *

form_fields = ('code', 'name_en', 'name_lc',
               'display_order', 'created_at', 'updated_at', 'file_upload')


class ProvinceFilter(filters.FilterSet):

    class Meta:
        model = Province
        exclude = form_fields


class DistrictFilter(filters.FilterSet):
    province_id = ModelChoiceFilter(label='Province', queryset=Province.objects.all(),
                                    empty_label='--select province--',
                                    widget=forms.Select(attrs={'class': 'form-control-sm filter-field', 'onchange': 'GAS.reloadList(this)'}))

    class Meta:
        model = District
        fields = ['province_id']


class LocalLevelTypeFilter(filters.FilterSet):
    class Meta:
        model = LocalLevelType
        exclude = form_fields


class LocalLevelFilter(filters.FilterSet):
    district_id = ModelChoiceFilter(label='District', queryset=District.objects.all(),
                                    empty_label='--select district--',
                                    widget=forms.Select(attrs={'class': 'form-control-sm filter-field', 'onchange': 'GAS.reloadList(this)'}))
    local_level_type_id = ModelChoiceFilter(label='Local Level Type', queryset=LocalLevelType.objects.all(),
                                            empty_label='--select local level type--',
                                            widget=forms.Select(attrs={'class': 'form-control-sm filter-field', 'onchange': 'GAS.reloadList(this)'}))

    class Meta:
        model = LocalLevel
        exclude = form_fields
        fields = ['district_id', 'local_level_type_id']


class FiscalYearFilter(filters.FilterSet):

    class Meta:
        model = FiscalYear
        exclude = form_fields


class NepaliMonthFilter(filters.FilterSet):

    class Meta:
        model = NepaliMonth
        exclude = form_fields


class GenderFilter(filters.FilterSet):
    
    class Meta:
        model = Gender
        exclude = form_fields
class AppClientFilter(filters.FilterSet):

    class Meta:
        model = AppClient
        exclude = form_fields
        

# class PropertyFilter(filters.FilterSet):

#     class Meta:
#         model = Property
#         exclude = form_fields
class BillingCycleFilter(filters.FilterSet):

    class Meta:
        model = BillingCycle
        exclude = form_fields
# class ContractFilter(filters.FilterSet):

#     class Meta:
#         model = Contract
#         exclude = form_fields

# class ContractFilter(filters.FilterSet):
#     class Meta:
#         model = Contract
#         exclude = form_fields

# class CustomerFilter(filters.FilterSet):

#     class Meta:
#         model = Customer
#         exclude = form_fields

        
# class DepartmentFilter(filters.FilterSet):

#     class Meta:
#         model = Department
#         exclude = form_fields
        
# class ComplaintTypeFilter(filters.FilterSet):

#     class Meta:
#         model = ComplaintType
#         exclude = form_fields
        
# class ComplaintSeverityFilter(filters.FilterSet):

#     class Meta:
#         model = ComplaintSeverity
#         exclude = form_fields
        
# class ComplaintDetailFilter(filters.FilterSet):

#     class Meta:
#         model = ComplaintDetail
#         exclude = form_fields
        
# class ComplaintTransferFilter(filters.FilterSet):

#     class Meta:
#         model = ComplaintTransfer
#         exclude = form_fields
       
# class SubPropertyFilter(filters.FilterSet):
#     class Meta:
#         model = SubPropertyForm
#         fields = ['property']


