# OpenAI Agents

Multi-Agent system with the OpenAI Agents framework.

Create a `.env` file with the local mongo URI and API key.

```bash
OPENAI_KEY=sk-proj-XXXXXX

MONGO_URI=mongodb://root:oaiAgents123@localhost:27020/
````

Start the local MongoDB container.

```bash
docker compose up -d
```

Install the dependencies with UV.

```bash
$ uv sync

Resolved 31 packages in 8ms
Audited 30 packages in 0.27ms
```

Run the agent system which will continuously loop.

> Break the loop with `ctrl + c`

```bash
$ python3 -m app.main

📝: What todo items do I have?
Here are your current todo items:

1. **Take out trash**
   - Completed: Yes
   - Due Date: March 13, 2025

2. **Create an AI agent**
   - Completed: No
   - Due Date: October 6, 2023

Let me know if you need any updates or changes!
```
