from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
db = SQLAlchemy(app)

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.String(200), nullable=False)
    bot_response = db.Column(db.String(200), nullable=False)

chatbot = ChatBot('WebBot')
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json.get("message")
    response = chatbot.get_response(user_input)
    chat_history = ChatHistory(user_message=user_input, bot_response=str(response))
    db.session.add(chat_history)
    db.session.commit()
    return jsonify({"response": str(response)})

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
