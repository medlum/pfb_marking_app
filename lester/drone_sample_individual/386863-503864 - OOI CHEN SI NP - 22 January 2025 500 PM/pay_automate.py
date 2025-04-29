from pathlib import Path
import csv

#####  Store your name, email, student_id and class_number as STRINGS #####
exercise = "Individual Assignment"
name = "ooi chen si"
np_email = "s10259035@connect.np.edu.sg"
student_id = "s102590356d"
class_number = "tc05"

#--------------- PART 1: Reading the CSV File --------------#
# Create a file path to the CSV file.
csv_file_path = Path.cwd() / "SpaceUsage.csv"

# Read the CSV file and store records
UsageRecords = []
with csv_file_path.open(mode="r", encoding="UTF-8", newline="") as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row

    # Append usage record into the UsageRecords list
    for row in reader:
        UsageRecords.append([row[0], row[1], row[2], row[3], row[4], row[5]])

print(UsageRecords[:30])

#--------------- PART 2: Processing the Data --------------#

# create dictionaries to store staff and SKU data
staff_salaries = {}
sku_boxes = {}

# create a function to calculate commission based on profit
def calculate_commission(profit):
    commission = 0
    if profit > 4500:
        commission += (profit - 4500) * 0.06
        profit = 4500
    if profit > 3000:
        commission += (profit - 3000) * 0.05
        profit = 3000
    if profit > 1500:
        commission += (profit - 1500) * 0.04
        profit = 1500
    commission += profit * 0.02
    return commission

# process each record
for record in UsageRecords:
    # extract and convert data types here
    order_no = record[0]
    sku = record[1]
    staff_id = record[2]
    boxes_picked = int(record[3])  # convert boxes picked to int
    unit_cost = float(record[4].replace("S$", ""))  # remove 'S$' and convert to float
    unit_selling = float(record[5].replace("S$", ""))  # remove 'S$' and convert to float
    profit = boxes_picked * (unit_selling - unit_cost)
    commission = calculate_commission(profit)

    # update the staff data
    if staff_id not in staff_salaries:
        staff_salaries[staff_id] = {
            "total_commission": 0,
            "salary": 1000,  # base salary
            "total_boxes": 0,
            "total_profit": 0  # initialize total profit
        }
    staff_salaries[staff_id]["total_boxes"] += boxes_picked
    staff_salaries[staff_id]["total_profit"] += profit  # add profit to total profit
    staff_salaries[staff_id]["total_commission"] += commission
    staff_salaries[staff_id]["salary"] += commission

    # update SKU data
    if sku not in sku_boxes:
        sku_boxes[sku] = 0
    sku_boxes[sku] += boxes_picked

# identify the top 5 SKUs by total boxes picked
def get_box_count(item):
    return item[1]
top_5_skus = sorted(sku_boxes.items(), key= get_box_count, reverse=True)[:5]

#--------------- PART 3: Writing the Output --------------#
# Sort staff data by staff ID in ascending order
sorted_staff_data = sorted(staff_salaries.items())

# write the summary into a text file
summary_file_path = Path.cwd() / "spaceSummary.txt"
with summary_file_path.open(mode="w", encoding="UTF-8") as file:
    file.write("Efficient Transit Payment Summary\n")
    file.write("=" * 40 + "\n\n")
    
    # staff salary details in ascending order by staff ID
    file.write("Staff Performance Summary:\n")
    file.write("Staff No, Boxes Picked, Profits, Commission, Salary\n")
    for staff_id, data in sorted_staff_data:
        file.write(f"{staff_id}, {data['total_boxes']}, ${data['total_profit']:.2f}, "
                   f"${data['total_commission']:.2f}, ${data['salary']:.2f}\n")
    file.write("\n")

    # top 5 SKUs
    file.write("Top 5 SKUs by Boxes Picked:\n")
    file.write("=" * 40 + "\n")
    for sku, boxes in top_5_skus:
        file.write(f"{sku}: {boxes} boxes\n")

print(f"Summary written to {summary_file_path}")