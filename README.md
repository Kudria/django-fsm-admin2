# django-fsm-admin2

[Django-fsm](https://github.com/viewflow/django-fsm) transition integration to django admin.

Passing arguments to transition is supported (unlike **django-fsm-admin** package).

## Installation

```pip install git://github.com/kudria/django-fsm-admin2.git#egg=django-fsm-admin2```

Add fsm_admin to your settings.INSTALLED_APPS
``` 
INSTALLED_APPS = [
    ...
    'fsm_admin2',
    ...
]
 ```

## Usage
Add FSMTransitionMixin to your admin class
```
# admin.py

from django.contrib import admin
from fsm_admin2.mixins import FSMTransitionMixin

class MyModelAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_fields = ['status',]    # list your fsm fields
    
    # you can override templates for transition arguments form view and transition buttons row
    fsm_transition_form_template = 'fsm_admin2/fsm_transition_form.html'         # default value
    fsm_transition_buttons_template = 'fsm_admin2/fsm_transition_buttons.html'   # default value
    ...
    
```
This will add current field value as readonly field and buttons row to perform transitions.
Only allowed transitions are displayed.

Customize transition display.

```
@transition(field=status, source='disabled', target='enabled',
            custom={'short_description': 'Activate!!!'})
def activate(self):
    ...
```

Add form to provide transition arguments. Form fields names should match transition function arguments.

```
class DeactivateForm(forms.Form):
    text = forms.Charfield()

@transition(field=status, source='enabled', target='disabled',
            custom={'short_description': 'Deactivate', 'form': DeactivateForm})
def deactivate(self, text):
    ...
```

Form class can also be set as import string: ```{'form': 'my_app.forms.DeactivateForm'}```


