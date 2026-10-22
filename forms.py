from django import forms
from .models import Demand

class DemandForm(forms.ModelForm):
    class Meta:
        model = Demand
        fields = ["project", "title", "description", "kind", "priority", "status", "owner", "due_date"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        projects = self.fields["project"].queryset.filter(status="active")
        if user and not user.is_staff:
            projects = projects.filter(members=user)
        self.fields["project"].queryset = projects
        self.fields["owner"].queryset = self.fields["owner"].queryset.filter(is_active=True)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
