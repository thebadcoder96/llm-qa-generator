from calendar import c
import streamlit as st

from module.extract_url import get_categories, get_urls, extract_urls
from module.create_trivia import generate_trivia

st.set_page_config(page_title="Trivia Generator", page_icon="🙋🏻‍♂️",)


st.title("🙋🏻‍♂️ Trivia Generator")

st.write("Welcome to the Trivia Generator!")
st.write("This app will help you generate trivia questions and answers using the relevant sources. 📚")

st.write("Choose a category and the number of questions you want to generate:")

with st.form("options_form", clear_on_submit=False):
        cols = st.columns(2)
        with cols[0]:
            category = st.selectbox("**Select Category:**", get_categories())

        with cols[1]:
            num_questions = st.number_input("**Number of Questions:**", min_value=1, max_value=10, value=2)
        submitted = st.form_submit_button(label='Generate Trivia')

if submitted:
     if category:
          urls = get_urls(category=category, number=num_questions)
          st.write(f"Chose {len(urls)} URLs for {category}.")
          with st.spinner(f"Extracting {category} URLs..."):
              for url in urls:
                st.write(f"- {url}")
              context = extract_urls(urls=urls)
              st.success(f"Extracted Successfully!")
               
          with st.spinner(f"Generating {num_questions} trivia questions and answers..."):
               result = generate_trivia(num_questions=num_questions, context=context)
               st.success(f"Generated Successfully!")
               st.subheader("Trivia Questions and Answers")
               for trivia in result.trivias:
                    st.write(f"Question: {trivia.question}")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"Answer: {trivia.answer.trivia_answer}")
                    with col2:
                        st.write(f"Wrong Answer: {trivia.wrong_answer}")
                    st.write(f"Fact/Reason: {trivia.answer.fact}")
                    st.write(f"Sources: {trivia.answer.sources}")
                    st.write(f"Citation: ... _{trivia.answer.substring_quote}_ ...")
                    st.write(f"Difficulty: {trivia.difficulty}")
                    st.write("---")