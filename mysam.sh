bwa index $2
bwa mem -t $3 $2 $1 -o $1.sam 
samtools view -b -S -o $1.bam $1.sam 
samtools \sort $1.bam -o $1.sorted.bam 
samtools index $1.sorted.bam 
samtools mpileup -uBg --max-depth 100000 --min-MQ $7 --min-BQ $6 --output-tags DP,AD,ADF,ADR,SP,INFO\/AD,INFO\/ADR -f $2 $1.sorted.bam --output $1.variants.bcf 
bcftools call --ploidy 1 --multiallelic-caller --keep-alts $1.variants.bcf > $1.variants.vcf
perl vcfparser.pl $1.variants.vcf $4 $5> $1.sam.tsv



