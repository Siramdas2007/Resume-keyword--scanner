from flask import Flask, render_template, request
import PyPDF2
import nltk
import os
from nltk.corpus import stopwords
app = Flask(__name__)
# This downloads the necessary data to the server
nltk.download('stopwords')
nltk.download('punkt') # You'll likely need this too for tokenization

stop_words = set(stopwords.words('english'))

def extract_text(file):
    text = ""
    pdf = PyPDF2.PdfReader(file)

    for page in pdf.pages:
        text += page.extract_text()

    return text.lower()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/scan', methods=['POST'])
def scan():

    resume = request.files['resume']
    job_description = request.form['job_description'].lower()

    resume_text = extract_text(resume)

    jd_words = job_description.split()
    resume_words = resume_text.split()

    # Remove stopwords
    jd_words = [word for word in jd_words if word not in stop_words]

    matched = []
    missing = []

    for word in jd_words:
        if word in resume_words:
            matched.append(word)
        else:
            missing.append(word)

    percentage = int((len(matched) / len(jd_words)) * 100)

    suggestions = []
    for skill in missing:
        suggestions.append(f"Add '{skill}' skill to improve your resume.")

    return render_template(
        "result.html",
        match=percentage,
        matched=matched,
        missing=missing,
        suggestions=suggestions
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
