from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

   path('candidate/<str:role>/<int:id>/', views.candidate_detail, name='candidate_detail'),
   path('candidate-schedule/<str:role>/<int:id>/', views.candidate_schedule, name='candidate_schedule'),



    # path('scheduled/', views.show_interviews, name='scheduled'),
    path('recruitment/', views.recruitment, name='recruitment'),
    path('job-posts/', views.job_posts, name='job_posts'),
   path('dashboard/', views.dashboard, name='dashboard'),
#    path('afterlogin', views.afterlogin_view,name='afterlogin'),
 path('api/telecaller/', views.telecaller_data),
   path('api/counselor/', views.counselor_list),
   path('success', views.success_page,name='success'),

   path('api/telecaller-schedules/', views.telecaller_schedule_data, name='telecaller_schedules'),
   path('recruitment/scheduledinterview/', views.scheduled_interviews, name='scheduled_interview'),
   path('api/offeres_roled_out/<str:role>/', views.offeres_roled_out, name='offeres_roled_out'),
   path('api/scheduledinterviews/<str:role>/', views.get_scheduled_interviews, name='scheduled_interviews'),
   path('api/updatestatus/<int:id>/', views.update_status, name='update_status'),






# path('schedule/<str:role>/<int:id>/', views.schedule_candidate, name='schedule_candidate'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
