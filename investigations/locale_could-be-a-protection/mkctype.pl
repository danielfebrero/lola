#!/usr/bin/env perl -wC
#
# Copyright 2009 Edwin Groothuis <edwin@FreeBSD.org>
# Copyright 2015 John Marino <draco@marino.st>
# Copyright 2021 Tintri by DDN, Inc. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

use strict;
use Encode qw(encode decode);

my $src = "$ARGV[0]";
my $unidir = "$ARGV[1]";

my %utf8map = ();
my $outfilename = "$src/data/locale/data/common.UTF-8.src";

get_utf8map("$src/data/locale/data/UTF-8.cm");
generate_header();
parse_unidata("$unidir/UnicodeData.txt");
generate_footer();

############################

sub utf8to32 {
	my @kl = split /\\x/, $_[0];

	shift @kl if ($kl[0] eq '');
	my $k = pack('H2' x scalar @kl, @kl);
	my $ux = encode('UTF-32BE', decode('UTF-8', $k));
	my $u = uc(unpack('H*', $ux));
	# Remove BOM
	$u =~ s/^0000FEFF//;
	# Remove heading bytes of 0
	while ($u =~ m/^0/ and length($u) > 4) {
		$u =~ s/^0//;
	}

	return $u;
}

sub get_utf8map {
	my $file = shift;

	open(FIN, $file);
	my @lines = <FIN>;
	close(FIN);
	chomp(@lines);

	my $incharmap = 0;
	foreach my $l (@lines) {
		$l =~ s/\r//;
		next if ($l =~ /^\#/);
		next if ($l eq "");

		if ($l eq "CHARMAP") {
			$incharmap = 1;
			next;
		}

		next if (!$incharmap);
		last if ($l eq "END CHARMAP");

		$l =~ /^(<[^\s]+>)\s+(.*)/;
		my $k = utf8to32($2);	# UTF-8 char code
		my $v = $1;

#		print STDERR "register: $k - $v\n";
		$utf8map{$k} = $v;
	}
}

sub generate_header {
	open(FOUT, ">", "$outfilename")
		or die ("can't write to $outfilename\n");
	print FOUT "LC_CTYPE\n";
}

sub generate_footer {
	print FOUT "\nEND LC_CTYPE\n";
	close (FOUT);
}

sub parse_unidata {
	my $file = shift;
	my %data = ();

	open(FIN, $file);
	my @lines = <FIN>;
	close(FIN);
	chomp(@lines);

	foreach my $l (@lines) {
		my @d = split(/;/, $l, -1);
		my $mb = $d[0];
		my $cat;

		# XXX There are code points present in UnicodeData.txt
		# and missing from UTF-8.cm
		next if !defined $utf8map{$mb};

		# Define the category
		if ($d[2] =~ /^Lu/) {
			$cat = "upper";
		} elsif ($d[2] =~ /^Ll/) {
			$cat = "lower";
		} elsif ($d[2] =~ /^Nd/) {
			$cat = "digit";
		} elsif ($d[2] =~ /^L/) {
			$cat = "alpha";
		} elsif ($d[2] =~ /^P/) {
			$cat = "punct";
		} elsif ($d[2] =~ /^Co/ || $d[2] =~ /^M/ || $d[2] =~ /^N/ ||
		    $d[2] =~ /^S/) {
			$cat = "graph";
		} elsif ($d[2] =~ /^C/) {
			$cat = "cntrl";
		} elsif ($d[2] =~ /^Z/) {
			$cat = "space";
		}
		$data{$cat}{$mb}{'wc'} = $d[0];

		# Check if it's a start or end of range
		if ($d[1] =~ /First>$/) {
			$data{$cat}{$mb}{'start'} = 1;
		} elsif ($d[1] =~ /Last>$/) {
			$data{$cat}{$mb}{'end'} = 1;
		}

		# Check if there's upper/lower mapping
		if ($d[12] ne "") {
			$data{'toupper'}{$mb} = $d[12];
		} elsif ($d[13] ne "") {
			$data{'tolower'}{$mb} = $d[13];
		}
	}

	my $first;
	my $inrange = 0;

	# Now write out the categories
	foreach my $cat (sort keys (%data)) {
		print FOUT "$cat\t";
		$first = 1;
	foreach my $mb (sort {hex($a) <=> hex($b)} keys (%{$data{$cat}})) {
		if ($first == 1) {
			$first = 0;
		} elsif ($inrange == 1) {
			# Safety belt
			die "broken range end wc=$data{$cat}{$mb}{'wc'}"
			    if !defined $data{$cat}{$mb}{'end'};
			print FOUT ";...;";
			$inrange = 0;
		} else {
			print FOUT ";/\n\t";
		}

		if ($cat eq "tolower" || $cat eq "toupper") {
			print FOUT "($utf8map{$mb},$utf8map{$data{$cat}{$mb}})";
		} else {
			if (defined($data{$cat}{$mb}{'start'})) {
				$inrange = 1;
			}
			print FOUT "$utf8map{$mb}";
		}
	}
		print FOUT "\n";
	}
}
