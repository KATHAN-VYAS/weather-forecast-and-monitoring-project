# weather forecast and analysis

import requests
import sys
import pandas as pd
import datetime
import matplotlib.pyplot as plt

def main():
        
        print("\nAs an example longitude and latitude of 2 location are already provided in code  : \n"
                "1. For Harvard University --> press 'H'\n"
                "2. For Pandit Deendayal Energy University --> press 'P'\n"
                "3. For location of your wish  --> press 'X'\n"
                "type exit to exit")

        key = input ("enter key : ")
        if key.rstrip() == "h" or key.rstrip() =="H":
                lat = 42.3770
                lon = -71.1167
                loc = "Harvard University"
        if key.rstrip() == "p" or key.rstrip() =="P":
                lat = 23.2196
                lon = 72.6812
                loc = "PDEU"
        if key.rstrip() == "x" or key.rstrip() =="X":
                lat = float(input("enter latitude of your location "))
                lon = float(input("enter longitude of you location "))
                loc = input("enter name of your place")
        if key.rstrip().lower() == "exit":
                sys.exit("Exited !!")

        api_key = "c93986d568f30cefc45c66d9d26ba3cb"

        #printing guide
        print("Hello ! this is your own weather forecast program\n")
        print("Features of this program are :")
        print("press 1 : To get current weather forecast \n"
                "press 2 : To get whole day forecast \n"
                "press 3 : To get analysis of temperature of upcoming week in form of graph \n"
                "press 4 : To get hourly chances of rain for next week \n"
                "press 5 : To get current information of polution of choosen location \n"
                "press 6 : To get predicted weather forecast of tomorrow \n"
                "press 7 : To get comparision of temperature of 2 provided dates by you \n"
        "press 8 : To exit from code")
        #getting choice
        try:
              choice = int(input("Enter your number: "))
        except ValueError:
              sys.exit("Incorrect number entered try again as per instructions")
        if choice == 1:
              current_forecast(lat,lon,loc,api_key)
        if choice == 2:
              today_forecast(lat,lon,loc,api_key)
        if choice == 3:
              nextweek_forecast(lat,lon)
        if choice == 4:
              rain(lat,lon)
        if choice == 5:
              polution(lat,lon,loc,api_key)
        if choice == 6:
              tomorrow_forecast(lat,lon,loc,api_key)
        if choice ==  7:
                date1 = input("enter date-1(YYYY-MM-DD): ")
                date2 = input("enter date-2(YYYY-MM-DD): ")
                compare_temp(lat,lon,date1,date2)
        if choice == 8 :
                sys.exit("program closed!!")

def current_forecast(lat,lon,loc,api_key):
        # geting responce 
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        response = requests.get(url)
        # 200 is used for OK response
        if response.status_code == 200:
                #to get in form of dictionary 
                data = response.json()
        else:
                sys.exit("Error fetching weather data. Try again after sometime")
        def temp_now(loc,data):
            #getting temperature 
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            temperature_celsius = temperature - 273.15
            print(f"Current temperature at {loc}: {temperature_celsius:.2f}°C")
            print(f"Humidity at {loc}: {humidity:.2f}%")
        try:  
                temp_now(loc,data)
        except ValueError :
                raise ValueError("something went wrong in this feature try again")

def today_forecast(lat, lon, loc, api_key):
    url1 = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    url2 = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"
    response = requests.get(url1)
    responce2 = requests.get(url2)

    if response.status_code == 200 and responce2.status_code == 200:
        data = response.json()  # Assign data here
        data2 = responce2.json()

        def day_weather(data, data2):  # Pass data as an argument
            times = data2["hourly"]["time"]
            temperatures = data2["hourly"]["temperature_2m"]
            with open("today_temp.csv","w")as file1:
                  for i in range (24):
                        file1.write(str(times[i])+", "+str(temperatures[i])+"\n")
            try:    
                graph("today_temp.csv",24)
            except FileNotFoundError:
                    raise FileNotFoundError("error in accessing file")

            clouds = data["clouds"]["all"]
            status = data["weather"][0]["main"]
            sunrise = convert_time(data["sys"]["sunrise"])
            sunset  = convert_time(data["sys"]["sunset"])
            
            print(f"Sunrise at {loc} at time : {sunrise}")
            print(f"Sunset at {loc} at time : {sunset}")
            print(f"Prcentage cloudiness {loc}: {clouds:.2f}%")
            print(f"Status of {loc}(Rain/snow/clouds/smoke): {status}")

    else:
        sys.exit("Can not connect to servers or incorrect URL, try again later")

    try:
        day_weather(data, data2)  # Pass data to the function

    except ValueError as e:
        print(e)

def nextweek_forecast(lat,lon):
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"
        responce = requests.get(url)
        if responce.status_code == 200:
                data = responce.json()
        else:
                sys.exit("Can not connect to servers or incorrect URL, try again later")
        def week_weather(data):
                times = data["hourly"]["time"]
                temperatures = data["hourly"]["temperature_2m"]
                with open("week_temp.csv","w")as file1:
                        for i in range (len(times)):
                                file1.write(str(times[i])+", "+str(temperatures[i])+"\n")
                try:    
                        graph2("week_temp.csv","temperature","°C")
                except FileNotFoundError:
                    raise FileNotFoundError("error in accessing file")
        try:
                week_weather(data)
        except ValueError or FileNotFoundError as e:
                print(e)
  
def polution(lat,lon,loc,api_key):
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"                     
        responce = requests.get(url)
        if responce.status_code == 200:
                data = responce.json()
        else:
                sys.exit("Error fetching weather data. Try again after sometime")
        def current_polution(loc,data):
                co = data['list'][0]['components']['co']
                no = data['list'][0]['components']['no']
                no2 = data['list'][0]['components']['no2']
                so2 = data['list'][0]['components']['so2']
                o3 = data['list'][0]['components']['o3']
                nh3 = data['list'][0]['components']['nh3']
                print(f"Concentration of CO at {loc} is {co} μg/m3")
                print(f"Concentration of NO at {loc} is {no} μg/m3")
                print(f"Concentration of NO2 at {loc} is {no2} μg/m3")
                print(f"Concentration of SO2 at {loc} is {so2} μg/m3")
                print(f"Concentration of O3 at {loc} is {o3} μg/m3")
                print(f"Concentration of NH3 at {loc} is {nh3} μg/m3")
        try:
                current_polution(loc,data)
        except ValueError :
                raise ValueError("something went wrong in this feature try again")
       
def tomorrow_forecast(lat,lon,loc,api_key):
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"
        responce = requests.get(url)
        if responce.status_code == 200:
                data = responce.json()
        else:
                sys.exit("Can not connect to servers or incorrect URL, try again later")
        def week_weather(data):
                times = data["hourly"]["time"]
                temperatures = data["hourly"]["temperature_2m"]
                with open("tomorrow_temp.csv","w")as file1:
                        for i in range (24,48):
                                file1.write(str(times[i])+", "+str(temperatures[i])+"\n")
                try:    
                        graph("tomorrow_temp.csv",24)
                except FileNotFoundError:
                    raise FileNotFoundError("error in accessing file")
        try:
                week_weather(data)
        except ValueError or FileNotFoundError as e:
                print(e)
       
def rain(lat,lon) :
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=rain"
        responce = requests.get(url)
        if responce.status_code == 200:
                data = responce.json()
                times = data["hourly"]["time"]
                probability = data["hourly"]["rain"]
        else:
                sys.exit("Can not connect to servers or incorrect URL, try again later")
        def week_rain():
                with open ("week_rain.csv","w") as file :
                        for i in range (len(times)):
                                file.write(str(times[i])+", "+str(probability[i])+"\n")
                try:    
                        graph2("week_rain.csv","rain","mm")
                except FileNotFoundError:
                    raise FileNotFoundError("error in accessing file")
        try:
                week_rain()
        except ValueError or FileNotFoundError as e:
                print(e)
        
def compare_temp(lat,lon,date1,date2):
        date1 = datetime.datetime.strptime(date1,"%Y-%m-%d")
        startdate1 = date1.strftime("%Y-%m-%d")
        enddate1 = date1.strftime("%Y-%m-%d")
        
        url1 = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={startdate1}&end_date={enddate1}&hourly=temperature_2m"
        
        date2 = datetime.datetime.strptime(date2,"%Y-%m-%d")
        startdate2 = date2.strftime("%Y-%m-%d")
        enddate2 = date2.strftime("%Y-%m-%d")
        
        url2 = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={startdate2}&end_date={enddate2}&hourly=temperature_2m"
        
        responce1 = requests.get(url1)
        responce2 = requests.get(url2)  
        if responce1.status_code == 200 and responce2.status_code == 200:
                data1 = responce1.json()
                data2 = responce2.json()
                
                times = data1["hourly"]["time"]
                temperatures1 = data1["hourly"]["temperature_2m"]
                temperatures2 = data2["hourly"]["temperature_2m"]
                
                def plot_compare():
                        with open ("comparing.csv","w")as file:
                                for i in range(len(times)):
                                        file.write(str(times[i])+", "+str(temperatures1[i])+"\n")
                                for i in range(len(times)):
                                        file.write(str(times[i])+", "+str(temperatures2[i])+"\n")
                        try:
                                graph3("comparing.csv",date1,date2)              
                        except FileNotFoundError:
                                raise FileNotFoundError("error in accessing file")
        else:
                print("Can not connect to servers or incorrect URL, try again later")
        try:
                plot_compare()
        except ValueError or FileNotFoundError as e:
                print(e)       
        
def graph(file,n):
        data = pd.read_csv(file,header=None, names=['timestamp', 'temperature'],nrows=n)
        data['timestamp'] = pd.to_datetime(data["timestamp"])
        plt.figure(figsize=(12,11))
        plt.plot(data["timestamp"],data["temperature"],marker = "o",linestyle = "-",color = "b")
        plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))
        plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.HourLocator(interval=1))
        plt.gcf().autofmt_xdate()
        plt.xlabel('Time (24-hour format)')
        plt.ylabel('Temperature (°C)')
        plt.title('Temperature Variation Over 24 Hours')
        plt.grid(True, linestyle='--', alpha=0.6)
        # to make graph more good 
        plt.legend()
        plt.gca().set_facecolor('#f4f4f4')
        plt.tick_params(axis='both', which='both', length=0)
        plt.show()

def graph2(file,var,unit):
        data1 = pd.read_csv(file,header = None,names =["timestamp",var],nrows = 24)
        data1 ["timestamp"] = pd.to_datetime(data1["timestamp"])
        
        data2 = pd.read_csv(file,header = None,names =["timestamp",var],skiprows=24,nrows = 24)
        data3 = pd.read_csv(file,header = None,names =["timestamp",var],skiprows=48,nrows = 24)
        data4 = pd.read_csv(file,header = None,names =["timestamp",var],skiprows=72,nrows = 24)
        data5 = pd.read_csv(file,header = None,names =["timestamp",var],skiprows=96,nrows = 24)
        data6 = pd.read_csv(file,header = None,names =["timestamp",var],skiprows=120,nrows = 24)
        data7 = pd.read_csv(file,header = None,names =["timestamp",var],skiprows=144,nrows = 24)
        
        plt.figure(figsize=(12,11))
        
        plt.plot(data1["timestamp"],data1[var],marker =  'o',linestyle = "-",color = "g",label = "today")
        plt.plot(data1["timestamp"],data2[var],marker =  'o',linestyle = "--",color = "r",label = "nextday - 1")
        plt.plot(data1["timestamp"],data3[var],marker =  'o',linestyle = "-.",color = "b",label = "nextday - 2")
        plt.plot(data1["timestamp"],data4[var],marker =  'o',linestyle = ":",color = "k",label = "nextday - 3")
        plt.plot(data1["timestamp"],data5[var],marker =  'o',linestyle = "solid",color = "c",label = "nextday - 4")
        plt.plot(data1["timestamp"],data6[var],marker =  'o',linestyle = "dashed",color = "m",label = "nextday - 5")
        plt.plot(data1["timestamp"],data7[var],marker =  'o',linestyle = "dashdot",color = "g",label = "nextday - 6")

        plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))
        plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.HourLocator(interval=1))
        plt.gcf().autofmt_xdate()
        
        plt.xlabel('Time (24-hour format)')
        plt.ylabel(var + unit)
        plt.title(var +" Variation Over 24 Hours")
        plt.grid(True, linestyle='--', alpha=0.6)
        # to make graph more good 
        plt.legend()
        plt.gca().set_facecolor('#f4f4f4')
        plt.tick_params(axis='both', which='both', length=0)
        
        plt.show()
   
def graph3(file,date1,date2):
        data1 = pd.read_csv(file,header = None,names =["timestamp","temperature1"],nrows = 24)
        data1 ["timestamp"] = pd.to_datetime(data1["timestamp"])
        
        data2 = pd.read_csv(file,header = None,names =["timestamp","temperature2"],skiprows=24,nrows = 24)
        plt.figure(figsize=(12,11))
        
        plt.plot(data1["timestamp"],data1["temperature1"],marker =  'o',linestyle = "-",color = "g",label = f"{pd.to_datetime(date1).strftime('%Y-%m-%d')}")
        plt.plot(data1["timestamp"],data2["temperature2"],marker =  'o',linestyle = "--",color = "r",label = f"{pd.to_datetime(date2).strftime('%Y-%m-%d')}")
        plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))
        plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.HourLocator(interval=1))
        plt.gcf().autofmt_xdate()
        
        plt.xlabel('Time (24-hour format)')
        plt.ylabel("Temperature °C")
        plt.title("Temperature Variation Over 24 Hours")
        plt.grid(True, linestyle='--', alpha=0.6)
        # to make graph more good 
        plt.legend()
        plt.gca().set_facecolor('#f4f4f4')
        plt.tick_params(axis='both', which='both', length=0)
        
        plt.show()
     
def convert_time(unix_time):
    utc_time = datetime.datetime.fromtimestamp(unix_time, datetime.timezone.utc)
    # IST = UTC+5:30
    ist_time = utc_time.astimezone(datetime.timezone(datetime.timedelta(hours=5, minutes=30))) 
    ist_time = str(ist_time) 
    time =[]
    time = ist_time.split(" ")
    ist_time = time[1]
    time = ist_time.split(":")
    ist_time = time[0]+":"+time[1]
    return ist_time

if __name__ == "__main__":
      main()
