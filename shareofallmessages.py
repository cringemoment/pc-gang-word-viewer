import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

start_date = datetime(2020, 3, 18, 3, 37)
end_date = datetime.now()
smoothness_factor = 7

date_dict = {}

current_date = start_date

lastdate = ""
keyterms = ["jaw", "leg", "hill"]

while current_date <= end_date:
    date_dict[current_date.strftime("%d-%b-%y")] = {}
    for keyterm in keyterms:
        date_dict[current_date.strftime("%d-%b-%y")][keyterm] = 0
    date_dict[current_date.strftime("%d-%b-%y")]["total"] = 0
    current_date += timedelta(days=1)

# Read the text file and process each line
with open("PC Gang - General - pc-pics [689739087581544556].txt", "r", encoding="utf-8") as file:
    for line in file:
        try:
            # Extract the timestamp and message
            if line.startswith("[") and "]" in line:
                lastdate = line.split("]")[0].split(" ")[0].strip("[")
            else:
                for keyterm in keyterms:
                    if keyterm in line.lower():
                        date_dict[lastdate][keyterm] += 1
                if(not line == ""):
                    date_dict[lastdate]["total"] += 1
        except KeyError:
            pass

dates = list(date_dict.keys())

for keyterm in keyterms:
    values = []
    for dateindex, i in enumerate(date_dict):
        values.append(sum([date_dict[j][keyterm] for j in list(date_dict.keys())[:dateindex]]))

    values = [i/sum([date_dict[j]["total"] for j in list(date_dict.keys())[:dateindex]]) * 100 for i in values]

    moving_avg = np.convolve(values, np.ones(smoothness_factor) / smoothness_factor, mode='same')
    plt.plot(dates, moving_avg, label = keyterm)

leg = plt.legend(loc='upper left')

plt.xlabel('Date')
plt.ylabel(f'Messages a day containing a keyterm')

if(smoothness_factor > 1):
    plt.title(f'The frequency of key terms in #general over time (Every {smoothness_factor} days)')
else:
    plt.title(f'The frequency of key terms in #general over time')

plt.xticks(rotation = 45)
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}%'))
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(20))
plt.tight_layout()
plt.show()
