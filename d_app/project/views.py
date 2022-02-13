import decimal

import numpy as np

from django.http import FileResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import TemplateView

from items.models import Worker
from items.models import Task
from plans.models import Plan
from teams.models import Team

from plans.utils import add_lost_values
from plans.utils import fill_array
from plans.utils import delete_all_zeros
from plans.utils import subtract_min_value_in_rows
from plans.utils import subtract_min_value_in_cols
from plans.utils import count_cost
from plans.utils import delete_added_items
from plans.utils import assign_values
from plans.utils import heuristic
from project.utils import get_able_teams
from project.utils import change_float_to_int


def media_access(request, path):
    access_granted = False
    user = request.user
    if user.is_authenticated:
        plans = Plan.objects.filter(user=user)
        for plan in plans:
            if plan.pdf == path:
                access_granted = True

    if access_granted:
        return FileResponse(open('c:\\hungarian_algorithm_webapp\\media\\'+path, 'rb'), content_type='application/pdf')
    else:
        return HttpResponseForbidden('Nie masz dostępu do tego pliku.')


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['teams'] = Team.objects.filter(user=self.request.user)
            context['able_teams'] = get_able_teams()
        return context

    def post(self, request):
        action = self.request.POST['action']
        added_values = []
        if action == 'show-steps-for-team-values':
            team = Team.objects.get(id=self.request.POST['team-filter'])
            added_values = add_lost_values(team)
            workers = Worker.objects.filter(team=team)
            tasks = Task.objects.filter(team=team)
            size = workers.count()
            cost_array = fill_array(workers, tasks, size)
        else:
            size = int(self.request.POST['elements'])
            cost_array = np.zeros((size, size), dtype=object)
            for row in range(size):
                for col in range(size):
                    cost_array[row, col] = round(decimal.Decimal(self.request.POST['array'+str(row)+str(col)]), 2)

        cost_array = change_float_to_int(cost_array, size)

        heuristic_cost = count_cost(cost_array.copy(), heuristic(cost_array.copy(), size), size)

        cost_array_after_subtract_in_rows = subtract_min_value_in_rows(cost_array, size, False)
        cost_array_after_subtract_in_rows = change_float_to_int(cost_array_after_subtract_in_rows, size)
        min_in_rows = subtract_min_value_in_rows(cost_array, size, True)

        cost_array_after_subtract_in_cols = subtract_min_value_in_cols(cost_array_after_subtract_in_rows, size,
                                                                       False)
        cost_array_after_subtract_in_cols = change_float_to_int(cost_array_after_subtract_in_cols, size)
        min_in_cols = subtract_min_value_in_cols(cost_array_after_subtract_in_rows, size, True)

        arrays, rows, cols, count, lines, all_min = delete_all_zeros(cost_array_after_subtract_in_cols.copy(), size,
                                                                     True,)
        for array in arrays:
            array = change_float_to_int(array, size)

        new_cost_array = delete_all_zeros(cost_array_after_subtract_in_cols.copy(), size, False)
        new_cost_array = change_float_to_int(new_cost_array, size)

        bool_cost_array = assign_values(new_cost_array, size)
        cost = count_cost(cost_array, bool_cost_array, size)

        if action == 'show-steps-for-team-values':
            if added_values:
                delete_added_items(added_values[1], added_values[0])

        context = {
            'size': range(size),
            'elements': size,
            'cost_array': cost_array,
            'cost_array_after_subtract_in_rows': cost_array_after_subtract_in_rows,
            'cost_array_after_subtract_in_cols': cost_array_after_subtract_in_cols,
            'min_in_rows': min_in_rows,
            'min_in_cols': min_in_cols,
            'arrays': arrays,
            'marked_rows': rows,
            'marked_cols': cols,
            'steps': range(count),
            'numbers_of_lines': lines,
            'minimum_values': all_min,
            'bool_cost_array': bool_cost_array,
            'cost': cost,
            'new_cost_array': new_cost_array,
            'heuristic_cost': heuristic_cost,
        }
        return render(request, 'calculations.html', context)
