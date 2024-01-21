import os
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from llm.pinecone_llm import PinecoinOperations
from pypdf import PdfReader
# from utils import *
from langchain.llms import AzureOpenAI






class Lang():

    def __init__(self,key= "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"):
        self.key=key


    def load_documents(self,file):
        print(f'Loading{file}')
        loader = PyPDFLoader(file)
        data = loader.load()  # the list that contain the pages elli en3amalha loading
        return data



    def chunk_data(self,data, chunksize):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunksize, chunk_overlap=40)
        chunks = text_splitter.split_documents(data)
        return chunks

    def create_embeddings(self,chunks_data, key):
        embeddings = OpenAIEmbeddings(openai_api_key=key)

        pinecone = PinecoinOperations()
        index_name= "gp"
        vector_store= Pinecone.from_existing_index(index_name,embeddings)
        vector_store.add_documents(chunks_data)
        return vector_store


    def return_vectore_store(self):
        embeddings = OpenAIEmbeddings(openai_api_key="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")
        pinecone = PinecoinOperations()
        index_name = "gp"
        vector_store = Pinecone.from_existing_index(index_name, embeddings)
        return vector_store

    def qa(self, vector_store_q, query):
        llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key="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")
        #embeddings = AzureOpenAI(deployment_name="first", model_name="gpt-35-turbo")
        retriever = vector_store_q.as_retriever(search_type="similarity", search_kwargs={'k': 3})
        chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

        answer_qa = chain.run(query)

        return answer_qa


    def qa_services(self, vector_store_q, query):
        llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key="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")
        retriever = vector_store_q.as_retriever(search_type="similarity", search_kwargs={'k': 5})
        chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

        answer_qa = chain.run(query)
        return answer_qa