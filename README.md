# cabinfevertargets
Cabin Fever Challenge Targets

This is not real or official yet. It is just me being
[nerdsniped](https://xkcd.com/356/) by a problem.

Don't use this.

Having said that, this is currently code to generate cabin fever challenge
scaled correctly for any distance, and printer, based upon the cabin fever
challenge division.

The intent would be to hook this up to a web form we need only one link for shooters to get an official target pdf. The shooter would input what division they wanted to shoot, what distance and units of measure they wanted to shoot it at, and what paper their printer used.

Therefore If I knew I wanted to shoot Division 2, at 75 yards, and I had printer using A4 paper, I could just put in those parameters and get a pdf to print a correct target for that distance.

For a maths-y discussion of target scaling, see [SCALING.md](SCALING.md)

For current output using simplistic target scaling, see the [samples](samples) directory

For current output using target scaling by scoring area accounting forbullet diameter, see the [bullet_width_scaled_samples](bullet_width_scaled_samples) directory. (This directory uses a bullet width of 8mm for div 1, 2, 3, and 7, 12 mm for div 4 and 5, and 6mm for div 6)

(normally we would not keep anything like a bunch of thesepregenerated files aroud, this is just for testing.)

The code for the program that does this is in the [src](src) directory if you are inclined to read or fiddle with it.

I have not yet hooked this up with a web front end to let a shooter just generate targets. It's not hard, but I'll do that if and when I know it generates correct stuff, and the CFC decides it actually wants to use this method, which might not be this year.



