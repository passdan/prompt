#!/bin/bash

for i in */*species*;
do
sed -i 's/(OTUs:[0-9]*)//' $i;
sort -k1 $i >tmp1.txt;
join -e 0 -o auto -a1 -a2 composite.txt tmp1.txt > tmp2.txt;
mv tmp2.txt composite.txt ;
done
rm tmp1.txt 

