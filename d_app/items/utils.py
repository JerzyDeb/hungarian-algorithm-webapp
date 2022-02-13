import string

from items.models import Worker, Task, Execution
from teams.models import Team


def create_worker(name, surname, team, is_artificial):
    """Creates a Worker object"""
    """is_artificial - true if we have to change no. workers to be equal to no. tasks. Then return id of added worker"""

    worker = Worker()
    worker.name = string.capwords(name)
    worker.surname = string.capwords(surname)
    worker.team = team
    worker.save()
    worker_to_tasks(worker, team)

    if is_artificial:
        return worker.id


def delete_worker(worker):
    """Deletes a Worker object"""

    worker = Worker.objects.get(id=worker)
    worker.delete()


def delete_task(task):
    """Deletes a task object"""

    task = Task.objects.get(id=task)
    task.delete()


def delete_team(team):
    """Deletes a Team object"""

    team = Team.objects.get(id=team)
    team.delete()


def create_task(name, team, is_artificial):
    """Creates a Task object"""
    """is_artificial - true if we have to change no. tasks to be equal to no. workers. Then return id of added task"""

    task = Task()
    task.name = string.capwords(name)
    task.team = team
    task.save()
    task_to_workers(task, team)

    if is_artificial:
        return task.id


def create_team(name, user):
    """Creates a Team object"""

    team = Team()
    team.name = name
    team.user = user
    team.save()

    return team


def create_execution(worker, task):
    """Creates a Execution object"""

    ex = Execution()
    ex.worker = worker
    ex.task = task
    ex.time = 0
    ex.save()


def worker_to_tasks(worker, team):
    """Fills executions after add worker"""

    tasks = Task.objects.filter(team=team)
    for task in tasks:
        create_execution(worker, task)


def task_to_workers(task, team):
    """Fills executions after add task"""

    workers = Worker.objects.filter(team=team)
    for worker in workers:
        create_execution(worker, task)


def update_execution(execution, time):
    """Updates executions"""

    ex = Execution.objects.get(id=execution)
    ex.time = time
    ex.save()
