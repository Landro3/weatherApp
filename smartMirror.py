# Class to handle main panel
import json
import ssl
from tkinter import Tk, Label, Frame, N, NE, E, SE, S, SW, W, NW, PhotoImage
from urllib.request import urlopen
from time import localtime, strftime
from datetime import datetime

class smartMirror():
    def __init__(self):
        self.background = 'black'
        self.foreground = 'white'
        self.Font1 = 'Helvetica'

        # API key and url
        f = open('key.txt', 'r')
        appId = f.readline()
        self.weatherURL = 'https://api.openweathermap.org/data/2.5/onecall?lat=39.290386&lon=-76.612190&exclude=minutely,hourly&appid=' + appId

        # Get current location


        # Create top window frame
        self.root = Tk()
        self.root.title("Weather App")
        self.root.configure(background=self.background, padx=25, pady=50)

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

        # Time Label
        self.timeLabel = Label(self.timeFrame,
                          font=(self.Font1,120),
                          bg=self.background,
                          fg=self.foreground)
        self.timeLabel.pack()

        # Date label
        self.dateLabel = Label(self.timeFrame,
                           font=(self.Font1,60),
                           bg=self.background,
                           fg=self.foreground)
        self.dateLabel.pack()

        # Location label
        self.locationLabel = Label(self.currentFrame,
                              font=(self.Font1, 75),
                              bg=self.background,
                              fg=self.foreground)
        self.locationLabel.grid(row=0, column=0, columnspan=2, sticky=W)


        # Current image
        self.iconImage = Label(self.currentFrame,bg=self.background)
        self.iconImage.grid(row=1, column=0, rowspan=2, sticky=NE)

        # Current temp label
        self.currentTempLabel = Label(self.currentFrame,
                                 font=(self.Font1,80),
                                 bg=self.background,
                                 fg=self.foreground)
        self.currentTempLabel.grid(row=1, column=1)

        # Current status label
        self.currentStatusLabel = Label(self.currentFrame,
                                   font=(self.Font1,45),
                                   bg=self.background,
                                   fg=self.foreground)
        self.currentStatusLabel.grid(row=2, column=1, sticky=N)

        # Forecast info arrays
        self.dayNames = []
        self.dayTemps = []
        self.dayImages = []
        # Day info class references in lists
        for day in range(3):
            # Day names
            self.dayName = Label(self.forecastFrame,
                      font=(self.Font1,60),
                      bg=self.background,
                      fg=self.foreground)
            self.dayName.grid(row=day, column=0, sticky=NW)
            self.dayNames.append(self.dayName)
            # Day temps
            self.dayTemp = Label(self.forecastFrame,
                                 font=(self.Font1,60),
                                 bg=self.background,
                                 fg=self.foreground)
            self.dayTemp.grid(row=day, column=1)
            self.dayTemps.append(self.dayTemp)
            # Day images
            self.dayImage = Label(self.forecastFrame,
                                  bg=self.background)
            self.dayImage.grid(row=day, column=2)
            self.dayImages.append(self.dayImage)

        # Update variable to only update weather once every 5 minutes
        # Time display is updated every second
        self.updateCounter = 0

        # Call draw GUI function
        self.drawGUI()
        self.root.mainloop()

    def drawGUI(self):
        # Draw Time
        # Display and hide the colon every second
        if self.updateCounter % 2 == 0:
            time = strftime('%-I:%M %p ', localtime())
        else:
            time = strftime('%-I %M %p ', localtime())
        self.timeLabel.configure(text=time)

        # Set date
        self.dateLabel.configure(text= strftime('%-d %b %Y', localtime()))

        """ Update all weather info every 5 minutes"""
        # Only update after update counter has reached 5 minutes
        if self.updateCounter == 0 or self.updateCounter == 5*60:
            # Reset counter so that it won't update twice at 5 minutes
            self.updateCounter = 1

            # Get current info from http call
            ssl._create_default_https_context = ssl._create_unverified_context
            webText = urlopen(self.weatherURL)
            data = webText.read()
            encoding = webText.info().get_content_charset('utf-8')
            weatherDictionary = json.loads(data.decode(encoding))

            # File for work offline
            # f = 'baltimore.json'
            # with open(f,'r') as f:
            #     weatherDictionary = json.loads(f.read())

            # Location string
            location = 'Baltimore'
            self.locationLabel.configure(text=location)

            # Current weather data
            currentWeather = weatherDictionary['current']
            # 3 day forecast data
            forecast = weatherDictionary['daily']

            # Current weather image
            icon = currentWeather['weather'][0]['main']
            photoImage = PhotoImage(file=self.icon_match(icon))
            self.iconImage.configure(image=photoImage)
            self.iconImage.image = photoImage

            # Current weather temperature
            # Temp string
            currentTemp = str(int(self.kToF(currentWeather['temp'])))
            self.currentTempLabel.configure(text=currentTemp)

            # Current status string
            currentStatus = currentWeather['weather'][0]['main']
            self.currentStatusLabel.configure(text=currentStatus)

            for day in range(1, 4):
                # Draw day name
                dayName = datetime.fromtimestamp(forecast[day]["dt"]).strftime('%a')
                dayName = dayName.upper() + ' '
                self.dayNames[day - 1].configure(text=dayName)
                # Draw forecast temps
                tempHigh = str(int(self.kToF(forecast[day]['temp']['max'])))
                tempLow = str(int(self.kToF(forecast[day]['temp']['min'])))
                dayTempString = tempHigh + ' \n' + tempLow + ' '
                self.dayTemps[day - 1].configure(text=dayTempString)
                # Draw forecast image
                icon = forecast[day]['weather'][0]['main']
                photoImage = PhotoImage(file=self.icon_match(icon))
                self.dayImages[day - 1].configure(image=photoImage)
                self.dayImages[day - 1].image = photoImage
        self.updateCounter += 1
        self.root.after(1000, self.drawGUI)

    def kToF(self, kelvin):
        fahrenheit = (kelvin - 273.15) * (9 / 5) + 32
        return fahrenheit

    def icon_match(self, icon):
        icons = {
            'Ash': 'images/partcloudy.gif',
            'Clear': 'images/sun.gif',
            'Clouds': 'images/cloudy.gif',
            'Drizzle': 'images/rain.gif',
            'Dust': 'images/partcloudy.gif',
            'Fog': 'images/partcloudy.gif',
            'Haze': 'images/partcloudy.gif',
            'Mist': 'images/partcloudy.gif',
            'Rain': 'images/rain.gif',
            'Sand': 'images/partcloudy.gif',
            'Smoke': 'images/partcloudy.gif',
            'Snow': 'images/snow.gif',
            'Thunderstorm': 'images/thunderstorm.gif',
            'Tornado': 'images/wind.gif'
        }
        match = icons[icon]
        if match:
            return match
        else:
            return 'images/sun.gif'


# Create frame
smartMirror = smartMirror()
