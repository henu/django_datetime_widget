from django.forms.utils import flatatt
from django.forms.widgets import Widget
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from datetime import datetime


JAVASCRIPT_CODE = """<script>
function openDatetimePicker(input_id)
{
    var input = document.getElementById(input_id);
}
</script>"""


class DatetimeWidget(Widget):

    def __init__(self, *args, **kwargs):
        self.datetime_format = kwargs.pop('format', '%c')
        super(DatetimeWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if not value:
            value = ''
        if isinstance(value, datetime):
            value = value.strftime(self.datetime_format)

        input_id = self.attrs.get('id') or attrs.get('id')

        final_attrs = self.build_attrs(
            attrs,
            type='text',
            name=name,
            value=value,
            onclick='openDatetimePicker("' + input_id + '");'
        )
        return mark_safe(JAVASCRIPT_CODE) + format_html('<input{} readonly />', flatatt(final_attrs))

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
