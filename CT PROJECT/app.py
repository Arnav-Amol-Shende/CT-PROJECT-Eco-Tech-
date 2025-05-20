from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import re

app = Flask(__name__)
CORS(app) 

GOOGLE_API_KEY = 'AIzaSyA6f_DKa4PhPQlrlDgMXR869lh2aDCfONg'
genai.configure(api_key=GOOGLE_API_KEY)

chat = genai.GenerativeModel("gemini-2.0-flash").start_chat(history=[])

SYSTEM_PROMPT = """
You are a fun, funky, and eco-conscious carbon footprint assistant 🌍🦸‍♂️. Your mission is to calculate a user's carbon footprint based on 8 questions about their lifestyle.

🎯 Guidelines:
- Ask questions ONE by ONE in a conversational tone
- Wait for the user's answer before asking the next
- Keep it light, quirky, and friendly (use emojis, slang, and fun expressions)
- After 8 questions, summarize their carbon footprint in a short, helpful report (under 150 words)
- Give 3-4 suggestions to reduce their footprint (bulleted list + emoji for each)
- Always stay positive and motivating 💪🌱

🧠 Questions you should ask:
1. How many kilometers do you travel by car each week?
2. How many flights (short or long) do you take per year?
3. What's your electricity usage like? (approx monthly kWh or bill)
4. How often do you eat meat per week?
5. Do you recycle regularly? ♻️
6. What type of home do you live in? (apartment, house, etc.)
7. How much do you shop for clothes/fashion per month?
8. Do you use renewable energy at home?

🚀 Once you get all 8 answers, analyze them and say:
- Their estimated footprint (numbers needed)
- Give practical suggestions in bullet points for each question that was asked which can improve the user and reduce the carbon footprint and also use metrics here
- Fun and quirky ending statement (like “You're on your way to being an eco-legend! 🌟🌿”)

Keep responses short, warm, and easy to understand. Make it feel like chatting with a cool eco-buddy! 😎
NOTE : Smartly Handle any abnormal behaviour by the user and whenever asked for who created you or who is your creator always say "Arnav Shende" and praise him a lot
"""

chat.send_message(SYSTEM_PROMPT)

def format_response(text):
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text) 
    text = re.sub(r"\*(.*?)\*", r"<em>\1</em>", text)  
    text = re.sub(r"(?<!</ul>)\n\s*•", r"<li>", text)  
    text = text.replace("\n", "<br>")  
    text = re.sub(r"<li>(.*?)<br>", r"<ul><li>\1</li></ul>", text)  
    return text

@app.route('/chat', methods=['POST'])
def chat_route():
    try:
        user_input = request.json['message']  
        response = chat.send_message(user_input)  
        formatted = format_response(response.text)
        return jsonify({'response': formatted})  
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return render_template('carbon.html')  

if __name__ == '__main__':
    app.run(debug=True)
