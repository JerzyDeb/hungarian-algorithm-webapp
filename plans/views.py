from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import TemplateView

from plans.models import Plan
from teams.models import Team

from plans.utils import delete_plan
from plans.utils import check_plan_name

from project.utils import get_able_teams


class PlanView(TemplateView):
    template_name = 'include/user_panel/plans.html'

    def get_context_data(self, **kwargs):
        context = super(PlanView, self).get_context_data(**kwargs)
        context['teams'] = Team.objects.filter(user=self.request.user)
        context['plans'] = Plan.objects.filter(user=self.request.user).order_by('-createdDate')
        context['able_teams'] = get_able_teams()
        return context

    def post(self, request):
        action = self.request.POST['action']

        if action == 'delete_plan':
            delete_plan(self.request.POST['id'])

        if action == 'add_plan':
            check_plan_name(request, self.request.user, self.request.POST['name'], self.request.POST['team-filter'], self.request.POST['method'])
        return HttpResponseRedirect('/panel/plans')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super(PlanView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('/accounts/login/')
