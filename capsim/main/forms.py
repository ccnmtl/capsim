from django import forms

DEFAULT_GAMMA = 1.


class RunForm(forms.Form):
    ticks = forms.IntegerField(
        initial=100,
        label="How many ticks?")
    number_agents = forms.IntegerField(
        initial=100,
        label="How many agents?")
    gamma_1 = forms.FloatField(
        initial=DEFAULT_GAMMA,
        label="Gamma 1",
        )
    gamma_2 = forms.FloatField(
        initial=DEFAULT_GAMMA,
        label="Gamma 2",
        )
    gamma_3 = forms.FloatField(
        initial=DEFAULT_GAMMA,
        label="Gamma 3",
        )
    gamma_4 = forms.FloatField(
        initial=DEFAULT_GAMMA,
        label="Gamma 4",
        )
    gamma_5 = forms.FloatField(
        initial=DEFAULT_GAMMA,
        label="Gamma 5",
        )
    gamma_6 = forms.FloatField(
        initial=DEFAULT_GAMMA,
        label="Gamma 6",
        )
