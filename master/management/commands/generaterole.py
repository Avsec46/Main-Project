from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group,Permission
from authentication.models import User
from master.models import Province
from django.core.management import call_command
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        
        if(Province.objects.count()==0):
            call_command('loaddata', 'master/seed/master.json', verbosity=0)

        super_group = Group.objects.create(name='Super Admin')
        client_group = Group.objects.create(name='Client')
        customer_group = Group.objects.create(name='Customer')

        super_permissions = Permission.objects.all()
        client_permissions = Permission.objects.filter(codename__in=[
            'view_property','add_property','change_property','delete_property',
            'view_customer','add_customer','change_customer','delete_customer',
            'view_contract','add_contract','change_contract','delete_contract',
        ])
        customer_permissions = Permission.objects.filter(codename__in=[
            'view_property',
            'view_subproperty','add_subproperty', 'change_subproperty','delete_subproperty',
            'view_contract',
        ])
        
        super_group.permissions.add(*super_permissions)
        client_group.permissions.add(*client_permissions)
        customer_group.permissions.add(*customer_permissions)

        super_user = User.objects.create_user(username='superadmin', password='111',email='super@admin.com',is_staff=True,is_superuser=True)
        client_user = User.objects.create_user(username='providentfund', password='111',email='epf@gmail.com',is_staff=False,is_superuser=False)
        customer_user = User.objects.create_user(username='sandip', password='111',email='sandip@gmail.com',is_staff=False,is_superuser=False)
        
        super_user.groups.add(super_group)
        client_user.groups.add(client_group)
        customer_user.groups.add(customer_group)