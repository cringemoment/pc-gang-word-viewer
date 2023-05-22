import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

start_date = datetime(2020, 3, 18, 3, 37)
end_date = datetime.now()
smoothness_factor = 50

date_dict = {}

current_date = start_date

lastdate = ""
keyterms = ["legs", "feet"]

while current_date <= end_date:
    date_dict[current_date.strftime("%d-%b-%y")] = {}
    for keyterm in keyterms:
        date_dict[current_date.strftime("%d-%b-%y")][keyterm] = 0
    date_dict[current_date.strftime("%d-%b-%y")]["total"] = 0
    current_date += timedelta(days=1)

channel = "#general"

allchannels = {
"#general": "PC Gang - General - general [569728778985537587].txt",
"#pc-pics": "PC Gang - General - pc-pics [689739087581544556].txt",
"#pc-research": "PC Gang - Research - pc-research [569730931544293395].txt"
}

# Read the text file and process each line
with open(allchannels[channel], "r", encoding="utf-8") as file:
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
allvalues = []

for keyterm in keyterms:
    values = []
    for i in date_dict:
        values.append(date_dict[i][keyterm]/date_dict[i]["total"] * 100 if date_dict[i]["total"] != 0 else 0)
    moving_avg = np.convolve(values, np.ones(smoothness_factor) / smoothness_factor, mode='same')
    plt.plot(dates, moving_avg, label = keyterm)
    allvalues.append(values)

allvalues = np.array(allvalues)
r = np.corrcoef(allvalues)[0, 1]

leg = plt.legend(loc='upper left')

plt.xlabel('Date')
plt.ylabel(f'Share of messages a day containing a keyterm')

if(smoothness_factor > 1):
    plt.title(f'The share of key terms in {channel} over time (Every {smoothness_factor} days)')
else:
    plt.title(f'The share of key terms in {channel}l over time')

plt.xticks(rotation = 45)
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}%'))
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(20))
plt.tight_layout()

plt.text(0.9, 0.05, f'r = {r:.2f}', ha='center', va='center', transform=plt.gca().transAxes)

plt.show()
