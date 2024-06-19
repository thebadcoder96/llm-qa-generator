import dotenv
from langchain_openai import ChatOpenAI


from citation_chain import create_trivia_with_citation_chain
from extract_url import extract_urls


dotenv.load_dotenv()

def generate_trivia(num_questions: str = "2"):
    # TODO: Add logic to determine the number of urls to extract based on number of questions
    formatted = extract_urls(number=2)

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    chain = create_trivia_with_citation_chain(llm)

    result = chain.invoke({"context": formatted, "num_questions": num_questions})
    return result

if __name__ == "__main__":
    result = generate_trivia(num_questions="2")
    print(result)
