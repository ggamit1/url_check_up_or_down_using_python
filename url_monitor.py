import mysql.connector
from datetime import datetime
import requests
import re

# check url up or not 
def check_website_status(url):
    
    url = url
    try:
        request = requests.get(url, timeout=10)
        response = requests.head(url, timeout=10)
        reason = response.reason
        if request.status_code == 200:
            return 'UP'
        return "(DOWN) " +str(reason)
    except Exception as er:
        return "DOWN "
    
    
# if url not https then we added with this function    
def check_https(url):
    
    if not re.match(r'http(s?)\:', url):
        url = 'https://'+ url
        return url
    
    else:
        return url
    
    
if __name__ == "__main__":
    
    user = 'root'
    password = 'codefire'
    database = 'domain_monitor'
    # host = "127.0.0.1"
    host = "localhost"
    try:
        # To connect with database 
        cnx = mysql.connector.connect(user=user,
                                      password=password,
                                      host=host,
                                      database=database,
                                      port=3306
                                    )
        cursor = cnx.cursor()
        
        query = "select URL, frequency, last_call_datetime, id from url_monitor where Status = 1"
        # excute sql query 
        cursor.execute(query)
        # extract data from  cursor object in list inside tuple
        urls = cursor.fetchall()
        # current date 
        current_time = datetime.now()
        for url_data in urls:
            url = url_data[0]
            frequency = url_data[1]
            last_time_call = url_data[2]
            id = url_data[3]
            # if last_time_call value recieved None then we need to change in date object 
            if last_time_call == None:
                last_time_call = datetime(2020,11,11,11,10,59) 
            # convert date string into datetime object  
            last_time_call = datetime.strptime(str(last_time_call), '%Y-%m-%d %H:%M:%S')
            
            # check last time for website up or with for frquency   
            if (current_time - last_time_call).total_seconds() >= frequency:
                
                print(url, id) # it,s for testing use
                #checking for url up or not funtion call
                status = check_website_status(url)
                # Update status to  database 
                cursor.execute("UPDATE url_monitor SET url_status = '{}' WHERE id = {}".format(status, id))
                # update last_call_datetime to database 
                cursor.execute("UPDATE url_monitor SET last_call_datetime = '{}' WHERE id = {}".format(current_time, id))
                # save/ commit value in database
                cnx.commit()
                
            
        cnx.close()

    except Exception as er:
        print(er)
        
