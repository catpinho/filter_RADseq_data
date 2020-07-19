#This script filters a structure-formatted file to:
#1) remove loci exhibiting more than mn (see below) SNPS per RADtag (should be chosen depending on the specific species and dataset)
#2) leave only one SNP (chosen by maximizing frequency difference between reference populations) per RADtag

#the structure formatted file should include two lines per individual, a population column and a header with marker loci
#MAXIMUM NUMBER OF SNPS PER TAG ALLOWED:
mn=8

import os
#enter indexes of the pops of interest - should match those in the second column of the structure file. Combinations of pops are valid (e.g."1+2", "9+10")

pops_of_interest=["1","3"]

#enter missing data format below
missing_data="-9"

def calcula_freqs(pops,loc):
    altypes=[]

    freqs=[]

    counts=[]
    for pop in pops:

        alls=[]
        
        m=pop.split("+")
        for line in fich[1:]:
            if line != "":
                if line.split("\t")[1] in m:

                    x=line.split("\t")[2].split(" ")[loc]
                    if x!=missing_data:
                        alls.append(x)
                        if x not in altypes:
                            altypes.append(x)

        counts.append(alls)
    
  

    if len(altypes)>2:
        print altypes
        print str(loc)+" NOT DIALLELIC"
    for pop in range(len(pops)):
        try:
            freqs.append(counts[pop].count(altypes[0])*1.0/len(counts[pop]))
        except ZeroDivisionError:
            freqs.append("NA")

    return freqs
#add here the name of the file with the data to filter (should be on the same folder; if not include path in the name):
filename="FILENAME"
fich=file(filename).read().split("\n")

locl=fich[0].split("\t")[2].split("  ")
loci=[]
for lu in locl:
    if lu != "":
        loci.append(lu)
loclist=[]
for l in loci:
    if l!="":
        if l.split(".")[1].split(":")[0] not in loclist:
            loclist.append(l.split(".")[1].split(":")[0])
indices=[]
for k in loclist:
    ind=[]
    for j in range(len(loci)):
        if k==loci[j].split(".")[1].split(":")[0]:
            ind.append(j)
    indices.append(ind)
chosenloc=[]
for loc in indices:
    if len(loc)<=mn:
        ci=loc[0]
        maxifd=0
        for l in loc:
            x=calcula_freqs(pops_of_interest,l)
            if "NA" not in x:
                if abs(x[0]-x[1])>maxifd:
                    maxifd=abs(x[0]-x[1])
                    ci=l
        chosenloc.append(ci)

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
print(len(chosenloc))
out.close()
