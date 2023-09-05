import os,json
import openai
from autogradingPrompts import autograder_sys_prompt , autograde_soln_init
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def AutoGrade(Question, correct_soln, student_portion, autograder_sys_prompt_fun):
    # print(autograde_soln_init.format(problem=Question, correct_solution=correct_soln, student_solution=student_portion))
    # print("")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": autograder_sys_prompt_fun
            },
            {
                "role": "user",
                "content": autograde_soln_init.format(problem=Question, correct_solution=correct_soln, student_solution=student_portion)
            }
        ],
        temperature=0,
        max_tokens=512,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    assistant_response = response.choices[0].message["content"]
    response_dictionery = json.loads(assistant_response)
    return response_dictionery


Question = """
Two water taps together can fill a tank in 9 ⅜ hours. The tap of larger diameter takes 10 hours less than the smaller one to fill the tank separately. Find the time in which each tap can separately fill the tank.
"""
correct_soln = """
Let the time taken by the smaller pipe to fill the tank be x hr.
Time taken by the larger pipe = (x - 10) hr
Part of tank filled by smaller pipe in 1 hour = 1/x
Part of tank filled by larger pipe in 1 hour = 1/(x - 10)

According to the problem, both pipes together can fill the tank in 9 3/8 hours, which is 75/8 hours. So, the part of the tank they can fill in 1 hour is 8/75.

Therefore, we can set up the equation:
1/x + 1/(x - 10) = 8/75
=> (x-10 + x)/ [x(x - 10)] = 8/75
=> (2x - 10) / [x(x - 10)] = 8/75
=> 75(2x - 10) = 8x(x - 10)
=> 150x - 750 = 8x^2 - 80x
=> 8x^2 - 230x + 750 = 0
=> 8x^2 - 200x -30x + 750 = 0
=> 8x(x-25) - 30(x-25) = 0
=> (x-25)(8x-30) = 0
=> x = 25, 30/8

Time taken by the smaller pipe cannot be 30/8 = 3.75 hours. As in this case, the time taken by the larger pipe will be negative, which is logically not possible.
Therefore, time taken individually by the smaller pipe and the larger pipe will be 25 and 25 - 10 =15 hours respectively.
"""
student_portion = """
Let the time taken by the larger pipe to fill the tank be x hr. 
Time taken by the smaller pipe = (x + 10) hr
Part of tank filled by larger pipe in 1 hour = 1/x
Part of tank filled by smaller pipe in 1 hour = 1/(x + 10)
It is given that the tank can be filled in 9 ⅜ = 75/8 hours by both the pipes together. Therefore,
1/x + 1/(x + 10) = 8/75
"""

student_portion1 = """
Let the time taken by the smaller pipe to fill the tank be x hr. 
Time taken by the larger pipe = (x + 10) hr
Part of tank filled by smaller pipe in 1 hour = 1/x
Part of tank filled by larger pipe in 1 hour = 1/(x + 10)
It is given that the tank can be filled in 9 ⅜ = 75/8 hours by both the pipes together. Therefore,
1/x + 1/(x - 10) = 8/75
"""
student_portion2 = "1/z + 1/(z + 10) = 8/75"
student_portion3 = "1/z + 1/(z - 10) = 8/75"
student_portion4 = """
Let the smaller tap take x hours to fill the tank on its own.
So, the larger tap takes (x - 10) hours .

Together, they fill the tank in 9 ⅜ hours = 9.375 hours.

The combined rate of both taps is 1/9.375 of the tank per hour.

So, the rate of the smaller tap = 1/x of the tank per hour,
 and the rate of the larger tap =  1/(x - 10) of the tank per hour.

Now, we can set up an equation:

1/x + 1/(x - 10) = 1/9.375

"""

Question_Input_pair1 = [Question,correct_soln,student_portion]
Question_Input_pair2 = [Question,correct_soln,student_portion1]
Question_Input_pair3 = [Question,correct_soln,student_portion2]
Question_Input_pair4 = [Question,correct_soln,student_portion3]
Question_Input_pair7 = [Question,correct_soln,student_portion4]

Question = """
A fruit vendor purchased x boxes of raspberries and 4 times as many kiwis as raspberries. In addition, he purchased 2 fewer boxes of blueberries
 than raspberries. Each box of raspberries costs $4, a box of kiwis costs $8, and a box of blueberries costs $6. Find the amount in dollars that the
 fruit vendor spent on the boxes of blueberries if he paid $156 in total.
"""
correct_soln = """
Number of boxes of raspberries = x
Number of boxes of kiwis = 4x
Number of boxes of blueberries = x - 2
Total amount that the fruit vendor spent = $156
4x + 8(4x) + 6(x - 2) = 156
4x + 32x + 6x - 12 = 156
42x = 168
x = 4
Number of boxes of blueberries = 4 - 2 = 2
Cost of one box of blueberries = $6
The amount spent on the boxes of blueberries = 2 * 6 = $12
"""
student_portion1 = """
Number of boxes of raspberries = x
Number of boxes of kiwis = 4x
Number of boxes of blueberries = x + 2
Total amount that the fruit vendor spent = $156
4x + 8(4x) + 6(x + 2) = 156
4x + 32x + 6x + 12 = 156
42x = 144
x = 24/7
Number of boxes of blueberries = 4 - 2 = 2
Cost of one box of blueberries = $6
The amount spent on the boxes of blueberries = 2 * 6 = $12
"""
student_portion2 = """
Number of boxes of raspberries = x
Number of boxes of kiwis = 4x
Number of boxes of blueberries = x - 2
Total amount that the fruit vendor spent = $156
8x + 4(4x) + 6(x - 2) = 156
8x + 16x + 6x - 12 = 156
30x = 168
x = 84/15
Number of boxes of blueberries = 4 - 2 = 2
Cost of one box of blueberries = $6
The amount spent on the boxes of blueberries = 2 * 6 = $12

"""
student_portion3 = """
Let the third integer integer be a.
Given that sum of the three consecutive integers = -63.
a -2 + a -1 + a = -63
3a -3 = -63
3a = -60
a = -20
Therefore, three consecutive integers are -22, -21 and -20.
"""
student_portion4 = """
Let the first integer be a.
Given that sum of the three consecutive integers = -63.
a -2 + a -1 + a = -63
3a -3 = -63
3a = -60
a = -20
Therefore, three consecutive integers are -22, -21 and -20.
"""
student_portion5 = """
Let the second integer be a.
Given that sum of the three consecutive integers = -63.
a -2 + a -1 + a = -63
3a -3 = -63
3a = -60
a = -20
Therefore, three consecutive integers are -22, -21 and -20.
"""
Question_Input_pair8 = [Question,correct_soln,student_portion1]
Question_Input_pair9 = [Question,correct_soln,student_portion2]
Question_Input_pair10 = [Question,correct_soln,student_portion3]
Question_Input_pair11 = [Question,correct_soln,student_portion4]
Question_Input_pair12 = [Question,correct_soln,student_portion5]
a,b,c = Question_Input_pair9
print(AutoGrade(Question=a,correct_soln=b,student_portion=c,autograder_sys_prompt_fun=autograder_sys_prompt))
