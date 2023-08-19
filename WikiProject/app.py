from flask import Flask, render_template, request, send_from_directory
from gtts import gTTS
import os


from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)


#AI focused code
openai_api_key='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'
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
llm = OpenAI(model_name="gpt-3.5-turbo-0301", openai_api_key=openai_api_key)

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

chat = ChatOpenAI(temperature=1, openai_api_key=openai_api_key)

def get_wikipedia_content(page_title):
    page_title = page_title.replace(' ', '_')
    url = f"https://en.wikipedia.org/wiki/{page_title}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return f"Error {response.status_code}: Unable to fetch the Wikipedia page."

    soup = BeautifulSoup(response.content, 'html.parser')
    content_div = soup.find('div', {'id': 'mw-content-text'})

    for unwanted_tag in content_div(['script', 'style', 'table', 'footer']):
        unwanted_tag.extract()

    return content_div.get_text()

def getllmoutput(llminput, added_prompt=""):
    # added_prompt = "make this into a short podcast:"
    llminput = added_prompt + llminput
    llmoutput = llm(llminput)
    return llmoutput


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['text']
        #here is where I'll do the data processing
        text = get_wikipedia_content(title)
        text = getllmoutput(text, added_prompt="make this into a short podcast:")
        tts = gTTS(text=text, lang='en')
        filename = title + "podcast.mp3"
        tts.save(filename)
        return send_from_directory(os.getcwd(), filename, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)




# from flask import Flask, render_template, request
# import requests
# from bs4 import BeautifulSoup

# app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     content = ""
#     if request.method == 'POST':
#         title = request.form['title']
#         content = get_wikipedia_content(title)

#     return render_template('index.html', content=content)



# if __name__ == '__main__':
#     app.run(debug=True)