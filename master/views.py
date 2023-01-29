from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.template.defaulttags import register
from .filters import *
from .forms import *
from .models import *
import json,re
from master.templatetags.custom_tags import check_permission

from django.contrib.auth.models import Group,Permission
from authentication.models import User

global master_models
master_models = ['Province', 'District', 'LocalLevel',
                 'LocalLevelType', 'FiscalYear', 'NepaliMonth', 'Gender','ComplaintDetailForm']


@login_required(login_url="login/")
def homepage(request):
    return render(request, 'layouts/dashboard.html')


@login_required(login_url="login/")
def redirect_to_dashboard(request):
    return redirect('/master/dashboard')

def checkPermission(request,slug,action):
    # check if Model is present or not
    try:
        model=eval(underscore_to_camelcase(slug))
        permission = underscore_to_camelcase(slug).lower()
    except Exception as e:
        return False

    # check for if a user has permission (check in both directly and through group)
    if request.user.has_perm("%s.%s_%s" % (model._meta.app_label,action,permission)):
        return True
    else:
        return False

# List Operation
@login_required(login_url="login/")
def crud_list(request, slug):
    # if(check_permission(request.user,('view',slug)) is False):
    #     return render(request,"adminlte/pages/error/403page.html")

    # get model name from slug
    model = underscore_to_camelcase(slug)

    # pass page header name
    header = model
    filterFields = ''

    # check if filter class is present or not
    try:
        filterClass = eval(model+'Filter')
    except NameError:
        filterClass = ''

    if filterClass:
        filterFields = filterClass(request.GET, queryset=eval(model).objects.all())

    if model in master_models:
        upload_button = True
    else:
        upload_button = False

    # shoe filter-section only if filters are available
    hasFilter = False
    if filterFields != '' and filterFields._meta.fields:
        hasFilter = True


    context = {'header': header, 'slug': slug, 'hasFilter': hasFilter,
               'filterFields': filterFields, 'upload_button': upload_button}
    return render(request, "adminlte/pages/list.html", context)


# Render List Operation partial view
@login_required(login_url="login/")
def filter_crud_list(request, slug):

    if(check_permission(request.user,('view',slug)) is False):
        return render(request,"adminlte/pages/error/403page.html")
    modelForm = ''
    columns = ''
    labels = ''
    new_tuple = ''
    # check for filter class; if filter class is present return lists as queryset else return list
    hasFilterClass=False
    # get model name from slug
    model = underscore_to_camelcase(slug)
    # buid form from model
    try:
        modelForm = eval(model+'Form')
    except NameError:
        modelForm = ''
    # get columns name and label  for list operation
    if modelForm != '':
        columns = modelForm._meta.fields
        try :
            new_var = modelForm.extra()
        except Exception as e:
            new_var = ''

        labels = modelForm._meta.labels
    # get all data from table
    lists = eval(model).objects.all()
    # for filter
    if request.GET is not None:
        # if filter is present
        filterClass=''
        try:
            filterClass = eval(model+'Filter')
        except NameError:
            filterClass = ''

        if filterClass != '':
            lists = filterClass(request.GET, queryset=lists)
            hasFilterClass=True

    if new_var :
        original_tuple = columns
        values_to_remove = new_var
        new_tuple = tuple(x for x in original_tuple if x not in values_to_remove)
        columns = new_tuple

    context = {'columns': columns, 'labels': labels,'hasFilterClass':hasFilterClass,
               'lists': lists, 'slug': slug}
    return render(request, "adminlte/pages/partial/datatable.html", context)

# Create or Update Operation
@login_required(login_url="login/")
def crud_create_or_update(request, slug, id=0):

    model = underscore_to_camelcase(slug)
    header = re.sub(r"(\w)([A-Z])", r"\1 \2", model)

    # check if Model is present or not
    try:
        evaluated_model=eval(model)
    except Exception as e:
        return render(request,"adminlte/pages/error/403.html")

    modelForm = model+'Form'

    if request.method == "GET":
        if id == 0:
            if(checkPermission(request,slug,'add') is False):
                return render(request,"adminlte/pages/error/403.html")
            form = eval(modelForm)()
            return render(request, "adminlte/pages/partial/create.html", {'form': form, 'slug': slug,'header':header})
        else:
            if(checkPermission(request,slug,'change') is False):
                return render(request,"adminlte/pages/error/403.html")
            entity = eval(model).objects.get(pk=id)
            form = eval(modelForm)(instance=entity)
            return render(request, "adminlte/pages/partial/edit.html", {'form': form, 'slug': slug, 'entry': entity,'header':header})
    else:
        message = ''
        if id == 0:
            if(checkPermission(request,slug,'add') is False):
                return render(request,"adminlte/pages/error/403.html")
            form = eval(modelForm)(request.POST, request.FILES)
        else:
            if(checkPermission(request,slug,'change') is False):
                return render(request,"adminlte/pages/error/403.html")
            entity = eval(model).objects.get(pk=id)
            form = eval(modelForm)(request.POST, request.FILES, instance=entity)

        if form.is_valid():
            form.save(commit=False)
            form.save()

            # creating user while saving customer
            if(slug == 'customer'):
                if(id == 0):
                    form_id = form.instance.id
                    create_user(form_id,request)

            if id == 0:
                message = 'The item has been added successfully !'
            else:
                message = 'The item has been modified successfully !'
        else:
            print('form errors')

        return JsonResponse({'message': message, 'slug': slug})

@login_required(login_url="login/")
def crud_delete(request, slug, id):
    if(checkPermission(request,slug,'delete') is False):
        return render(request,"adminlte/pages/error/403.html")
    model = underscore_to_camelcase(slug)
    entity = eval(model).objects.get(pk=id)
    delete_status = entity.delete()
    if(delete_status):
        status = 'success'
        value = 1
    else:
        status = 'error'
        value = 0
    return JsonResponse({'status': status, 'value': value, 'slug': slug})

# file upload


def upload(request, slug):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            model = underscore_to_camelcase(slug)

            if(eval(model).objects.count() > 0):

                return redirect('/master/'+slug+'/list')
            else:
                upload_file = request.FILES['file']
                json_data = json.load(upload_file)

                for row in json_data:
                    # check for foreign key and init model instance if exits
                    row = check_for_foreign_key(row, slug)

                    eval(model).objects.create(**row)
            return redirect('/master/'+slug+'/list')
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()

    context = {'slug': slug}
    return render(request, 'adminlte/pages/partial/upload.html', context)


def underscore_to_camelcase(value):
    output = ""
    first_word_passed = False
    for word in value.split("_"):
        if not word:
            output += "_"
            continue
        if first_word_passed:
            output += word.capitalize()
        else:
            output += word.capitalize()
        first_word_passed = True
    return output


# foreign key check

def check_for_foreign_key(row, slug):
    if slug == 'district':
        row['province'] = Province.objects.get(pk=row['province_id'])

    if slug == "local_level":
        row['district'] = District.objects.get(pk=row['district_id'])
        row['local_level_type'] = LocalLevelType.objects.get(
            pk=row['local_level_type_id'])
        row['display_order'] = 0

    return row

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter
def has_permission(request,action, slug):
    try:
        model=eval(underscore_to_camelcase(slug))
        permission = underscore_to_camelcase(slug).lower()
    except Exception as e:
        return False

    # check for if a user has permission (check in both directly and through group)
    if request.user.has_perm("%s.%s_%s" % (model._meta.app_label,action,permission)):
        return True
    else:
        return False

# for getting column label
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# for getting value from db using column key
@register.filter
def get_item_value(item, column):
    value = 'item.'+column
    return eval(value)

## get districts
def get_districts(request,province_id):
    districts = District.objects.filter(province_id=province_id).values('id','name_en')
    districts =list(districts)
    return JsonResponse(districts,safe=False)

## get_local_levels
def get_local_levels(request,district_id):
    local_levels = LocalLevel.objects.filter(district_id=district_id).values('id','name_en')
    local_levels =list(local_levels)
    return JsonResponse(local_levels,safe=False)

def get_district_locallevel(request,entry_id):
    # print(request)
    result = Property.objects.filter(pk=entry_id).values('district_id','local_level_id')
    result =list(result)
    return JsonResponse(result,safe=False)

def create_user(form_id,request):
    username=request.POST.get('name_en')
    email=request.POST.get('email')
    customer_id = form_id
    app_client_id = int(request.POST.get('client'))
    customer_user = User.objects.create_user(username=username, password='User@1234',email=email,is_staff=False,is_superuser=False,customer_id=customer_id,app_client_id=app_client_id)
    my_group = Group.objects.get(name='Customer')
    my_group.user_set.add(customer_user)
    return True

    formEntity = ''
    imgForm = ''

    if id == 0:
        try :
            imgForm = eval(imageForm)()
        except Exception as E:
            imgForm = ''
    else:
        try :
            imgForm = eval(imageForm)()
            try:
                formEntity = eval(imageModel).objects.filter(property_id=id).all()
                try:
                    imgForm = eval(imageForm)(instance=formEntity)
                except Exception as E:
                    imgForm = imgForm

            except Exception as E:
                formEntity = ''

        except Exception as E:
            imgForm = ''

    return {'imgForm':imgForm,
            'formEntity':formEntity}