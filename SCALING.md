# Target Scaling Musings
## (AKA: Hold on while I overthink this)

When thinking about target scaling, we think about taking the size of a target, and then scaling it to be the same effective size at a different distance. So for example, if we take a 203mm target at 100 metres, and downsize it to 50 metres, we could simply downsize the target to 102mm, and the target is proportionally sized.

## The target is not the area that scores

However, when we shoot targets, generally, any hit that breaks the outer line of the target counts for score. This means that the effective area that will score is not the area of the target, but rather the area of the target **plus a ring aound the target of the diameter of the bullet being fired at it**

So in reducing the range to shoot at, if we scale a target linearly, we have a problem. *It is an advantage to shoot at a shorter distance* .

## Bullet width matters with large reductions

If we take a target:

* 203 mm at 100 metres (radius 102)
* 102 mm at 50 metres  (radius 51)
* 51 mm at 25 metres (radius 26)

If we assume (as in, let's say the case of vintage) a competitive rifle will
make an approximately 8mm hole. The radius of the scoring area changes:

At 100 metres the scoring radius is 110 mm (Scoring area .038 m2)

However with the target area changing but the bullet width staying constant the scoring gets effectively bigger at shorter distances:

* At 50 it is 59 mm - equivalent to a 118 mm scoring radius at 100 metres (Scoring area .044 m2 - a 15% larger scoring area than the 100 meter target)
* St 25 it is 34 mm - equivalent to a 136 mm scoring radius at 100 metres! (Scoring area .056 m2 - a 47% larger scoring area than the 100 meter target!)

We want to give shooters some flexibility, and while it might be
tempting to allow for a 15% advantage to make it easier for people to
shoot the CFC, a 47% advantage is plainly ridiculous.

The solution actually isn't that hard:

## Scale the scoring area, not the target.

To do this, we consider an actual, or typical bullet width for the division, and keep that constant,

The scoring area is scaled from the "optimal" distance, and the visible target size we print must then be the circle left over by removing the bullet width from the scaled scoring area (in this case we remove 8mm from each radius)

This turns into

* Scoring radius of 110 at 100 metres (target radius 102mm) Target diameter 203mm
* Scoring radius of 55 at 50 metres (target radius 47mm) Target diameter 94mm
* Scoring radius of 28 at 25 metres (target radius 20mm) Target diameter 40mm

This results in basically the exactly equivalent scoring area at each distance.

There is still a maximum distance, in that we can not really print much larger than a 203mm diameter target on A4 or letter paper.

There is still a ridiculous minimum distance, With the above example somewhere
around 7 metres we have a scoring radius of less than an 8mm bullet width, so we won't have any visible target left to print.

A more practical minimum distance is "how many bullet strikes can we put in this and still score the target" - A rough estimate is actually to "fill" the target with the area the bullet, for the number of shots. Some quick experimenting seems to indicate a good cutoff appears to take the area of the hole made by the expected size of the bullet, and multiply this by 2 times the number of rounds to be fired at the target. If this is larger than the visible area of the target, it becomes challenging to score. As noticed by a CFC submittter, if we have this situation and still want to shoot a small target, we can just shoot more targets with fewer rounds (i.e. one target per each position, or one target per round).

Needless to say, the target size, minimum distance, etc. just becomes a mathmatical formula, and could generate a target for any distance over the minimum, allowing for things like a 40 meter range, 75 yard range, etc, with a no significant advantage to the shooter.

## Could this be used this in CFC?

This would be completely bonkers and infeasable if we were pre-generating the PDF targets. We'd have way too many files to sort through.

However if we switch to a model where the user *generates* the non-standard
targets - its easy to deal with, and easy to confirm looking at the target that
has the division, intended distance and size of the target in millimetres printed right on the target.

To use this in CFC we could decide to:

1) Use a "typical" bullet diameter for a competitive rifle in the class (The samples here use 6mm for div 6, 8mm for div 1, 2, 3, 7, and 12mm for div 4 and 5)

Or if we felt like asking the shooter for one more thing when they generate their target:

2) Ask the shooter for the bullet diameter on the web form to make the target and use that.

Something makes me think 1) is enough.

















