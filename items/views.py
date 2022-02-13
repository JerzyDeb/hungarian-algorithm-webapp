import string

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib import messages

from teams.models import Team
from items.models import Worker
from items.models import Task
from items.models import Execution

from items.utils import create_worker
from items.utils import create_task
from items.utils import delete_worker
from items.utils import update_execution
from items.utils import delete_task
from items.utils import create_team
from items.utils import delete_team
from plans.utils import check_plan_name
from project.utils import change_context
from project.utils import get_able_teams


class PanelView(TemplateView):
    template_name = 'include/user_panel/teams.html'

    def get_context_data(self, **kwargs):
        context = super(PanelView, self).get_context_data(**kwargs)
        context['teams'] = Team.objects.filter(user=self.request.user)
        context['actual_team'] = context['teams'].first()
        context['able_teams'] = get_able_teams()
        context['workers'] = Worker.objects.filter(team=context['actual_team'])
        context['tasks'] = Task.objects.filter(team=context['actual_team'])
        context['executions'] = Execution.objects.filter()

        return context

    def post(self, request):
        context = None
        action = self.request.POST['action']

        if action == 'delete_worker':
            delete_worker(self.request.POST['id'])

        if action == 'delete_task':
            delete_task(self.request.POST['id'])

        if action == 'delete_team':
            delete_team(self.request.POST['id'])
            return HttpResponseRedirect('/panel/')

        if action == 'add_plan':
            check_plan_name(request, self.request.user, self.request.POST['name'], self.request.POST['team-filter'], self.request.POST['method'])
            return HttpResponseRedirect('/panel/plans')

        if action == 'add_worker':
            team = Team.objects.get(id=self.request.POST['team'])
            name = self.request.POST['name']
            surname = self.request.POST['surname']
            if Worker.objects.filter(name=string.capwords(name.strip()), surname=string.capwords(surname.strip()), team=team).exists():
                messages.error(request, "Istnieje już taki pracownik")
            else:
                create_worker(name, surname, team, False)

        if action == 'add_task':
            name = self.request.POST['name']
            team = Team.objects.get(id=self.request.POST['team'])
            if Task.objects.filter(name=string.capwords(name.strip()), team=team).exists():
                messages.error(request, "Istnieje już takie zadanie")
            else:
                create_task(name, team, False)

        if action == 'add_team':
            team = create_team(self.request.POST['name'], request.user)
            context = change_context(self.request.user, Team.objects.get(id=team.id))

        if action == 'update_execution':
            for ex in Execution.objects.filter():
                for key, value in self.request.POST.lists():
                    if str(ex.id) == key:
                        update_execution(key, request.POST.get(key, ""))

        if action == 'filter':
            context = change_context(self.request.user, Team.objects.get(id=self.request.POST['team-filter']))

        if action != 'filter' and action != 'add_team':
            context = change_context(self.request.user, Team.objects.get(id=self.request.POST['team']))

        return render(request, 'include/user_panel/teams.html', context)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super(PanelView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('/accounts/login/')
