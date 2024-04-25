# Import necessary libraries
from flask import Flask, render_template, request
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.chains.llm import LLMChain
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import os
import PyPDF2

# Set up Flask application
app = Flask(__name__)

# Configure OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

# Initialize OpenAI model
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle form submission
@app.route('/process', methods=['POST'])
def process():
    # Get user input from form
    user_question = request.form['question']
    user_pdf_path = request.files['pdf']

    # Load PDF content
    pdf_text = extract_text_from_pdf(user_pdf_path)
    
    # Define system message
    system_message_entity_prompt = """You are an expert in reading articles. Please read the article carefully and answer the question about it. Please answer only based on the given text, without adding your own interpretation."""
    
    # Create prompt template
    prompt_template_entity = ChatPromptTemplate.from_messages([
        ("system", f'''{system_message_entity_prompt}'''),
        ("human", user_question)
    ])
    
    # Initialize LLMChain
    llm_chain = LLMChain(llm=llm, prompt=prompt_template_entity, verbose=True)
    
    # Run the model
    output = llm_chain.run(user_input=pdf_text)
    
    return render_template('result.html', result=output)

if __name__ == '__main__':
    app.run(debug=True)
