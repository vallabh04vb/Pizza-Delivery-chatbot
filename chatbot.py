import openai
import gradio as gr
import os
import locale
# print(locale.getpreferredencoding())
locale.getpreferredencoding = lambda: "UTF-8"



from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv("OPENAI_API_KEY", "sk-proj-nUHNf8ShJnYIuuPARsJkT3BlbkFJdxDhSKeOYnyvohKXVSUD")

# Function to get completion from messages
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content
messages =  [  
{'role':'system', 'content':'You are friendly chatbot.'},
{'role':'user', 'content':'Hi, my name is Isa'},
{'role':'assistant', 'content': "Hi Isa! It's nice to meet you. \
Is there anything I can help you with today?"},
{'role':'user', 'content':'Yes, you can remind me, What is my name?'}  ]
response = get_completion_from_messages(messages, temperature=1)
print(response)

# Global context for the conversation
context = [ {'role':'system', 'content':"""
You are OrderBot, an automated service to collect orders for a pizza restaurant. \
You first greet the customer, then collects the order, \
and then asks if it's a pickup or delivery. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else. \
If it's a delivery, you ask for an address. \
Finally you collect the payment.\
Make sure to clarify all options, extras and sizes to uniquely \
identify the item from the menu.\
You respond in a short, very conversational friendly style. \
The menu includes \
pepperoni pizza  12.95, 10.00, 7.00 \
cheese pizza   10.95, 9.25, 6.50 \
eggplant pizza   11.95, 9.75, 6.75 \
fries 4.50, 3.50 \
greek salad 7.25 \
Toppings: \
extra cheese 2.00, \
mushrooms 1.50 \
sausage 3.00 \
canadian bacon 3.50 \
AI sauce 1.50 \
peppers 1.00 \
Drinks: \
coke 3.00, 2.00, 1.00 \
sprite 3.00, 2.00, 1.00 \
bottled water 5.00 \
"""} ]  # accumulate messages

# Function to collect messages and interact with the bot
def collect_messages(user_input, chat_history):
    context.append({'role': 'user', 'content': user_input})
    response = get_completion_from_messages(context)
    context.append({'role': 'assistant', 'content': response})

    # Add messages to chat history without labels
    # Add user and assistant messages to chat history
    chat_history.append(("user", user_input))
    chat_history.append(("assistant", response))
    print(context)
    return chat_history, ""
# Gradio Interface
with gr.Blocks(css="""
    .container {
        max-width: 400px;
        margin: auto;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        background-color: #f9f9f9;
    }
    .chatbox {
        display: flex;
        flex-direction: column;
        gap: 10px;
        padding: 10px;
        background-color: white;
        border-radius: 10px;
        border: 1px solid #ddd;
    }
    .chatbox .user {
        align-self: flex-end;
        background-color: #daf1da;
        padding: 8px 12px;
        border-radius: 10px;
        max-width: 75%;
        
    }
    .chatbox .assistant {
        align-self: flex-start;
        background-color: #f1f1f1;
        padding: 8px 12px;
        border-radius: 10px;
        max-width: 75%;
    }
""") as demo:
    with gr.Column(elem_id="container"):
        chatbot = gr.Chatbot(label="Pizza Order Chat Bot")
        user_input = gr.Textbox(label="Chat Here", placeholder="Enter your message here...", lines=3)
        submit_button = gr.Button("Submit")

        def submit_message(user_input, chat_history):
            print(chat_history)
            return collect_messages(user_input, chat_history)

        submit_button.click(submit_message, inputs=[user_input, chatbot], outputs=[chatbot, user_input])

demo.launch(share=True)
