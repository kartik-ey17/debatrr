import ollama
import json

cloud_model = "gpt-oss:120b-cloud"

straycat = input("Elaborate any idea you have and want to stress test : ")

prompt = f"""

You are a master in taking vague ideas and turning them into structured JSON ,
your job is to look at the input and analyze the input which is the idea , to the best of your ability , you have to extract the following data , whether stated explicitly or not , but if any of the below field is genuinely not predicatable at all , leave it empty , the fields are:
1. core_claim - it is a one sentence distillation of what the idea is actually asserting. Basically a one line summary of what the core of the idea or input is.
2. domain - whether the idea or input belongs to tech domain , health or finance or even farming etc. list all the major related domains only , you can skip the minor domains that might fall into the idea but do mention the major ones.
3. target_audience - it is a reasoning category , reason through the idea or input and predict what type of audience could be the target of this specific idea , the target audience could be a specific age group , a certain country people , people from a specific profession or sport ; there can be multiple target audience but mention only the major ones.
4. assumed_constraints - again a reasoning category , be very reasonable on this one , if unable to find out , leave it empty , you basically have to analyze the idea on this one and predict what the idea is silently assuming true ; like if i say i am making an ai for farmers to increase their productivity , i am here assuming that 1. farmers are used to ai tech and can handle ai and even pay for it ; 2. I am assuming that farmers want their productivity increased , i am assuming the pain here ; which may or may not exist ; you have to include these types of assumptions the input or idea would be hiding silently behind the words.
5. success_conditions - basically , what does it look like if the idea works? predict what the 'success' could be based on the input of the user , again a tricky reasoning job.
6. potential_risks - this one is tricky , you basically have to point out the obvious risks the ideas have , you have to evaluate the idea a bit here and point ouot some surface level flaws , no need to explain why those flaws , just mention what you can predict that can go wrong. 

Your output should be like :
core_claim : "..." ,
domain : "..." ;
target_audience : "..." ,
assumed_constraints : "..." ,
success_conditions : "..." ,
potential_risks : "..."

thats it , nothing other than this , just an output of this format.

the idea or input - {straycat}
Return ONLY JSON output
"""

response = ollama.generate(
    model = 'gpt-oss:120b-cloud',
    prompt = prompt ,
     stream = False
)

raw = response["response"]

data = json.loads(raw)

for_agent_mem = []
against_agent_mem = []

transcript = []

def add_to_transcript(agent_name , argument):
    transcript.append({'agent' : agent_name ,'content' : argument})
def for_agent() :
    for_prompt = f"""
    You are a master in debating for arguments , meaning you are very good in debating in the favour of the argument you have a tough opponent who will argue against your arguments , HOLD A GENUINE DEBATE WITH THEM;
    Your job is to go through the user specified idea and past arguments on the topic thoroughly and speak in the favour of the idea or the argument that is mentioned.
    {data} contains the essential information about the idea specified by user in detail , take information from that , speak only FOR the arguments mentioned , NEVER go off topic or return IRRELEVANT statements ; ONLY argue LOGICALLY ; go deep on what possible GOOD the idea could have and if possible support it by a numerical metric IF NECESSARY , IF NOT , DONT , 
    {for_agent_mem} is a list of arguments you have stated in the past ; go through them for relevancy and context. Look only at idea if this list is empty.
    {against_agent_mem} is a list of arguments your opponent , who is speaking against the idea. This is highly relevant for you as you have to tackle arguments from this , DONT REPEAT YOUR ARGUMENTS , look at {transcript} to check if the topic has already been raised , if it is already raised DONT EVER MENTION IT AGAIN , if this list is empty , look only at the idea.

    Your output should be a string only ;
    the data you will be given is structured as :
    core claim:
    domain:
    target_audience:
    assumed_constraints:
    success_conditions:
    potential_risks:

    just for example , you can start with reasoning about the vision behind the core claim , the target audience relevancy , the increasing growth of the domain , (if)success conditions being achieveable ; but everything here is a big IF , dont argue factually wrong things , if a field or domain has no obvious growth , dont make it up and present false arguments.
    
    max 120 words per round , dont go horizontal and dont try to add many points in one round , go for 1-2 points and go a bit deep into them and reason how they favour the claim.
"""
    response = ollama.generate(
        model = "gpt-oss:120b-cloud",
        prompt = for_prompt,
        stream = False
    )

    bruh = response["response"]
    for_agent_mem.append(bruh)
    add_to_transcript("for_agent" , bruh)
    print(bruh)

def against_agent():
    against_prompt = f"""
    you are a master in debating against an argument , meaning , you look at the core idea and the argument passed by your opponent , who is a master in speaking in favour of the argument , 
    you have to understand the core idea by reading {data} which contains structured content of the idea , then you have to look at {for_agent_mem[-1]} and tackle their claims and add 1-2 points against the core idea itself as well
    the idea you will be given is structured as:
    core claim:
    domain:
    target_audience:
    assumed_constraints:
    success_conditions:
    potential_risks:

    as you can see , going deeper in the potential risks section and assumed constraints section from the idea is benefitial for your argument , 

    your opponent's argument would be basically a string of words and some states , you can pushback through stats or tackle wherever the opponent is off

    note that your output SHOULD NOT EXCEED 90 words , return a string of no more than 90 words , you would get many chances to put your words , try to go for max 3 topics in the entire output for each round.
    Last but not the least , dont behave like you are giving an output to a human , your output is supposed to be in the backend , write the output like you are GENUINELY debating a person , not explaining them or teaching them.
"""
    response = ollama.generate(
        model = 'gpt-oss:120b-cloud',
        prompt = against_prompt,
        stream = False
    )
    against = response["response"]
    against_agent_mem.append(against)
    add_to_transcript("against_agent" , against)
    print(against)

def debate_supervisor():
    eval_prompt = f"""
    You are a professional debate evaluator. Your only job is to evaluate the LAST EXCHANGE of a debate and reurn a JSON score object.
    The idea that the debate is on about is {data} , understand it for the context for further evaluation.
    the last exhange happened was {transcript} ; 

    SCORE on these 5 parameters , each on a scale of 1-5 ONLU:
    1. argument_novelty - did the last exchange introduce any new points or just restate the old ones?
        1 = pure repitition ; 5 = entirely new angles introduced
    2. rebuttal_quality - did "against_agent" address what "for_agent" said , or argue in parallel?
        1 = ignored opponent completely ; 5 = directly dismantled opponent's specific points
    3. depth_of_reasoning - were the arguments surface level or did they go deeper?
        1= generic obvious points ; 5 = nuanced specific reasoning
    4. coverage - how much of the idea's major angles have been addressed across the full debate?
        1 = barely scratched the surface ; 5 = all major angles covered
    5. contention_level - is there still meaningful disagreement or are positions converging?
        1 = both sides essentially agree now ; 5 = strong unresolved disagrerement remains.

    Return ONLY JSON, nothing else , no markdown backticks , no reasoning:
    {{
  "argument_novelty": <1-5>,
  "rebuttal_quality": <1-5>,
  "depth_of_reasoning": <1-5>,
  "coverage": <1-5>,
  "contention_level": <1-5>,
  "reasoning": "<one sentence explaining why you stopped or continued>"
  }}
"""
    response = ollama.generate(
        model = 'gpt-oss:120b-cloud',
        prompt = eval_prompt ,
        stream = False
    )
    evaluation = response["response"]
    value = json.loads(evaluation)
    return value
value = debate_supervisor()

def cut_debate(value, round_no):
    if round_no < 2:
        return False
    if round_no > 6:
        return True
    if value["argument_novelty"] < 3 and value["contention_level" ] < 3:
        return True
    if value["coverage"] >= 4 and value["depth_of_reasoning"] < 3 :
        return True
    return False

round_no = 1
stop = False

while not stop:
    print("----Round", round_no, "----")
    for_agent()
    against_agent()

    scores = debate_supervisor()
    print(f"Supervisor scores are: {scores}")

    stop = cut_debate(scores, round_no)
    round_no += 1

print("Debate completed.")

def insight_agent():
    insight_prompt = f"""
    You are a sharp and serious idea analyst. You have just observed a full debate on an idea and your job is to deliver a final structured verdict.

    idea is {data}
    debate transcript: {transcript}

    Based on the debate above, deliver a verdict on the following structure, return ONLY a JSON , dont reason anything and no markdown backticks :
    {{
        "strongest_argument_for": "<the  most compelling argument made in favour of the idea>",
        "strongest_argument_against": "<the most compelling argument made against the idea.>",
        "fatal_flaw": "<the one thing that could kill this idea if not addressed properly , leave empty string if NONE>"
        "verdict": "<one of:  STRONG IDEA / PROMISING BUT RISKY / NEEDS RETHINKING / FUNDAMENTALLY FLAWED>"
        "confidence": <1-5>
        "reasoning": "<2-3 sentences max on why you gave this verdict , be direct.>"
    }}
    Rules:
    Do not introduce new topics
    Be honest and dont sugarcoat anything
    Your verdict should reflect the weight of evidence from the debate, not your own opinion of the idea.
    If the debate was shallow , reflect that in a lower confidence score.
"""
    response = ollama.generate(
        model= cloud_model , 
        prompt= insight_prompt,
        stream= False
    )
    raw = response["response"]
    return json.loads(raw)

verdict = None

while True:
    print("----What would you like to do next?---- \n")
    print("1. Review the points presented in favor of your idea.")
    print("2. Review the points presented against your idea.")
    print("3. Get a summary and insight on the whole debate.")
    print("4. Exit.")

    choice = input("Choose between 1-4 : ").strip()

    if choice == '1':
        for i, arg in enumerate(for_agent_mem, 1) :
            print(f"Round {i} \n {arg}")

    elif choice == '2':
        for i,arg in enumerate(against_agent_mem, 1):
            print(f"Round{i} \n {arg}")

    elif choice == '3':
        if not verdict:
            verdict = insight_agent()
        print(verdict)
    
    elif choice == '4':
        print("Goodbye!")
    
    else:
        print("Choose a valid option.")
        continue
