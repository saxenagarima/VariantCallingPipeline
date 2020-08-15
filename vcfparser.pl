#!/usr/bin/perl -w
$f=$ARGV[0];
$name=$f;
open(F,$f);
$outfile = $f.".tsv";
$noisefile = $f.".noise.tsv";
open (F1, ">$outfile");
open (F2, ">$noisefile");
while (<F>){
	chomp;
	next if $_=~m/##/;
	@info=split('\t', $_);
	$pos=$info[1];
	$refnuc=$info[3];
	@alternative=split(',',$info[4]);	
	$altnuc=$alternative[0];
	if($_=~m/IDV=(\d+)/){
		$variant=$1;	
		if($_=~m/DP=(\d+)/){$tot=$1;}
		$ref=$tot-$variant;
		$pc=($variant/($ref+$variant)*100);
		if ($pc>=$ARGV[1]&&($ref+$variant)>$ARGV[2]){
			print F1 "$name\t$pos\t$refnuc\t$altnuc\t$ref\t$variant\t$pc\n";
		}
		elsif ($pc>0 && $variant>0){
			print F2 "$name\t$pos\t$refnuc\t$altnuc\t$ref\t$variant\t$pc\n";
		}

	}
	elsif ($_=~m/DP4=(.+);MQ/){
		@nums=split(',', $1);
		$ref=$nums[0]+$nums[1];
		$variant=$nums[2]+$nums[3];
		next if ($ref+$variant==0);	
		$pc=($variant/($ref+$variant)*100);
		if ($pc>=$ARGV[1]&&($ref+$variant)>$ARGV[2]){
			print F1 "$name\t$pos\t$refnuc\t$altnuc\t$ref\t$variant\t$pc\n";
		}
		elsif ($pc>0 && $variant>0){
			print F2 "$name\t$pos\t$refnuc\t$altnuc\t$ref\t$variant\t$pc\n";
		}
			

	}
}

