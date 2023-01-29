from django import template
from django.contrib.auth import *
from master.models import *
from django.contrib.auth.models import Group
import itertools

import sys
register = template.Library()


@register.simple_tag
def create_list(*args):
    return args

@register.filter
def check_permission(user,param):
    # check if Model is present or not
    action=param[0]
    slug=param[1]
    
    try:
        utc=underscore_to_camelcase(slug)
        model=eval(utc)
        permission = underscore_to_camelcase(slug).lower()
    except Exception as e:
        print(e)
        return False
    # check for if a user has permission (check in both directly and through group)
    # get group permission from user group
    group_permissions = Group.objects.get(name=user.groups.first()).permissions.all().values_list('codename')
    #join all tuples in single list
    user_permissions = [i for i in itertools.chain(*group_permissions)]
    #check if persmission exists
    check_perm = "%s_%s" % (action,permission)
    
    if check_perm in user_permissions:
        return True
    else:
        return False

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