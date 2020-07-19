#This script filters a structure-formatted file to:
#1) remove loci exhibiting more than mn (see below) SNPS per RADtag (should be chosen depending on the specific species and dataset)
#2) leave only one SNP (chosen at random) per RADtag

#the structure formatted file should include two lines per individual and a header with marker loci

#MAXIMUM NUMBER OF SNPS PER TAG ALLOWED:
mn=8
#add here the name of the file with the data to filter (should be on the same folder; if not include path in the name):
filename="FILENAME"
fich=file(filename).read().split("\n")

#enter missing data format below
missing_data="-9"
import random
loci=fich[0].split("\t")[2].split("  ")
loclist=[]
for l in loci:
    if l!="":
        if l.split(".")[0] not in loclist:
            loclist.append(l.split(".")[0])
indices=[]
for k in loclist:
    ind=[]
    for j in range(len(loci)):
        if k==loci[j].split(".")[0]:
            ind.append(j)
    indices.append(ind)
chosenloc=[]
for x in indices:
    if len(x)<=mn:
        chosenloc.append(random.sample(x,1)[0])


#enter the name of the desired output file below (replace "OUTFILE_NAME"):
outfile="OUTFILE_NAME"        
out=file(outfile,"w")
out.write("\t\t")
for c in chosenloc:
    out.write("  "+loci[c])
out.write("\n")
for li in fich[1:]:
    if li!="":
        spl=li.split("\t")
        out.write(spl[0]+"\t"+spl[1]+"\t")
        for ck in chosenloc[:-1]:
           out.write(spl[2].split(" ")[ck]+" ")
        out.write(spl[2].split(" ")[chosenloc[-1]])
        out.write("\n")
out.close()
