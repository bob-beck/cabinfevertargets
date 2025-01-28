# cabinfevertargets
Cabin Fever Challenge Targets

This is not real or official yet. It is just me being
[nerdsniped](https://xkcd.com/356/) by a problem.

Don't use this.

Having said that, this is currently code to generate cabin fever challenge
scaled correctly for any distance, and printer, based upon the cabin fever
challenge division.

The intent would be to hook this up to a web form we need only one link for shooters to get an official target pdf. The shooter would input what division they wanted to shoot, what distance and units of measure they wanted to shoot it at, and what paper their printer used.

Therefore If I knew I wanted to shoot Division 2, at 50 yards, and I had printer using A4 paper, I could just put in those parameters and get a pdf to print a correct target for that distance.

If the division can be shot at the distance, but the target can not be printed
on Letter or A4, well, it tells you that.

For current output using the 2025 official target sizes, see the [samples](samples) directory

# Experimental Scaling

For a maths-y discussion of target scaling, see [SCALING.md](SCALING.md)

For current output using target scaling by scoring area accounting for bullet diameter, see the [bullet_width_scaled_samples](bullet_width_scaled_samples) directory. (This directory uses a bullet width of 8mm for div 1, 2, 3, and 7, 12 mm for div 4 and 5, and 6mm for div 6)

If you want to nerd out on target scaling and compare to the official, go for it.

These are NOT the official target diameters from today, and this might not ever be used.

# There are too many files.

Don't panic.

Normally we would not keep anything like a bunch of these pregenerated files aroud, this is just for testing. Were we to use this we would make a form
for the user to say what they are shooting and generate the target pdf on
demand.

The code for the program that does this is in the [src](src) directory if you are inclined to read or fiddle with it.

I have not yet hooked this up with a web front end to let a shooter just [generate targets](src/form.html). It's not hard, but I'll do that if and when I know it generates correct stuff, and the CFC decides it actually wants to use this method, which might not be this year.



