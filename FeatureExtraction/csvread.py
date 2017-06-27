import csv
import sys
fp = open(sys.argv[1])

data = csv.reader(fp)
#for row in data:
#   print len(row)

# length of list is 80
fw = open("consolidated_annotations_redone_for_nominations.csv", "w")
csv_w = csv.writer(fw, delimiter=',')
#csv_w.writerow(['HITID', 'TurkerID', 'Tweet','Tweet_ID', 'Veridicality Annotation', 'Desire Annotation'])
for row in data: #each row is a hit
    HitID = row[0]
    #print HitID
    #dataForTweet = []
    #dataForTweet.append(HitID)
    for i in range(0,10):
        if i == 0:       
            dataForTweet = []
            dataForTweet.append(HitID)
            dataForTweet.append(row[15])     #TurkerID
            dataForTweet.append(row[27])     #tweet Content
            dataForTweet.append(str(HitID) + "_Veridical_Tweet1") #Tweet_ID
            dataForTweet.append(row[28]) #veridicality question
            dataForTweet.append(row[29]) #desire question
            dataForTweet.append(row[69]) #Veridical_Annot
            dataForTweet.append(row[59]) #Desire Annot
            csv_w.writerow(dataForTweet)
        elif i == 1:
            dataForTweet = []
            dataForTweet.append(HitID)
            dataForTweet.append(row[15])     #TurkerID
            dataForTweet.append(row[30])     #tweet Content
            dataForTweet.append(str(HitID) + "_Veridical_Tweet2") #Tweet_ID
            dataForTweet.append(row[31]) 
            dataForTweet.append(row[32]) 
            dataForTweet.append(row[70]) #Veridical_Annot
            dataForTweet.append(row[60]) #Desire Annot
            csv_w.writerow(dataForTweet)
        elif i == 2:
            dataForTweet = []
            dataForTweet.append(HitID)
            dataForTweet.append(row[15])     #TurkerID
            dataForTweet.append(row[33])     #tweet Content
            dataForTweet.append(str(HitID) + "_Veridical_Tweet3") #Tweet_ID
            dataForTweet.append(row[34]) 
            dataForTweet.append(row[35]) 
            dataForTweet.append(row[71]) #Veridical_Annot
            dataForTweet.append(row[61]) #Desire Annot
            csv_w.writerow(dataForTweet)
        elif i == 3:
            dataForTweet = []
            dataForTweet.append(HitID)
            dataForTweet.append(row[15])     #TurkerID
            dataForTweet.append(row[36])     #tweet Content
            dataForTweet.append(str(HitID) + "_Veridical_Tweet4") #Tweet_ID
            dataForTweet.append(row[37]) 
            dataForTweet.append(row[38]) 
            dataForTweet.append(row[72]) #Veridical_Annot
            dataForTweet.append(row[62]) #Desire Annot
            csv_w.writerow(dataForTweet)
        elif i == 4:
            dataForTweet = []
            dataForTweet.append(HitID)
            dataForTweet.append(row[15])     #TurkerID
            dataForTweet.append(row[39])     #tweet Content
            dataForTweet.append(str(HitID) + "_Veridical_Tweet5") #Tweet_ID
            dataForTweet.append(row[40]) 
            dataForTweet.append(row[41]) 
            dataForTweet.append(row[73]) #Veridical_Annot
            dataForTweet.append(row[63]) #Desire Annot
            csv_w.writerow(dataForTweet)
        elif i == 5:
            dataForTweet = []
            dataForTweet.append(HitID)
            dataForTweet.append(row[15])     #TurkerID
            dataForTweet.append(row[42])     #tweet Content
            dataForTweet.append(str(HitID) + "_Veridical_Tweet6") #Tweet_ID
            dataForTweet.append(row[43]) 
            dataForTweet.append(row[44]) 
            dataForTweet.append(row[74]) #Veridical_Annot
            dataForTweet.append(row[64]) #Desire Annot
            csv_w.writerow(dataForTweet)
        elif i == 6:
            dataForTweet = []
            dataForTweet.append(HitID)
            dataForTweet.append(row[15])     #TurkerID
            dataForTweet.append(row[45])     #tweet Content
            dataForTweet.append(str(HitID) + "_Veridical_Tweet7") #Tweet_ID
            dataForTweet.append(row[46]) 
            dataForTweet.append(row[47]) 
            dataForTweet.append(row[75]) #Veridical_Annot
            dataForTweet.append(row[65]) #Desire Annot
            csv_w.writerow(dataForTweet)
        elif i == 7:
            dataForTweet = []
            dataForTweet.append(HitID)
            dataForTweet.append(row[15])     #TurkerID
            dataForTweet.append(row[48])     #tweet Content
            dataForTweet.append(str(HitID) + "_Veridical_Tweet8") #Tweet_ID
            dataForTweet.append(row[49]) 
            dataForTweet.append(row[50]) 
            dataForTweet.append(row[76]) #Veridical_Annot
            dataForTweet.append(row[66]) #Desire Annot
            csv_w.writerow(dataForTweet)
        elif i == 8:
            dataForTweet = []
            dataForTweet.append(HitID)
            dataForTweet.append(row[15])     #TurkerID
            dataForTweet.append(row[51])     #tweet Content
            dataForTweet.append(str(HitID) + "_Veridical_Tweet9") #Tweet_ID
            dataForTweet.append(row[52]) 
            dataForTweet.append(row[53]) 
            dataForTweet.append(row[77]) #Veridical_Annot
            dataForTweet.append(row[67]) #Desire Annot
            csv_w.writerow(dataForTweet)
        elif i == 9:
            dataForTweet = []
            dataForTweet.append(HitID)
            dataForTweet.append(row[15])     #TurkerID
            dataForTweet.append(row[54])     #tweet Content
            dataForTweet.append(str(HitID) + "_Veridical_Tweet10") #Tweet_ID
            dataForTweet.append(row[55]) 
            dataForTweet.append(row[56]) 
            dataForTweet.append(row[68]) #Veridical_Annot
            dataForTweet.append(row[58]) #Desire Annot
            csv_w.writerow(dataForTweet)

#fw = open("consolidated_annotations.csv", "w")
#csv_w = csv.writer(fw, delimiter=',')
#csv_w.writerow(['abc', 'def', '123','Hello, there friend!'])
