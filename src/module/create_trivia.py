import dotenv
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq


from module.citation_chain import create_trivia_with_citation_chain


dotenv.load_dotenv()

def generate_trivia(num_questions: str = "2", context: str = ""):
    # TODO: Add logic to determine the number of urls to extract based on number of questions
    # urls = get_urls(number=2)
    # formatted = extract_urls(urls=urls)

    llm = ChatGroq(temperature=0, model="llama3-70b-8192")
    chain = create_trivia_with_citation_chain(llm)

    result = chain.invoke({"context": context, "num_questions": num_questions})
    return result

# if __name__ == "__main__":
#     result = generate_trivia(num_questions="2")
#     print(result)
