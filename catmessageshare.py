import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

start_date = datetime(2020, 3, 18, 3, 37)
end_date = datetime.now()

date_dict = {}

current_date = start_date
while current_date <= end_date:
    date_dict[current_date.strftime("%d-%b-%y")] = {"total": 0, "cat_count": 0}
    current_date += timedelta(days=1)

keyterm = "ppb"

# Read the text file and process each line
with open("PC Gang - General - general [569728778985537587].txt", "r", encoding="utf-8") as file:
    total_cat_count = 0
    total_message_count = 0
    for line in file:
        # Extract the timestamp and message
        if line.startswith("[") and "]" in line:
            date = line.split("]")[0].split(" ")[0].strip("[")
            if date in date_dict:
                date_dict[date]["total"] = total_message_count
                date_dict[date]["cat_count"] = total_cat_count
        if keyterm in line.lower():
            total_cat_count += 1
        total_message_count += 1

dates = list(date_dict.keys())
percentages = [
    (date_dict[date]["cat_count"] / date_dict[date]["total"]) * 100 if date_dict[date]["total"] != 0 else 0 for date in
    dates]

window_size = 50
moving_avg = np.convolve(percentages, np.ones(window_size) / window_size, mode='same')

plt.plot(dates, moving_avg)
plt.xlabel('Date')
plt.ylabel('Percentage of Cat messages')
plt.title(f'The frequency of the term "{keyterm}" in #general over time')
plt.xticks(rotation=45)
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}%'))
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(20))
plt.tight_layout()
plt.show()
