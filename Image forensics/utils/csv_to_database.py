import sqlite3
from cs50 import SQL 
import pandas as pd

csv_file_path = 'D:\\Cyber Security\\PGDCD\\projects\\Image forensics\\utils\\image_metadata.csv'
df = pd.read_csv(csv_file_path)
df.to_csv(csv_file_path,index=False)
df = pd.read_csv(csv_file_path)
# print(df['gps latitude'])

def csv_to_db_cs50():
    db = SQL("sqlite:///data.db")
    rows = db.execute("SELECT * FROM image_metadata")
    length_of_db = len(rows)
    for i in range(length_of_db):
        db.execute("INSERT INTO image_metadata('file_name','size','height,'width','format','is_animated','frames','camera model','date and time','gps latitude','gps longitude','google_maps_url') VALUES(:file_name,:size,:height,:width,:format,:is_animated,:frames,:camera_model:,:date_and_time,:gps_latitude,:gps_longitude,:google_maps_url)",
                    file_name = df['file_name'][i],
                    size = df['size'][i],
                    height = df['height'][i],
                    width = df['width'][i],
                    format = df['format'][i],
                    is_animated = df['is_animated'][i],
                    frames = df['frames'][i],
                    camera_model = df['camera model'][i],
                    date_and_time = df['date and time'][i],
                    gps_latitude = df['gps latitude'][i],
                    gps_longitude = df['gps longitude'][i],
                    google_maps_url = df['google_maps_url'][i])

csv_to_db_cs50()

def csv_to_db():
    #Csv File Path
    # csv_file_path = 'D:\\Cyber Security\\PGDCD\\projects\\Image forensics\\utils\\image_metadata.csv'

    # df = pd.read_csv(csv_file_path)

    # # Connection of Database
    connection = sqlite3.connect('data.db')
    # db = SQL("sqlite:///data.db")
    
    df.to_sql('image_metadata',connection,if_exists='replace')

    connection.close() 
    
# csv_to_db()
    
    
    # cursor = connection.cursor()


    # with open(csv_file_path,"r") as file:
    #     for row in file:
    #         # data = row.split(",")
    #         # print(data[0])
    #         cursor.execute("INSERT INTO image_metadata('file_name','size','height','width','format','is_animated','frames','camera_model','date and time','gps latitude','gps longitude','google_maps_url') VALUES(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11])")
    #         connection.commit()

    # Close connection
    # connection.close()

# # csv_to_db()
# # def pdd():
# #     df = pd.read_csv('D:\\Cyber Security\\PGDCD\\projects\\Image forensics\\utils\\image_metadata.csv')
# #     print