# 📄 Smart Assistant for Research Summarization

This project is a **GenAI-powered document assistant** built using **Cohere API** and **Streamlit**. It helps users summarize uploaded documents, ask context-aware questions, and take personalized AI-generated challenges with instant feedback — all in one place.

---

## 🚀 Features

- 📤 Upload **PDF** or **TXT** files  
- 📑 Auto-generate AI-powered **summaries**  
- 💬 Ask questions and receive contextual answers  
- 🧠 Generate 3 personalized **challenge questions**  
- ✅ Get real-time **AI feedback** on your answers  
- 🎨 Beautiful sidebar UI with emoji badges and pill tags

---

## 🧰 Tech Stack

| Technology | Purpose              |
|------------|----------------------|
| Python     | Core scripting       |
| Streamlit  | Web UI               |
| Cohere     | Language model API   |
| dotenv     | Secure API keys      |
| FAISS      | Text similarity (optional) |

---



## 🗂️ Folder Structure

├── app.py
├── .env # Add your COHERE_API_KEY here
├── utils/
│ ├── parser.py # Extracts text from PDF/TXT
│ ├── qa.py # Embeds, finds chunks, answers
│ └── challenge.py # Creates & evaluates questions


## 🧪 How to Run

> ⚠️ Requires Python 3.10+ and internet access

1. **Clone the repo**
```bash
git clonehttps://github.com/19anujshukla/Smart-Research-Assistant
cd smart-research-assistant
```

✅ Install dependencies
```bash
pip install -r requirements.txt
```

Create .env file with your Cohere API key:
```bash
COHERE_API_KEY=foYE8RLxsvisp7MHNoS9fpldZgWvT86El9x2q4ZU
```

Launch the app
```bash
python -m streamlit run app.py
```

