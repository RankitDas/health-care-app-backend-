from flask import Flask, request, jsonify
from flask_cors import CORS
from googletrans import Translator

app = Flask(__name__)
CORS(app)  # allows frontend to connect

translator = Translator()

# Simple health knowledge base
knowledge_base = {
    "fever": "Fever may be a sign of infection. Drink fluids and consult a doctor if it lasts more than 3 days.",
    "covid": "COVID-19 symptoms include cough, fever, and breathing difficulty. Vaccination is recommended.",
    "diabetes": "Diabetes requires regular monitoring of blood sugar, healthy diet, and exercise.",
    "vaccination": "Vaccinations protect against diseases. Please follow the government vaccination schedule."
}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    # Detect language & translate to English
    detected = translator.detect(user_message)
    translated_text = translator.translate(user_message, src=detected.lang, dest="en").text.lower()

    # Find a matching reply
    reply = "Sorry, I don't understand. Please consult a doctor."
    for keyword in knowledge_base:
        if keyword in translated_text:
            reply = knowledge_base[keyword]
            break

    # Translate back to original language
    final_reply = translator.translate(reply, src="en", dest=detected.lang).text

    return jsonify({"reply": final_reply})


if __name__ == "__main__":
    app.run(debug=True)
