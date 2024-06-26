import json
import os
import re

import dotenv
from crewai import Agent, Crew, Process, Task
from crewai.tasks.task_output import TaskOutput
from langchain_groq import ChatGroq

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
    callback=lambda output: save_file(output, "filtered_content.json"),
)

analyzerAgent = Agent(
    role="Analyzes the filtered content to identify themes, trends, and important updates.",
    goal="Extract meaningful insights from the filtered data.",
    backstory="With a foundation in trend analysis and predictive modeling, this agent has been fine-tuned to pick up on subtle nuances in social interactions and community dynamics.",
    llm=GROQ_LLM,
    verbose=False,
    allow_delegation=False,
    max_iter=5,
    memory=True,
)

analyzerTask = Task(
    description="""
                        Analyze the feed of the user's fid {fid} filtered by user's topic of interest: \n {interests} \n & extract various insights, identify trending discussions, trending topics, community sentiment, mention frequency analysis.
                        Context: The feed is from a decentralized social media network/protcool called, farcaster. Warpcast is the first and biggest client on this protocol. The network is built on Optimism (Layer2 on Ethereum) and is similar to twitter and reddit. Users can post called 'cast', own their identity and data and can freely move to another client app, without losing their network and data. Channels on farcaster written as /channel_name are similar to subreddits or groups in SM platforms. Most popular activity on farcaster is tipping memecoins, most famously $DEGEN. Other famous memecoins are $TN100x aka Ham, floties, $onchain, $higher, $build (where builders nominate (tip) each other), $enjoy and bunch of other. Most these memecoins are on Base network (A layer2 on ethereum). Base is the most used blockchain network around where most activities happen on farcaster. 
                        json output template: 
                        "trending_discussions": []
                        "trending_topics": []
                        "community_sentiment": []
                        "mention_frequency_analysis":[]
                        """,
    expected_output="""
                            A valid json. No preamble or epilogue, only pure parsable JSON.
                            """,
    agent=analyzerAgent,
    callback=lambda output: save_file(output, "analyzed_content.json"),
)

summerizeAgent = Agent(
    role="Creates a concise, easy-to-digest summary of the analyzed data.",
    goal="Provide a clear and comprehensive summary of the most important insights from the past 24 hours.",
    backstory="Born from a need to translate complex datasets into executive summaries for busy stakeholders, this agent specializes in clear, effective communication.",
    llm=GROQ_LLM,
    verbose=False,
    allow_delegation=False,
    max_iter=5,
    memory=True,
)

summerizeTask = Task(
    description="""
                        Generate a brief report of the user's fid {fid} analyzed feed. Condense it in a paragraph of 50 words maximum.
                        json Template: "Topic of interest": "50 words summary"
                        """,
    expected_output="""
                            A valid jason. No preamble or epilogue, only pure parsable JSON.
                            """,
    agent=summerizeAgent,
    callback=lambda output: save_file(output, "summarized_content.json"),
)

AgentCrew = Crew(
    agents=[cleanerAgent, analyzerAgent, summerizeAgent],
    tasks=[filterTask, analyzerTask, summerizeTask],
    verbose=2,
    process=Process.sequential,
)

if __name__ == "__main__":

    fid = 3
    casts = [
        {"text": "text1"},
        {"text": "text2"},
        {"text": "text3"},
        {"text": "text4"},
        {"text": "text5"},
    ]
    interests = ["AI", "web3"]

    result = AgentCrew.kickoff(
        inputs={"fid": fid, "casts": casts, "interests": interests}
    )

    print(f"result {result}\n")


def save_file(output: TaskOutput, filename: str) -> bool:

    match = re.search(r"fid (\d+)", output.description)
    if match:
        fid = int(match.group(1))
        print("matched\n")

    is_json_parsable_cast = is_json_parsable(output.exported_output)
    print(f"parsable? {is_json_parsable_cast}\n")

    if fid is not None and is_json_parsable_cast:
        print("is parsable\n")

        with open(os.path.join(os.getcwd(), "data", f"{fid}_{filename}"), "w") as f:
            f.write(str(output.exported_output))

        print(f"Saved file {fid}_{filename}\n")
        return True

    print("Failed to save file\n")
    return False


def is_json_parsable(input_string: str) -> bool:
    try:
        json.loads(input_string)
        return True
    except json.JSONDecodeError:
        return False
