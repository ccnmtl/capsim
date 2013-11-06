from django import forms


class RunForm(forms.Form):
    ticks = forms.IntegerField(
        initial=100,
        label="How many ticks?")
    number_agents = forms.IntegerField(
        initial=100,
        label="How many agents?")
