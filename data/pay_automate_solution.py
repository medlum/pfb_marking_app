from pathlib import Path
import csv

# --------------- PART 1: This part of the program is completed for you --------------#

# create a file path to csv file.
fp = Path.cwd()/"DeliveryRecords.csv"

# create an empty list for drone show records
DeliveryRecords = []

# read the csv file.
with fp.open(mode="r", encoding="UTF-8", newline="") as file:
    reader = csv.reader(file)
    next(reader)  # skip header

    # append drone show record into the DeliveryRecords list
    for row in reader:
        # get the Route No, Station, Packages, Distance, Zone Complexity, Delivery Status and Late Time
        # and append to the DeliveryRecords list
        DeliveryRecords.append(
            [row[0], row[1], row[2], row[3], row[4], row[5], row[6]])


# ---------------------------- PART 2: Insert your own code ---------------------------#
# 1. Calculate efficiently the earning per route based on the requirement.
# 2. At the same time, accumulate the total earnings, total number of routes,
#           total packages delivered, and total distance covered for every
#           delivery station. Then get the top 5 stations.
# 3. Use functions to organize your code


# define a funciton to remove ".", ":" from column data
def clean_data(rawData):

    data = rawData.replace('.', '').replace(':', '').strip()
    print(rawData, data)
    return data


# Route No,Station,Distance (km),Zone Complexity,Delivery Status,Late Time (minutes)
# define a funciton to calculate charges for packages used
def CalculatePkgFees(pkgs):
    pkgFee = 150
    if pkgs > 20:
        pkgs -= 20
        block = pkgs//10
        if pkgs % 10 > 0:
            block += 1
        pkgFee += block * 40
    return pkgFee

# define a funciton to calculate charges for distance


def CalculateDistanceFees(distance):
    distanceFee = 80
    if distance > 25:
        distance -= 25
        distanceFee += 120 + 180 + distance * 25
    elif distance > 20:
        distanceFee += 120 + 180
    elif distance > 15:
        distanceFee += 120
    return distanceFee

# define a funciton to calculate late penalty


def CalculateLatePenalty(minute):
    latePenalty = 0
    if 0 < minute <= 60:
        latePenalty -= 75
    elif minute <= 120:
        latePenalty -= 150
    else:
        latePenalty = -300
    return latePenalty


# Adictionary for zone complexity fee
complexityFees = {
    "Residential": 25,
    "Commercial": 60,
    'Industrial': 120,
    "High-Security": 250
}

DeliverySummary = {}
# Calculate the boxes picked, profit per order, commission per order
for Record in DeliveryRecords:
    station = clean_data(Record[1])
    pkgs = int(clean_data(Record[2]))
    distance = float(clean_data(Record[3]))
    complexity = clean_data(Record[4])
    lateMinutes = float(clean_data(Record[6]))

    pkgFee = CalculatePkgFees(pkgs)
    distanceFee = CalculateDistanceFees(distance)
    complexityFee = complexityFees[complexity]
    latePenalty = CalculateLatePenalty(lateMinutes)
    earning = 0
    if latePenalty > -300:  # -300 means deliver is cancelled
        earning = pkgFee + distanceFee + complexityFee + latePenalty
    else:
        earning = -300

    if not (station in DeliverySummary):
        # use list for summary info, can use dictionary as well
        # [total earning, total number of routes, total packages delivered, and total distance, station]
        DeliverySummary[station] = [0, 0, 0, 0, station]

    # add revenue and number of sales
    DeliverySummary[station][0] += earning
    DeliverySummary[station][1] += 1
    DeliverySummary[station][2] += pkgs
    DeliverySummary[station][3] += distance


# To find the top 5 programs
# there is no need to use lambda or key= feature
# we can just sort the dictionary value list and the station is already included in the list item
topStation = sorted(DeliverySummary.values(), reverse=True)

# for key, value in DeliverySummary.items():
#      topStation.append([value['revenue'], key])

# topStation.sort(reverse=True)

# ---------------------------- PART 3: Insert your own code ---------------------------#
# 1. Write the calculated info to a txt file. Name it as DroneSummary.txt
fp_txt = Path.cwd()/"DeliverySummary.txt"
with fp_txt.open(mode="w", encoding="UTF-8") as file:
    file.write("DeliveryMax Summary\n")
    file.write("===================\n")
    file.write(
        "Station,Total_Earning,Total_Packages,Number_of_Routes,Total_Distance\n")
    for station in sorted(DeliverySummary):
        info = DeliverySummary[station]
        file.write(
            f"{station},{info[0]:.2f},{info[1]},{info[2]},{info[3]:.2f}\n")

    # in case, there are fewer than 5 programs
    number_of_Station = len(topStation)
    if number_of_Station > 5:
        top_of_Station = 5  # To ensure we don't try to get more that what we have
    else:
        top_of_Station = number_of_Station
    file.write(f'\n\nTop {top_of_Station} of {number_of_Station} programs\n')
    file.write('===================\n')
    for station in topStation[:top_of_Station]:
        # file.write(station)
        file.write(f"{station[-1]},{station[0]:.2f}\n")
