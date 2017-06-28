Set up 
  $ . $TESTDIR/setup.sh

#Test pbalign with dataset in and out
  $ D=$TESTDATASETS/lambda/2372215/0007_tiny/Analysis_Results/m150404_101626_42267_c100807920800000001823174110291514_s1_p0.all.subreadset.xml
  $ T=$REFDIR/lambda/lambda.referenceset.xml
  $ O=$OUTDIR/tiny_bam.bam
  $ rm -f $O
  $ pbalign $D $T $O --algorithmOptions=" --holeNumbers 1-1000,30000-30500,60000-60600,100000-100500" >/dev/null

Try feeding an aligned bam back in...
  $ RA=$OUTDIR/tiny_bam_realigned.bam
  $ pbalign $O $T $RA >/dev/null

Call samtools index to check whether out.bam is sorted or not and coverage is sufficient and basic mapped stats
  $ samtools index $O $TMP1.bai && ls $TMP1.bai >/dev/null && echo $?
  0

Sum of depth > 197740
  $ samtools depth $O | awk '{sum+=$3} END {if (sum >= 197740) print "TRUE"; else print "FALSE"}'
  TRUE

  $ samtools flagstat $O
  248 + 0 in total (QC-passed reads + QC-failed reads)
  0 + 0 secondary
  0 + 0 supplementary
  0 + 0 duplicates
  248 + 0 mapped * (glob)
  0 + 0 paired in sequencing
  0 + 0 read1
  0 + 0 read2
  0 + 0 properly paired * (glob)
  0 + 0 with itself and mate mapped
  0 + 0 singletons * (glob)
  0 + 0 with mate mapped to a different chr
  0 + 0 with mate mapped to a different chr (mapQ>=5)


