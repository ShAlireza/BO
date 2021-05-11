import datetime

with open("/home/alireza/PycharmProjects/backup-organizer/dateInfo.txt", 'w') as out_file:
    out_file.write("\n" + str(datetime.datetime.now()))
