#!/usr/bin/perl
# Copyright (c) 2025 Bob Beck <beck@obtuse.com>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

use warnings;
use strict;

use PDF::API2;

##################################################################
# As I have noted for many years, *when* I go to Hell for the many
# things I have done to probably deserve it, I will be perpetually
# in a room with Printers, with a healthy side dose of OpenSSL.

# Enough with wonky printerscaled images in pdf files as targets that
# we never are super sure of what's what. Surely there is a way to
# make a consistent sized circle on a page. We should be able to just
# do this by ah.. drawing a circle of the right size for the right
# distance.. (and don't call me Shirley).
#
# It would also be darn nice if the competitor stapling up the target
# at their range, and the div leaders looking at it, could have a
# visual confirmation this was the correctly scaled target for the
# division, and distance they were shooting at, and even how big we
# believe the target *should* be at that range so the shooter
# can indeed confirm their printer did not screw them before
# shooting at the target.
#
# All the shooter need know is:
# 1) What division
# 2) What distance, and what units they want to shoot at
# 3) What paper (Letter or A4) they want to print the target on.
#
# All we need to decide is the miniumum and max distance each
# division may be shot at. This allows a competitor with access
# to perhaps, a 40 yard only indoor range, to still shoot the
# CFC divisions at 40 yards with a correctly scaled target,
# which is then easily confirmed by the div leader that "yep
# they say they are shooting at 40 yards, and they are using the
# official 40 yard scaled target."
#
# Currently we only link targets for a few distances because
# the links to many static pdf files are bit of a pain, and
# hard for both us and shooters to decipher.
#
# I propose instead to replace with one "get a target" link to a web
# form that runs this underneath, enabling a shooter to shoot at *any*
# distance between our set max and minumums for the division, with a
# correctly sized target.
#
# And don't whine that it's perl, the "Talk Glock but carry a J frame"
# of the tech world.
###################################################################

# PDF natively uses a point sie of 72 per inch, so all coordinates are
# done based on that.

# Target is an 8 inch (203mm) circle at 100M, therefore a 4 inch radius
use constant R8 => (4 * 72);
# Target is an 4 inch (203mm) circle at 50M, therefore a 2 inch radius
use constant R4 => (2 * 72);

# When scaling, we convert everythig to metric.
use constant mm => 25.4 / 72;
use constant YardsPerMetre => 0.9144;

# Things to warm the hearts of old rifle nerds:
use constant ArshinPerMeter => 0.7112;
# seems the standard Austrian Value. The KuK kept the Schritt on rifle
# sights until the very end. 
use constant SchrittPerMeter => 0.7586;
# Prussian Schritt were 2 Fuss 4 Zoll - so 0.7322 meters.
# https://books.google.de/books?id=12pnAAAAcAAJ&pg=RA1-PA11#v=onepage&q&f=false
# https://books.google.de/books?id=AEkIAAAAQAAJ&pg=PA95#v=onepage&q&f=false
# This is also confusing because before unification nobody in the
# German states could agree on the length of a Fuss. This comment is
# kept here for posterity, but I think we'll just stick to a Schritt
# from Austria, since the German states went metric in the 1860's. A
# Division 4 entry with a Dreyse wanting a to shoot target in Schritt
# for cool factor can probably just treat them the same given the
# distances involved, and the lack of match grade ammunition for
# sub-MOA Dreyse shooting.

sub round($$)
{
  my ($value, $places) = @_;
  my $factor = 10**$places;
  return int($value * $factor + 0.5) / $factor;
}

# "Nonsuch" because perl arrays are 0 indexed.
my @div_name = ("Nonsuch", "Vintage", "Modern-Open", "Manual-Open",
		"Single-Shot", "Muzzleloaders", "22-Rimfire", "Manual-Irons");
my @max_dist = (1000, 100, 100, 100, 100, 50, 50, 100); # Meters
my @min_dist = (0, 25, 25, 25, 25, 25, 25, 25); # Yards
## The optimal target radius
my @target_radius = (0, R8, R8, R8, R8, R8, R4, R8); # Radius
## The distance at which the optimal target is shot
my @target_distance = (0, 100, 100, 100, 100, 50, 50, 100); # Meters
## Bullet diameter that adds to scoring area
my @bullet_dia = (0, 8/mm, 8/mm, 8/mm, 12/mm , 12/mm, 6/mm, 8/mm);
#my @bullet_dia = (0, 0, 0, 0, 0, 0, 0, 0);

# Make a Cabin Fever Challenge Target, arguments are division number,
# followed by distance, followed by units you want to shoot it at.
#
# Example:
#  makeCFCtarget(1, 100, "Metres", "A4");
#  makeCFCtarget(1, 100, "Yards", "Letter");
#  makeCFCTarget(5, 50, "Arshin", "A4");
#
# Currently this writes out a pdf file on success. Will die if the
# chosen distance is outside the min/max distances to shoot the
# Division at - Hooked up to a web form the inputs should be
# pre-validated, and units will be a selector so we don't need to
# worry about things like Metre being spelled in English instead
# of 'Murrican.
sub makeCFCtarget($$$$) {
    my ($division, $distance, $units, $paper) = @_;

    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
    $year = $year+1900;

    my $pdf  = PDF::API2->new;

    my $page = $pdf  -> page;

    # Set our page boundaries to the correct paper size.
    die "Paper must be A4 or Letter"
	unless (($paper eq "A4") | $paper eq "Letter");
    $page->boundaries(media => $paper);

    # XXX decide if we should mess with prepend or not?
    my $gfx  = $page -> graphics(-prepend=>0);
    my $txt  = $page -> text;

    my $conversion;
    if ($units eq "Metres") {
	$conversion = 1.0;
    } elsif ($units eq "Yards")  {
	$conversion = YardsPerMetre;
    } elsif ($units eq "Schritt") {
	$conversion = SchrittPerMeter;
    } elsif ($units eq "Arshin") {
	$conversion = ArshinPerMeter;
    } else {
	die "Unknown unit of measuerment: $units";
    }

    # Compute the actual shooting distance.
    my $metricdistance = round($distance * $conversion, 2);
    my $yardsdistance =  round($metricdistance / YardsPerMetre, 2);

    if ($yardsdistance < $min_dist[$division]) {
	die "$distance $units is too short a distance to shoot Division $division";
    }
    if ($metricdistance > $max_dist[$division]) {
	die "$distance $units is too far a distance to shoot Division $division";
    }


    # The scoring radius of the target at the correct distance.
    my $optimal_scoring_r = $target_radius[$division] +
	$bullet_dia[$division];

    # Scale the scoring radius of the desired distance based on the scoring
    # radius at the correct distance.
    my $scaled_scoring_r = $optimal_scoring_r *
	($metricdistance / $target_distance[$division]);

    # Now remove the bullet width from the scaled scoring radius to get a
    # correctly scaled target radius for the circle we will draw.
    my $actualsize = $scaled_scoring_r - $bullet_dia[$division];

    # Compute how big in milimeters it is supposed to be. We
    # display this right on the target for confirmation purposes.
    my $diameterinmm = round($actualsize * mm * 2.0, 0);

    # Finally, put some text on the target
    $txt->font($pdf->corefont('Helvetica Bold'), 18);
    $txt->position(5/mm, 270/mm);

    #First line is what year and Division this is for.
    $txt->text("Cabin Fever Challenge $year, Division $division (".$div_name[$division].")");
    $txt->crlf();

    # Second line is the distance in requested units, an equivalent
    # reminder distance, and the size of the target in millimeters.
    # The reminder distance for metric is in yards, for any other
    # unit of measure it is in metric. This serves as a bit of a
    # wakeup call to someone shooting a yards target at metric distance
    # and vice versa, as they are stapling it up.
    if ($units eq "Metres") {
	$txt->text("Target For Distance: $distance Metres ($yardsdistance Yards) Diameter $diameterinmm mm");
    } else {
	$txt->text("Target For Distance: $distance $units ($metricdistance Metres) Diameter $diameterinmm mm");
    }
    $txt->crlf();

    # Third line is the reminder for what paper they should be printed on.
    $txt->text("Must be printed on $paper size paper");

    # Finally, let's draw the big black circle for them to poke holes in.
    $gfx -> fillcolor('black');
    # find the centre of the page.
    my ($x1, $y1, $x2, $y2) = $page->boundaries('media');
    my $midx = ($x2 - $x1) / 2;
    my $midy = ($y2 - $y1) / 2;
    # make the circle at the centre of the page
    $gfx -> circle( $midx, $midy, $actualsize);
    $gfx -> fill;

    my $filename = "Division-$division-" .$div_name[$division]."-$distance-$units-$paper.pdf";
    $filename =~ s/ /-/g;
    $pdf -> saveas($filename);
    $pdf -> end;
}

## Just for testing - if these look ok, We
## do the work to hook up "makeCFCtarget" to a
## little web form for a competitor to generate
## their own target.
makeCFCtarget(1, 100, "Metres", "Letter");
makeCFCtarget(1, 100, "Yards", "Letter");
makeCFCtarget(2, 100, "Metres", "Letter");
makeCFCtarget(2, 100, "Yards", "Letter");
makeCFCtarget(3, 100, "Metres", "Letter");
makeCFCtarget(3, 100, "Yards", "Letter");
makeCFCtarget(4, 100, "Metres", "Letter");
makeCFCtarget(4, 100, "Yards", "Letter");
makeCFCtarget(7, 100, "Metres", "Letter");
makeCFCtarget(7, 100, "Yards", "Letter");

makeCFCtarget(1, 50, "Metres", "Letter");
makeCFCtarget(1, 50, "Yards", "Letter");
makeCFCtarget(2, 50, "Metres", "Letter");
makeCFCtarget(2, 50, "Yards", "Letter");
makeCFCtarget(3, 50, "Metres", "Letter");
makeCFCtarget(3, 50, "Yards", "Letter");
makeCFCtarget(4, 50, "Metres", "Letter");
makeCFCtarget(4, 50, "Yards", "Letter");
makeCFCtarget(5, 50, "Metres", "Letter");
makeCFCtarget(5, 50, "Yards", "Letter");
makeCFCtarget(6, 50, "Metres", "Letter");
makeCFCtarget(6, 50, "Yards", "Letter");
makeCFCtarget(7, 50, "Metres", "Letter");
makeCFCtarget(7, 50, "Yards", "Letter");

makeCFCtarget(1, 25, "Metres", "Letter");
makeCFCtarget(1, 25, "Yards", "Letter");
makeCFCtarget(2, 25, "Metres", "Letter");
makeCFCtarget(2, 25, "Yards", "Letter");
makeCFCtarget(3, 25, "Metres", "Letter");
makeCFCtarget(3, 25, "Yards", "Letter");
makeCFCtarget(4, 25, "Metres", "Letter");
makeCFCtarget(4, 25, "Yards", "Letter");
makeCFCtarget(5, 25, "Metres", "Letter");
makeCFCtarget(5, 25, "Yards", "Letter");
makeCFCtarget(6, 25, "Metres", "Letter");
makeCFCtarget(6, 25, "Yards", "Letter");
makeCFCtarget(7, 25, "Metres", "Letter");
makeCFCtarget(7, 25, "Yards", "Letter");

makeCFCtarget(5, 50, "Schritt", "Letter");
makeCFCtarget(4, 100, "Arshin", "Letter");


makeCFCtarget(1, 100, "Metres", "A4");
makeCFCtarget(1, 100, "Yards", "A4");
makeCFCtarget(2, 100, "Metres", "A4");
makeCFCtarget(2, 100, "Yards", "A4");
makeCFCtarget(3, 100, "Metres", "A4");
makeCFCtarget(3, 100, "Yards", "A4");
makeCFCtarget(4, 100, "Metres", "A4");
makeCFCtarget(4, 100, "Yards", "A4");
makeCFCtarget(7, 100, "Metres", "A4");
makeCFCtarget(7, 100, "Yards", "A4");

makeCFCtarget(1, 50, "Metres", "A4");
makeCFCtarget(1, 50, "Yards", "A4");
makeCFCtarget(2, 50, "Metres", "A4");
makeCFCtarget(2, 50, "Yards", "A4");
makeCFCtarget(3, 50, "Metres", "A4");
makeCFCtarget(3, 50, "Yards", "A4");
makeCFCtarget(4, 50, "Metres", "A4");
makeCFCtarget(4, 50, "Yards", "A4");
makeCFCtarget(5, 50, "Metres", "A4");
makeCFCtarget(5, 50, "Yards", "A4");
makeCFCtarget(6, 50, "Metres", "A4");
makeCFCtarget(6, 50, "Yards", "A4");
makeCFCtarget(7, 50, "Metres", "A4");
makeCFCtarget(7, 50, "Yards", "A4");

makeCFCtarget(1, 25, "Metres", "A4");
makeCFCtarget(1, 25, "Yards", "A4");
makeCFCtarget(2, 25, "Metres", "A4");
makeCFCtarget(2, 25, "Yards", "A4");
makeCFCtarget(3, 25, "Metres", "A4");
makeCFCtarget(3, 25, "Yards", "A4");
makeCFCtarget(4, 25, "Metres", "A4");
makeCFCtarget(4, 25, "Yards", "A4");
makeCFCtarget(5, 25, "Metres", "A4");
makeCFCtarget(5, 25, "Yards", "A4");
makeCFCtarget(6, 25, "Metres", "A4");
makeCFCtarget(6, 25, "Yards", "A4");
makeCFCtarget(7, 25, "Metres", "A4");
makeCFCtarget(7, 25, "Yards", "A4");

makeCFCtarget(5, 50, "Schritt", "A4");
makeCFCtarget(4, 100, "Arshin", "A4");
