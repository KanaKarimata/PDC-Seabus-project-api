from django.contrib import admin

from .models import OperationRule, OperationStatus, OperationStatusDetail, TimeScheduleDetail, TimeSchedule, EditPermission, UserEditPermission

admin.site.register(OperationRule)
admin.site.register(OperationStatus)
admin.site.register(OperationStatusDetail)
admin.site.register(TimeScheduleDetail)
admin.site.register(TimeSchedule)
admin.site.register(EditPermission)
admin.site.register(UserEditPermission)
