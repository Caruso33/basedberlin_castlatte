import os
from crewai import Agent, Crew, Process, Task
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

filterTask = Task(
    description="""
            Receive a long list of posts from the user's fid {fid} feed for the last 24 hours. Process each post, determine its relevance to the user's specified topic of interest: \n {interests} \n, and filter out any posts that do not match this interest. 
            24H feed:\n\n {casts} \n\n
            Context: The feed is from a decentralized social media network/protcool called, farcaster. Warpcast is the first and biggest client on this protocol. The network is built on Optimism (Layer2 on Ethereum) and is similar to twitter and reddit. Users can post called 'cast', own their identity and data and can freely move to another client app, without losing their network and data. Channels on farcaster written as /channel_name are similar to subreddits or groups in SM platforms. Most popular activity on farcaster is tipping memecoins, most famously $DEGEN. Other famous memecoins are $TN100x aka Ham, floties, $onchain, $higher, $build (where builders nominate (tip) each other), $enjoy and bunch of other. Most these memecoins are on Base network (A layer2 on ethereum). Base is the most used blockchain network around where most activities happen on farcaster. 
            """,
    expected_output="""
            A list of filtered social media posts in JSON format. No preamble or epilogue, only pure parsable JSON.
            """,
    agent=cleanerAgent,
)

AgentCrew = Crew(
    agents=[cleanerAgent],
    tasks=[filterTask],
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
interests = ["AI", "web3"]

result = AgentCrew.kickoff(inputs={"fid": fid, "casts": casts, "interests": interests})

print(f"result {result}\n")
