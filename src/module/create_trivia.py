import dotenv
from langchain_openai import ChatOpenAI


from citation_chain import create_trivia_with_citation_chain
from extract_url import extract_urls


dotenv.load_dotenv()


question = "4"
# Add logic to determine the number of urls to extract based on number of questions
formatted = extract_urls(number=2)

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
llm_chain = create_trivia_with_citation_chain(llm)

result = llm_chain.run(num_questions=question, context=formatted)
print(result)
