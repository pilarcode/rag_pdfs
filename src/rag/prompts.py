

LANGUAGE_PROMPT_TEMPLATE="""What is the language of the text:'{question}'?. 
{format_instructions}
"""



ANSWER_PROMPT_TEMPLATE="""Answer the question based only on the following context:
<context>
{context}
</context>

Translate the answer to {language}.
Query: {query}
"""


PROMPT_TEMPLATE = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer. 
{context}
Query: {query}
Helpful Answer:"""


RAG_FUSION_PROMPT_TEMPLATE="""
You are a helpful assistant that generates multiple search queries based on a single input query.
Generate multiple search queries related to:
<query>
{query}
</query>

OUTPUT (4 queries):
"""