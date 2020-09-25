# Script is run from the qbb2020-answers/week2 directory
# Q1 - Index the sacCer3 genome with bwa index
bwa index sacCer3.fa

#Q2 – Alignment with bwa mem
#bwa mem -R "@RG\tID:Sample1\tSM:Sample1" sacCer3.fa A01_09.fastq > test.sam
#	echo {i%%.fastq}
for i in A01_*.fastq
do
	bwa mem -t 4 -R "@RG\tID:${i%%.fastq}\tSM:${i%%.fastq}" sacCer3.fa $i > ${i%%.fastq}.sam
done

#Q3 – Create a sorted bam file with samtools, for input to variant callers
# first convert to bam format
for i in *.sam
do
	samtools view -b $i > ${i%%.sam}.bam
done

for i in *.bam
do
	samtools sort $i > ${i%%.bam}_sorted.bam
done

#Q4 – Variant calling with freebayes
freebayes --genotype-qualities -f sacCer3.fa *sorted.bam > vars.vcf

#Q5 – Filter variants based on genotype quality using vcffilter
vcffilter -f "QUAL > 20" vars.vcf > vars_filtered.vcf

#Q6
vcfallelicprimitives -k -g vars_filtered.vcf > vars_filtered_decomposed.vcf

#Q7
snpeff ann R64-1-1.86 vars_filtered_decomposed.vcf > vars_annotated.vcf

# making a version of this file for pandas input 
grep -v '##' vars_annotated.vcf > pd_input.vcf
