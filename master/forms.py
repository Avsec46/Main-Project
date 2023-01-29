from django import forms
from .models import *
from django.utils.safestring import mark_safe


global form_labels, form_fields
form_labels = {
    'code': 'Code',
    'name_en': 'Name',
    'name_lc': 'नाम',
    'display_order': 'Display Order',
}

form_fields = ('code', 'name_en', 'name_lc', 'display_order')


class UploadFileForm(forms.Form):
    file = forms.FileField()


class ImageWidget(forms.widgets.ClearableFileInput):
    template_name = "widgets/image_widget.html"

class ProvinceForm(forms.ModelForm):

    class Meta:
        model = Province
        fields = form_fields
        labels = form_labels

    def __init__(self, *args, **kwargs):
        super(ProvinceForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

class DistrictForm(forms.ModelForm):

    class Meta:
        model = District
        fields = form_fields[:1]+('province',)+form_fields[1:]
        form_labels.update({'province': 'Province'})
        labels = form_labels

    def __init__(self, *args, **kwargs):
        super(DistrictForm, self).__init__(*args, **kwargs)
        self.fields['province'].empty_label = "Select Province"
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

class LocalLevelTypeForm(forms.ModelForm):
    class Meta:
        model = LocalLevelType
        fields = form_fields
        labels = form_labels

    def __init__(self, *args, **kwargs):
        super(LocalLevelTypeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

class LocalLevelForm(forms.ModelForm):
    class Meta:
        model = LocalLevel
        fields = form_fields[:1]+('district',
                                  'local_level_type')+form_fields[1:]
        fields = fields[:5]+('wards_count', 'gps_lat', 'gps_long')+fields[5:]

        form_labels.update({'district': 'District',
                            'local_level_type': 'Local Level Type',
                            'wards_count': 'Wards Count',
                            'gps_lat': 'GPS Latitude',
                            'gps_long': 'GPS Longitude'})
        labels = form_labels

    def __init__(self, *args, **kwargs):
        super(LocalLevelForm, self).__init__(*args, **kwargs)
        self.fields['district'].empty_label = "Select District"
        self.fields['local_level_type'].empty_label = "Select Locallevel Type"
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

class FiscalYearForm(forms.ModelForm):
    class Meta:
        model = FiscalYear
        fields = ('code', 'from_date_bs', 'from_date_ad',
                  'to_date_bs', 'to_date_ad', 'display_order')
        form_labels.update({'from_date_bs': 'From Date(B.S)',
                            'from_date_ad': 'From Date(A.D)',
                            'to_date_bs': 'To Date(B.S)',
                            'to_date_ad': 'To Date(A.D)'})
        labels = form_labels
        widgets = {
            'from_date_bs': forms.TextInput(attrs={'class': 'input-nepali-date', 'id': 'from_date_bs', 'relatedId': 'from_date_ad', 'placeholder': 'yyyy-mm-dd', 'onclick': 'fieldDateChange(this)'}),
            'to_date_bs': forms.TextInput(attrs={'class': 'input-nepali-date', 'id': 'to_date_bs', 'relatedId': 'to_date_ad', 'placeholder': 'yyyy-mm-dd', 'onclick': 'fieldDateChange(this)'}),
            'from_date_ad': forms.DateInput(attrs={'id': 'from_date_ad', 'type': 'date'}),
            'to_date_ad': forms.DateInput(attrs={'id': 'to_date_ad', 'type': 'date'})
        }
    def __init__(self, *args, **kwargs):
        super(FiscalYearForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

class NepaliMonthForm(forms.ModelForm):

    class Meta:
        model = NepaliMonth
        fields = form_fields
        labels = form_labels

    def __init__(self, *args, **kwargs):
        super(NepaliMonthForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

class GenderForm(forms.ModelForm):
    class Meta:
        model = Gender
        fields = form_fields
        labels = form_labels

    def __init__(self, *args, **kwargs):
        super(GenderForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

class AppClientForm(forms.ModelForm):
    class Meta:
        model = AppClient
        fields = form_fields[:3]+('province','district','local_level','admin_email')+form_fields[3:]
        form_labels.update({
                            'province': 'Province',
                            'district': 'District',
                            'local_level': 'Local Level',
                            'admin_email': 'Admin E-mail'})
        labels = form_labels
        widgets = {
            'district': forms.Select(attrs={'class': 'district_id', 'id': 'district_id'}),
            'local_level': forms.Select(attrs={'class': 'local_level_id', 'id': 'local_level_id'}),
        }
    def __init__(self, *args, **kwargs):
        super(AppClientForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ('client','name_en', 'name_lc','parent','province','district','local_level',
                    'address','block_no','floor_no','flat_no','room_no','total_area','price',
                    'display_order','photo','own_porperty','is_active','remarks')
        form_labels.update({
                    'client':'Client',
                    'parent':'Parent',
                    'province': 'Province',
                    'district': 'District',
                    'local_level':'Local Level',
                    'address':'Address',
                    'block_no':'Block No',
                    'floor_no':'Floor No',
                    'flat_no':'Flat No',
                    'room_no':'Room No',
                    'total_area':'Total Area',
                    'own_porperty':'Own Porperty?',
                    'price':'Price',
                    'is_active':'Is Active?',
                    'remarks': 'Remarks',
                    'photo':'Property Photo',
                })
        labels = form_labels
        widgets = {
            'district': forms.Select(attrs={'class': 'district_id', 'id': 'district_id'}),
            'local_level': forms.Select(attrs={'class': 'local_level_id', 'id': 'local_level_id'}),
            'photo' : ImageWidget,
            'remarks': forms.Textarea(attrs={'class': 'remarks', 'id': 'remarks','cols':4,'rows':3}),
        }
    def extra():
        return ('code','client','province','district','local_level','own_porperty','is_active')

    def __init__(self, *args, **kwargs):
        super(PropertyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name == 'remarks':
                visible.field.widget.attrs['col'] = 'col-md-12'
            else:
                visible.field.widget.attrs['col'] = 'col-md-4'

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('client','name_en', 'name_lc','province','district','local_level',
                        'address','contact','secondary_contact','email','photo', 'display_order')
        form_labels.update({
                    'client':'Client',
                    'province': 'Province',
                    'district': 'District',
                    'local_level':'Local Level',
                    'address':'Address',
                    'contact':'Contact',
                    'secondary_contact':'Secondary Contact',
                    'email':'Email',
                    'photo':'Profile Image'
                })
        labels = form_labels
        widgets = {
            'district': forms.Select(attrs={'class': 'district_id', 'id': 'district_id'}),
            'local_level': forms.Select(attrs={'class': 'local_level_id', 'id': 'local_level_id'}),
        }
    def extra():
        return ('code','client','province','district','local_level')

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

class BillingCycleForm(forms.ModelForm):
    class Meta:
        model = BillingCycle
        fields = ('name_en', 'name_lc','days_count','display_order')
        form_labels.update({
                    'days_count':'Cycle Days',
                })
        labels = form_labels

    def __init__(self, *args, **kwargs):
        super(BillingCycleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = '__all__'
        labels = {
            'client':'Client',
            'province':'Province',
            'district':'District',
            'local_level':'Local Level',
            'address':'Address',
            'contact':'Contact',
            'secondary_contact':'Secondary Contact',
            'email':'Email',
            'photo':'Photo',
            'is_active':'Is Active ?',
        }
    def __init__(self, *args, **kwargs):
        super(OwnerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ('customer','name_en', 'name_lc','property','billing_cycle','contract_file',
                        'date_from','date_to','rent_amount','increment_year','increment_rate','display_order')
        form_labels.update({
                    'property':'Property',
                    'customer': 'Customer',
                    'billing_cycle': 'Billing Cycle',
                    'contract_file':'Scanned Copy',
                    'date_from':'Date From',
                    'date_to':'Date To',
                    'rent_amount':'Rent Amount',
                    'increment_year':'Increment Year',
                    'increment_rate':'Increment Rate'
                })
        labels = form_labels

    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'
class SubPropertyForm(forms.ModelForm):
    class Meta:
        model = SubProperty
        fields = ('name_en', 'name_lc', 'property', 'customer', 'contract', 'block_no','floor_no','flat_no','room_no','total_area','remarks','file','display_order','is_active')
        labels = {
            'property': 'Property',
            'customer': 'Customer',
            'contract': 'Contract',
            'block_no': 'Block Nunber',
            'floor_no': 'Floor Number',
            'flat_no': 'Flat Number',
            'room_no': 'Room No',
            'total_area': 'Total Area',
            'remarks': 'Remarks',
            'file': 'File',
            'is_active': 'Is Active ?',
        }
    def __init__(self, *args, **kwargs):
        super(SubPropertyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

class ThirdPartyForm(forms.ModelForm):

    class Meta:
        model = ThirdParty
        fields = ('name_en', 'name_lc', 'property', 'customer', 'contract', 'block_no','floor_no','flat_no','room_no','total_area','remarks','file','display_order','is_active')
        labels = {
            'property': 'Property',
            'customer': 'Customer',
            'contract': 'Contract',
            'block_no': 'Block Nunber',
            'floor_no': 'Floor Number',
            'flat_no': 'Flat Number',
            'room_no': 'Room No',
            'total_area': 'Total Area',
            'remarks': 'Remarks',
            'file': 'File',
            'is_active': 'Is Active ?',
        }

    def __init__(self, *args, **kwargs):
        super(ThirdPartyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

class EndUserForm(forms.ModelForm):
    class Meta:
        model = EndUser
        fields = '__all__'
        labels = {
            'client':'Client',
            'customer':'Customer',
            'sub_property':'Sub Property',
            'province':'Province',
            'district':'District',
            'local_level':'Local Level',
            'address':'Address',
            'contact':'Contact',
            'secondary_contact':'Secondary Contact',
            'email':'Email',
            'photo':'Photo',
            'is_active':'Is Active ?',
        }
        widgets = {
            'district': forms.Select(attrs={'class': 'district_id', 'id': 'district_id'}),
            'local_level': forms.Select(attrs={'class': 'local_level_id', 'id': 'local_level_id'}),
        }
    def __init__(self, *args, **kwargs):
        super(EndUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'


# class CustomerForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         fields = form_fields[:4]+('remarks',)+form_fields[4:]
#         form_labels.update({'remarks': 'remarks'})
#         labels = form_labels


# class ComplaintTypeForm(forms.ModelForm):
#     class Meta:
#         model = ComplaintType
#         fields = form_fields[:4]+('remarks',)+form_fields[4:]
#         form_labels.update({'remarks': 'remarks'})
#         labels = form_labels


# class ComplaintSeverityForm(forms.ModelForm):
#     class Meta:
#         model = ComplaintSeverity
#         fields = form_fields[:4]+('remarks',)+form_fields[4:]
#         form_labels.update({'remarks': 'remarks'})
#         labels = form_labels


# class ComplaintDetailForm(forms.ModelForm):
#     class Meta:
#         model = ComplaintDetail
#         fields = form_fields[:1]+('complaint_detail_number',
#                                   'client', 'date_bs', 'date_ad', 'province', 'district', 'local_level', 'ward_no', 'tole', 'complaint_type', 'complaint_severity', 'complaint_description', 'file_upload', 'user',)+form_fields[4:]
#         form_labels.update({'complaint_detail_number': 'Complaint Detail Number',
#                             'client': 'Client',
#                             'date_bs': 'Date BS',
#                             'date_ad': 'Date AD',
#                             'province': 'Province',
#                             'district': 'District',
#                             'local_level': 'Local Level',
#                             'ward_no': 'Ward Number',
#                             'tole': 'Tole',
#                             'complaint_type': 'Complaint Type',
#                             'complaint_severity': 'Complaint Severity',
#                             'complaint_description': 'Complaint Description',
#                             'file_upload': 'File Upload',
#                             'user': 'User'
#                             })
#         labels = form_labels
#         widgets = {
#             'date_bs': forms.TextInput(attrs={'class': 'input-nepali-date', 'id': 'date_bs', 'relatedId': 'date_ad', 'placeholder': 'yyyy-mm-dd', 'onclick': 'fieldDateChange(this)'}),
#             'date_ad': forms.DateInput(attrs={'id': 'date_ad', 'type': 'date'}),
#         }


# class ComplaintTransferForm(forms.ModelForm):
#     class Meta:
#         model = ComplaintTransfer
#         fields = ('complaint', 'ministry',
#                   'department', 'remarks', 'is_solved')

#         labels = ({'complaint': 'Complaint',
#                             'ministry': 'Ministry',
#                             'department': 'Department',
#                             'remarks': 'Remarks',
#                             'is_solved': 'Is the problem solved ?'})