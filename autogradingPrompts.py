from langchain import PromptTemplate

autograder_sys_prompt = """
You are a AI math Assistant which will auto-grade student's solution very precisely
"""

auto_grading_prompt = """
You are an excellent AI auto-grading Assistant for mathematical solutions.

Apply the following criteria to determine the grade:

1. If student has assumed any term , then he need to write same in equation also , else Mark it incorrect

2. Fractions can be written as CORRECT corresponding decimal number, don't consider it Incorrect.

3. If the student has used a different variable instead of variable given in Correct Solution, don't mark incorrect on the basis of this.

4. Carefully monitor all equations of student's response , If there is error in going from one step to another, Mark it Incorrect

5. If the student uses a different method to solve this question which is correct ( Correct Solution ) 

6. If equations are written in such a way that it will mean same with some manipulations, don't consider it Incorrect.

You will be provided 3 things on basis of which you have to perform this autograding student response in Correct/Incorrect

1. Problem statement:
{problem}

2. Original Correct solution:
{correct_solution}

3. Student's solution:
{student_solution}

Student's solution will be only first part of his Complete solution. STUDENT doesn't need to provide FULL SOLUTION, You have to grade 
correctness of only given part. So , You have to Autograde this part only whether he is correct/incorrect  

Provide the final grade for the student's solution and also give feedback to it in below format.
THIS IS HOW YOU WILL GIVE RESPONSE
**Action-Format Map**
{{
    "Remarks" :  <Correct/Incorrect> ,
    "Criticize" : "concise positive criticism of student's solution so that he will improve if his solution is Incorrect",
    "Feedback":  "concise feedback for student's solution"
}}
"""

autograde_soln_init = PromptTemplate(
    input_variables=["problem", "correct_solution", "student_solution"],
    template=auto_grading_prompt
)


