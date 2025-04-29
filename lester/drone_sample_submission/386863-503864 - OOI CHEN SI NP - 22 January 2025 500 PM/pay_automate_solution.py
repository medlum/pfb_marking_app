from pathlib import Path
import csv

#--------------- PART 1: This part of the program is completed for you --------------#

# create a file path to csv file.
fp = Path.cwd()/"DroneShow.csv"

# create an empty list for drone show records
DroneShowRecords=[] 

# read the csv file.
with fp.open(mode="r", encoding="UTF-8", newline="") as file:
    reader = csv.reader(file)
    next(reader) # skip header

    # append drone show record into the DroneShowRecords list
    for row in reader:
        #get the Order No., program, drones, duratoin, complexity for each record
        #and append to the DroneShowRecords list
        DroneShowRecords.append([row[0],row[1],row[2],row[3],row[4]])   


#---------------------------- PART 2: Insert your own code ---------------------------#
# 1. Calculate the revenue for each show according to the requirements
# 2. At the same time, total up the revenue, number of sales, number of drones used
#    duration for each program to get the top 5 programs
# 3. Use functions to organize your code

#define a funciton to remove "." from program
def clean_program(program):
     program=program.replace('.','').strip()
     return program

#define a funciton to extract duration
def getDuration(duration):
     duration=duration.replace("minutes", "").strip()
     return float(duration)

#define a funciton to calculate charges for drones used
def CalculateDroneFees(drones):
     droneFee = 10000
     if drones > 100:
          drones -= 100
          block = drones//30
          if drones%30 > 0:
               block += 1
          droneFee += block * 2000
     return droneFee

#define a funciton to calculate charges for duration
def CalculateDurationFees(duration):
     durationFee = 3000
     if duration > 14:
          duration -= 14
          durationFee += 5000 + 7500 + duration * 3000
     elif duration > 12:
          durationFee += 5000 + 7500
     elif duration > 10:
          durationFee += 5000
     return durationFee

#Adictionary for complexity fee
complexityFees={
     "Simple": 3000,
     "Medium": 7000,
     'High': 15000,
     "Very High": 35000
}

droneShowSummary={}
#Calculate the boxes picked, profit per order, commission per order
for Record in DroneShowRecords:
     program_id=clean_program(Record[1])
     dronesUsed=int(Record[2])
     duration=getDuration(Record[3])
     complexity=Record[4]

     droneFee=CalculateDroneFees(dronesUsed)
     duratoinFee=CalculateDurationFees(duration)
     complexityFee=complexityFees[complexity]

     if not (program_id in droneShowSummary):
          #use list for summary info, can use dictionary as well
          #[program, revenue,number_of_sales, average_revenue]
          droneShowSummary[program_id]={ #record 1 is staff id
               'revenue': 0,
               'no_of_sales': 0,
               'average_revenue': 0,
               'no_of_drones': 0,
               'total_duration': 0
          }     
     
     
     #add revenue and number of sales
     droneShowSummary[program_id]['revenue'] += droneFee + duratoinFee + complexityFee
     droneShowSummary[program_id]['no_of_sales'] += 1
     droneShowSummary[program_id]['no_of_drones'] += dronesUsed
     droneShowSummary[program_id]['total_duration'] += duration

     if not (program_id in droneShowSummary):
          droneShowSummary[program_id] = 0
     
#To find the top 5 programs, we can use the sorted with lamda and key feature
#However, as we do not have time to teach students on these more advance
#we just play a trick to work around the dictionary. This will also teach
#students we need to be flexible in solving problem when tools are not available
#Swap the key and value in the dictionary for sorting to get top 5 programs
topProgram = []

for key, value in droneShowSummary.items():
     topProgram.append([value['revenue'], key])

topProgram.sort(reverse=True)

#---------------------------- PART 3: Insert your own code ---------------------------#
# 1. Write the calculated info to a txt file. Name it as DroneSummary.txt
fp_txt = Path.cwd()/"DroneSummary.txt"
with fp_txt.open(mode="w", encoding="UTF-8") as file:
     file.write("FantaxySky Drone Air Show Summary\n")
     file.write("==================================\n")
     file.write("Program,Revenue,Number_of_Sales,Average_Revenue,Total_Number_of_Drones, Total_Duration\n")
     for program in sorted(droneShowSummary):
          info=droneShowSummary[program]
          file.write(f"{program},{info['revenue']:.2f},{info['no_of_sales']:.0f},{info['revenue']/info['no_of_sales']:.2f},{info['no_of_drones']:.0f}, {info['total_duration']:.0f}\n")


     number_of_program=len(topProgram) #in case, there are fewer than 5 programs
     if number_of_program > 5:
          top_of_program = 5   #To ensure we don't try to get more that what we have
     else:
          top_of_program = number_of_program
     file.write(f'\n\nTop {top_of_program} of {number_of_program} programs\n')
     file.write('===================\n')
     for program in topProgram[:top_of_program]:
          file.write(f"{program[0]:.2f},{program[1]}\n")
         



