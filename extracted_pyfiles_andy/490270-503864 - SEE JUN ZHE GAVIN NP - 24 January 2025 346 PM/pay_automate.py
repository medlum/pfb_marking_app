from pathlib import Path
import csv

#####  Store your, name, email, student_id and class_number as STRINGS #####
#exercise = "Individual Assignment"
#name = See Jun Zhe Gavin
#np_email = S10265979@np.connect.edu.sg
#student_id = S10265979B
#class_number = Tc05

##--------------- PART 1: This part of the program is completed for you --------------#

# create a file path to csv file.
fp = Path.cwd()/"SpaceUsage.csv"

# read the csv file.
with fp.open(mode="r", encoding="UTF-8", newline="") as file:
    reader = csv.reader(file)
    next(reader) # skip header

    # create an empty list for tour records
    UsageRecords=[] 

    # append tour record into the tourRecords list
    for row in reader:
        #get the Order No., SKU, Staff, Boxes_Picked, Unit_Cost_Price, Unit_Selling_Price for each record
        #and append to the UsageRecords list
        UsageRecords.append([row[0],row[1],row[2],row[3],row[4],row[5]])   

print(UsageRecords[:30])

#---------------------------- PART 2: Insert your own code ---------------------------#
# 1. Calculate the boxes picked, profit per order, commission per order
# 2. Calculate total boxes picked, total profit, total commission and the salary. 
# 3. At the same time, total up the boxes picked for each SKU to get the top 5 SKUs
total_boxes_picked = 0
total_profit = 0
total_commission = 0
staff_data = {}
sku_data = {}

def calculate_profit(order):
    usp = float(order[5].replace("S$", ''))
    ucp = float(order[4].replace("S$", ''))
    qty = int(order[3])
    return (usp - ucp) * qty

def initialize_sku_count(order):
    if order[1] in sku_data:
        sku_data[order[1]] += int(order[3])
    else:
        sku_data[order[1]] = int(order[3])

def create_staff_dict(order):
    staff_id = order[2]
    if staff_id not in staff_data:
        staff_data[staff_id] = {
            "total_boxes_picked": 0,
            "total_profit": 0,
            "total_commission": 0,
            "total_salary": 1000
        }

for record in UsageRecords:
    order_no, sku, staff_id, boxes_picked, unit_cost, unit_sell = record
    boxes_picked = int(boxes_picked)
    unit_cost = float(unit_cost[2:])
    unit_sell = float(unit_sell[2:])

    # Calculate profit
    profit = calculate_profit(record)

    # Calculate commission
    commission = 0
    remaining_profit = profit
    if remaining_profit > 1500:
        commission += 1500 * 0.02
        remaining_profit -= 1500
        if remaining_profit > 1500:
            commission += 1500 * 0.04
            remaining_profit -= 1500
            if remaining_profit > 1500:
                commission += 1500 * 0.05
                remaining_profit -= 1500
                commission += remaining_profit * 0.06
            else:
                commission += remaining_profit * 0.05
        else:
            commission += remaining_profit * 0.04
    else:
        commission += remaining_profit * 0.02
    #round commission to 2 decimal places
    commission = round(commission,2)
    # Update staff data
    create_staff_dict(record)
    staff_data[staff_id]["total_boxes_picked"] += boxes_picked
    staff_data[staff_id]["total_profit"] += profit
    staff_data[staff_id]["total_commission"] += commission
    staff_data[staff_id]["total_salary"] += commission

    # Update SKU data
    initialize_sku_count(record)

# Calculate total boxes picked
total_boxes_picked = sum(sku_data.values())

# Get top 5 SKUs
sku_count = {sku: count for sku, count in sku_data.items()}
top_sku = []
for sku in sku_count:
    top_sku.append([sku_count[sku], sku])
top_sku.sort(reverse=True)

# Sort staff data by staff ID
staff_dict = {staff: data for staff, data in staff_data.items()}
sorted_staff = []
for staff in staff_dict:
    sorted_staff.append(staff)
sorted_staff.sort()

# Output
print("Top 5 SKUs:", top_sku[:5])
print("Sorted Staff Data:", sorted_staff)


#---------------------------- PART 3: Write to a text file ---------------------------
# 1. Write the calculated info to a txt file. Name it as spaceSummary.txt
fp = Path.cwd() / "spaceSummary.txt"

# write the summary to the text file
with fp.open(mode="w", encoding="UTF-8", newline="") as file:
    file.writelines("Efficient Transit Payment Summary\n")
    file.writelines("==================================\n")
    file.write("Staff,Boxed Picked,Profits,Commission,Salary\n")

    for staff in sorted_staff:
        qty = staff_data[staff]["total_boxes_picked"]
        profit = staff_data[staff]["total_profit"]
        commission = staff_data[staff]["total_commission"]
        salary = staff_data[staff]["total_salary"]

        file.write(f"{staff},{qty},{profit:.2f},{commission:.2f},{salary:.2f}\n")
    file.write('\n')

    file.write("Top 5 of 20 SKUs\n")
    file.write("=================\n")
    for sku in top_sku[0:5]:
        file.write(f"{sku[0]},{sku[1]}\n")
