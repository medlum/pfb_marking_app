
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
        'Team members': list,  
        'Code Readability': float,
        'Code Efficiency': float,
        'Documentation': float,
        'Assignment Specifications': float
        'Feedback' : str
      }  
    - Use double quotation "" for strings in the dictionary.
    - Your answer should only contain the returned dictionary and nothing else. 
"""


system_message_output = """
1. Your primary task is to evaluate the output based on a structured marking rubric.  
2. Follow the instructions to mark:
    - Refer to the provided marking rubric to ensure accurate grading.
    - Compare the students output with the marking rubrics output and assign the marks accordingly.  
    - Do not assign more than the maximum mark in each marking criterion.
    - Feedback on why the marks are given.
    - Return the marks and feedback in a dictionary : 
      {   
        'Team members': list,  
        'Program Correctness': float,
        'Feedback' : str
      }  
    - Use double quotation "" for strings in the dictionary.
    - Your answer should only contain the returned dictionary and nothing else. 
"""

mark_rubrics_output_decreasing = """
1. Correct output and the marking rubrics for 'decreasing trend' data: (Max 2 marks)

[HIGHEST OVERHEAD] RENTAL EXPENSE: 25.97%
[CASH DEFICIT] CASH ON EACH DAY IS LOWER THAN THE PREVIOUS DAY
[HIGHEST CASH DEFICIT] DAY: 43, AMOUNT: USD2898.00
[NET PROFIT DEFICIT] NET PROFIT ON EACH DAY IS LOWER THAN THE PREVIOUS DAY
[HIGHEST NET PROFIT DEFICIT] DAY: 48, AMOUNT: USD329988.00

- 1.6 marks - 2 marks: Students output has identifed more than 90 percent of correct values for the'day' and 'amount', with no unnecessary details and no missing required elements.
- 1.4 to less than 1.6 marks:  Students output has identifed more than 80-90 percent of correct values for the'day' and 'amount', with minor unnecessary details and no missing required elements.
- 1.2 to less than 1.4: Students output has identifed more than 70-79 percent of correct values for the'day' and 'amount', with some unnecessary details and no missing required elements.
- 1 to less than 1.2 marks: Students output has identifed more than 60-69 percent of correct values for the'day' and 'amount', with many unnecessary details and no missing required elements.
- Less than 1 marks: Students output has identifed less than 60 percent of correct values for the'day' and 'amount', with major unnecessary details and no missing required elements.
"""

mark_rubrics_output_increasing = """
2. Correct output and the marking rubrics for 'increasing trend' data: (Max 2 marks)

[HIGHEST OVERHEAD] RENTAL EXPENSE: 25.97%
[CASH SURPLUS] CASH ON EACH DAY IS HIGHER THAN THE PREVIOUS DAY
[HIGHEST CASH SURPLUS] DAY: 49, AMOUNT: USD1987.00
[NET PROFIT SURPLUS] NET PROFIT ON EACH DAY IS HIGHER THAN THE PREVIOUS DAY
[HIGHEST NET PROFIT SURPLUS] DAY: 41, AMOUNT: USD40004.00

- 1.6 marks - 2 marks: Students output has identifed more than 90 percent of correct values for the'day' and 'amount', with no unnecessary details and no missing required elements.
- 1.4 to less than 1.6 marks:  Students output has identifed more than 80-90 percent of correct values for the'day' and 'amount', with minor unnecessary details and no missing required elements.
- 1.2 to less than 1.4: Students output has identifed more than 70-79 percent of correct values for the'day' and 'amount', with some unnecessary details and no missing required elements.
- 1 to less than 1.2 marks: Students output has identifed more than 60-69 percent of correct values for the'day' and 'amount', with many unnecessary details and no missing required elements.
- Less than 1 marks: Students output has identifed less than 60 percent of correct values for the'day' and 'amount', with major unnecessary details and no missing required elements.
"""

mark_rubrics_output_volatile = """
3.⁠ Correct ⁠output and the marking rubrics for 'volatile trend' data: (Max 3 marks)
[HIGHEST OVERHEAD] RENTAL EXPENSE: 25.97%
[CASH DEFICIT] DAY: 41, AMOUNT: USD1455893.00
[CASH DEFICIT] DAY: 42, AMOUNT: USD60510.00
[CASH DEFICIT] DAY: 43, AMOUNT: USD51789.00
[CASH DEFICIT] DAY: 44, AMOUNT: USD638547.00
[CASH DEFICIT] DAY: 45, AMOUNT: USD120172.00
[CASH DEFICIT] DAY: 49, AMOUNT: USD384432.00
[HIGHEST CASH DEFICIT] DAY: 41, AMOUNT: USD1455893.00
[2ND HIGHEST CASH DEFICIT] DAY: 44, AMOUNT: USD638547.00
[3RD HIGHEST CASH DEFICIT] DAY: 49, AMOUNT: USD384432.00
[NET PROFIT DEFICIT] DAY: 44, AMOUNT: USD27311.00
[NET PROFIT DEFICIT] DAY: 45, AMOUNT: USD5406.00
[NET PROFIT DEFICIT] DAY: 48, AMOUNT: USD93445.00
[NET PROFIT DEFICIT] DAY: 49, AMOUNT: USD37546.00
[HIGHEST NET PROFIT DEFICIT] DAY: 48, AMOUNT: USD93445.00
[2ND HIGHEST NET PROFIT DEFICIT] DAY: 49, AMOUNT: USD37546.00
[3RD HIGHEST NET PROFIT DEFICIT] DAY: 44, AMOUNT: USD27311.00

- 2.4 marks - 3 marks: Students output has identifed more than 90 percent of correct values for the'day' and 'amount', with no unnecessary details and no missing required elements.
- 2.1 to less than 2.4 marks: Students output has identifed more than 80-90 percent of correct values for the'day' and 'amount', with minor unnecessary details and no missing required elements.
- 1.8 to less than 2.1 marks: Students output has identifed more than 70-79 percent of correct values for the'day' and 'amount', with some unnecessary details and no missing required elements.
- 1.5 to less than 1.8 marks: Students output has identifed more than 60-69 percent of correct values for the'day' and 'amount', with many unnecessary details and no missing required elements.
- Less than 1.5 marks: Students output has identifed less than 60 percent of correct values for the'day' and 'amount', with major unnecessary details and no missing required elements.

"""

mark_rubrics_output_reference = """
1. Marking rubrics for 'decreasing trend' data: (Max 2 marks)
- 1.6 marks - 2 marks: Students output has identifed more than 90 percent of correct values for the'day' and 'amount', with no unnecessary details and no missing required elements.
- 1.4 to less than 1.6 marks:  Students output has identifed more than 80-90 percent of correct values for the'day' and 'amount', with minor unnecessary details and no missing required elements.
- 1.2 to less than 1.4: Students output has identifed more than 70-79 percent of correct values for the'day' and 'amount', with some unnecessary details and no missing required elements.
- 1 to less than 1.2 marks: Students output has identifed more than 60-69 percent of correct values for the'day' and 'amount', with many unnecessary details and no missing required elements.
- Less than 1 marks: Students output has identifed less than 60 percent of correct values for the'day' and 'amount', with major unnecessary details and no missing required elements.


2. Marking rubrics for 'increasing trend' data: (Max 2 marks)
- 1.6 marks - 2 marks: Students output has identifed more than 90 percent of correct values for the'day' and 'amount', with no unnecessary details and no missing required elements.
- 1.4 to less than 1.6 marks:  Students output has identifed more than 80-90 percent of correct values for the'day' and 'amount', with minor unnecessary details and no missing required elements.
- 1.2 to less than 1.4: Students output has identifed more than 70-79 percent of correct values for the'day' and 'amount', with some unnecessary details and no missing required elements.
- 1 to less than 1.2 marks: Students output has identifed more than 60-69 percent of correct values for the'day' and 'amount', with many unnecessary details and no missing required elements.
- Less than 1 marks: Students output has identifed less than 60 percent of correct values for the'day' and 'amount', with major unnecessary details and no missing required elements.

3. Marking rubrics for 'volatile trend' data: (Max 3 marks)
- 2.4 marks - 3 marks: Students output has identifed more than 90 percent of correct values for the'day' and 'amount', with no unnecessary details and no missing required elements.
- 2.1 to less than 2.4 marks: Students output has identifed more than 80-90 percent of correct values for the'day' and 'amount', with minor unnecessary details and no missing required elements.
- 1.8 to less than 2.1 marks: Students output has identifed more than 70-79 percent of correct values for the'day' and 'amount', with some unnecessary details and no missing required elements.
- 1.5 to less than 1.8 marks: Students output has identifed more than 60-69 percent of correct values for the'day' and 'amount', with many unnecessary details and no missing required elements.
- Less than 1.5 marks: Students output has identifed less than 60 percent of correct values for the'day' and 'amount', with major unnecessary details and no missing required elements.

"""
mark_rubrics_list = [mark_rubrics_output_decreasing,
                    mark_rubrics_output_increasing, 
                    mark_rubrics_output_volatile]




mark_rubrics_code = """

1. Code Readability (Max 2 marks)
- 1.6 marks - 2 marks: Excellent readability, meaningful names, consistent formatting, proper indentation, clear inline comments.
- 1.4 to less than 1.6 marks: Mostly readable, minor inconsistencies in formatting or naming, limited comments for complex logic.
- 1.2 to less than 1.4 marks: Some readability issues, inconsistent spacing, missing comments, unclear variable names.
- 1 to less than 1.2 marks: Hard to read, lack of indentation, poor naming, minimal commenting, messy structure.
- Less than 1 marks: Very poor readability, no comments, unreadable formatting, confusing structure.

2. ⁠Code Efficiency (Max 5 marks)
- 4 marks - 5 marks: Highly optimized, efficient algorithms, no redundant computations, uses built-in functions properly, write meaningful functions to reduce repeating codes.
- 3.5 to less than 4 marks: Mostly efficient, minor unnecessary loops or operations, some scope for optimization.
- 3 to less than 3.5 marks: Correct logic but inefficient, unnecessary loops, redundant calculations, poor data structures.
- 2.5 to less than 3 marks: Inefficient code, high time complexity, excessive memory use, performance issues.
- Less than 2.5 marks: Highly inefficient, repetitive computations, excessive memory use, brute force solutions.

3. ⁠Documentation (Max 3 marks)
- 2.4 marks - 3 marks: Well-structured documentation, clear docstrings, meaningful comments, algorithm explanations.
- 2.1 to less than 2.4 marks: Mostly well-documented, but some function docstrings or explanations may be missing.
- 1.8 to less than 2.1 marks: Some documentation present but lacks details in function descriptions or inline comments.
- 1.5 to less than 1.8 marks: Minimal documentation, few comments, missing docstrings for key functions.
- Less than 1.5 marks: No meaningful documentation, missing docstrings, no explanation of the code.

4. ⁠Assignment Specifications (Max 3 marks)
- 2.4 marks - 3 marks: Fully meets all assignment requirements, for example:
    -- Filename convention: 'summary_report.txt' are used when writing output to file.
    -- Did not import additional python modules except for 'csv' and 'pathlib' modules.
    -- Strict use 'pathlib' module to handle reading and writing files.
    -- Did not use list comprehensive in the code. 
- 2.1 to less than 2.4 marks: Mostly meets specifications, but minor missing details or formatting issues.
- 1.8 to less than 2.1 marks: Partially meets specifications, missing some key requirements but still functional.
- 1.5 to less than 1.8 marks: Significant missing requirements, incorrect submission format.
- Less than 1.5 marks: Does not follow assignment requirements, incorrect format, missing important elements.
"""

output_volatile = """
[HIGHEST OVERHEAD] RENTAL EXPENSE: 25.97%
[CASH DEFICIT] DAY: 41, AMOUNT: USD1455893.00
[CASH DEFICIT] DAY: 42, AMOUNT: USD60510.00
[CASH DEFICIT] DAY: 43, AMOUNT: USD51789.00
[CASH DEFICIT] DAY: 44, AMOUNT: USD638547.00
[CASH DEFICIT] DAY: 45, AMOUNT: USD120172.00
[CASH DEFICIT] DAY: 49, AMOUNT: USD384432.00
[HIGHEST CASH DEFICIT] DAY: 41, AMOUNT: USD1455893.00
[2ND HIGHEST CASH DEFICIT] DAY: 44, AMOUNT: USD638547.00
[3RD HIGHEST CASH DEFICIT] DAY: 49, AMOUNT: USD384432.00
[NET PROFIT DEFICIT] DAY: 44, AMOUNT: USD27311.00
[NET PROFIT DEFICIT] DAY: 45, AMOUNT: USD5406.00
[NET PROFIT DEFICIT] DAY: 48, AMOUNT: USD93445.00
[NET PROFIT DEFICIT] DAY: 49, AMOUNT: USD37546.00
[HIGHEST NET PROFIT DEFICIT] DAY: 48, AMOUNT: USD93445.00
[2ND HIGHEST NET PROFIT DEFICIT] DAY: 49, AMOUNT: USD37546.00
[3RD HIGHEST NET PROFIT DEFICIT] DAY: 44, AMOUNT: USD27311.00
"""


output_increasing = """
[HIGHEST OVERHEAD] RENTAL EXPENSE: 25.97%
[CASH SURPLUS] CASH ON EACH DAY IS HIGHER THAN THE PREVIOUS DAY
[HIGHEST CASH SURPLUS] DAY: 49, AMOUNT: USD1987.00
[NET PROFIT SURPLUS] NET PROFIT ON EACH DAY IS HIGHER THAN THE PREVIOUS DAY
[HIGHEST NET PROFIT SURPLUS] DAY: 41, AMOUNT: USD40004.00
"""

output_decreasing = """
[HIGHEST OVERHEAD] RENTAL EXPENSE: 25.97%
[CASH DEFICIT] CASH ON EACH DAY IS LOWER THAN THE PREVIOUS DAY
[HIGHEST CASH DEFICIT] DAY: 43, AMOUNT: USD2898.00
[NET PROFIT DEFICIT] NET PROFIT ON EACH DAY IS LOWER THAN THE PREVIOUS DAY
[HIGHEST NET PROFIT DEFICIT] DAY: 48, AMOUNT: USD329988.00
"""
