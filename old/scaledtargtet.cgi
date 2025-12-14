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
use CGI ':standard';
use File::Slurp;

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

#######
# Helpful constants.

# PDF natively uses a point size of 72 per inch, so all coordinates are
# done based on that.
# Target is an 8 inch (203mm) circle at 100M, therefore a 4 inch radius
use constant R8 => (4 * 72);
# Target is an 4 inch (102mm) circle at 50M, therefore a 2 inch radius
use constant R4 => (2 * 72);
# Target is a 2 inch (51 mm) circle at 25M - therefore a one inch radius
use constant R2 => (1 * 72);

# When scaling, we convert everythig to metric.
use constant mm => 25.4 / 72;
use constant YardsPerMetre => 0.9144;

# Things to warm the hearts of old rifle nerds which we may or may
# not choose to use.
use constant ArshinPerMeter => 0.7112;
# seems the standard Austrian Value. The KuK kept the Schritt on rifle
# sights until the very end. 
use constant SchrittPerMeter => 0.7586;
# Prussian Schritt were 2 Fuss 4 Zoll - so 0.7322 metres.
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

######
# Round a number.
sub round($$)
{
  my ($value, $places) = @_;
  my $factor = 10**$places;
  return int($value * $factor + 0.5) / $factor;
}


#####
# Convert a distance in $units to $to_units;
sub convert_distance($$$) {
    my ($distance, $units, $to_units) = @_;

    die if ($to_units ne "Yards") && ($to_units ne "Metres");

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

    my $metricdistance =  round($distance * $conversion, 2);
    if ($to_units eq "Yards") {
	return round($metricdistance / YardsPerMetre, 2);
    }
    return $metricdistance;
}

#####
# Return a scaled target radius, in points, given a division,
# distance, and units.  Absolutely not the official 2025 values - we
# can ponder this for possible future use.
sub Scaled_radius($$$)
{
    my ($division, $distance, $units) = @_;

    my @min_dist = (0, 25, 25, 25, 25, 25, 25, 25, 25); # Yards
    ## The optimal target radius
    my @target_radius = (0, R8, R8, R8, R8, R8, R2, R8, R8); # Radius
    ## The distance at which the optimal target is shot
    my @target_distance = (0, 100, 100, 100, 100, 50, 25, 100, 100); # Metres
    ## Bullet diameter that adds to scoring area
    my @bullet_dia = (0, 8/mm, 8/mm, 8/mm, 12/mm , 15/mm, 6/mm, 8/mm, 8/mm);


    die if ($division > 8 || $division < 1);

    my $metricdistance = convert_distance($distance, $units, "Metres");
    my $yardsdistance = convert_distance($distance, $units, "Yards");

    # if ($yardsdistance < $min_dist[$division]) {
    #	return 0;
    # }

    # Ths scoring radius is the target radius, plus the bullet diameter.
    my $optimal_scoring_r = $target_radius[$division] +
    $bullet_dia[$division];

    # Scale the scoring radius of the desired distance based on the scoring
    # radius at the optimal distance for the division.
    my $scaled_scoring_r = $optimal_scoring_r *
	($metricdistance / $target_distance[$division]);

    # Now remove the bullet width from the scaled scoring radius to get a
    # correctly scaled target radius for the circle we will draw.
    # This should give an equivalent scoring area at any distance
    # for the given bullet diameter.
    my $targetradius = $scaled_scoring_r - $bullet_dia[$division];

    my $bullet_radius = ($bullet_dia[$division]) / 2;
    my $bullet_area = 3.1415 * $bullet_radius * $bullet_radius;
    my $target_area = 3.1415 * $targetradius * $targetradius;
    my $rounds_per_match = 20;
    if ($division == 5) {
	$rounds_per_match = 4;
    }
    if (($bullet_area * (2 * $rounds_per_match)) < $target_area) {
	# Can we fit 40 bullet areas into the visible area? If so we can
	# score 20 hits per target
	return ($targetradius, 20);
    } elsif (($bullet_area * ($rounds_per_match / 2)) < $target_area) {
	return ($targetradius, 5);
    } else {
	# We use one target per round
	return ($targetradius, 1);
    }
}

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
sub makeCFCtarget($$$$$) {
    my ($division, $distance, $units, $paper) = @_;

    die "Paper $paper is not valid"
	unless (($paper eq "A4") |
		$paper eq "Letter" |
		$paper eq "Legal" |
		$paper eq "11x17" |
		$paper eq "12x18" |
		$paper eq "24x36" |
		$paper eq "36x48" |
		$paper eq "48x48" |
		$paper eq "A0"	  |
		$paper eq "A1"    |
		$paper eq "A2"    |
		$paper eq "A3"    
	);

    my @div_name = ("Nonsuch", "Vintage", "Modern-Open", "Manual-Open",
		 "Single-Shot", "Muzzleloaders", "Air Rifle",
		 "Manual-Irons", "Single Load Repeater");

    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
    $year = $year+1900;

    my $pdf  = PDF::API2->new;

    # Try to prevent scaling in viewers which may turn into scaling when
    # printed from viewers (i.e. a browser) instead of sending the file
    # directly to a printer.
    $pdf->preferences(-printscalingnone=>1);

    # Set our page boundaries to the correct paper size, with repeated
    # hints to attempt to ensure the randomly written browser and
    # printer software stacks that will be touching this will
    # hopefully be convinced to not pervert it themselves. We probably
    # can't win 100% of the time, but it would be nice if it is usually
    # correct in the common cases with the correct paper size selected.
    $pdf->mediabox($paper);
    my $page = $pdf  -> page;
    $page->boundaries(media => $paper);

    # XXX decide if we should mess with prepend or not?
    my $gfx  = $page -> graphics();
    my $txt  = $page -> text;

    my $actualsize;
my $rounds_per_target = 20;
    # What is the radius ot the circle we should print, in points?
    ($actualsize, $rounds_per_target) = Scaled_radius($division,
						      $distance,
						      $units);

    # Compute how big in millimetres it is supposed to be. We
    # display this right on the target for confirmation purposes.
    my $diameterinmm = round($actualsize * mm * 2.0, 0);
    # Metric is hard in some places.
    my $diameterininches = round(($actualsize / 72) * 2.0, 2);

    # Finally, put some text on the target
    $txt->font($pdf->corefont('Helvetica Bold'), 18);
    my ($x1, $y1, $x2, $y2) = $page->boundaries('media');
    $txt->position($x1 + 30, $y2 - 30);

    #First line is what year and Division this is for.
    $txt->text("EXPERIMENTAL DO NOT USE, Division $division (".$div_name[$division].")");
    $txt->crlf();

    # Second line is the distance in requested units, an equivalent
    # reminder distance, and the size of the target in millimetres.
    # The reminder distance for metric is in yards, for any other
    # unit of measure it is in metric. This serves as a bit of a
    # wakeup call to someone shooting a yards target at metric distance
    # and vice versa, as they are stapling it up.
    if ($units eq "Metres") {
	my $yardsdistance = convert_distance($distance, $units, "Yards");
	$txt->text("Target For Distance: $distance Metres ($yardsdistance Yards) Diameter $diameterinmm mm");
    } else {
	my $metricdistance = convert_distance($distance, $units, "Metres");
	$txt->text("Target For Distance: $distance $units ($metricdistance Metres) Diameter $diameterinmm mm");
    }
    # Third line is the reminder for what paper they should be printed on.
    $txt->crlf();
    $txt->text("Must be printed on $paper size paper with printer set to print $paper");

    if ($diameterinmm < 9) {
	# Don't allow super small targets. You will have to be further away.
	$actualsize = 0;
    }
    
    if ($actualsize == 0) {
	# We can not shoot at this distance
	$txt->crlf();
	$txt->crlf();
	$txt->text("You can not shoot Divison $division at $distance $units!");
    } elsif ($actualsize * 2 > $x2 - $x1 || $actualsize * 2 > $y2 - $y1) {
	# You can shoot at this distance, but we can't print the width
	# of the target within the size of the paper. Note that this
	# assumes we can print the entire page, which isn't really normal
	# but every printer is different, so passing this could still mean
	# that the target gets slightly cropped by the printer.
	$txt->crlf();
	$txt->crlf();
	$txt->text("Division $division max target size at $distance $units is $diameterinmm mm");
	$txt->crlf();
	$txt->text("This is too big to print on $paper paper");
	$txt->crlf();
	$txt->text("If you shoot an unofficial target at this distance,");
	$txt->crlf();
	$txt->text("please show a ruler over the target with your submission.");
    } else {
	$txt->font($pdf->corefont('Helvetica'), 12);
	$txt->crlf();
	$gfx -> fillcolor('black');
	my $xstart = $x1 + 15/mm + $actualsize;
	my $xend = $x2 - 15/mm  - $actualsize;
	my $ystart = $y1 + 15/mm + $actualsize;
	my $yend = $y2 - 60/mm - $actualsize;

	my $number_of_targets = 20 / $rounds_per_target;
	if ($division == 5) {
	    if ($number_of_targets > 1) {
		$number_of_targets = $number_of_targets / 5;
		$rounds_per_target = $rounds_per_target / 5;
	    }
	} 
	    

	if ($number_of_targets == 20 &&
	    ($xend - $xstart) / 4 < $actualsize * 6) {
	    # If the targets would end up very close together
	    # when printed 5 across, insist the user print
	    # 5 copies and shoot 1 round per target
	    $number_of_targets = 4;
	} elsif ($number_of_targets == 4 &&
	    ($xend - $xstart) < $actualsize * 6) {
	    # If the targets would end up very close together
	    # when printed 2 across, insist the user print
	    # 5 copies and shoot 5 rounds per target
	    $number_of_targets = 1;
	}
	
	if ($number_of_targets == 1) {
	    $txt->text("Check that the target is $diameterinmm mm ($diameterininches inches) wide before shooting!");
	    $txt->crlf();
	    $txt->text("If the target has not printed correctly, check that your printer and tray settings are set to $paper");
	    if ($rounds_per_target == 5) {
		$txt->crlf();
		$txt->text("Each target may score a maximum of 5 hits. Shoot 5 rounds at each target.");
		$txt->crlf();
		$txt->text("Print 4 copies of this page to shoot the match!");
	    }
	    # find the centre of the page.
	    my $midx = ($x2 - $x1) / 2;
	    my $midy = ($y2 - $y1) / 2;
	    # make the circle at the centre of the page
	    $gfx -> fillcolor('black');
	    $gfx -> strokecolor('black');
	    $gfx -> circle( $midx, $midy, $actualsize);
	    $gfx -> paint;
	} else {
	    # Finally, let's draw the circles for them to poke holes in.
	    if ($number_of_targets == 20) {
	    $txt->text("Check that each target is $diameterinmm mm ($diameterininches inches) wide before shooting!");
	    $txt->crlf();
	    $txt->text("If the targets have not printed correctly, check that your printer and tray settings are set to $paper");
    	    $txt->crlf();
	    $txt->text("Each target may score a maximum of 1 hit. Shoot 1 round at each target.");
	    # draw 5 targets in four rows.
	    for (my $j = 0; $j < 4; $j++) {
		my $ydelta = $j * (($yend - $ystart) / 3);
		for (my $i = 0; $i < 5; $i++) {
		    my $xdelta = $i * (($xend - $xstart) / 4);
		    my $gfx = $page->graphics();
		    $gfx -> fillcolor('black');
		    $gfx -> strokecolor('black');
		    $gfx -> circle( $xstart + $xdelta, $ystart + $ydelta, $actualsize);
		    $gfx -> paint;
		}
	    }
	    } else {
		# 1 round per target, targets alternate up/down on page
		$txt->text("Check that each target is $diameterinmm mm ($diameterininches inches) wide before shooting!");
		$txt->crlf();
		$txt->text("If the targets have not printed correctly, check that your printer and tray settings are set to $paper");
		$txt->crlf();
		if ($rounds_per_target == 1) {
		    $txt->text("Each target may score a maximum of 1 hit. Shoot 1 round at each target.");
		    if ($division != 5) {
			$txt->crlf();
			$txt->text("Print 5 copies of this page to shoot the match!");
		    }
		} else {
		    $txt->text("Each target may score a maximum of 5 hits. Shoot 5 rounds at each target.");
		}
		my $ydelta = 0;
		my $xdelta = 0;
		for (my $j = 0; $j < 4; $j++) {
		    my $gfx = $page->graphics();
		    $gfx -> fillcolor('black');
		    $gfx -> strokecolor('black');
		    $gfx -> circle( $xstart + $xdelta, $ystart + $ydelta, $actualsize);
		    $gfx -> paint;
		    if ($xdelta == 0) {
			$xdelta = $xend - $xstart;
		    } elsif ($ydelta == 0) {
			$ydelta = $yend - $ystart;
			$xdelta = 0;
		    }
		}
	    }
	}
    }

#    my $filename = "Division-$division-" .$div_name[$division]."-$distance-$units-$paper.pdf";
#    $filename =~ s/ /-/g;
#    $pdf -> saveas($filename);
    return $pdf->to_string();
    $pdf -> end;
}

my $cgi = CGI->new();
my $Division = $cgi->param('Division');
my $Distance = $cgi->param('Distance'); 
my $Units = $cgi->param('Units'); 
my $Paper = $cgi->param('Paper');
my $OldTargets = $cgi->param('OldTargets');

if (!$OldTargets) {
    if (!$Distance) {
	$Distance = 100;
	if ($Division == 5 || $Division == 6) {
	    $Distance = 50;
	}
    }
    my $pdfstring = makeCFCtarget($Division, $Distance, $Units, $Paper);
    print $cgi->header('application/pdf');
    print $pdfstring;
} else {
    my $file_content = "";
    if ($Division == 6) {
	if ($Units eq "Yards") {
	    if ($Distance == 50) {
		$file_content = read_file('/var/www/foad/cfc/oldcfctargets/CFC_22_Rimfire_Target.pdf');
	    } elsif ($Distance == 25) {
		$file_content = read_file('/var/www/foad/cfc/oldcfctargets/Y25_D6_25yd.pdf');
	    }
	} else {
	    if ($Distance == 50) {
		$file_content = read_file('/var/www/foad/cfc/oldcfctargets/CFC_22_Rimfire_Target.pdf');
	    } elsif ($Distance == 25) {
		$file_content = read_file('/var/www/foad/cfc/oldcfctargets/M25_D6_25m.pdf');
	    }
	}
    }
    if ($Division == 5) {
	if ($Units eq "Yards") {
	    if ($Distance == 50) {
		$file_content = read_file('/var/www/foad/cfc/oldcfctargets/Y100_D1-4_7_100yd.pdf');
	    }
	} else {
	    if ($Distance == 50) {
		$file_content = read_file('/var/www/foad/cfc/oldcfctargets/MAD_MIN_2.pdf');
	    }
	}
    }
    else {
	# Div 1-4, 7
	if ($Units eq"Yards") {
	    if ($Distance == 100) {
		$file_content = read_file('/var/www/foad/cfc/oldcfctargets/Y100_D1-4_7_100yd.pdf');
	    } elsif ($Distance == 50) {
		$file_content = read_file('/var/www/foad/cfc/oldcfctargets/M50_D1-4_7_50m.pdf');
	    }
	} else {
	    if ($Distance == 100) {
		$file_content = read_file('/var/www/foad/cfc/oldcfctargets/MAD_MIN_2.pdf');
	    } elsif ($Distance == 50) {
		$file_content = read_file('/var/www/foad/cfc/oldcfctargets/M50_D1-4_7_50m.pdf');
	    }
	}
    }
    if ($file_content ne "") {
	print $cgi->header('application/pdf');
	print $file_content;
    } else {
	print $cgi->header('text/html');
	print <<EOT;
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>No Target At That Distance</title>
</head>

<body>
  <H2>Sorry</H2>
  You can't shoot Division $Division at $Distance $Units
  <HR>
  You can <A HREF="https://obtuse.com/cfc/">Try Again</A>
</body>
</html>
EOT
    }
}	    
    

