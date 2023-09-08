import os,json
import openai
from autogradeStep_Prompts import autograde_planner_sys_prompt, autograde_verifier_sys_prompt,autograde_planner_init,autograde_verifier_init
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def change_userResponse_format(user_response):
    user_response_dict = []
    for i in range(len(user_response)):
        dic = {"step":i+1,"content":user_response[i]}
        user_response_dict.append(dic)
    return user_response_dict

class AutoGrader:
    def __init__(self,student_data):
        self.problem = student_data["problem"]
        self.correct_solution = student_data["solution"]
        self.student_steps = change_userResponse_format(student_data["student_steps"])
        self.check_from = student_data["correctly_verified_upto"]+1
        self.context_for_correctly_verified_steps = ""
        if self.check_from>1:
            self.context_for_correctly_verified_steps = "Student solution is already correctly verified upto {verified_upto} steps \n".format(verified_upto =student_data["correctly_verified_upto"] )
        self.verifier_student_data = {"problem":self.problem,"Student_steps":self.student_steps,"correctly_verrified_upto":student_data["correctly_verified_upto"]}
        self.planner_data = ""
        self.is_student_solution_complete = True
    
    def Planner(self):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": autograde_planner_sys_prompt
                },
                {
                    "role": "user",
                    "content": autograde_planner_init.format(
                                    problem=self.problem,
                                    solution=self.correct_solution,
                                    student_steps_arr=json.dumps(self.student_steps,indent=4),
                                    context_for_correctly_verified_steps = self.context_for_correctly_verified_steps,
                                    check_from=self.check_from
                                    )
                }
            ],
            temperature=0,
            max_tokens=512,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        assistant_response = response.choices[0].message["content"]
        print("PLANNER")
        print(assistant_response)
        print(" ")
        response_json = json.loads(assistant_response)
        self.is_student_solution_complete = response_json["is_student_solution_complete"]
        self.planner_data = response_json["verification_plans"]
        # print(self.is_student_solution_complete)
        # print(self.planner_data)
        return assistant_response
    
    def Verifier(self):
        # print(autograde_verifier_init.format(student_data=self.verifier_student_data, check_from=self.check_from,Planner_data = json.dumps(self.planner_data,indent = 4)))
        # return None
        print("  ")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": autograde_verifier_sys_prompt
                },
                {
                    "role": "user",
                    "content": autograde_verifier_init.format(student_data=json.dumps(self.verifier_student_data,indent = 4), check_from=self.check_from,Planner_data = json.dumps(self.planner_data,indent = 4))
                }
            ],
            temperature=0,
            max_tokens=512,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        assistant_response = response.choices[0].message["content"]
        print("VERIFIER")
        print(assistant_response)
        return assistant_response

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
      "Let no. of people who like vegetables be p. ",
      " So, no. of people who like fruits will be 4p.",
      "No. of people like vegetables = p+12 ",
      "No. of people like fruits = 4p - 12 ",
      "The number of people who like vegetables would be equal to the number of people who like fruits. So, equations (i) and (ii) must be equal.",
      "4p + 12 = p - 12",
      "3p = -24 ",
      "p = 8",
      "So, No. of people who like fruits is 4p =  32"
  ],
  "correctly_verified_upto": 2
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
      "x(x+1)+8 = (x+2)(x-2)",
      "x^2+x+8 = x^2-2x+2x-4 ",
      "2x^2+x+4 = 0 ",
      "So, it is quadratic equation"
  ],
  "correctly_verified_upto": 1
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
        "let 3x + 9y = -60 is equation 1 and 9x+9y = 90 be equation 2",
        "Subtract equation 1 from equation 2---> (2)-(1)",
        "6x = 30",
        "x = 5",
        "9(5) + 9y = -90",
        "45 + 9y = -90"    
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
      "Let the second integer be a",
      "Given that sum of the three consecutive integers = -63.",
      "a -1 + a + a + 1 = -63",
       "3a = -63",
      "3a = -63",
       "a = -21",
      "Therefore, three consecutive integers are -22, -21 and -20"
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
      "Let the first integer be a",
      "Given that sum of the three consecutive integers = -63.",
      "a -2 + a -1 + a = -63",
       "3a - 3 = -63",
      "3a = -60",
      "a = -20",
       "Therefore, three consecutive integers are -22, -21 and -20"
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
      "Let the second integer be a",
      "Given that sum of the three consecutive integers = -63.",
      "a -2 + a -1 + a = -63",
      "3a - 3 = -63",
      "3a = -60",
      "a = -20",
      "Therefore, three consecutive integers are -22, -21 and -20"
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
      "Let the third integer be a",
      "Given that sum of the three consecutive integers = -63.",
      "a + a +1 + a+2 = -63",
       "3a + 3 = -63",
      "3a = -66",
      "a = -22",
       "Therefore, three consecutive integers are -22, -21 and -20"
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
        "Let the third integer be a",
        "Given that sum of the three consecutive integers = -63.",
        "a -2 + a -1 + a = -63",
        "3a - 3 = -63",
        "3a = -60",
        "a = -20",
        "Therefore, three consecutive integers are -22, -21 and -20"
  ],
  "correctly_verified_upto": 2
}


arr = [test1,test2,test3,test4,test5,test6,test7,test8]
# test1   ---> "4p + 12 = p - 12", instead of "4p - 12 = p + 12",
# test2--> "x^2+x+8 = x^2-2x+2x-4 ",--> "2x^2+x+4 = 0 ",
# test3--->  9x+9y = 90   should be 9x+9y = -90
# test4 ---> correct
# test5---> "Let the first integer be a",---> "a -2 + a -1 + a = -63",
# test6---> "Let the second integer be a",-->  "a -2 + a -1 + a = -63",
# test7 ---> "Let the third integer be a",--> "a + a +1 + a+2 = -63",
# test8 ---> correct



# CURRENTLY GPT CAN'T FIND ERRORS IN TESTCASE 7
for i in range(6,len(arr)-1):
    print("TESTCASE:",i+1)
    obj = AutoGrader(student_data=arr[i])
    obj.Planner()
    print(" ")
    obj.Verifier()
    print(" ")
