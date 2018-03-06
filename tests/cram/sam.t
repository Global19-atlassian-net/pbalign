Set up 
  $ . $TESTDIR/setup.sh

#Test pbalign with bam in sam out with tmpDir
  $ Q=/pbi/dept/secondary/siv/testdata/pbalign-unittest/data/test_bam/tiny_bam.fofn
  $ T=/pbi/dept/secondary/siv/references/lambda/sequence/lambda.fasta
  $ O=aln.sam
  $ pbalign $Q $T $O --tmpDir mytmp/ >/dev/null

#see if aln.sam exist
  $ test -e aln.sam; echo $?
  0

