from pathlib import Path
import csv

#####  Store your, name, email, student_id and class_number as STRINGS #####
#exercise = "Individual Assignment"
#name = Yap Jietong
#np_email = s10259164@connect.np.edu.sg
#student_id = S10259164E
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


def boxesprofitcommissionper_order (UsageRecords):
    """
    This function will calculate the boxes picked, profit and commission earned per order
    """
    for row in (UsageRecords):
        staff_id = row [2]
        boxes_picked = int(row [3])
        unitcost_price = (float(row[4].replace('$','').replace('S','')))
        unitselling_price = (float(row[5].replace('$','').replace('S','')))
        profit = round(boxes_picked * (unitselling_price - unitcost_price),2) #formula to find the profit per order
        commission = {0}
        if profit <= 1500:
            commission = (profit * 0.02) 
        elif profit > 1500 and profit <= 3000:
            commission = (1500 * 0.02 + (profit - 1500)* 0.04) 
        elif profit > 3000 and profit <= 4500:
            #for any values that meets this critera, the code below will calculate the commission earned
            commission = ((1500 * 0.02) + (1500 * 0.04) + (profit-3000)*0.05)
        else:
          commission = ((1500 * 0.02) + (1500 * 0.04) + (1500 * 0.05) + (profit - 4500)*0.06)   
        print (f"{staff_id},{boxes_picked},{(profit):.2f},{(commission):2f}")
        #the staff id, boxes picked, profit and commission will be returned together
boxesprofitcommissionper_order(UsageRecords) # will calculate the boxes picked, profits and commission based on the datas in usagerecords

def totalboxes_profitcommission_salary (UsageRecords):
    """
    This function will calculate and print the total salary earned for each staff
    """
    # create 4 empty lists to store values from for loop
    total_profits_earned = {}
    total_boxes_picked = {}
    total_commission_earned = {}
    total_salary_earned = {}
    for i in range(len(UsageRecords)): # creating a loop 
        staff_id = (UsageRecords[i][2]) # links the variable to the data in usagerecords
        boxes_picked = int(UsageRecords[i][3]) # "int" is added to convert the string into an integer
        unitcost_price = float(UsageRecords[i][4].replace('$','').replace('S','')) # "float" is added to convert the string into a float
        unitselling_price = float(UsageRecords[i][5].replace('$','').replace('S',''))
        profit = (boxes_picked * (unitselling_price - unitcost_price)) # formula to calculate the profits earned
        
        commission = {0} # a conditional is created to calculate the commissions earned based on profits
        if profit <= 1500:
            commission = (profit * 0.02) 
        elif profit >1500 and profit <= 3000:
            commission = (1500 * 0.02) + (profit-1500) * 0.04
        elif profit > 3000 and profit <= 4500:
             #for any values that meets this critera, the code below will calculate the commission earned
            commission = (1500 * 0.02) + (1500 * 0.04) + (profit-3000) * 0.05
        else:
          commission = (1500 * 0.02) + (1500 * 0.04) + (1500 * 0.05) + (profit-4500) * 0.06
        
        
        if profit <= 1500: # a conditional is created to calculate the salary earned based on profits
            salary =  ((profit * 0.02)) 
        elif profit >1500 and profit <= 3000:
            salary =  ((1500 * 0.02) + (profit-1500) * 0.04) 
        elif profit > 3000 and profit <= 4500:
            #for any values that meets this critera, the code below will calculate the commission earned
            salary =  ((1500 * 0.02) + (1500 * 0.04) + (profit-3000) * 0.05) 
        else:
          salary = ((1500 * 0.02) + (1500 * 0.04) + (1500 * 0.05) + (profit-4500)*0.06) 

        if staff_id in total_commission_earned:
            # to check if the staff_id already exists in total_commission_earned and if it does it will add the respective variables together
            total_profits_earned[staff_id] = total_profits_earned[staff_id] + profit 
            total_boxes_picked[staff_id] = total_boxes_picked[staff_id] + boxes_picked
            total_commission_earned[staff_id] = total_commission_earned [staff_id] + commission
            total_salary_earned [staff_id] = total_salary_earned [staff_id] + salary
        else:
            #so if the staff_id does not exists, it will just return the variables with its values for the particular staff_id
            total_profits_earned [staff_id] = profit 
            total_boxes_picked [staff_id] = boxes_picked
            total_commission_earned [staff_id] = commission
            total_salary_earned [staff_id] = salary

    sort_amount = []
    for staff_id in total_commission_earned:
       sort_amount.append(staff_id) # I appended staff_id so that the salary, profits and commission earned by each staff id will be tallied up.
       sort_amount.sort() # this will sort the staff id from ascending order  
    for staff_id in (sort_amount):
     total_amount = [staff_id, # the code is too long so I broke it down
                        total_boxes_picked[staff_id],
                        round(total_profits_earned[staff_id],2),
                        round(total_commission_earned[staff_id],2),
                        round(total_salary_earned[staff_id],2)+1000 # adding $1000 to find total salary earned
                         ] 
     print (total_amount)
totalboxes_profitcommission_salary(UsageRecords) # will calculate the total boxes picked, profits, commission and salary based on the datas in usagerecords
      
def total_boxesperskus(UsageRecords):
    """
    This function will calculate the total number of boxes picked by each SKU, and sort it by top 5 highest boxes picked
    """
    total_boxes_picked = {}
    for i in range(len(UsageRecords)): #creating a loop
        skus = (UsageRecords[i][1])
        boxes_picked = int(UsageRecords[i][3])
        if skus in total_boxes_picked: # to check if skus already exists in total_boxes_picked and if it does it will add the respective variables together
           total_boxes_picked[skus] = total_boxes_picked[skus] + boxes_picked
        else:
           total_boxes_picked[skus] = boxes_picked #so if skus does not exists, it will just return the variables with its values for the particular sku

    sort_topskus = []
    for skus in total_boxes_picked:
       sort_topskus.append(skus)
    sort_topskus.sort(reverse=True) # sorts the value in descending order
    for skus in sort_topskus[:5]: #will sort the top 5 out of the 20 in the code generated
     boxes_picked = total_boxes_picked[skus] 
      
     print (f"{boxes_picked},{skus}")
total_boxesperskus(UsageRecords) # this will calculate the total boxes picked per skus based on the data in UsageRecords
 



#---------------------------- PART 3: Insert your own code ---------------------------#
# 1. Write the calculated info to a txt file. Name it as spaceSummary.txt
from pathlib import Path
def totalboxes_profitcommission_salary(UsageRecords): #used the code from part 2 to write into the txt file
    """
    This function will calculate and print the total salary earned for each staff and write the output to a file.
    """
    # create 4 empty lists to store values from for loop
    total_profits_earned = {}
    total_boxes_picked = {}
    total_commission_earned = {}
    total_salary_earned = {}
  
    for i in range(len(UsageRecords)): # creating a loop 
        staff_id = UsageRecords[i][2] 
        boxes_picked = int(UsageRecords[i][3])  
        unitcost_price = float(UsageRecords[i][4].replace('$', '').replace('S', ''))  
        unitselling_price = float(UsageRecords[i][5].replace('$', '').replace('S', ''))
        profit = boxes_picked * (unitselling_price - unitcost_price)  
        
        
        if profit <= 1500:
            commission = profit * 0.02
        elif profit > 1500 and profit <= 3000:
            commission = (1500 * 0.02) + (profit - 1500) * 0.04
        elif profit > 3000 and profit <= 4500:
            commission = (1500 * 0.02) + (1500 * 0.04) + (profit - 3000) * 0.05
        else:
            commission = (1500 * 0.02) + (1500 * 0.04) + (1500 * 0.05) + (profit - 4500) * 0.06
        
       
        if profit <= 1500:
            salary = profit * 0.02
        elif profit > 1500 and profit <= 3000:
            salary = (1500 * 0.02) + (profit - 1500) * 0.04
        elif profit > 3000 and profit <= 4500:
            salary = (1500 * 0.02) + (1500 * 0.04) + (profit - 3000) * 0.05
        else:
            salary = (1500 * 0.02) + (1500 * 0.04) + (1500 * 0.05) + (profit - 4500) * 0.06

        if staff_id in total_commission_earned:
            total_profits_earned[staff_id] = total_profits_earned[staff_id] + profit
            total_boxes_picked[staff_id] = total_boxes_picked[staff_id] + boxes_picked
            total_commission_earned[staff_id] = total_commission_earned [staff_id] + commission
            total_salary_earned[staff_id] = total_salary_earned[staff_id] + salary
        else:
            total_profits_earned[staff_id] = profit
            total_boxes_picked[staff_id] = boxes_picked
            total_commission_earned[staff_id] = commission
            total_salary_earned[staff_id] = salary

    
    with open('spaceSummary.txt','w') as file: # naming the file
      file.write('Efficient Transit Payment Summary\n') # \n is added so that it will be printed out line by line
      file.write('===================================================\n')
      file.write("Staff id, Boxes Picked, Profits, Commission, Salary\n")
      sort_amount = []
      for staff_id in total_commission_earned:
        sort_amount.append(staff_id)
        sort_amount.sort()
      for staff_id in (sort_amount):
        total_amount = [staff_id,
                         total_boxes_picked[staff_id],
                         round(total_profits_earned[staff_id],2),
                         round(total_commission_earned[staff_id],2),
                         round(total_salary_earned[staff_id],2)+1000
                         ]
        file.write(f"{total_amount[0]},{total_amount[1]},{total_amount[2]},{total_amount[3]},{total_amount[4]}\n") #will print the total boxes picked, profits, commission and salary earned
      
      
      file.write ('Top 5 of 20 SKUs\n')
      file.write ('=================\n')
   
def total_boxesperskus (UsageRecords):# used the code from part 2 to write into the txt file
   """
   This function will calculate the total number of boxes picked by each SKU and also rank the top 5 out of 20
   """
   total_boxes_picked = {}
   for i in range(len(UsageRecords)):
      skus = (UsageRecords[i][1])
      boxes_picked = int(UsageRecords[i][3])

      if skus in total_boxes_picked:
         total_boxes_picked[skus] = total_boxes_picked[skus] + boxes_picked
      else:
         total_boxes_picked[skus] = boxes_picked
    
   with open('spaceSummary.txt','a') as file: # appending the file so that the top 5 data will be added after the total boxes, profit, commission and salary is written
      sort_topskus = []
      for skus in total_boxes_picked:
        sort_topskus.append(skus)
      sort_topskus.sort(reverse=True)
      for skus in sort_topskus[:5]:
          boxes_picked = total_boxes_picked[skus]
          file.write(f"{boxes_picked},{skus}\n")
total_boxesperskus(UsageRecords)



