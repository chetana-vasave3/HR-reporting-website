from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from openpyxl import load_workbook
from django.http import HttpResponse
import os
from django.conf import settings
from openpyxl import load_workbook
from django.http import HttpResponseRedirect,HttpResponse
from .models import Telecaller
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
import json


excel_path = os.path.join(settings.MEDIA_ROOT, 'scheduled_interview.xlsx')
def dashboard(request):
    return render(request, 'dashboard.html')
def recruitment(request):
    return render(request, 'recruitments.html')
def job_posts(request):
    return render(request, 'job_posts.html')
def dashboard(request):
    return render(request, 'dashboard.html')
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')
from django.http import JsonResponse
from .models import Telecaller,Counselor,Schedule ,RolledOutStatus 
from django.views.decorators.csrf import csrf_exempt

from .serializers import TelecallerSerializer
    
def telecaller_data(request):
    data = list(Telecaller.objects.values())
    return JsonResponse(data, safe=False)
def counselor_list(request):
    data = list(Counselor.objects.values())  # spelling should match your model
    return JsonResponse(data, safe=False)

def get_candidate_by_id(request, role, id):
    candidate = get_object_or_404(Telecaller, id=id, role__iexact=role)
    data = {
        "id": candidate.id,
        "name": candidate.name,
        "contact": candidate.contact,
        "mail_id": candidate.mail_id,
        "gender": candidate.gender,
        "experience": candidate.experience,
        "role": candidate.role
    }
    return JsonResponse(data)


def candidate_detail(request, role, id):
    model_map = {
        'telecaller': Telecaller,
        'counselor': Counselor,
       
    }

    model = model_map.get(role.lower())

    if not model:
        return render(request, '404.html')  # or raise Http404

    candidate = get_object_or_404(model, id=id)

    return render(request, 'candidate.html', {'candidate': candidate, 'role': role.capitalize()})
from django.contrib.contenttypes.models import ContentType

# def schedule_candidate(request, role, id):
#     try:
#         model = ContentType.objects.get(model=role.lower()).model_class()
#     except ContentType.DoesNotExist:
#         return HttpResponse("Invalid role", status=400)

#     candidate = get_object_or_404(model, id=id)

#     if request.method == 'POST':
#         scheduled_on = request.POST.get('schedule')
#         remark = request.POST.get('remark')

#         Schedule.objects.create(
#             content_type=ContentType.objects.get_for_model(candidate),
#             object_id=candidate.id,
#             scheduled_on=scheduled_on,
#             remark=remark
#         )

#         return redirect('success')

#     return render(request, 'your_template.html', {
#         'candidate': candidate,
#         'role': role.capitalize()
#     })
def success_page(request):
    return render(request, 'success.html', {'message': 'Interview scheduled successfully!'})

ROLE_MODELS = {
    'telecaller': Telecaller,
    'counselor': Counselor,
    
}

def candidate_schedule(request, role, id):
    role = role.lower()
    model = ROLE_MODELS.get(role)

    if not model:
        return HttpResponse("Invalid role.", status=400)

    candidate = get_object_or_404(model, id=id)
    content_type = ContentType.objects.get_for_model(model)

    if request.method == 'POST':
        scheduled_on = request.POST.get('schedule')
        remark = request.POST.get('remark')

        Schedule.objects.create(
            content_type=content_type,
            object_id=candidate.id,
            scheduled_on=scheduled_on,
            remark=remark
        )
        return redirect('success')  # or render a thank you message

    schedules = Schedule.objects.filter(content_type=content_type, object_id=id).order_by('-scheduled_on')

    return render(request, 'scheduledinterview.html', {
        'candidate': candidate,
        'schedules': schedules,
        'role': role.capitalize()
    })

def telecaller_schedule_data(request):
    telecaller_type = ContentType.objects.get_for_model(Telecaller)
    schedules = Schedule.objects.filter(content_type=telecaller_type)

    data = []
    for schedule in schedules:
        candidate = schedule.candidate
        data.append({
            'Name': candidate.name,
            'Contact': candidate.contact,
            'Mail ID': candidate.mail_id,
            'Gender': candidate.gender,
            'Experience': candidate.experience,
            'Date': schedule.scheduled_on.strftime("%Y-%m-%d %H:%M"),
            'Remarks': schedule.remark,
        })

    return JsonResponse(data, safe=False)
def scheduled_interviews(request):
    schedules = Schedule.objects.all()
    return render(request, 'scheduledinterview.html', {'schedules': schedules})
@csrf_exempt
def update_status(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            status = data.get('status')
            remark = data.get('remark', '')

            print(f"Received data: {data}")

            schedule = Schedule.objects.get(id=id)

            # Update Schedule model
            schedule.status = status
            schedule.remark = remark
            schedule.save()

            # Save or update RolledOutStatus for all statuses
            rolled_out, created = RolledOutStatus.objects.get_or_create(
                content_type=schedule.content_type,
                object_id=schedule.object_id
            )
            rolled_out.status = status
            rolled_out.remark = remark
            rolled_out.save()

            return JsonResponse({"success": True, "updated_status": status})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Schedule.DoesNotExist:
            return JsonResponse({"error": "Schedule not found"}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def offeres_roled_out(request, role):
    # Filter based on the role
    if role.lower() not in ['telecaller', 'counselor', 'trainer', 'hr']:
        return JsonResponse({"error": "Invalid role"}, status=400)

    # Get the schedules for the given role
    schedules = RolledOutStatus.objects.filter(content_type__model=role.lower())

    data = []
    for schedule in schedules:
        candidate = schedule.content_object  # Assuming content_object is the candidate object
        data.append({
            "candidate_name": candidate.name,
            "date": schedule.scheduled_on.strftime("%Y-%m-%d"),
            "time": schedule.scheduled_on.strftime("%H:%M"),
            "remark": schedule.remark,
        })

    return JsonResponse(data, safe=False)
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import Schedule, Telecaller, Counselor  # Import your models

# def get_scheduled_interviews(request, role):
#     model_map = {
#         "telecaller": Telecaller,
#         "counselor": Counselor,
#         # Add other roles here...
#     }

#     model = model_map.get(role.lower())
#     if not model:
#         return JsonResponse({"error": "Invalid role"}, status=400)

#     content_type = ContentType.objects.get_for_model(model)
#     schedules = Schedule.objects.filter(content_type=content_type)

#     data = []
#     for schedule in schedules:
#         candidate = schedule.candidate
#         data.append({
#             "id": schedule.id,  # ✅ Include ID for frontend use
#             "candidate_name": candidate.name,
#             "contact": candidate.contact,
#             "mail_id": candidate.mail_id,
#             "gender": candidate.gender,
#             "experience": candidate.experience,
#             "date": schedule.scheduled_on.strftime("%Y-%m-%d"),  # date part
#             "time": schedule.scheduled_on.strftime("%I:%M %p"),  # time part
#             "status": getattr(schedule, 'status', None),  # Optional: include status if stored here
#             "remark": schedule.remark,
#         })

#     return JsonResponse(data, safe=False)
def get_scheduled_interviews(request, role):
    model_map = {
        "telecaller": Telecaller,
        "counselor": Counselor,
        
        # Add any other roles here
    }

    model = model_map.get(role.lower())
    if not model:
        return JsonResponse({"error": "Invalid role"}, status=400)

    content_type = ContentType.objects.get_for_model(model)
    schedules = Schedule.objects.filter(content_type=content_type)

    data = []
    for schedule in schedules:
        candidate = schedule.candidate

        # Get status and remark from RolledOutStatus if exists
        try:
            rollout = RolledOutStatus.objects.get(
                content_type=schedule.content_type,
                object_id=schedule.object_id
            )
            status = rollout.status
            remark = rollout.remark
        except RolledOutStatus.DoesNotExist:
            status = "Not Set"
            remark = ""

        data.append({
            "id": schedule.id,  # Important for updateStatus
            "candidate_name": candidate.name,
            "contact": candidate.contact,
            "mail_id": candidate.mail_id,
            "gender": candidate.gender,
            "experience": candidate.experience,
            "date": schedule.scheduled_on.strftime("%Y-%m-%d"),
            "time": schedule.scheduled_on.strftime("%H:%M"),
            "remark": remark,
            "status": status,
        })

    return JsonResponse(data, safe=False)

