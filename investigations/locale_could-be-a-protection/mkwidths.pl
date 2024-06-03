#!/usr/bin/env perl -w
#
# Copyright 2009 Edwin Groothuis <edwin@FreeBSD.org>
# Copyright 2015 John Marino <draco@marino.st>
# Copyright 2020 Yuri Pankov <yuripv@FreeBSD.org>
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

my %utf8map = ();
my $outfilename = "$src/data/locale/data/widths.txt";

get_utf8map("$src/data/locale/data/UTF-8.cm");
generate_header();
make_widths();
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
	my $version = <STDIN>;
	chomp($version);

	open(FOUT, ">", "$outfilename")
		or die ("can't write to $outfilename\n");
	print FOUT <<EOF;
# Warning: Do not edit. This file is automatically generated using the
# tools in tools/locale. The data is obtained from the utf8proc $version.
# -----------------------------------------------------------------------------
WIDTH
EOF
}

sub generate_footer {
	print FOUT "END WIDTH\n";
	close (FOUT);
}

sub make_widths {
	my @lines = <STDIN>;
	chomp(@lines);

	foreach my $l (@lines) {
		my ($wc, $wcw) = split(/ /, $l, -1);

		next if !defined $utf8map{$wc};

		print FOUT "$utf8map{$wc}\t$wcw\n";
	}
}
