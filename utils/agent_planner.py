import requests

def query_ollama(prompt, model="mistral"):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["response"]

def plan_steps_from_goal(goal):
    planning_prompt = f"""
You are a senior AI product strategist.

Break down the following product goal into a sequence of clear, logical analysis steps.

Each step should represent a reasoning or investigation task an intelligent product agent should perform.

Use bullet points.

Goal:
{goal}
"""
    raw_output = query_ollama(planning_prompt)
    
    # Split response into steps (strip bullets and extra whitespace)
    lines = [line.strip("-• ").strip() for line in raw_output.splitlines() if line.strip()]
    steps = [line for line in lines if len(line) > 0]
    return steps
