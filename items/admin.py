from django.contrib import admin
from .models import Worker
from .models import Task
from .models import Execution
from plans.models import Plan


admin.site.register(Worker)
admin.site.register(Task)
admin.site.register(Execution)
admin.site.register(Plan)

