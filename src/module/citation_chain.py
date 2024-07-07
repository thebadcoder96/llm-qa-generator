from typing import Iterator, List

from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field

from langchain_core.runnables import RunnablePassthrough



class FactWithEvidence(BaseModel):
    """Class representing a single statement.

    Each fact has a body and a list of sources.
    If there are multiple facts make sure to break them apart
    such that each one only uses a set of sources that are relevant to it.
    """

    fact: str = Field(..., description="Body of the sentence, as part of a response")
    trivia_answer: str = Field(..., description="Trivia-style answer, like one word or phrase")
    substring_quote: str = Field(
        ...,
        description=(
            "The source should be a direct quote from the context, "
            "as a substring of the original content"
        ),
    )
    sources: str = Field(
        ..., description="The EXACT source link corresponding to the substring_quote"
    )

    def _get_span(self, quote: str, context: str, errs: int = 100) -> Iterator[str]:
        import regex

        minor = quote
        major = context

        errs_ = 0
        s = regex.search(f"({minor}){{e<={errs_}}}", major)
        while s is None and errs_ <= errs:
            errs_ += 1
            s = regex.search(f"({minor}){{e<={errs_}}}", major)

        if s is not None:
            yield from s.spans()

    def get_spans(self, context: str) -> Iterator[str]:
        for quote in self.substring_quote:
            yield from self._get_span(quote, context)


class QuestionAnswer(BaseModel):
    """Trivia style questions and its answers as a list of facts each one should have a source.
    each sentence contains a body and a list of sources."""

    question: str = Field(..., description="Question that was asked")
    wrong_answer: str = Field(..., description="A trivia-style answer that is wrong")
    difficulty: str = Field(..., description="Difficulty level of the question")
    answer: FactWithEvidence = Field(
        ...,
        description=(
            "Body of the answer, the fact should be "
            "its separate object with a body and a list of sources"
        ),
    )

class QuestionAnswersList(BaseModel):
    """Class representing a list of trivia style questions and answers with correct and exact citations.
    each sentence contains a body and a list of sources."""

    trivias : List[QuestionAnswer] = Field(..., description="List of questions and answers as a list of facts")


def create_trivia_with_citation_chain(llm: BaseLanguageModel) -> RunnablePassthrough:
    """Create a trivia with citation chain.

    Args:
        llm: Language model to use for the chain.

    Returns:
        Chain that can be used to genetate trivia questions and answers with citations.
    """
    messages = [
        SystemMessage(
            content=(
                "You are a world class algorithm to generate trivia "
                "questions and answers with correct and exact citations."
            )
        ),
         HumanMessagePromptTemplate.from_template(
                "Generate {num_questions} sets of trivia-style questions "
                "and answers using the following context"
        ),
        MessagesPlaceholder("context"),
        HumanMessage(
            content=(
                "Tips: Make sure to cite your sources, "
                "and use the exact words from the context."
            )
        ),
    ]
    prompt = ChatPromptTemplate(messages=messages)

    chain = prompt | llm.with_structured_output(QuestionAnswersList)
    return chain
