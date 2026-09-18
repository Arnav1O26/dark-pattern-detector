# 🕵️‍♂️ Dark Pattern Detector

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E.svg)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg)

An end-to-end NLP web application designed to identify and expose **Dark Patterns**—manipulative e-commerce UI/UX tactics designed to rush, guilt, or deceive users into making unintended decisions.

## 🚀 Features
* **Targeted Web Scraping:** Uses `BeautifulSoup4` to surgically extract short-form UI text (buttons, spans, labels) while ignoring irrelevant paragraph text. Includes intelligent fallback logic for raw text inputs.
* **Dual-Tier Detection Engine:** 
  * *Tier 1:* A high-speed, rule-based Regex engine for identifying industry-standard manipulative phrasing (e.g., "Only 1 left!").
  * *Tier 2:* A Machine Learning baseline (`Scikit-Learn` TF-IDF + Logistic Regression) to catch nuanced, contextual manipulations that bypass static rules.
* **Algorithmic Scoring:** Aggregates detected patterns into a mathematical 0-100 "Manipulation Score" based on severity and model confidence.
* **Interactive Dashboard:** Built with `Streamlit` and `Plotly` to visualize data through interactive horizontal bar charts, progress gauges, and sortable data tables.

## 🧠 Detected Categories
1. **False Urgency:** Manufactured deadlines to rush decisions (e.g., *"Offer ends in 02:14"*).
2. **Social Proof Pressure:** Using group behavior to pressure users (e.g., *"15 people are looking at this"*).
3. **Forced Continuity:** Making subscriptions easy to join but hard to leave (e.g., *"Card will be charged automatically"*).
4. **Confirmshaming:** Guilt-tripping the user for opting out (e.g., *"No thanks, I hate saving money"*).
5. **Hidden Costs:** Undisclosed fees added at final checkout (e.g., *"Service fee applied"*).

## 🏗️ Project Architecture
The application is strictly modularized to separate the frontend UI layer from the machine learning and data extraction logic:
* `app.py`: The Streamlit frontend and Plotly visualization logic.
* `scraper.py`: Handles HTTP requests, HTML parsing, and graceful error handling.
* `detector.py`: Houses the Regex dictionaries, TF-IDF vectorizer, classification models, and scoring algorithms.
* `Dockerfile`: Configures the lightweight Python 3.12 container for cloud deployment.

## 💻 Local Installation & Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR-USERNAME/dark-pattern-detector.git
    cd dark-pattern-detector
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On macOS/Linux use: source venv/bin/activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application:**
    ```bash
    streamlit run app.py
    ```

## 🐳 Docker & Cloud Deployment
This application is fully containerized and ready for deployment on platforms like Render, AWS, or Google Cloud. 

To build and run the Docker container locally:
```bash
docker build -t dark-pattern-detector .
docker run -p 8501:8501 dark-pattern-detector
```

## 🔮 Future Roadmap 
* **Deep Learning Upgrade:** Replace the baseline Logistic Regression model with a fine-tuned `DistilBERT` transformer model via the Hugging Face `transformers` library to improve contextual understanding of subtle manipulations.