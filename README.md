# What will you find
- In this repository there is the Arduino code to collect data on the COM4 port, to configure the Arduino:

![image](https://github.com/BrandonSaraiva/umidade_temperatura_quarto/assets/90096835/40a30f8e-6b7f-4785-a3cb-eeef49a0c87e)

- A folder with the slides from the presentation I made
- A folder that contains the csvs generated by the collections
- The various Python functions that insert data, collect the data, and process the data.
- The getting_data is the function that receives the data of the arduino, the rest in on the folder creating_and_analyze.
- Teste.py makes sure that the site is working well to we collect the actual data of Brasília.

# Intro
The project involved collecting data using the DHT22 sensor, installed in my room. The sensor took temperature and humidity measurements every hour. At the same time, I carried out a web scraping process to obtain information about the current temperature and humidity in Brasília, at the exact time of collection. This information was used to establish a point of comparison between the weather conditions in my room and the city.
# Libraries used:
##Python
- matplotlib
- json
- elasticsearch
- pandas
- os
- chardet
- csv
- requests
- series
- bs4
- datetime
## In the arduino
- Wire.h
- Adafruit_Sensor.h
- DHT.h
- DHT_U.h
- LiquidCrystal_I2C.h

# Operation
Data was collected hourly, from September 21st to November 14th, totaling 1,210 records. At each collection, web scraping was carried out simultaneously to collect current data for Brasília from the website https://weather.com/pt-BR/clima/hoje/l/d99d429a569c3150c4f12a9c12900b06f6a0c0a2fed398fc6c25ae018d0e51c8. Initially, the data was stored in CSV format. They were then subjected to various treatments to transform them into a dataframe, which was then inserted into a database.
# Methodology
I used Elasticsearch as a database for storage. Inserting 1,210 records took less than 1 second, which is an incredibly fast speed. After insertion, the data was queried using the same index and transformed back into a dataframe.
# Analytics
![image](https://github.com/BrandonSaraiva/umidade_temperatura_quarto/assets/90096835/a86bbb6f-4e90-4fec-9bc2-a269d0053812)

The blank spaces in the graph are due to a problem that caused my notebook to restart itself in the early hours of the morning, causing the data to be lost.

We can see that the temperature in the room varies very little. The real temperature, although it generally has the highest temperature peaks, reaches very low values during the early hours of the morning, which makes its average lower. The bedroom, on the other hand, almost never drops below 25 degrees, even in the early hours of the morning.

Therefore, even though the real temperature varies so much, reaching a difference of 15 degrees between its lowest and highest observation, it still has an average much lower than that of the room. While the real average is around 25 degrees, the room average is around 28.5 degrees.

An interesting thing to note is that, after the week of November 10th, the temperature only tended to increase. In recent decades, this behavior was the opposite: the temperature tended to decrease at this time of year due to rain.

![image](https://github.com/BrandonSaraiva/umidade_temperatura_quarto/assets/90096835/8fabf351-1c0b-44ca-880a-45ae8c0bc63d)

The variation in humidity is even more pronounced. The lowest actual observed value was less than 20% and the highest observed value was more than 90%. This high humidity occurs due to rain. As it doesn't rain in my room, the humidity barely exceeds 70%. This may explain why my room's average was lower than actual, even though humidity values are usually higher than actual.

![image](https://github.com/BrandonSaraiva/umidade_temperatura_quarto/assets/90096835/59c53bf0-7210-4f31-9764-8458129ebdb6)

The day of the week that is least hot in my room is Saturday, with an average of 28º. This is 3th more than the city average, which is 25th. The least hot day in Brasília is Friday. The hottest day in my room is Thursday, with an average of 29º. In the city, the hottest day is Tuesday or Sunday.

![image](https://github.com/BrandonSaraiva/umidade_temperatura_quarto/assets/90096835/23df692f-3ab2-467f-b315-9cee9a176e86)

The three hottest times in my room are between 3pm and 5pm, while the three hottest actual temperatures are between 12pm and 2pm. The three coldest times in my room are between 7am and 9am, while the three coldest actual temperatures are between 3am and 5am. It may just be a coincidence, but there seems to be a pattern: the temperature in Brasília takes about three hours to be felt in my room. Another interesting thing is that the three coldest times in my room barely reach 26º, while those in Brasília reach 20º.

![image](https://github.com/BrandonSaraiva/umidade_temperatura_quarto/assets/90096835/56bccb3d-5df6-4734-af18-7072a321867a)

It is interesting to note that the most and least humid times in my room coincide with the coldest and hottest times in Brasília. Likewise, the most and least humid times in Brasília are very close to the most or least cold times in the city. If we were in the North, we would realize that humidity and temperature are not very related. However, here in Brasília, this relationship is very strong, perhaps because it is an extremely dry place.

# Conclusion about the data

The room temperature is, on average, 3.5°C higher than in Brasília, while room humidity is, on average, 4% lower than in Brasília.
