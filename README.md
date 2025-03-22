## Masumi Cardano Agent

<p align="center">
  <img src="docs/crypto-degen.png" alt="Degen" width="250">
</p>

An AI Agent that interacts with the Cardano blockchain and runs on the Masumi network.

## Setup

1. **Create and activate a new Python virtual environment:**

```bash
python -m venv .venv && source .venv/bin/activate
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Plug your agent 🤖 :** The `execute_job` function is where your agent will be invoked. You might also want to change the logic for calculating the price and the shape of the inputs your agent accepts.

4. **Run your Agent API:** 

```bash
python main.py
```