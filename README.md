# 🪄 Text2Manim

**Text2Manim** is an open-source tool that lets you generate stunning math animations using [Manim](https://www.manim.community/) — just by describing them in plain English.

> No need to write code.  
> Just describe the animation → Get Manim code → Render your video.


## 🎯 Aim

To make mathematical animations accessible to everyone — educators, students, and creators — by allowing them to describe what they want using natural language, and automatically generating the corresponding [Manim](https://www.manim.community/) Python code.


## 🧠 Motivation

Manim is a powerful animation engine but has a steep learning curve. Many educators and students don’t have the time to learn its syntax.  
**Text2Manim** removes that barrier by converting natural descriptions into Manim animations, helping users bring abstract ideas to life with ease.


## ✅ Objectives

- Convert plain English descriptions into Manim code
- Render the code into animation previews or downloadable videos
- Provide a simple web interface to view animations

💡 **Model Flexibility**

> Text2Manim supports any LLM of your choice — including OpenAI, Claude, and open models via [OpenRouter](https://openrouter.ai).

To use other Models Change the model name and model provider
```python
model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
```

To use OpenRouter:
```python
from backend.utils.openrouter_llm import ChatOpenRouter
llm = ChatOpenRouter()
```

## 🔧 Setup (Run Locally)

Follow these steps to run **Text2Manim** locally on your machine:

### 1. Clone the repository

```bash
git clone https://github.com/your-username/text2manim.git
cd text2manim
````

### 2. Set up a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Start Redis (via Docker)

Make sure Docker is installed and running, then start Redis:

```bash
docker run -d -p 6379:6379 --name text2manim-redis redis
```

### 5. Create `.env` file

Create a `.env` file in the project root:

```
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=ap-south-1
GOOGLE_API_KEY=your-key
```

> Replace with your actual AWS credentials and configuration.

### 6. Start the FastAPI server

```bash
uvicorn backend.api.app:app --reload
```

### 7. Run Manim rendering container

For sandbox Manim rendering, build the image first:

```bash
docker build -t manim-renderer -f backend/worker/Dockerfile .
```

Manim rendering will be handled in isolation when invoked from the backend.
  
