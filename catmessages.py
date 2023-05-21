import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

start_date = datetime(2020, 3, 18, 3, 37)
end_date = datetime.now()
smoothness_factor = 1

date_dict = {}

current_date = start_date
while current_date <= end_date:
    date_dict[current_date.strftime("%d-%b-%y")] = 0
    current_date += timedelta(days=1)

lastdate = ""
keyterm = "nya"

# Read the text file and process each line
with open("PC Gang - General - pc-pics [689739087581544556].txt", "r", encoding="utf-8") as file:
    for line in file:
        try:
            # Extract the timestamp and message
            if line.startswith("[") and "]" in line:
                lastdate = line.split("]")[0].split(" ")[0].strip("[")
            if keyterm in line.lower():
                date_dict[lastdate] += 1
        except KeyError:
            pass

dates = list(date_dict.keys())
values = list(date_dict.values())

# Apply moving average smoothing
moving_avg = np.convolve(values, np.ones(smoothness_factor) / smoothness_factor, mode='same')

plt.plot(dates, moving_avg)
plt.xlabel('Date')
plt.ylabel(f'{keyterm} messages a day')

if(smoothness_factor > 1):
    plt.title(f'The frequency of the term "{keyterm}" in #general over time (Smoothed)')
else:
    plt.title(f'The frequency of the term "{keyterm}" in #general over time')

plt.xticks(rotation = 45)
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(20))
plt.tight_layout()
plt.show()
