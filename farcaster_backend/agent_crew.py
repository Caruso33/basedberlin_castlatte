import os
from crewai import Agent, Crew, Process
from langchain_groq import ChatGroq
import dotenv

dotenv.load_dotenv()


API_KEY_GROQ = os.getenv("API_KEY_GROQ")
GROQ_LLM = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.0,
    api_key=API_KEY_GROQ,
)


cleanerAgent = Agent(
    role="Filter and curate content relevant to the user's specified interests.",
    goal="""Pass only the posts that are relevant to the user's interest in (AI) from the provided list of all posts within the last 24 hours.""",
    backstory="""a sophisticated AI assistant designed to help users manage their information intake by filtering out irrelevant content. Developed with advanced natural language processing capabilities, this agent understands the user's interests and can accurately identify and curate content that matches those interests.""",
    llm=GROQ_LLM,
    verbose=True,
    allow_delegation=False,
    max_iter=5,
    memory=True,
)

AgentCrew = Crew(
    agents=[cleanerAgent],
    tasks=[],
    verbose=2,
    process=Process.sequential,
)

fid = 3
casts = [
    {"text": "text1"},
    {"text": "text2"},
    {"text": "text3"},
    {"text": "text4"},
    {"text": "text5"},
]

result = AgentCrew.kickoff(inputs={"fid": fid, "casts": casts})

print(f"result {result}\n")
