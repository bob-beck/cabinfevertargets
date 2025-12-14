# cabinfevertargets
Cabin Fever Challenge Targets

This is the result of my being [nerdsniped](https://xkcd.com/356/) by
a problem.

This is code to generate cabin fever challenge scaled correctly for
any distance, and printer, based upon the cabin fever challenge
division.

When fed the parameters of Division, Distance, Units of measure, and Paper,
it makes the target by spitting out pdf code to draw and fill a circle
of the correct size. 

If the division can be shot at the distance, but the target can not be printed
on the selected paper size, it tells you that. 

I have hooked this up to a web form that can generates the 2025 size targets
at [https://obtuse.com/cfc/](https://obtuse.com/cfc/), which lets you pick
the parameters on the form and make any officially shootable target.

The source code is in th the [src](src) directory if you want to
peruse the program. (You can also submit pull requests or issues if
you like.  The index of the cfc page is in
[src/form.html](src/form.html), and the cgi program source code is in
[src/cabinfevertargets.cgi](src/cabinfevertargets.cgi).
