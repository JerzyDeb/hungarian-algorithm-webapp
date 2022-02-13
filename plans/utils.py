import decimal
import string

import numpy as np

from django.contrib import messages

from datetime import datetime

from items.models import Worker
from items.models import Task
from items.models import Execution
from plans.models import Plan
from teams.models import Team

from items.utils import create_task
from items.utils import create_worker
from project.utils import render_to_pdf
from project.utils import change_float_to_int


def delete_plan(plan):
    """Deletes a plan object"""

    plan = Plan.objects.get(id=plan)
    plan.delete()


def create_plan(name, team, user, is_hungarian):
    """Creates a plan object"""

    team = Team.objects.get(id=team)
    added_values = add_lost_values(team)
    workers = Worker.objects.filter(team=team)
    tasks = Task.objects.filter(team=team)
    size = workers.count()

    original_array = fill_array(workers, tasks, size)
    bool_array = original_array.copy()

    hungarian_array = hungarian(bool_array.copy(), size)
    heuristic_array = heuristic(bool_array.copy(), size)

    original_array = change_float_to_int(original_array, size)
    plan = Plan()
    if is_hungarian == 'True':
        plan.method = 'W'
        second_cost = count_cost(original_array, heuristic_array, size)
        bool_array = hungarian_array
    else:
        plan.method = 'H'
        second_cost = count_cost(original_array, hungarian_array, size)
        bool_array = heuristic_array

    plan.name = string.capwords(name)
    plan.team = team.name
    plan.createdDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {
        'is_hungarian': is_hungarian,
        'user': user,
        'cost': count_cost(original_array, bool_array, size),
        'second_cost': second_cost,
        'count': range(tasks.count()),
        'date': plan.createdDate,
        'tasks': tasks,
        'workers': workers,
        'plan': original_array,
        'plan_name': plan.name,
        'ones': bool_array,
    }
    plan.user = user
    plan.pdf.save(plan.name+'.pdf', render_to_pdf('pdf/pdf-template.html', data))

    plan.save()

    if added_values:
        delete_added_items(added_values[1], added_values[0])


def hungarian(array, size):
    """Generates a bool assign array based on hungarian algorithm"""

    array = subtract_min_value_in_rows(array, size, False)
    array = subtract_min_value_in_cols(array, size, False)
    array = delete_all_zeros(array, size, False)
    array = assign_values(array, size)

    return array


def heuristic(array, size):
    """Generates a bool assign array based on heuristic algorithm"""

    for x in range(size):
        cords = []
        min_in_row = 999999
        for row in range(size):
            for col in range(size):
                type_of = type(array[row, col])
                if (type_of == decimal.Decimal or type_of == int) and array[row, col] < min_in_row:
                    cords = [row, col]
                    min_in_row = array[row, col]
        array[cords[0], :] = False
        array[:, cords[1]] = False
        array[cords[0], cords[1]] = True

    return array


def add_lost_values(team):
    """Adds new artificial tasks/workers if no. tasks and no. workers are not equal"""

    workers = Worker.objects.filter(team=team)
    tasks = Task.objects.filter(team=team)
    added_values = {}
    if tasks.count() > workers.count():
        add_workers = True
        added_values[add_workers] = fill_workers([], tasks.count() - workers.count(), team)
        [(k, v)] = added_values.items()
        return [k, v]
    if workers.count() > tasks.count():
        add_workers = False
        added_values[add_workers] = fill_tasks([], workers.count() - tasks.count(), team)
        [(k, v)] = added_values.items()
        return [k, v]


def fill_tasks(added, diff, team):
    """Runs function to create new artificial tasks 'diff' times"""

    for i in range(diff):
        added.append(create_task('Zadanie Uzupełniające', team, True))
    return added


def fill_workers(added, diff, team):
    """Runs function to create new artificial workers 'diff' times"""

    for i in range(diff):
        added.append(create_worker('Pracownik', 'Uzupełniający', team, True))
    return added


def delete_added_items(added, are_workers):
    """Deletes added artificial workers/tasks"""
    """are_workers - true if we have to delete added artificial workers"""

    for pk in added:
        if are_workers:
            Worker.objects.get(id=pk).delete()
        else:
            Task.objects.get(id=pk).delete()


def fill_array(workers, tasks, size):
    """Creates a 2D array based on executions"""

    array = np.empty((0, size), object)
    for worker in workers:
        row = []
        for task in tasks:
            row.append(Execution.objects.get(task=task, worker=worker).time)
        array = np.append(array, np.array([row]), axis=0)
    return array


def delete_all_zeros(array, size, show_steps):
    """Marks all zeros by fewest number of lines"""
    """show_steps - if True, function returns every generate values and arrays"""
    """show_steps - if False, function returns only final array"""

    all_deleted_rows = []
    all_deleted_cols = []
    all_number_of_lines = []
    all_minimum_values = []
    arrays = []
    count = 0

    number_of_lines = 0
    while number_of_lines != size:
        arrays.append(array.copy())
        bool_cost_array = array == 0

        marked_zeros = mark_zeros(bool_cost_array.copy(), size)

        marked_rows = []
        for marked_zero in marked_zeros:
            marked_rows.append(marked_zero[0])

        non_marked_rows = []
        for row_number in range(size):
            if row_number not in marked_rows:
                non_marked_rows.append(row_number)

        marked_cols = []
        change = True
        while change:
            change = False
            for non_marked_row in non_marked_rows:
                for col in range(size):
                    if bool_cost_array[non_marked_row, col] and col not in marked_cols:
                        marked_cols.append(col)
                        change = True

            for row, col in marked_zeros:
                if row not in non_marked_rows and col in marked_cols:
                    non_marked_rows.append(row)
                    change = True
        marked_rows = []

        for row_number in range(size):
            if row_number not in non_marked_rows:
                marked_rows.append(row_number)

        number_of_lines = len(marked_rows) + len(marked_cols)

        if number_of_lines < size:
            non_marked_values = []
            for row in range(size):
                for col in range(size):
                    if row not in marked_rows and col not in marked_cols:
                        non_marked_values.append(array[row, col])
            all_minimum_values.append(min(non_marked_values))
            array = subtract_min_value(array, marked_rows, marked_cols, min(non_marked_values), size)

        count += 1
        all_deleted_rows.append(marked_rows)
        all_deleted_cols.append(marked_cols)
        all_number_of_lines.append(number_of_lines)
    if show_steps:
        return arrays, all_deleted_rows, all_deleted_cols, count, all_number_of_lines, all_minimum_values
    return array


def assign_values(array, size):
    """Assigns tasks to workers"""

    marked_zeros = mark_zeros(array == 0, size)
    assign_array = array.copy()
    assign_array[:, :] = False
    for row, col in marked_zeros:
        assign_array[row, col] = True

    return assign_array


def mark_zeros(array, size):
    """Marks all zeros in array by min no. zeros in col/row"""

    marked_zeros = []
    number_of_zeros = np.count_nonzero(array)
    while number_of_zeros > 0:

        zeros_in_rows = count_zeros(array, size)
        zeros_in_cols = count_zeros(array.T, size)
        min_row = min(zip(zeros_in_rows.values(), zeros_in_rows.keys()))
        min_col = min(zip(zeros_in_cols.values(), zeros_in_cols.keys()))

        if min_row[0] < min_col[0]:
            for col_num in range(size):
                if array[min_row[1], col_num]:
                    array[min_row[1], :] = False
                    array[:, col_num] = False
                    marked_zeros.append([min_row[1], col_num])
                    break
        else:
            for row_num in range(size):
                if array[row_num, min_col[1]]:
                    array[row_num, :] = False
                    array[:, min_col[1]] = False
                    marked_zeros.append([row_num, min_col[1]])
                    break
        number_of_zeros = np.count_nonzero(array)

    return marked_zeros


def count_zeros(array, size):
    """Counts all zeros in each row"""

    counting_zeros = {}
    for row in range(size):
        if np.count_nonzero(array[row]) > 0:
            counting_zeros[row] = np.count_nonzero(array[row])

    return counting_zeros


def subtract_min_value_in_rows(org_array, size, show_steps):
    """Subtracts min value from each row"""
    """show_steps - if True, functions returns min value in each row"""
    """show_steps - if False, functions returns modified array"""

    min_in_rows = []
    array = org_array.copy()
    for row in range(size):
        min_in_rows.append(min(array[row]))
        array[row] = array[row] - min(array[row])
    if show_steps:
        return min_in_rows

    return array


def subtract_min_value_in_cols(org_array, size, show_steps):
    """Subtracts min value from each col"""
    """show_steps - if True, functions returns min value in each col"""
    """show_steps - if False, functions returns modified array"""

    min_in_cols = []
    array = org_array.T.copy()
    for row in range(size):
        min_in_cols.append(min(array[row]))
        array[row] = array[row] - min(array[row])
    if show_steps:
        return min_in_cols

    return array.T


def subtract_min_value(array, marked_rows, marked_cols, min_value, size):
    """Subtracts min non-marked value from other non-marked values and adds that value to double-marked values"""

    for row in range(size):
        for col in range(size):
            if row in marked_rows and col in marked_cols:
                array[row][col] = array[row][col] + min_value
            if row not in marked_rows and col not in marked_cols:
                array[row][col] = array[row][col] - min_value

    return array


def count_cost(original_array, assign_array, size):
    """Counts optimal cost"""

    cost = 0
    for row in range(size):
        for col in range(size):
            if assign_array[row, col] is True:
                cost += original_array[row, col]

    return cost


def check_plan_name(request, user, name, team, method):
    """Checks if plan with given name exists"""

    if Plan.objects.filter(user=user, name=string.capwords(name.strip())).exists():
        messages.error(request, "Istnieje już plan o takiej nazwie")
    else:
        create_plan(name,team, user, method)
