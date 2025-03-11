from pathlib import Path
import csv

#####  Store your, name, email, student_id and class_number as STRINGS #####
#exercise = "Individual Assignment"
#name = Nur Dini Balqis Binte Ahmad Badaruddin
#np_email = s10259030@connect.np.edu.sg
#student_id = S10259030J
#class_number = TC05

#--------------- PART 1: This part of the program is completed for you --------------#

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

# To convert the list provided in part 1 to dictionary
def convert_to_dictionary(input):
    output = []
    for order in UsageRecords:
        convertedOrder = {
            "SKU": str(order[1]),
            "StaffID": str(order[2]),
            "BoxesPicked": int(float(order[3])),
            "UnitCostPrice": float(order[4][2:]),
            "UnitSellingPrice": float(order[5][2:])
        }
        output.append(convertedOrder)
    return(output)

# To calculate profit for each order
def calculate_profit(order):
    return round((order["UnitSellingPrice"] - order["UnitCostPrice"]) * order["BoxesPicked"], 2)

# To calculate commission (based on total profit)
def calculate_commission(total_profit):
    commission = 0
    if total_profit > 4500:
        commission += round((total_profit - 4500) * 0.06, 2)
        total_profit = 4500
    if total_profit > 3000:
        commission += round((total_profit - 3000) * 0.05, 2)
        total_profit = 3000
    if total_profit > 1500:
        commission += round((total_profit - 1500) * 0.04, 2)
        total_profit = 1500
    commission += round(total_profit * 0.02, 2)

    return commission

# To calculate staff commissions and total salary
def process_staff_data(orders):
    # To store results for each staff
    staff_data = {}  
    # To count total boxes for each SKU
    sku_counts = {}  

    for order in orders:
    # Calculate profit for this order
        profit = calculate_profit(order)

    # Update staff data
        staff_id = order["StaffID"]
        if staff_id not in staff_data:
            staff_data[staff_id] = {"BoxesPicked": 0, "TotalProfit": 0, "Commission": 0, "Salary": 1000}
        staff_data[staff_id]["TotalProfit"] += profit
        staff_data[staff_id]["BoxesPicked"] += order["BoxesPicked"]

    # Count boxes picked for each SKU
        sku = order["SKU"]
        if sku not in sku_counts:
           sku_counts[sku] = 0
        sku_counts[sku] += order["BoxesPicked"]

    # Calculate commission and salary for each staff per order
        commission = calculate_commission(profit)
        # salary + commission
        staff_data[staff_id]["Commission"] += commission
        staff_data[staff_id]["Salary"] += commission
        
    return staff_data, sku_counts

#---------------------------- PART 3: Insert your own code ---------------------------#
# 1. Write the calculated info to a txt file. Name it as spaceSummary.txt

# To sort skus in a descending order and return top 5
def sort_skus(sku_counts):
    sorted_skus = []
    for sku in sorted(sku_counts, key=sku_counts.get, reverse=True)[:5]:
        sorted_skus.append((sku, sku_counts[sku]))
    return sorted_skus

# What will appear in the txt file
def write_results(filename, staff_data, sku_counts):
    with open(filename, 'w') as file:
        file.write("Efficient Transit Payment Summary:\n")
        file.write("==================================\n")
        file.write("Staff, Boxes Picked, Profits, Commission, Salary\n")
        for staff_id, data in staff_data.items():
            file.write(f"{staff_id}, {data['BoxesPicked']}, {data['TotalProfit']:.2f}, "
                    f"{data['Commission']:.2f}, {data['Salary']:.2f}\n")
        
        file.write("\nTop 5 of 20 SKUs:\n")
        file.write("==================================\n")
        for sku, boxes in sort_skus(sku_counts):
            file.write(f"{boxes}, {sku}\n")

# Read data from SpaceUsage.csv and store file data rows into a list
def main():
    fp = Path.cwd() / "SpaceUsage.csv"
    with fp.open(mode="r", encoding="UTF-8", newline="") as file:
        reader = csv.reader(file)
        next(reader)
        UsageRecords = [row for row in reader]

    # Changing name to spaceSummary
    output_file = "spaceSummary.txt"   

    # Read orders from CSV
    orders = convert_to_dictionary(UsageRecords)

    # Process staff data and calculate commissions/salaries
    staff_data, sku_counts = process_staff_data(orders)

    # Write results to a plain text file
    write_results(output_file, staff_data, sku_counts)

    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()