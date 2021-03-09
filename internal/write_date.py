import datetime

with open("dateInfo.txt", 'a') as out_file:
    out_file.write("\n" + str(datetime.datetime.now()))

