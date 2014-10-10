#!/usr/bin/perl

use strict;
use warnings;
use 5.010;
use JavaScript::Minifier qw(minify);

my $file = $ARGV[0];
my $file_noext = $file;
$file_noext =~ s/\.[^.]+$//;

open(INFILE, $file) or die;
open(OUTFILE, '>' . $file_noext . '.min.js') or die;
minify(input => *INFILE, outfile => *OUTFILE);
close(INFILE);
close(OUTFILE);

exit 0;


