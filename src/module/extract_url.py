from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
import pandas as pd


df = pd.read_csv("src/module/data/resources.csv")
df.replace('\n', '', regex=True, inplace=True)
df.replace(' ', '', regex=True, inplace=True)

def get_categories():
    return df['Category'].unique().tolist()

def get_urls(category: str = 'Water', number: int = 1):
    cat_df = df.loc[df['Category'] == category]
    cat_df = cat_df.sample(number)['Resources']
    return cat_df.values.tolist()

def extract_urls(urls: list = []):
    # Add logic to determine the number of urls to extract based on number of questions
    # urls = get_urls(number=number)
    
    loader = WebBaseLoader(urls)
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()

    docs_transformed = bs_transformer.transform_documents(docs,       
            unwanted_tags=["script", "style", "footer", "header", "nav", "form", "noscript"],
            remove_lines=True,
            remove_comments=True)
    
    formatted = [
        f"Source ID: {i}\nArticle Title: {doc.metadata}\nArticle Snippet: {doc.page_content}"
        for i, doc in enumerate(docs_transformed)
    ]
    return formatted

# if __name__ == "__main__":
#     formatted = extract_urls()
#     print(formatted)
