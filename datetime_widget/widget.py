from django.forms.utils import flatatt
from django.forms.widgets import Widget
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.timezone import now

from datetime import datetime


JAVASCRIPT_CODE = """<script>
var MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

function openDatetimePicker(input_id)
{
    var input = document.getElementById(input_id);

    var picker_id = input_id + '_datetime_picker';

    var picker = document.getElementById(picker_id);
    if (picker) {
        return true;
    }

    var picker_div = document.createElement('div');
    picker_div.setAttribute('style', 'position: absolute; background-color: #fff; border: 1px solid #000;');
    picker_div.setAttribute('id', picker_id);

    // Read date information from the input
    var date_now = new Date(input.dataset['date']);
    var year_now = date_now.getFullYear();
    var month_now = date_now.getMonth() + 1;
    var day_now = date_now.getDate();

    var first_day_of_month = new Date(year_now, month_now, 1).getDay();
    if (first_day_of_month == 0) {
        first_day_of_month = 7;
    }
    var days_in_month = new Date(year_now, month_now + 1, 0).getDate();
    var days_in_last_month = new Date(year_now, month_now, 0).getDate();

    var picker_html = ''

    // Year input
    picker_html += '<div style="width: 250px; text-align: center;">';
    picker_html += '<a style="float: left; text-decoration: none;" href="#">&nbsp;&nbsp;&laquo;&nbsp;&nbsp;</a>';
    picker_html += '<span id="' + picker_id + '_year">' + year_now + '</span>';
    picker_html += '<a style="float: right; text-decoration: none;" href="#">&nbsp;&nbsp;&raquo;&nbsp;&nbsp;</a>';
    picker_html += '</div>';

    // Month input
    picker_html += '<div style="width: 250px; text-align: center;">';
    picker_html += '<a style="float: left; text-decoration: none;" href="#">&nbsp;&nbsp;&laquo;&nbsp;&nbsp;</a>';
    picker_html += '<span id="' + picker_id + '_month">' + MONTH_NAMES[month_now] + '</span>';
    picker_html += '<a style="float: right; text-decoration: none;" href="#">&nbsp;&nbsp;&raquo;&nbsp;&nbsp;</a>';
    picker_html += '</div>';

    // Grid of days
    picker_html += '<table style="width: 250px;">';
    picker_html += '<tr><td style="text-align: center;">Sun</td><td style="text-align: center;">Mon</td><td style="text-align: center;">Tue</td><td style="text-align: center;">Wed</td><td style="text-align: center;">Thu</td><td style="text-align: center;">Fri</td><td style="text-align: center;">Sat</td></tr>';
    for (var row = 0; row < 6; ++ row) {
        picker_html += '<tr>';
        for (var col = 0; col < 7; ++ col) {
            var day_of_month = row * 7 + col - first_day_of_month + 1;

            if (day_of_month < 1) {
                picker_html += '<td style="text-align: center; color: #888;">' + (day_of_month + days_in_last_month) + '</td>';
            } else if (day_of_month > days_in_month) {
                picker_html += '<td style="text-align: center; color: #888;">' + (day_of_month - days_in_month) + '</td>';
            } else if (day_of_month == day_now) {
                picker_html += '<td style="text-align: center;"><strong>' + day_of_month + '</strong></td>';
            } else {
                picker_html += '<td style="text-align: center;">' + day_of_month + '</td>';
            }

        }
        picker_html += '</tr>';
    }
    picker_html += '</table>';

    picker_div.innerHTML = picker_html;

    input.parentElement.appendChild(picker_div);
}
</script>"""


class DatetimeWidget(Widget):

    def __init__(self, *args, **kwargs):
        self.datetime_format = kwargs.pop('format', '%c')
        super(DatetimeWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if not value:
            date_isoformat = now().isoformat()
            value = ''
        if isinstance(value, datetime):
            date_isoformat = value.isoformat()
            value = value.strftime(self.datetime_format)

        input_id = self.attrs.get('id') or attrs.get('id')

        final_attrs = self.build_attrs(
            attrs,
            type='text',
            name=name,
            value=value,
            onclick='openDatetimePicker("' + input_id + '");',
        )
        return mark_safe(JAVASCRIPT_CODE) + format_html('<input{} readonly data-date="' + date_isoformat + '" />', flatatt(final_attrs))

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
