# Class to handle main panel
import json
from tkinter import *
from urllib.request import urlopen
from time import localtime, strftime

class smartMirror():
    def __init__(self):
        """Saving settings as variables"""
        self.background = 'black'
        self.foreground = 'white'
        self.Font1 = 'Helvetica'
        self.url = 'http://api.wunderground.com/api/3c8e35eb14de7c47/forecast/geolookup/conditions/q/MD/Baltimore.json'
        
        # Create top window frame
        self.root = Tk()
        self.root.title("Weather App")
        self.root.configure(background=self.background)

        # Create current info frame
        self.currentFrame = Frame(self.root)
        self.currentFrame.configure(background=self.background)
        self.currentFrame.grid(row=0, column=0)
        
        # Create time frame
        self.timeFrame = Frame(self.root)
        self.timeFrame.configure(background=self.background)
        self.timeFrame.grid(row=0, column=1, sticky=NE)
        self.root.columnconfigure(1, weight=1)
        
        # Create empty spacing frame
        self.emptyFrame = Frame(self.root)
        self.emptyFrame.configure(background=self.background)
        self.emptyFrame.grid(row=1, column=0)
        self.root.rowconfigure(1, minsize=30)

        # Create forecast info frame to go below current info
        self.forecastFrame = Frame(self.root)
        self.forecastFrame.configure(background=self.background)
        self.forecastFrame.grid(row=2, column=0, sticky=W)
        
        # Update variable to only update weather once every 10 minutes
        # Time display is updated every second
        self.updateCounter = 0
    
        # Call draw GUI function
        self.drawGUI(self.updateCounter)

    def drawGUI(self, updateCounter):
       
        # Draw Time
        # Display and hide the colon every second
        if updateCounter % 2 == 0:
            time = strftime('%H:%M %p ', localtime())
        else:
            time = strftime('%H %M %p ', localtime())
        timeLabel = Label(self.timeFrame,
                          text=time,
                          font=(self.Font1,120),
                          bg=self.background,
                          fg=self.foreground)
        timeLabel.grid(row=0, column=0)
        
        """ Update all weather info every 3 minutes"""
        # Forecast day, image, and temps
        # Only update after update counter has reached 5 minutes
        #if updateCounter == 0 or updateCounter == 5*60:
        if updateCounter >= 0:
            
            # Reset counter so that it won't update twice at 5 minutes
            #updateCounter = 1

            # Get current info from http call
            webURL = urlopen(self.url)
            data = webURL.read()
            encoding = webURL.info().get_content_charset('utf-8')
            weatherDictionary = json.loads(data.decode(encoding))

            """ File for work offline
            f = 'baltimore.json'
            with open(f,'r') as f:
            weatherDictionary = json.loads(f.read())
            """
        
            # Location string
            location = weatherDictionary['location']['city']
            locationLabel = Label(self.currentFrame,
                                  text=location,
                                  font=(self.Font1, 75),
                                  bg=self.background,
                                  fg=self.foreground)
            locationLabel.grid(row=0, column=0, columnspan=2, sticky=W)
                                  
            # Current weather data
            currentWeather = weatherDictionary['current_observation']
            # 3 day forecast data
            forecast = weatherDictionary['forecast']['simpleforecast']['forecastday']

            # Current weather image
            icon = currentWeather['icon']
            photoImage = PhotoImage(file=self.icon_match(icon))
            iconImage = Label(self.currentFrame, image=photoImage, bg=self.background)
            iconImage.image = photoImage
            iconImage.grid(row=1, column=0, rowspan=2, sticky=NE)
                              
            # Current weather temperature
            # Temp string
            currentTemp = str(int(currentWeather['temp_f']))
            currentTempLabel = Label(self.currentFrame,
                                     text=currentTemp,
                                     font=(self.Font1,80),
                                     bg=self.background,
                                     fg=self.foreground)
            currentTempLabel.grid(row=1, column=1)
                              
            # Current status string
            currentStatusString = currentWeather['weather']
            if updateCounter == 0:
                currentStatusString = currentWeather['weather']
            else:
                currentStatusString = 'LOL'
            currentStatusLabel = Label(self.currentFrame,
                                       text=currentStatusString,
                                       font=(self.Font1,45),
                                       bg=self.background,
                                       fg=self.foreground)
            print('iran')
 
            currentStatusLabel.grid(row=2, column=1, sticky=N)

            for day in range(3):
                # Draw day name
                day_name = forecast[day]['date']['weekday_short']
                day_name = day_name.upper() + ' '
                w = Label(self.forecastFrame,
                          text=day_name,
                          font=(self.Font1,60),
                          bg=self.background,
                          fg=self.foreground)
                w.grid(row=day+3, column=0, sticky=NW)
                # Draw forecast temps
                temp_high = forecast[day]['high']['fahrenheit']
                temp_low = forecast[day]['low']['fahrenheit']
                temp_string = temp_high + ' \n' + temp_low + ' '
                w = Label(self.forecastFrame,
                          text=temp_string,
                          font=(self.Font1,60),
                          bg=self.background,
                          fg=self.foreground)
                w.grid(row=day+3, column=1)
                # Draw forecast image
                icon = forecast[day]['icon']
                photoImage = PhotoImage(file=self.icon_match(icon))
                w = Label(self.forecastFrame,
                          image=photoImage,
                          bg=self.background)
                w.image = photoImage
                w.grid(row=day+3, column=2)
        updateCounter += 1
        self.root.after(1000, self.drawGUI, updateCounter)
        self.root.mainloop()
    
    def updateGUI

    def icon_match(self, icon):
        icons = {
            'chanceflurries':'images/snow.gif',
            'chancerain':'images/rain.gif',
            'chancesleet':'images/snow.gif',
            'chancesnow':'images/snow.png',
            'chancestorms':'images/thunderstorm.gif',
            'chancetstorms':'images/thunderstorm.gif',
            'clear':'images/sun.gif',
            'cloudy':'images/cloudy.gif',
            'flurries':'images/snow.gif',
            'fog':'images/partcloudy.gif',
            'hazy':'images/partcloudy.gif',
            'mostlycloudy':'images/partcloudy.gif',
            'mostlysunny':'images/partcloudy.gif',
            'partlycloudy':'images/partcloudy.gif',
            'partlysunny':'images/partcloudy.gif',
            'sleet':'images/snow.gif',
            'rain':'images/rain.gif',
            'snow':'images/snow.gif',
            'sunny':'images/sun.gif',
            'tstorms':'images/thunderstorm.gif',
            'unknown':'images/thunderstorm.gif'
        }
        match = icons[icon]
        return match


# Create frame
smartMirror = smartMirror()

