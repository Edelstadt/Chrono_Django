from django.forms import ModelForm, ModelChoiceField

from frontend.models import Saint


class SaintForm(ModelForm):
    field1 = ModelChoiceField(queryset=Saint.objects.all(), empty_label="(Nothing)")

    class Meta:
        model = Saint
        fields = ['field1', ]

    def clean(self):
        pass

    def save(self, commit=False):
        pass
