from django.forms.utils import flatatt
from django.forms.widgets import Widget
from django.utils.html import format_html


class DatetimeWidget(Widget):

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, type="text", name=name)
        return format_html('<input{} disabled />', flatatt(final_attrs))
