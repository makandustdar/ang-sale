from django import forms
from .models import Clue, SellOpportunity


class ClueForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Clue
        fields = ['title', 'expert', 'first_name', 'last_name', 'company', 'role', 'phone', 'mobile', 'email',
                  'website', 'address', 'company_activity_area', 'staff_count', 'source', 'rate', 'status']


class OpportunityForm(forms.ModelForm):
    sell_date = forms.DateField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = SellOpportunity
        fields = [
            'title',
            'account',
            'sell_date',
            'status',
            'sell_probability',
            'expert',
            'total_price',
            'source',
            'next_step',
            'description',
        ]