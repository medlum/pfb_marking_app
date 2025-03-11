from pathlib import Path
import csv

#####  Store your, name, email, student_id and class_number as STRINGS #####
#exercise = "Individual Assignment"
# name = Koay Yu Xiang
# np_email = S10265857@connect.np.edu.sg
# student_id = S10265857G
# class_number = TC05

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

#create a function to calculate datas needed
def data_calculator(data):
    """
    -This function returns data calculated
    -1 parameter, data, which allows the different datas from the calculator to be selected
    """
    #create dictionary to store staff details
    staff_dict = {}
    #create dictionary to count boxes picked per SKU
    sku_num = {}

    #iterate over rows in the data
    for row in data:

        #convert boxes picked to integer
        boxes_picked = int(row[3])

        #strip currency symbol and convert unit cost price to a float
        unit_cost_price = float(row[4][2:])

        #strip currency symbol and convert unit cost price to a float
        unit_selling_price = float(row[5][2:])

        #calculate profit
        staff_profit = (unit_selling_price - unit_cost_price) * boxes_picked

        #initialize staff data if it is not in the dictionary
        if row[2] not in staff_dict:
            staff_dict[row[2]] = {"staff_boxes": 0, "staff_profit": 0, "staff_commission": 0 }
        
        #update data
        staff_dict[row[2]]["staff_boxes"] += boxes_picked
        staff_dict[row[2]]["staff_profit"] += staff_profit
        
        #calculate commission
        staff_commission = 0
        remaining_profit = staff_profit

        #set commission rates
        if remaining_profit > 4500:
            staff_commission += (remaining_profit - 4500) * 0.06
            remaining_profit = 4500

        elif remaining_profit > 3000:
            staff_commission += (remaining_profit - 3000) * 0.05
            remaining_profit = 3000

        elif remaining_profit > 1500:
            staff_commission += (remaining_profit - 1500) * 0.04
        else:
            remaining_profit = 1500

        staff_commission += remaining_profit * 0.02


        #round and update commission
        staff_commission = round(staff_commission,2)
        staff_dict[row[2]]["staff_commission"] += staff_commission

        #calculate and store data
        staff_dict[row[2]]["salary"] = round(1000 + staff_dict[row[2]]["staff_commission"], 2)

        #update SKU num
        sku = row[1]
        if sku not in sku_num:
            sku_num[sku] = 0
        sku_num[sku] += boxes_picked

    #Convert staff data dictionary into a sorted list
    staff_dict = list(staff_dict.items())
    staff_dict.sort()

    #create function to get the top 5 SKUs by box count
    def top_skus_calculator(sku_num):
        """
        -this function returns the top 5 SKUs
        -1 parameter, sku_num
        """
        #convert the dictionary to a list
        sku_list = list(sku_num.items())

        #create a list to store the top 5 SKUs
        top_skus = []

        #create a while loop that stops once it stores the top 5 SKUs
        while len(top_skus) < 5 and sku_list:
            max_skus = sku_list[0]
            for sku in sku_list:
                if sku[1] > max_skus[1]:
                    max_skus = sku

            top_skus.append(max_skus)
            sku_list.remove(max_skus)

        #return the top 5 SKUs
        return top_skus

    #call the function with SKU num
    top_skus = top_skus_calculator(sku_num)

    #return the data 
    return staff_dict, top_skus

#Use the `commission_calculator` function to calculate and retrieve data
staff_dict, top_skus = data_calculator(UsageRecords)




#---------------------------- PART 3: Insert your own code ---------------------------#
# 1. Write the calculated info to a txt file. Name it as spaceSummary.txt

file_path = Path.cwd() / "spaceSummary.txt"

# Create and write to the 'spaceSummary.txt' file
with file_path.open(mode ='w', encoding = 'UTF-8') as file:
    # Efficient Transit Payment Summary
    file.write("Efficient Transit Payment Summary\n")
    file.write("============================================\n")
    file.write("Staff,Boxes Picked,Profits,Commission,Salary\n")

    for staff, data  in staff_dict:
        file.write(
            f"{staff},{data['staff_boxes']},"  
            f"{data['staff_profit']:.2f},"
            f"{data['staff_commission']:.2f},"
            f"{data['salary']:.2f}\n"
        )
    # Top 5 SKUs
    file.write("\nTop 5 of 20 SKUs\n")
    file.write("====================\n")

    for i, (sku, boxes) in enumerate(top_skus, start=1):
        file.write(f"{boxes}, {sku}\n")

