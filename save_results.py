#please read your_code.py

import csv

# This has been changed to create txt files as csv didn't work on the r-pi
class ResultsSave():


    def __init__(self,vision_file_name,plc_file_name,):

        # vision_file=open(vision_file_name, mode='w')
        # fieldnames = ['tray', 'part', 'type','description']
        # self.writer_vision = csv.DictWriter(vision_file, fieldnames=fieldnames)
        # self.writer_vision.writeheader()
        self.vision_file = open(vision_file_name,"w")
        self.vision_file.write('tray - part - type - description\n')

        self.plc_file = open(plc_file_name,'w')
        self.plc_file.write('tray - message\n')

        # plc_file=open(plc_file_name, mode='w')
        # fieldnames = ['tray','message']
        # self.writer_plc = csv.DictWriter(plc_file, fieldnames=fieldnames)
        # self.writer_plc.writeheader()

    def insert_vision(self,tray,part,ty,fault):

        self.vision_file.write('{0} - {1} - {2} - {3}\n'.format(tray,part,ty,fault))

        # item={}
        # item['tray']=tray
        # item['part']=part
        # item['type']=ty
        # item['description']=fault
        # self.writer_vision.writerow(item)


    def insert_plc(self,tray,message):

        self.plc_file.write('{0} - {1}\n'.format(tray,message))

        # item={}
        # item['tray']=tray
        # item['message']=message

        # self.writer_plc.writerow(item)

    def close_files(self):
        self.vision_file.close()
        self.plc_file.close()