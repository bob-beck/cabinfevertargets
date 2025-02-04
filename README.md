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

For test sample output using the 2025 official target sizes, see the [samples](samples) directory

# Experimental Scaling

<strong> This is not official, do not use this </strong>

For a maths-y discussion of target scaling, see [SCALING.md](SCALING.md)

For current output using target scaling by scoring area accounting for bullet diameter, see the [bullet_width_scaled_samples](bullet_width_scaled_samples) directory. (This directory uses a bullet width of 8mm for div 1, 2, 3, and 7, 12 mm for div 4 and 5, and 6mm for div 6)

If you want to nerd out on target scaling and compare to the official, go for it.

There is a web form to generate the experimental targets as discussed
in [SCALING.md](SCALING.md). <string>DO NOT SHOOT THESE TARGETS FOR
THE CABIN FEVER CHALLENGE</strong> This is at
[https://obtuse.com/cfc-experimental/](https://obtuse.com/cfc-experimental/). Again,
this does *NOT* generate correct size targets, so only look at this if
you've read the SCALING doc and are curious. <em>This scheme might not ever be used</em>
