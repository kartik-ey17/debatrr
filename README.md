# debatrr
debatrr is an LLM Orchestration to stress test any of your startup ideas.

To validate a business idea , we often have to first research on the idea for a long time , and still we have our biases , **debatrr** makes this process easy by unbiasedly evaluating both the good and bad aspects of the idea and provide a clearer picture of the idea along with useful insights.

**debatrr** takes user input(idea) in free form and enhance it in the form of a clear JSON. Then according to the JSON , an agent speaks FOR the idea and an agent speaks AGAINST the idea for n number of rounds, the 'n' is decided by an evaluating agent which , after every interaction between the 2 agents , gives certain scores which determine when to cut off the debate. After the completion of the debate , the user is given options to view the points raised by the FOR agent or the AGAINST agent , the user may also check out the insights which consists of the strongest arguments and the fatal flaws and other important insights.

# Architecture
- Enrichment Agent - Converts the free form user input(idea) into a structured JSON with necessary categories
- FOR_Agent - Takes in the idea JSON and the AGAINST_Agent's past response to speak in favour of the user's idea.
- AGAINST_Agent - Takes in the idea JSON and the FOR_Agent's argument to speak in opposition of the user's idea.
- Supervising_Agent - Takes in the {transcript} of the past interactions between the two debating agents and generate scores to determine whether the debate is going on track or is going astray.
- Insight_Agent - The Final agent which takes in the {transcript} to generate useful insights on the core idea and helping the user with a clearer , unbiased picture.

# Tech Stack
- Python
- Ollama module
- gpt-oss:120b-cloud
- JSON module

# Setup & Install
Download the Ollama application and create an account on ollama.com to use the cloud model named 'gpt-oss:120b-cloud' ; then *pip install ollama* in the preferred IDE terminal  ; then copy paste the code in the IDE to run the tool in your setup.

# Limitation
No web search feature , The evaluating agent can be upgraded and a better debate cutting logic can be implemented , No GUI , No database storage , The models may hallucinate some of the data.

# Future Upgrades
- Add a web searching module like duckduckgo
- Make the evaluating agent more efficient
- return downloadable pdfs/txt files with a clear format.
- Make more and better guardrails to prevent hallucination till some extent.
 
