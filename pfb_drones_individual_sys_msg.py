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
9. This is the solution code for your reference:

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

      #define a function to remove "." from program
      def clean_program(program):
          program=program.replace('.','').strip()
          return program

      #define a function to extract duration
      def getDuration(duration):
          duration=duration.replace("minutes", "").strip()
          return float(duration)

      #define a function to calculate charges for drones used
      def CalculateDroneFees(drones):
          droneFee = 10000
          if drones > 100:
                drones -= 100
                block = drones//30
                if drones%30 > 0:
                    block += 1
                droneFee += block * 2000
          return droneFee

      #define a function to calculate charges for duration
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
          file.write("FantaxySky Drone Air Show Summary\\n")
          file.write("==================================\\n")
          file.write("Program,Revenue,Number_of_Sales,Average_Revenue,Total_Number_of_Drones, Total_Duration\\n")
          for program in sorted(droneShowSummary):
                info=droneShowSummary[program]
                file.write(f"{{program}},{info['revenue']:.2f},{info['no_of_sales']:.0f},{info['revenue']/info['no_of_sales']:.2f},{info['no_of_drones']:.0f}, {info['total_duration']:.0f}\\n")


          number_of_program=len(topProgram) #in case, there are fewer than 5 programs
          if number_of_program > 5:
                top_of_program = 5   #To ensure we don't try to get more that what we have
          else:
                top_of_program = number_of_program
         file.write(f'\\n\\nTop {{top_of_program}} of {{number_of_program}} programs\\n')
          file.write('===================\\n')
          for program in topProgram[:top_of_program]:
            file.write(f"{{program[0]:.2f}},{{program[1]}}\\n")
     
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
1.⁠ Correct ⁠output and the marking rubrics for 'FantaxySky Drone Air Show Summary': (Max 20 marks)

FantaxySky Drone Air Show Summary
==================================
Program,Revenue,Number_of_Sales,Average_Revenue,Total_Number_of_Drones, Total_Duration
Aether Drift,699000.00,10,69900.00,2160, 194
Celestial Circuit,622000.00,10,62200.00,2180, 198
Chronos Cascade,479000.00,10,47900.00,1860, 168
Infinity Pulse,873500.00,10,87350.00,2510, 220
Luminous Horizon,325000.00,10,32500.00,1380, 132
Neon Nebula,641500.00,10,64150.00,1820, 162
Orion Flight,879000.00,10,87900.00,2460, 218
Photon Odyssey,813500.00,10,81350.00,2680, 238
Sky Symphony,381000.00,10,38100.00,1480, 136
Stellar Echoes,639000.00,10,63900.00,1910, 170

- 16 marks and more: Generated output has more than 90 percent of correct format, correct values for Program,Revenue,Number_of_Sales,Average_Revenue,Total_Number_of_Drones, Total_Duration, no unnecessary details and no missing required elements.
- 14 to less than 16 marks: Generated output has 80-90 percent of correct format, correct values for Program,Revenue,Number_of_Sales,Average_Revenue,Total_Number_of_Drones, Total_Duration, minor unnecessary details, or minor missing required elements.
- 12 to less than 14 marks: Generated output has 70-79 percent of correct format, correct values for Program,Revenue,Number_of_Sales,Average_Revenue,Total_Number_of_Drones, Total_Duration,  some unnecessary details, or some missing required elements.
- 10 to less than 12 marks: Generated output has 60 - 69 percent of correct format, correct values for Program,Revenue,Number_of_Sales,Average_Revenue,Total_Number_of_Drones, Total_Duration,  many unnecessary details, or many missing required elements.
- Less than 10 marks: Generated output has less than 60 percent of correct format, correct values for Program,Revenue,Number_of_Sales,Average_Revenue,Total_Number_of_Drones, Total_Duration, major unnecessary details, or major missing required elements.


2.⁠ ⁠ Correct ⁠output and the marking rubrics for 'Top 5 of 10 programs': (Max 10 marks)
Top 5 of 10 programs
===================
879000.00,Orion Flight
873500.00,Infinity Pulse
813500.00,Photon Odyssey
699000.00,Aether Drift
641500.00,Neon Nebula

- 8 marks and more: Generated output has more than 80 percent of correct format, correct values for Top 5 of 10 programs, no unnecessary details and no missing required elements.
- 7 to less than 8 marks: Generated output has 70-80 percent of correct format, correct values for Top 5 of 10 programs, minor unnecessary details, or minor missing required elements.
- 6 to less than 7 marks: Generated output has 60-70 percent of correct format, correct values for Top 5 of 10 programs,  some unnecessary details, or some missing required elements.
- 5 to less than 6 marks: Generated output has 50-60 percent of correct format, correct values for Top 5 of 10 programs,  many unnecessary details, or many missing required elements.
- Less than 5 marks: Generated output has less than 50 percent of correct format, correct values for Top 5 of 10 programs, major unnecessary details, or major missing required elements.
"""

mark_rubrics_output_reference = """
1.⁠ Marking rubrics for 'FantaxySky Drone Air Show Summary': (Max 20 marks)

- 16 marks and more: Generated output has more than 90 percent of correct format, correct values with no unnecessary details and no missing required elements.
- 14 to less than 16 marks: Generated output has 80-90 percent of correct format, correct values with minor unnecessary details, or minor missing required elements.
- 12 to less than 14 marks: Generated output has 70-79 percent of correct format, correct values with  some unnecessary details, or some missing required elements.
- 10 to less than 12 marks: Generated output has 60 - 69 percent of correct format, correct values with  many unnecessary details, or many missing required elements.
- Less than 10 marks: Generated output has less than 60 percent of correct format, correct values with major unnecessary details, or major missing required elements.


2.⁠ Marking rubrics for 'Output for Top 5 of 10 programs': (Max 10 marks)

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
FantaxySky Drone Air Show Summary
==================================
Program,Revenue,Number_of_Sales,Average_Revenue,Total_Number_of_Drones, Total_Duration
Aether Drift,699000.00,10,69900.00,2160, 194
Celestial Circuit,622000.00,10,62200.00,2180, 198
Chronos Cascade,479000.00,10,47900.00,1860, 168
Infinity Pulse,873500.00,10,87350.00,2510, 220
Luminous Horizon,325000.00,10,32500.00,1380, 132
Neon Nebula,641500.00,10,64150.00,1820, 162
Orion Flight,879000.00,10,87900.00,2460, 218
Photon Odyssey,813500.00,10,81350.00,2680, 238
Sky Symphony,381000.00,10,38100.00,1480, 136
Stellar Echoes,639000.00,10,63900.00,1910, 170


Top 5 of 10 programs
===================
879000.00,Orion Flight
873500.00,Infinity Pulse
813500.00,Photon Odyssey
699000.00,Aether Drift
641500.00,Neon Nebula


"""