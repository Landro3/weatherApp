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
        self.weatherURL = 'http://api.wunderground.com/api/3c8e35eb14de7c47/forecast/geolookup/conditions/q/MD/Baltimore.json'
        self.workoutURL = 'http://www.bluecrabcrossfit.com/hanover/wod/'

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

        # Create workout info frame to go below current timeFrame
        self.workoutFrame = Frame(self.root)
        self.workoutFrame.configure(background=self.background)
        self.workoutFrame.grid(row=2, column=1, sticky=E)

        # Time Label
        self.timeLabel = Label(self.timeFrame,
                          font=(self.Font1,120),
                          bg=self.background,
                          fg=self.foreground)
        self.timeLabel.pack()

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

        # Workout label
        self.workoutLabel = Label(self.workoutFrame,
                                  font=(self.Font1,40),
                                  bg=self.background,
                                  fg=self.foreground)
        self.workoutLabel.pack()

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
            time = strftime('%I:%M %p ', localtime())
        else:
            time = strftime('%I %M %p ', localtime())
        self.timeLabel.configure(text=time)

        """ Update all weather info every 5 minutes"""
        # Only update after update counter has reached 5 minutes
        if self.updateCounter == 0 or self.updateCounter == 5*60:
            # Reset counter so that it won't update twice at 5 minutes
            self.updateCounter = 1
            # Get current info from http call
            webText = urlopen(self.weatherURL)
            data = webText.read()
            encoding = webText.info().get_content_charset('utf-8')
            weatherDictionary = json.loads(data.decode(encoding))

            # Get workout info from http call
            webText = urlopen(self.workoutURL)
            workoutText = webText.read().decode('utf-8')


            """ File for work offline
            f = 'baltimore.json'
            with open(f,'r') as f:
            weatherDictionary = json.loads(f.read())
            """

            # Location string
            location = weatherDictionary['location']['city']
            self.locationLabel.configure(text=location)

            # Current weather data
            currentWeather = weatherDictionary['current_observation']
            # 3 day forecast data
            forecast = weatherDictionary['forecast']['simpleforecast']['forecastday']

            # Current weather image
            icon = currentWeather['icon']
            photoImage = PhotoImage(file=self.icon_match(icon))
            self.iconImage.configure(image=photoImage)
            self.iconImage.image = photoImage

            # Current weather temperature
            # Temp string
            currentTemp = str(int(currentWeather['temp_f']))
            self.currentTempLabel.configure(text=currentTemp)

            # Current status string
            currentStatus = currentWeather['weather']
            self.currentStatusLabel.configure(text=currentStatus)

            for day in range(3):
                # Draw day name
                dayName = forecast[day]['date']['weekday_short']
                dayName = dayName.upper() + ' '
                self.dayNames[day].configure(text=dayName)
                # Draw forecast temps
                tempHigh = forecast[day]['high']['fahrenheit']
                tempLow = forecast[day]['low']['fahrenheit']
                dayTempString = tempHigh + ' \n' + tempLow + ' '
                self.dayTemps[day].configure(text=dayTempString)
                # Draw forecast image
                icon = forecast[day]['icon']
                photoImage = PhotoImage(file=self.icon_match(icon))
                self.dayImages[day].configure(image=photoImage)
                self.dayImages[day].image = photoImage


            '''
            for c in string:
                if c == '>':
                    print(c)
                elif c != '\n' and c != '\t':
                    print(c, end="")
            '''
            # Header above workout text
            i = workoutText.find("<h2>Blue")

            # Run until finding the end of the text
            workoutString = ""
            while workoutText [i:i+2] != '<a':
                if workoutText[i] == '>':
                    i += 1
                elif workoutText[i] == '<':
                    i += 1
                    while workoutText[i] != '>':
                        i += 1
                elif workoutText[i:i+5] == "&#37;":
                    workoutString += "%"
                    # print("%", end="")
                    i += 5
                elif workoutText[i:i+6] == "&#215;":
                    workoutString += "x"
                    print("x", end="")
                    i += 6
                elif workoutText[i:i+7] == "&#8211;":
                    workoutString += "-"
                    # print("-", end="")
                    i += 7
                else:
                    workoutString += workoutText[i]
                    # print(string[i], end="")
                    i += 1
            self.workoutLabel.configure(text=workoutString, justify=RIGHT)
        self.updateCounter += 1
        self.root.after(1000, self.drawGUI)


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
