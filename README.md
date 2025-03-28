## Masumi Cardano Agent

<p align="center">
  <img src="docs/crypto-degen.png" alt="Degen" width="350">
</p>

A CrewAI that interacts with the Cardano blockchain and runs on the Masumi network via the [Masumi Cardano Agent API](https://github.com/idopterlabs/masumi-cardano-agent-api)

## Setup

1. **Create and activate a new Python virtual environment:**

```bash
python -m venv .venv && source .venv/bin/activate
```

2. **Install dependencies:**

```bash
pip install crewai
crewai install
```

3. **Set your envs**

Copy `.env.example` into `.env` and populate with your credentials. Access to [Kupo](https://cardanosolutions.github.io/kupo/#section/Overview) is required. If you don't
manage one, then you can use one from https://demeter.run/

4. **Running the Crew**

```bash
crewai run
```