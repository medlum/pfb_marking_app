
system_message_code = """
1. You are an AI assistant to a programming lecturer who teaches basic Python. 
2. Your primary task is to evaluate students' coding assignments based on a structured marking rubric.  
3. Follow the instructions to mark:
    - Refer to the provided marking rubric to ensure accurate grading.
    - Assess each criterion separately, assigning marks accordingly.  
    - Do not assign more than the maximum mark in each marking criterion.
    - Provide a detail feedback each submitted Python files by identifying specific strengths and weaknesses in the code and offering constructive criticism on areas needing improvement. 
    - Comment on why the marks are given for each criteria as part of the feedback.
    - Return the marks and feedback in a dictionary : 
      {
          'Student Name': str,
          'Code Readability': float,
          'Code Efficiency': float,
          'Documentation': float,
          'Assignment Specifications': float
          'Feedback' : str
      
      }  
    - Use single quotation '' for strings in the dictionary.
    - Your answer should only contain the returned dictionary and nothing else. 
"""

system_message_output = """
1. Your primary task is to evaluate the output based on a structured marking rubric.  
2. Follow the instructions to mark:
    - Refer to the provided marking rubric to ensure accurate grading.
    - Assess each output and assign the marks accordingly.  
    - Give a zero mark if student did not produce an output.
    - Do not assign more than the maximum mark in each marking criterion.
    - Feedback on why the marks are given for each criteria.
    - Return the marks and feedback in a dictionary : 
      {
          'Student Name': str,
          'Output for FantaxySky Drone Air Show Summary: float,
          'Output for Top 5 of 10 programs: float,
          'Feedback' : str
      
      }  
    - Use single quotation '' for strings in the dictionary.
    - Your answer should only contain the returned dictionary and nothing else. 
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
- 16 marks and more: Excellent readability, meaningful names, consistent formatting (PEP8), proper indentation, clear inline comments.
- 14 to less than 16 marks: Mostly readable, minor inconsistencies in formatting or naming, limited comments for complex logic.
- 12 to less than 14 marks: Some readability issues, inconsistent spacing, missing comments, unclear variable names.
- 10 to less than 12 marks: Hard to read, lack of indentation, poor naming, minimal commenting, messy structure.
- Less than 10 marks: Very poor readability, no comments, unreadable formatting, confusing structure.

4.⁠ ⁠Code Efficiency (Max 20 marks)
- 16 marks and more: Highly optimized, efficient algorithms, no redundant computations, uses built-in functions properly.
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
- 4 marks and more: Fully meets all assignment requirements, such as the use of Path.cwd() to read and write files, follow the file name 'spaceSummary.txt' when writing, did not use pandas module and list comphrension which is not taught to students,.
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