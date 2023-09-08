# PROMPT SET 1
autograde_planner_sys_prompt = """
You are a super intelligent math expert and strategist
"""

autograde_planner_init_prompt = """
You are excellent math expert and decision maker who will make plans for verification of student's solution.

The Planner's task is to formulate a step-by-step plan to validate the correctness of the proposed solution of Student.
Student's solution can be COMPLETE / INCOMPLETE . So, Planner have to make plans for only what is provided.

Student's approach can be different from given in solution, You have been provided solution only for reference. So, just check correctness of each step.

So, Planner will be provided 4 things on the basis of which you have to make a plan on how to verify student's solution.
1. Question    2. Correct Solution     3. Step by step solution of student    4.correctly_verified_upto
Student solution is verified till step number --> "correctly_verified_upto" value . So , u have to make plan for  student solution after this step only.


{student_data}

According to the student's solution , you have to make a excellent step-by-step plan on how we will check student's solution from Step No-->{check_from}.

Planner is very smart and intelligent and expert of all types of problems like logical reasoning, word problems, algebra, geometry, calculus, etc.
Planner is always careful and strict when making plans to verifying the solution ,especially in the case of Logical Reasoning problems such as Data Sufficiency, Statement and Assumption, and Statement and Conclusion.


Planner doesn't have to make any conclusion whether student's step is correct or not , just provide plan for checking. 
PLANNER: (Please detail your plan step-by-step from student's solution step--->{check_from})
like --->
 Step (student step number): Plan.....
and so on
"""


autograde_verifier_sys_prompt = """
You are a super intelligent math expert and precise AI grader for student's solution.
"""

autograde_verifier_init_prompt = """
You're an exceptionally intelligent mathematics expert tasked with verifying students' solutions based on specified plans. Your job is to check student solutions starting from step {check_from} and stop when an error is detected. Students may have either complete or incomplete solutions, so you must verify only the corresponding steps.

Students may jump a step , it doesn't means You will mark it incorrect until and unless  equations represent the same relationship. 


You will receive 4 pieces of information for verification:
1. Question
2. Student's Step-by-Step Solution
3. Correctly Verified Up To Step
4. Plans

{student_data}

Student solutions are verified up to the step number indicated by "correctly_verified_upto." Therefore, you should  start from step {check_from}. Based on the provided plans, you must verify the corresponding student steps.

Here is Plans:
{Planner_data}

Here is the format for your JSON output:

{{
  "is_mistake": <bool>,
  "in_step": <step_no/None>,
  "feedback_to_student": "<pointing_out_errors_and_providing_detailed_correction/None>"
}}

* If you find an error in a step, set is_mistake to True; otherwise, it should be False.
* If you identify an error in a step, specify the step number where the first error occurs in the in_step field. If no errors are found, set it to None.
* Finally, provide feedback to the student regarding the first error detected or an overall feedback message if all steps are correct.

You are an excellent Verifier and you have to STRICTLY give results as Verifier's output in the above mentioned format not anything else.
"""







test1 = {
  "problem": """
     In a survey, the number of people who like fruits is 4 times the number of people who like vegetables. If 12 people who like fruits like vegetables
    instead, the number of people who like vegetables would be equal to the number of people who like fruits. How many people like fruits?
     """
  ,
  "solution": """
     Let no. of people who like vegetables be q.
    So, no. of people who like fruits will be 4q.
    According to the question,
    4 q - 12 …. (i)
    q + 12 …. (ii)
    The number of people who like vegetables would be equal to the number of people who like fruits. So, equations (i) and (ii) must be equal.
    4q - 12 = q + 12
    3 q = 24
    q = 8
    i.e. 4q = 32
    So, No. of people who like fruits is 32
    """
  ,
  "student_steps": [
    {
      "step": 1,
      "content": "Let no. of people who like vegetables be p. "
    },
    {
      "step": 2,
      "content": " So, no. of people who like fruits will be 4p."
    },
    {
      "step": 3,
      "content": "No. of people like vegetables = p+12 "
    },
    {
      "step": 4,
      "content": "No. of people like fruits = 4p - 12 "
    },
    {
      "step": 5,
      "content": "The number of people who like vegetables would be equal to the number of people who like fruits. So, equations (i) and (ii) must be equal."
    },
    {
      "step": 6,
      "content": "4p - 12 = p + 12"
    },
    {
      "step": 7,
      "content": "5p = 24 "
    },
    {
      "step": 8,
      "content": "p = 24/8 "
    }
  ],
  "correctly_verified_upto": 5
}


test2 = {
  "problem": """   
        Check if x(x + 1) + 8 = (x + 2) (x - 2) is in the form of quadratic equation
       """,
  "solution":  """   
        Given,
        x(x + 1) + 8 = (x + 2) (x – 2)
        x^2+x+8 = x^2-2^2 [By algebraic identities]

        Cancel x2 both the sides.
        x+8=-4
        x+12=0
        Since, this expression is not in the form of ax2+bx+c, hence it is not a quadratic equation.
       """,
  "student_steps": [
    {
      "step": 1,
      "content": "x(x+1)+8 = (x+2)(x-2)"
    },
    {
      "step": 2,
      "content": "x^2+x+8 = x^2-2x+2x-4 "
    },
    {
      "step": 3,
      "content": "2x^2+x+4 = 0 "
    },
    {
      "step": 4,
      "content": "So, it is quadratic equation"
    }
  ],
  "correctly_verified_upto": 2
}

test3 = {
  "problem": """   
        Solve the following simultaneous equation by elimination method.
        3x + 9y = -60
        9x + 9y = -90
       """,
  "solution":  """   
       3x + 9y = -60 ..........(1);
       9x + 9y = -90 ..........(2); 
       Subtract eq(2) from eq(1)
       -6x = 30 
       Therefore, x = -5 ,
       Substitute x = -5 in eq(1),
       3(-5)+9y = -60
       -15+9y = -60
       9y = -45 
       Therefore, y = -5 ),
       """,
  "student_steps": [
    {
      "step": 1,
      "content": "let 3x + 9y = -60 is equation 1 and 9x+9y = 90 be equation 2"
    },
    {
      "step": 2,
      "content": "Subtract equation 1 from equation 2---> (2)-(1)"
    },
    {
      "step": 3,
      "content": "6x = 30"
    },
    {
      "step": 4,
      "content": "x = 5"
    },
    {
      "step": 5,
      "content": "9(5) + 9y = -90"
    },
    {
      "step": 6,
      "content": "45 + 9y = -90"
    }
  ],
  "correctly_verified_upto": 0
}

test4 =  {
  "problem": """   
        Find three consecutive integers whose sum is -63
       """,
  "solution":  """   
        Let the first integer to be x.
        Given that sum of the three consecutive integers = -63.
        (x) + (x + 1) + (x + 2) = -63
        3x + 3 = -63
        3x = -66
        x = -22
        Therefore, three consecutive integers are -22, -21 and -20.
       """,
  "student_steps": [
    {
      "step": 1,
      "content": "Let the first integer be a"
    },
    {
      "step": 2,
      "content": "Given that sum of the three consecutive integers = -63."
    },
    {
      "step": 3,
      "content": "a + a + 1 + a + 2 = -63"
    },
    {
      "step": 4,
      "content": "3a + 3 = -63"
    },
    {
      "step": 5,
      "content": "3a = -66"
    },
    {
      "step": 6,
      "content": "a = -22"
    },
    {
      "step": 7,
      "content": "Therefore, three consecutive integers are -22, -21 and -20"
    }
  ],
  "correctly_verified_upto": 2
}

test5 =  {
  "problem": """   
        Find three consecutive integers whose sum is -63
       """,
  "solution":  """   
        Let the first integer to be x.
        Given that sum of the three consecutive integers = -63.
        (x) + (x + 1) + (x + 2) = -63
        3x + 3 = -63
        3x = -66
        x = -22
        Therefore, three consecutive integers are -22, -21 and -20.
       """,
  "student_steps": [
    {
      "step": 1,
      "content": "Let the second integer be a"
    },
    {
      "step": 2,
      "content": "Given that sum of the three consecutive integers = -63."
    },
    {
      "step": 3,
      "content": "a -1 + a + a + 1 = -63"
    },
    {
      "step": 4,
      "content": "3a = -63"
    },
    {
      "step": 5,
      "content": "3a = -63"
    },
    {
      "step": 6,
      "content": "a = -21"
    },
    {
      "step": 7,
      "content": "Therefore, three consecutive integers are -22, -21 and -20"
    }
  ],
  "correctly_verified_upto": 2
}

test6 =  {
  "problem": """   
        Find three consecutive integers whose sum is -63
       """,
  "solution":  """   
        Let the first integer to be x.
        Given that sum of the three consecutive integers = -63.
        (x) + (x + 1) + (x + 2) = -63
        3x + 3 = -63
        3x = -66
        x = -22
        Therefore, three consecutive integers are -22, -21 and -20.
       """,
  "student_steps": [
    {
      "step": 1,
      "content": "Let the third integer be a"
    },
    {
      "step": 2,
      "content": "Given that sum of the three consecutive integers = -63."
    },
    {
      "step": 3,
      "content": "a -2 + a -1 + a = -63"
    },
    {
      "step": 4,
      "content": "3a - 3 = -63"
    },
    {
      "step": 5,
      "content": "3a = -60"
    },
    {
      "step": 6,
      "content": "a = -20"
    },
    {
      "step": 7,
      "content": "Therefore, three consecutive integers are -22, -21 and -20"
    }
  ],
  "correctly_verified_upto": 2
}

test7 =  {
  "problem": """   
        Find three consecutive integers whose sum is -63
       """,
  "solution":  """   
        Let the first integer to be x.
        Given that sum of the three consecutive integers = -63.
        (x) + (x + 1) + (x + 2) = -63
        3x + 3 = -63
        3x = -66
        x = -22
        Therefore, three consecutive integers are -22, -21 and -20.
       """,
  "student_steps": [
    {
      "step": 1,
      "content": "Let the first integer be a"
    },
    {
      "step": 2,
      "content": "Given that sum of the three consecutive integers = -63."
    },
    {
      "step": 3,
      "content": "a -2 + a -1 + a = -63"
    },
    {
      "step": 4,
      "content": "3a - 3 = -63"
    },
    {
      "step": 5,
      "content": "3a = -60"
    },
    {
      "step": 6,
      "content": "a = -20"
    },
    {
      "step": 7,
      "content": "Therefore, three consecutive integers are -22, -21 and -20"
    }
  ],
  "correctly_verified_upto": 2
}

test8 =  {
  "problem": """   
        Find three consecutive integers whose sum is -63
       """,
  "solution":  """   
        Let the first integer to be x.
        Given that sum of the three consecutive integers = -63.
        (x) + (x + 1) + (x + 2) = -63
        3x + 3 = -63
        3x = -66
        x = -22
        Therefore, three consecutive integers are -22, -21 and -20.
       """,
  "student_steps": [
    {
      "step": 1,
      "content": "Let the second integer be a"
    },
    {
      "step": 2,
      "content": "Given that sum of the three consecutive integers = -63."
    },
    {
      "step": 3,
      "content": "a -2 + a -1 + a = -63"
    },
    {
      "step": 4,
      "content": "3a - 3 = -63"
    },
    {
      "step": 5,
      "content": "3a = -60"
    },
    {
      "step": 6,
      "content": "a = -20"
    },
    {
      "step": 7,
      "content": "Therefore, three consecutive integers are -22, -21 and -20"
    }
  ],
  "correctly_verified_upto": 2
}






# Rohan Planner prompt
autograde_planner_init_prompt = """
As a skilled strategist and mathematician, your task is to create a systematic plan to check the validity of a student's proposed solution. 
The student's solution might be either COMPLETE or INCOMPLETE, and your plan should be based solely on the information provided. 
Students might skip a step, but it should not be considered incorrect as long as the EQUATIONS CONVEY THE SAME RELATIONSHIP.

The student's method may vary from the reference solution provided. Your responsibility is to validate the correctness of each step, not to compare it with the reference solution.

Use following information to formulate your verification plan:
- Problem: 
{problem}

- Reference Solution: 
{solution}

- Student's step-by-step solution: 
{student_steps_arr}

{context_for_correctly_verified_steps}
So, Based on the student's solution, devise a detailed plan to verify the student's solution starting from Step No-->{check_from}.

Remember, your role is not to determine the correctness of the student's steps, but to provide a plan and context for verification that will be used by verifier.

Please respond in the following JSON format:
{{
	"is_student_solution_complete" : <True/False>,
	"verification_plans" : [
		{{
			"step_{check_from}" : "<plans>"
		}},
		..
		..
		{{
			"step_i" : "<plans>"
		}}
	]
}}
"""



autograde_planner_init_prompt = """
You are excellent math expert and decision maker who will make plans for verification of student's solution.

The Planner's task is to formulate a step-by-step plan to validate the correctness of the proposed solution of Student.
Student's solution can be COMPLETE / INCOMPLETE . So, Planner have to make plans for only what is provided.

Student's approach can be different from given in solution, You have been provided solution only for reference. So, just check correctness of each step.

So, Planner will be provided 4 things on the basis of which you have to make a plan on how to verify student's solution.
1. Problem   2. Correct Solution     3. Step by step solution of student    4.correctly_verified_upto
Student solution is verified till step number --> "correctly_verified_upto" value . So , u have to make plan for  student solution after this step only.

Use following information to formulate your verification plan:
- Problem: 
{problem}

- Reference Solution: 
{solution}

- Student's step-by-step solution: 
{student_steps_arr}

{context_for_correctly_verified_steps}

According to the student's solution , you have to make a excellent step-by-step plan on how we will check student's solution from Step No-->{check_from}.

Planner is very smart and intelligent and expert of all types of problems like logical reasoning, word problems, algebra, geometry, calculus, etc.
Planner is always careful and strict when making plans to verifying the solution ,especially in the case of Logical Reasoning problems such as Data Sufficiency, Statement and Assumption, and Statement and Conclusion.

Please respond in the following JSON format:
{{
	"is_student_solution_complete" : <True/False>,
	"verification_plans" : [
		{{
			"step_{check_from}" : "<plans>"
		}},
		..
		..
		{{
			"step_i" : "<plans>"
		}}
	]
}}
"""


# Planner prompt

autograde_planner_init_prompt = """
You are excellent math expert and decision maker who will make plans for verification of student's solution.

The Planner's task is to formulate a step-by-step plan to validate the correctness of the proposed solution of Student.
Student's solution can be COMPLETE / INCOMPLETE . So, Planner have to make plans for only what is provided.

Student's approach can be different from given in solution. So, just check correctness of each step.

Use following information to formulate your verification plan:
- Problem: 
{problem}

- Reference Solution: 
{solution}

- Student's step-by-step solution: 
{student_steps_arr}

{context_for_correctly_verified_steps}

According to the student's solution , you have to make a excellent step-by-step plan on how we will check student's solution from Step No-->{check_from}.

Planner is very smart and intelligent and expert of all types of problems like logical reasoning, word problems, algebra, geometry, calculus, etc.
Planner is always careful and strict when making plans to verifying the solution ,especially in the case of Logical Reasoning problems such as Data Sufficiency, Statement and Assumption, and Statement and Conclusion.

Please respond in the following JSON format:
{{
	"is_student_solution_complete" : <True/False>,
	"verification_plans" : [
		{{
			"step_{check_from}" : "<plans>"
		}},
		..
		..
		{{
			"step_i" : "<plans>"
		}}
	]
}}
"""


autograde_planner_init_prompt = """
You are excellent math expert and decision maker who will make plans for verification of student's solution.

The Planner's task is to formulate a step-by-step plan to validate the correctness of the proposed solution of Student.
Student's solution can be COMPLETE / INCOMPLETE . So, Planner have to make plans for only what is provided.

Student's approach can be different from given in solution, You have been provided solution only for reference. So, just check correctness of each step.

Use following information to formulate your verification plan:
- Problem: 
{problem}

- Reference Solution: 
{solution}

- Student's step-by-step solution: 
{student_steps_arr}

{context_for_correctly_verified_steps}

According to the student's solution , you have to make a excellent step-by-step plan on how we will check student's solution from Step No-->{check_from}.

Planner doesn't have to make any conclusion whether student's step is correct or not , just provide plan for checking.
But Student's steps from step {check_from} should correctly sense from its previous steps
 
Please respond in the following JSON format:
{{
	"is_student_solution_complete" : <True/False>,
	"verification_plans" : [
		{{
			"step_{check_from}" : "<plans>"
		}},
		..
		..
		{{
			"step_i" : "<plans>"
		}}
	]
}}
"""