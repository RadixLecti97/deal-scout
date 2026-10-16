import json
import csv

with open("labels.json",encoding="utf-8") as f:
    labels = json.load(f)


def stringCleaner(csvtext)->str:
    

    if(csvtext=="" or csvtext == None):
        csvtext=""
    csvtext = str(csvtext)

    outputStr = csvtext.strip().lower()
    return outputStr

#labels is a dictionary of dictionaries
#labels["article_3.txt"]["buyer"]
score = 0
total=0
missList =[]
fieldCounts={}
fieldTotals = {}

with open ('results.csv',newline = '', encoding="utf-8") as csvfile:
    spamreader = csv.DictReader(csvfile,delimiter=',')
    for row in spamreader:
        if row['file'] not in labels:
            print(f"{row['file']} not found in labels.json")
            continue
        expected = labels[row['file']]
        for field in expected:
            #print(field)
          
            if(stringCleaner(expected[field]) == stringCleaner(row[field])):
                fieldCounts[field]=fieldCounts.get(field,0)+1
                score+=1
            else:
                missList.append({"file":row['file'],"field":field,"incorrect value":row[field],"expected value":expected[field]})
            fieldTotals[field]=fieldTotals.get(field,0)+1
            total+=1
print(f"Overall Score:{score}/{total} \nOverall Percentage Correct: {score/total:.0%}")
for fields in fieldTotals:
    print(f"{fields}: {fieldCounts[fields]}/{fieldTotals[fields]} ({fieldCounts[fields]/fieldTotals[fields]:.0%})")
for miss in missList:
    print(miss)