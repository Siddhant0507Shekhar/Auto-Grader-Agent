from langchain import PromptTemplate

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


Planner doesn't have to make any conclusion whether student's step is correct or not , just provide plan for checking. 
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


autograde_verifier_sys_prompt = """
You are a super intelligent math expert and precise AI grader for student's solution.
"""

autograde_verifier_init_prompt = """
You're an exceptionally intelligent mathematics expert tasked with verifying students' solutions based on specified plans. Your job is to check student solutions starting from step {check_from}. 
Students may have either COMPLETE or INCOMPLETE solutions, so you must verify only the corresponding steps.
Students might skip a step, but it should not be considered incorrect as long as the EQUATIONS CONVEY THE SAME RELATIONSHIP.

You will receive 4 pieces of information for verification:
1. Question
2. Student's Step-by-Step Solution
3. Correctly Verified Up To Step
4. Plans

{student_data}

Student solutions are verified up to the step number indicated by "correctly_verified_upto." Therefore, you should  start from step {check_from}. Based on the provided plans, you must verify the corresponding student steps.

Here is Plans which u have to STRICTLY follow to check studnet's solution:
{Planner_data}

Here is the format for your JSON output:

{{
 “steps_data”: [
{{
"step_no":{check_from},
“Valid_response”: 0/1,
“Error”: “feedback for this step ( error if detected or overview of step)”,
"Misconception":<If student step is wrong then write about the misconception he has about this step in 3-4 words/ else None>
}},
...and so on for further steps
]
}}
For each step , if that particular step is wrong then Valid_response corresponding to that step will be 0 else 1.
You are an excellent Verifier and you have to STRICTLY give results as Verifier's output in the above mentioned format not anything else.
"""



autograde_planner_init = PromptTemplate(
    input_variables=["problem", "solution","student_steps_arr","context_for_correctly_verified_steps","check_from"],
    template=autograde_planner_init_prompt
)

autograde_verifier_init = PromptTemplate(
    input_variables=[ "check_from","student_data","Planner_data"],
    template=autograde_verifier_init_prompt
)

