Description
===========

A datetime widget for Django. Nothing fancy, just
a simple and crude widget that should be as easy
to install as possible.

On a down side, it is bloat, because it embeds all
required Javascript everytime the Widget is needed.

Time selection is still missing.


Screenshot
==========

![](http://i.imgur.com/mm8gfwx.png)


How to use
==========

```
from datetime_widget import DatetimeWidget

class SampleForm(forms.Form):

    some_date = forms.DateTimeField(widget=DatetimeWidget())
```
