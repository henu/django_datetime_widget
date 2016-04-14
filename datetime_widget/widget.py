from django.forms.utils import flatatt
from django.forms.widgets import Widget
from django.utils.html import format_html

from datetime import datetime


class DatetimeWidget(Widget):

    def __init__(self, *args, **kwargs):
        self.datetime_format = kwargs.pop('format', '%c')
        super(DatetimeWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if not value:
            value = ''
        if isinstance(value, datetime):
            value = value.strftime(self.datetime_format)

        final_attrs = self.build_attrs(
            attrs,
            type="text",
            name=name,
            value=value,
        )
        return format_html('<input{} readonly />', flatatt(final_attrs))

    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)

        # Convert text value to datetime object.
        # If conversion fails, then string data is suitable. It gives error and can be edited by user.
        if value:
            try:
                value = datetime.strptime(value, self.datetime_format)
            except ValueError:
                pass

        return value
