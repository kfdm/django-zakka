from celery import current_app
from celery.execute import send_task

from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.views.generic.base import RedirectView, TemplateView, View


class TaskForm(forms.Form):
    task = forms.CharField(label="Your name", max_length=100)


class CeleryJobs(UserPassesTestMixin, View):
    def get(self, request):
        current_app.loader.import_default_modules()
        return render(
            request, "zakka/celery/tasks.html", {"tasks": sorted(current_app.tasks)}
        )

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            messages.add_message(
                request, messages.INFO, "Running %s" % form.data["task"]
            )
            send_task(form.data["task"])
        else:
            messages.add_message(request, messages.ERROR, "Invalid %s" % form.errors)
        return self.get(request)

    def test_func(self):
        return self.request.user.is_superuser
