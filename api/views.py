from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from api.serializers import AppClientSerializer, DistrictSerializer, LocalLevelSerializer, ProvinceSerializer, UserSerializer
from authentication.forms import SignUpForm
# from master.forms import ComplaintDetailForm
from master.models import (Province, District,
    LocalLevel, AppClient )

from django.conf import settings
from authentication.models import User



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def methodForAuthenticatedOnly(request):
    data = [
        {
            'id':request.user.id,
            'message':'welcome '+request.user.username+'you are logged in'
        }
    ]
    return Response(data)

@api_view(['POST'])
def user_register(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        message = 'New user registered successfully !!'
        status = True
        data = [
            {
                'message':message,
                'status':status,
            }
        ]
        # redirect to login view if user is registered
    else:
        message = form.errors
        status = False
        data = [
            {
                'message':message,
                'status':status,
            }
        ]
    return Response(data)

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def complainDetail(request,id=0):
    if request.method == "POST":
        if(id==0):
            form = ComplaintDetailForm(request.POST, request.FILES)
            temp_message = 'complaint registered successfully !!'
        else:
            entity = ComplaintDetail.objects.get(pk=id)
            form = ComplaintDetailForm(request.POST, request.FILES,instance=entity)
            temp_message = 'complaint updated successfully !!'

        if form.is_valid():
            form.save()
            message = temp_message
            status = True
            data = [
                {
                    'message':message,
                    'status':status,
                }
            ]
            # redirect to login view if user is registered
        else:
            message = form.errors
            status = False
            data = [
                {
                    'message':message,
                    'status':status,
                }
            ]
        return Response(data)
    else:
        app_clients = AppClient.objects.get(pk=request.user.app_client.id)
        local_level = LocalLevel.objects.get(pk=request.user.app_client.local_level.id)
        # complaint_type = ComplaintType.objects.all()
        # complain_severity = ComplaintSeverity.objects.all()
        users = User.objects.get(pk=request.user.id)
        data = [
            {
                'client':AppClientSerializer(app_clients,many=False).data,
                'local_level':LocalLevelSerializer(local_level,many=False).data,
                # 'complaint_type':ComplaintTypeSerializer(complaint_type,many=True).data,
                # 'complain_severity':ComplaintSeveritySerializer(complain_severity,many=True).data,
                'users':UserSerializer(users).data,
            }
        ]
        return Response(data)