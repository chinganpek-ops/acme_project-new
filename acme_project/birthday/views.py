# birthday/views.py# birthday/views.py
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown


# Наследуем класс от встроенного ListView:
class BirthdayListView(ListView):
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # ...сортировку, которая будет применена при выводе списка объектов:
    ordering = 'id'
    # ...и даже настройки пагинации:
    paginate_by = 10
    context_object_name = 'birthdays'


class BirthdayMixin:
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayFormMixin:
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'


class BirthdayCreateView(BirthdayMixin, BirthdayFormMixin, CreateView):
    pass


class BirthdayUpdateView(BirthdayMixin, BirthdayFormMixin, CreateView):
    pass


class BirthdayDeleteView(BirthdayMixin, DeleteView):
    pass    


def birthday(request, pk=None):
    if pk is not None:
        instance = get_object_or_404(Birthday, pk=pk)
    else:
        instance = None

    form_data = request.POST if request.method == 'POST' else None
    form_files = request.FILES if request.method == 'POST' else None

    form = BirthdayForm(
        form_data,
        form_files,
        instance=instance,
    )
    context = {'form': form}

    if form.is_valid():
        saved_birthday = form.save()
        context.update({
            'birthday_countdown': calculate_birthday_countdown(
                saved_birthday.birthday,
            ),
            'first_name': saved_birthday.first_name,
            'last_name': saved_birthday.last_name,
            'record_id': saved_birthday.pk,
            'show_result': True,
        })

    return render(request, 'birthday/birthday.html', context)
