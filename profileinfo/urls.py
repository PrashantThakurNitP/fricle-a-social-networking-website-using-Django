from django.urls import path
from .import views
from django.contrib.auth.models import User

urlpatterns = [
   # path('admin/', admin.site.urls),
   
    #Authentication
    

    #todo
    path('updateprofile/',views.updateprofile,name="updateprofile"),
    
    path('seeprofile/',views.seeprofile,name="seeprofile"),
    path('viewprofile/<int:id1>/',views.viewprofile,name="viewprofile"),
    path('sendmemessage/<int:id1>',views.sendmemessage,name="sendmemessage"),
    path('sendmessage/',views.sendmessage,name="sendmessage"),

    #path('todo/<int:todo_pk>/complete',views.completetodo,name="completetodo"),
    #path('todo/<int:todo_pk>/delete',views.deletetodo,name="deletetodo"),
]
