system_message_code = """
You are an AI assistant helping a programming lecturer evaluate student Python assignments.

1. Evaluate only Part 2 and Part 3 of the code. Part 1 is pre-completed and must not be marked.
2. Use the provided marking rubric to assess each criterion.
3. Assign a score for each criterion (0 to maximum allowed).
4. Provide concise but constructive feedback explaining the marks awarded.
5. Your response must be a single valid JSON object with the exact keys below:
{
  "Student Name": "John Doe",
  "Code Readability": 5.0,
  "Code Efficiency": 4.0,
  "Documentation": 3.5,
  "Assignment Specifications": 5.0,
  "Feedback": "Clear logic, good use of functions. Missing docstrings for some functions."
}
6. Use double quotes for all keys and string values.
7. Do NOT include extra text, markdown, or explanation. Only return the JSON object.
8. Ensure ALL keys are present, even if the score is 0.
9. Here is the suggested solution code to reference when evaluating the code:
    
    ```python
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
                f"{{station}},{{info[0]:.2f}},{{info[1]}},{{info[2]}},{{info[3]:.2f}}\n")

        # in case, there are fewer than 5 programs
        number_of_Station = len(topStation)
        if number_of_Station > 5:
            top_of_Station = 5  # To ensure we don't try to get more that what we have
        else:
            top_of_Station = number_of_Station
        file.write(f'\n\nTop {{top_of_Station}} of {{number_of_Station}} programs\n')
        file.write('===================\n')
        for station in topStation[:top_of_Station]:
            # file.write(station)
            file.write(f"{{station[-1]}},{{station[0]:.2f}}\n")

    ```
     
"""

system_message_output = """
You are an AI assistant evaluating the output generated by a student's Python program.

1. Use the provided marking rubric to assess the output.
2. If the student did not produce any output, assign 0 to all criteria and state why in feedback.
3. Do NOT assign more than the maximum allowed marks for each criterion.
4. Provide brief feedback explaining the scores.

Respond ONLY with a single valid JSON object in this format:
{
  "Student Name": "John Doe",
  "Output for FantaxySky Drone Air Show Summary": 5.0,
  "Output for Top 5 of 10 programs": 5.0,
  "Feedback": "Output is correct and matches expected format."
}

Rules:
- Use double quotes for all keys and string values.
- Do NOT include any extra text, markdown, or explanation.
- Ensure ALL keys are present, even if the score is 0.
- If output is missing, set scores to 0 and explain in feedback.
"""


mark_rubrics_output = """
1.⁠ Correct ⁠output and the marking rubrics for 'DeliveryMax Summary' (Max 20 marks):

    DeliveryMax Summary
    ===================
    Station,Total_Earning,Total_Packages,Number_of_Routes,Total_Distance
    Central Hub,20305.00,44,2336,1185.00
    City Center,24880.00,51,2360,1509.00
    East Gate,24035.00,48,2270,1291.00
    Gateway Station,18505.00,46,2279,1254.00
    Harbor Point,14740.00,31,1635,946.00
    Industrial Park,19880.00,40,2085,1265.00
    Lakeside Terminal,25500.00,40,1964,1184.00
    Metro Junction,23100.00,46,2367,1210.00
    Mountain View,26495.00,52,2526,1408.00
    North Point,19550.00,47,2322,1288.00
    Riverside Hub,33485.00,50,2525,1622.00
    South Terminal,25830.00,44,2089,1311.00
    Sunset Plaza,26070.00,51,2600,1528.00
    Valley Ridge,25145.00,48,2566,1419.00
    West Station,17895.00,39,1963,1212.00

    - 16 marks and more: Generated output has more than 90 percent of correct format, correct values for Program,Revenue,Number_of_Sales,Average_Revenue,Total_Number_of_Drones, Total_Duration, no unnecessary details and no missing required elements.
    - 14 to less than 16 marks: Generated output has 80-90 percent of correct format, correct values for Program,Revenue,Number_of_Sales,Average_Revenue,Total_Number_of_Drones, Total_Duration, minor unnecessary details, or minor missing required elements.
    - 12 to less than 14 marks: Generated output has 70-79 percent of correct format, correct values for Program,Revenue,Number_of_Sales,Average_Revenue,Total_Number_of_Drones, Total_Duration,  some unnecessary details, or some missing required elements.
    - 10 to less than 12 marks: Generated output has 60 - 69 percent of correct format, correct values for Program,Revenue,Number_of_Sales,Average_Revenue,Total_Number_of_Drones, Total_Duration,  many unnecessary details, or many missing required elements.
    - Less than 10 marks: Generated output has less than 60 percent of correct format, correct values for Program,Revenue,Number_of_Sales,Average_Revenue,Total_Number_of_Drones, Total_Duration, major unnecessary details, or major missing required elements.


2.⁠ ⁠ Correct ⁠output and the marking rubrics for 'Top 5 of 15 programs' (Max 10 marks) :
    Top 5 of 15 programs
    ===================
    Riverside Hub,33485.00
    Mountain View,26495.00
    Sunset Plaza,26070.00
    South Terminal,25830.00
    Lakeside Terminal,25500.00


- 8 marks and more: Generated output has more than 80 percent of correct format, correct values for Top 5 of 10 programs, no unnecessary details and no missing required elements.
- 7 to less than 8 marks: Generated output has 70-80 percent of correct format, correct values for Top 5 of 10 programs, minor unnecessary details, or minor missing required elements.
- 6 to less than 7 marks: Generated output has 60-70 percent of correct format, correct values for Top 5 of 10 programs,  some unnecessary details, or some missing required elements.
- 5 to less than 6 marks: Generated output has 50-60 percent of correct format, correct values for Top 5 of 10 programs,  many unnecessary details, or many missing required elements.
- Less than 5 marks: Generated output has less than 50 percent of correct format, correct values for Top 5 of 10 programs, major unnecessary details, or major missing required elements.
"""

mark_rubrics_output_reference = """
1.⁠ Marking rubrics for 'DeliveryMax Summary': (Max 20 marks)

- 16 marks and more: Generated output has more than 90 percent of correct format, correct values with no unnecessary details and no missing required elements.
- 14 to less than 16 marks: Generated output has 80-90 percent of correct format, correct values with minor unnecessary details, or minor missing required elements.
- 12 to less than 14 marks: Generated output has 70-79 percent of correct format, correct values with  some unnecessary details, or some missing required elements.
- 10 to less than 12 marks: Generated output has 60 - 69 percent of correct format, correct values with  many unnecessary details, or many missing required elements.
- Less than 10 marks: Generated output has less than 60 percent of correct format, correct values with major unnecessary details, or major missing required elements.


2.⁠ Marking rubrics for 'Output for Top 5 of 15 programs': (Max 10 marks)

- 8 marks and more: Generated output has more than 80 percent of correct format, correct values with no unnecessary details and no missing required elements.
- 7 to less than 8 marks: Generated output has 70-80 percent of correct format, correct values with minor unnecessary details, or minor missing required elements.
- 6 to less than 7 marks: Generated output has 60-70 percent of correct format, correct values with  some unnecessary details, or some missing required elements.
- 5 to less than 6 marks: Generated output has 50-60 percent of correct format, correct values with  many unnecessary details, or many missing required elements.
- Less than 5 marks: Generated output has less than 50 percent of correct format, correct values with major unnecessary details, or major missing required elements.
"""

mark_rubrics_code = """
3.⁠ ⁠Code Readability (Max 20 marks)
- 16 marks and more: Excellent readability, meaningful names, consistent formatting (PEP8), proper indentation, clear inline comments, create neccesary functions in attempt to reduce repetition and improve readability.
- 14 to less than 16 marks: Mostly readable, minor inconsistencies in formatting or naming, limited comments for complex logic, create some functions in attempt to reduce repetition and improve readability.
- 12 to less than 14 marks: Some readability issues, inconsistent spacing, missing comments, unclear variable names, create few functions in attempt to reduce repetition and improve readability.
- 10 to less than 12 marks: Hard to read, lack of indentation, poor naming, minimal commenting, messy structure, lack of functions to reduce repetition.
- Less than 10 marks: Very poor readability, no comments, unreadable formatting, confusing structure, lack of functions to reduce repetition.

4.⁠ ⁠Code Efficiency (Max 20 marks)
- 16 marks and more: Highly optimized, efficient algorithms, no redundant computations, uses built-in functions properly, 
- 14 to less than 16 marks: Mostly efficient, minor unnecessary loops or operations, some scope for optimization.
- 12 to less than 14 marks: Correct logic but inefficient, unnecessary loops, redundant calculations, poor data structures.
- 10 to less than 12 marks: Inefficient code, high time complexity, excessive memory use, performance issues.
- Less than 10 marks: Highly inefficient, repetitive computations, excessive memory use, brute force solutions.

5.⁠ ⁠Documentation (Max 25 marks)
- 20 marks and more: Well-structured documentation, clear docstrings, meaningful comments, algorithm explanations.
- 17.5 to less than 20 marks: Mostly well-documented, but some function docstrings or explanations may be missing.
- 15 to less than 17.5 marks: Some documentation present but lacks details in function descriptions or inline comments.
- 12.5 to less than 15 marks: Minimal documentation, few comments, missing docstrings for key functions.
- Less than 12.5 marks: No meaningful documentation, missing docstrings, no explanation of the code.

6.⁠ ⁠Assignment Specifications (Max 5 marks)
- 4 marks and more: Fully meets all assignment requirements, such as the use of Path.cwd() to read and write files, follow the file name convention: 'DroneSummary.txt', did not use pandas module and list comphrension which are not taught to students.
- 3.5 to less than 4 marks: Mostly meets specifications, but minor missing details or formatting issues.
- 3 to less than 3.5 marks: Partially meets specifications, missing some key requirements but still functional.
- 2.5 to less than 3 marks: Significant missing requirements, incorrect submission format.
- Less than 1.5 marks: Does not follow assignment requirements, incorrect format, missing important elements.

"""


OutputSummary = """
DeliveryMax Summary
===================
Station,Total_Earning,Total_Packages,Number_of_Routes,Total_Distance
Central Hub,20305.00,44,2336,1185.00
City Center,24880.00,51,2360,1509.00
East Gate,24035.00,48,2270,1291.00
Gateway Station,18505.00,46,2279,1254.00
Harbor Point,14740.00,31,1635,946.00
Industrial Park,19880.00,40,2085,1265.00
Lakeside Terminal,25500.00,40,1964,1184.00
Metro Junction,23100.00,46,2367,1210.00
Mountain View,26495.00,52,2526,1408.00
North Point,19550.00,47,2322,1288.00
Riverside Hub,33485.00,50,2525,1622.00
South Terminal,25830.00,44,2089,1311.00
Sunset Plaza,26070.00,51,2600,1528.00
Valley Ridge,25145.00,48,2566,1419.00
West Station,17895.00,39,1963,1212.00


Top 5 of 15 programs
===================
Riverside Hub,33485.00
Mountain View,26495.00
Sunset Plaza,26070.00
South Terminal,25830.00
Lakeside Terminal,25500.00

"""