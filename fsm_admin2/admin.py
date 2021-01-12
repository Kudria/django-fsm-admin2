from django.contrib import messages
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import path, reverse
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _
from django.http import HttpResponseBadRequest


class FSMTransitionMixin:
    """ Mixin class to use with django.admin.ModelAdmin

    Add buttons to perform transition for FSM fields listed in cls.fsm_fields.
    Buttons rendered by fsm_diaplay_FIELD method.
    """
    fsm_fields = []
    fsm_transition_form_template = 'fsm_admin2/fsm_transition_form.html'
    fsm_transition_buttons_template = 'fsm_admin2/fsm_transition_buttons.html'

    def __init_subclass__(cls, **kwargs):
        for fsm_field in cls.fsm_fields:
            setattr(cls, _get_display_func_name(fsm_field), _get_display_func(fsm_field))

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        # We need request.user to get available transitions in fsm_display_FIELD method
        self.request = request
        return super().changeform_view(request, object_id, form_url, extra_context)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj) or [])
        for fsm_field in self.fsm_fields:
            readonly_fields.append(fsm_field)
            readonly_fields.append(_get_display_func_name(fsm_field))
        return readonly_fields

    def fsm_transition_view(self, request, *args, **kwargs):
        transition_name = request.GET.get('transition')
        obj = self.get_object(request, kwargs['object_id'])
        transition_method = getattr(obj, transition_name)
        if not hasattr(transition_method, '_django_fsm'):
            return HttpResponseBadRequest(f'{transition_name} is not a transition method')
        transitions = transition_method._django_fsm.transitions
        if isinstance(transitions, dict):
            transitions = list(transitions.values())
        transition = transitions[0]

        form_class = _get_transition_form(transition)
        if form_class:
            if request.method == 'POST':
                form = form_class(request.POST)
                if form.is_valid():
                    transition_method(**form.cleaned_data)
                else:
                    return render(request,
                                  self.fsm_transition_form_template,
                                  {'transition': transition_name, 'form': form}
                                  )
            else:
                form = form_class()
                return render(request,
                              self.fsm_transition_form_template,
                              {'transition': transition_name, 'form': form}
                              )
        else:
            transition_method()

        obj.save()
        self.message_user(request,
                          _('Transition %(transition)s applied') %{'transition': _get_transition_title(transition)},
                          messages.SUCCESS,
                          )
        info = self.model._meta.app_label, self.model._meta.model_name
        return redirect('admin:%s_%s_change' % info, object_id=obj.id)

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        return [
                   path('<path:object_id>/transition/',
                        self.admin_site.admin_view(self.fsm_transition_view),
                        name='%s_%s_transition' % info),
               ] + super().get_urls()


def _get_display_func_name(fsm_field_name):
    return f'fsm_display_{fsm_field_name}'


def _reverse_object_admin_url(obj):
    info = obj._meta.model._meta.app_label, obj._meta.model._meta.model_name
    return reverse('admin:%s_%s_change' % info, kwargs={'object_id': obj.id})


def _get_transition_title(transition):
    if hasattr(transition.target, 'label'):
        return transition.target.label
    return transition.custom.get('short_description') or transition.name


def _get_transition_form(transition):
    form = transition.custom.get('form')
    if isinstance(form, str):
        form = import_string(form)
    return form


def _get_display_func(field_name):
    def display_func(self, obj=None):
        if obj is None:
            return ''
        transitions = getattr(obj, f'get_available_user_{field_name}_transitions')(self.request.user)

        info = obj._meta.model._meta.app_label, obj._meta.model._meta.model_name
        url = reverse('admin:%s_%s_transition' % info, kwargs={'object_id': obj.id})

        buttons = [{'url': f'{url}?transition={transition.name}',
                    'title': _get_transition_title(transition)}
                   for transition in transitions]
        return render_to_string(self.fsm_transition_buttons_template, {'transition_buttons': buttons})

    display_func.short_description = _('Transitions')
    return display_func
