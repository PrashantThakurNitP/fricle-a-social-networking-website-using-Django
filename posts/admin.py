
"""from django.contrib import admin
from .models import feedsModel
# Register your models here.
class feedAdmin(admin.ModelAdmin):
	readonly_fields=(created,)#it says to add readonly field created to admin
admin.site.register(feedsModel)
"""


from django.contrib import admin
from .models import feedsModel,VoteModel,CommentModel

# Register your models here.
class feedAdmin(admin.ModelAdmin):
    readonly_fields=('created',)#it says to add readonly field created to admin
admin.site.register(feedsModel,feedAdmin)
admin.site.register(VoteModel)
admin.site.register(CommentModel)

