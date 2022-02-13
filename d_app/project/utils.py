import os

from io import BytesIO

from project import settings

from django.core.files.base import ContentFile
from django.template.loader import get_template
from xhtml2pdf import pisa

from items.models import Worker
from items.models import Task
from items.models import Execution
from items.models import Team
from plans.models import Plan


def change_context(user, team):
    """Changes context after create new team or filter by team"""

    context = {
        'teams': Team.objects.filter(user=user),
        'actual_team': team,
        'able_teams': get_able_teams(),
        'workers': Worker.objects.filter(team=team),
        'tasks': Task.objects.filter(team=team),
        'plans': Plan.objects.filter(user=user),
        'executions': Execution.objects.filter(),
    }

    return context


def get_able_teams():
    """Gets able teams to create plan (able team must have one or more tasks and workers)"""

    workers_teams = []
    tasks_teams = []
    able_teams = []

    for worker in Worker.objects.filter():
        workers_teams.append(worker.team)

    for task in Task.objects.filter():
        tasks_teams.append(task.team)

    for team in Team.objects.filter():
        if team in workers_teams and team in tasks_teams:
            able_teams.append(team)

    return able_teams


def change_float_to_int(array, size):
    """Changes float values to int: 0,00 -> 0"""

    for row in range(size):
        for col in range(size):
            if float(array[row, col]).is_integer():
                array[row, col] = int(array[row, col])

    return array


def fetch_pdf_resources(uri, rel):
    """Gets a pdf resource"""

    if uri.find(settings.MEDIA_URL) != -1:
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
    elif uri.find(settings.STATIC_URL) != -1:
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ''))
    else:
        path = None
    return path


def render_to_pdf(template_src, context_dict={}):
    """Renders html to pdf"""

    template = get_template(template_src)
    html = template.render(context_dict)

    result = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(html.encode('UTF-8')), result, encoding='utf-8', link_callback=fetch_pdf_resources)
    if not pdf.err:
        return ContentFile(result.getvalue())
    return None
