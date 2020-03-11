from django.contrib import admin

# Register your models here.
from .models import User1
import time

# admin.site.register(User1)


@admin.register(User1)
class UserAdmin(admin.ModelAdmin):
    exclude = ['openid']  # 和inexclude 相反  不显示xx属性

    def save_model(self, request, obj, form, change):
        obj.openid = obj.nickname + str(time.time())
        return super(UserAdmin, self).save_model(request, obj, form, change)
