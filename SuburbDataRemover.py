import csv

csvfile = open("postcodeData.csv");
reader =csv.reader(csvfile);
final = []
for row in reader:
    if row[5] not in ["HUNTER","NSW NORTH COAST","GOLD COAST","TOOWOOMBA SE CNR", "ILLAWARRA","NEW CNTRY WEST","CANBERRA","VIC FAR COUNTRY","ST GEORGE"]:
        newlist = [row[1],row[2],row[5]];
        final.append(newlist);
with open("FinalSuburbs.csv",'w', newline='') as file:
    writer = csv.writer(file);
    writer.writerows(final);