import chromadb
from google import genai
from dotenv import load_dotenv
from google.genai import types

load_dotenv()

# setting the environment

DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(name="EU_AI_Act")


user_query = input("What do you want to know about EU AI Act?\n\n")

results = collection.query(
    query_texts=[user_query],
    n_results=30
)

for doc in results['documents']:
    print(doc)
# print(results['documents'])
#print(results['metadatas'])

client = genai.Client()

system_prompt = """
You are a helpful assistant to AI deployers. You answer questions about the EU AI Act and compliance to the regulatory framework. 
But you only answer based on knowledge I'm providing you. You don't use your internal 
knowledge and you don't make things up.
If you don't have the exact answer, give context and information that can be useful to the user based on the data I'm providing you.
By the end of your answer, give compliance recommendations to the user based on the EU AI Act.
Always provide the metadata (like page number and short citation in quotes from the document) of the information you are using to answer the user's question.
--------------------
The information you have is the following:
"""+str(results['documents'])+str(results['metadatas'])+"""
"""

#print(system_prompt)

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    config=types.GenerateContentConfig(
    system_instruction=system_prompt
    ),
    contents=user_query
)

print("\n\n---------------------\n\n")

print(response.text)