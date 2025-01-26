# Target Scaling Musings
## (AKA: Hold on while I overthink this)

When thinking about target scaling, we think about taking the size of a target, and then scaling it to be the same effective size at a different distance. So for example, if we take a 203 MM target at 100 metres, and downsize it to 50 metres, we simply downsize the target to 102MM and we have the same did at 100.  The process is simple, and close enough most of the time.

## The target is not the area that scores

However, when we shoot targets, generally, any hit that breaks the outer line of the target counts for score. This means that the effective area that will score is not the area of the target, but rather the area of the target **plus a ring of the diameter of the bullet being fired at it**

This leads us to *It is an advantage to shoot a a shorter distance* well, because it is, and it makes us uncomfortable allowing it by "too much"

## Bullet width matters with large reductions

If we take a target:

* 203 mm at 100 meters (radius 102)
* 102 mm at 50 meters  (radius 51)
* 51 mm at 25 meters (radius 26)

if we assume (as in, let's say the case of vintage) a competitive rifle will
make an approximately 8mm hole. The radius of the scoring area changes

At 100 meters the scoring radius is 110 mm (Scoring area .038 m2)

however with the target area changing but the bullet width staying constant we get

* At 50 it is 59 mm - equivalent to a 118 mm scoring radius at 100 meters (Scoring area .044 m2 - a 15% larger scoring area than the 100 meter target)
* St 25 it is 34 mm - equivalent to a 136 mm scoring radius at 100 meters! (Scoring area .056 m2 - a 47% larger scoring area than the 100 meter target!)

While it might be tempting to allow for a 15% advantage to make it easier for people to shoot, a 47% advantage seems really over the top.

The solution actually isn't that hard

## Scale the scoring area, not the target.

With this we then consider an actual, or typical bullet width for the division, and keep that constant,

The scoring area is scaled down from the "optimal" distance, and the visible target size is the cirgle left over by removing the bullet width (in this case 8mm from each radius)

This turns into

* Scoring radius of 110 at 100 meters (target radius 102mm) Target diameter 203mm
* Scoring radius of 55 at 50 meters (target radius 47mm) Target diameter 94mm
* Scoring radius of 28 at 25 meters (target radius 20mm) Target diameter 40mm

This results in basically the exactly equivalent scoring area at each distance.

There is still a maximum distance, in that we can not really print much larger than a 203mm diameter target on A4 or letter paper.

There is still a ridiculous minimum distance, With the above example somewhere
around 7 meters we have a scoring radius of less than an 8mm bullet width, so we won't have any visible target left to print.

## Can we use this in CFC?

This would be completely bonkers and infeasable if we were pre-generating the PDF targets. We'd have way too many files to sort through.

However if we switch to a model where the user *generates* the non-standard
targets - its easy to deal with, and easy to confirm looking at the target that
has the division, intended distance and size of the target in millimeters printed right on the target.

To use this in CFC we could decide to:

1) Use a "typical" bullet diameter for a competitive rifle in the class (The samples here use 6mm for div 6, 8mm for div 1, 2, 3, 7, and 12mm for div 4 and 5)

Or if we felt like asking the shooter for one more thing when they generate their target:

2) Ask the shooter for the bullet diameter and use that. (I think this might be going too far)



















