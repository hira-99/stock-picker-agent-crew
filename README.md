# StockPicker Crew

Hey! This is a learning project I'm working on to understand how multi-agent AI systems work using [crewAI](https://crewai.com). I thought it'd be cool to build something that actually does something useful, so I made a system that picks stocks (well, at least tries to help with that).

## What's This About?

So basically, I wanted to see if I could get multiple AI agents to work together on a task. The idea is simple: find trending companies, research them, and pick the best one. But instead of doing it all with one agent, I split it up into specialized agents that each do one thing well.

Here's what happens:

1. **Manager Agent** - This guy is in charge. He coordinates everything and tells the other agents what to do.
2. **Trending Companies Finder** - Searches the web to find 2-3 companies that are trending in a specific sector (I defaulted it to "Electric Vehicles" but you can change it).
3. **Financial Researcher** - Takes those companies and does a deep dive on each one. Looks at market position, future outlook, all that stuff.
4. **Stock Picker** - Finally, this agent looks at all the research and picks the best company, then emails you about it.

The cool part is they all work together in a hierarchy - the manager delegates tasks, and each agent passes their results to the next one.

## How It Works

The workflow is pretty straightforward:
- Manager tells the finder to go find companies
- Finder comes back with a list
- Manager gives that list to the researcher
- Researcher does their thing and creates a report
- Manager gives the report to the picker
- Picker makes a decision and sends you an email

I'm using a few tools here:
- **SerperDevTool** for web searching (you'll need a Serper API key)
- **EmailTool** - I built a custom one using Resend to send emails

The outputs get saved to files in the `output/` directory so you can see what each agent did.

## Setup

You'll need Python 3.10+ (but less than 3.14). I'm using [UV](https://docs.astral.sh/uv/) for managing dependencies because it's fast and easy.

First, install uv if you don't have it:
```bash
pip install uv
```

Then install the project dependencies:
```bash
crewai install
```

### API Keys

You'll need to add these to a `.env` file in the root directory:

- `OPENAI_API_KEY` - For the LLM (I'm using GPT-4o-mini, it's cheaper and works fine)
- `SERPER_API_KEY` - For web searching (get one at serper.dev)
- `RESEND_API_KEY` - For sending emails (get one at resend.com)

Don't forget to update the email address in `email_tool.py` - I left a placeholder there.

### Project Structure

Here's how I organized things:
```
stock-picker-agent-crew/
├── src/two_stock_picker/
│   ├── main.py              # Where you set the inputs (sector, year)
│   ├── crew.py              # The crew setup with all agents and tasks
│   ├── config/
│   │   ├── agents.yaml      # Agent configs - roles, goals, etc.
│   │   └── tasks.yaml       # Task definitions
│   └── tools/
│       ├── custom_tool.py   # Just a template, not really used
│       └── email_tool.py    # My custom email tool
└── knowledge/
    └── user_preference.txt  # Some context about the user
```

## Running It

Just run this from the project root:
```bash
crewai run
```

It'll start the crew, and you'll see each agent working through their tasks. The manager will coordinate everything, and you'll get output files in the `output/` folder.

By default, it searches for companies in the "Electric Vehicles" sector. You can change that in `main.py`:

```python
inputs = {
    "sector": "Electric Vehicles",  # Change to whatever sector you want
    "year": datetime.now().year
}
```

## The Agents

Let me break down what each agent does:

**Manager Agent**
- Role: Financial Stock Market Manager
- What it does: Coordinates everything, delegates tasks
- It's using hierarchical management, which means it's in charge of the workflow

**Trending Companies Finder**
- Role: Finds trending companies
- Tools: SerperDevTool for web search
- Output: A JSON file with 2-3 companies, their tickers, and why they're trending

**Financial Researcher**
- Role: Does the financial analysis
- Tools: Also uses SerperDevTool to search for financial info
- Input: Gets the trending companies from the finder
- Output: A detailed report on each company's market position, outlook, and investment potential

**Stock Picker**
- Role: Makes the final decision
- Tools: EmailTool to send you the results
- Input: Gets all the research from the previous step
- Output: Picks the best company and emails you about it (also saves to a markdown file)

The tasks run in order:
```
find_trending_companies
    ↓
research_trending_companies (uses results from above)
    ↓
pick_best_company (uses research from above)
```

Each task saves its output and passes it along to the next one.

## What I Learned

This was a good way to understand a few concepts:

- **Hierarchical agents** - Having a manager coordinate other agents is pretty powerful
- **Task dependencies** - Tasks can depend on each other's outputs, which is neat
- **Structured outputs** - Using Pydantic models makes sure the data is consistent
- **Custom tools** - Building the email tool was fun, shows you can extend the system
- **Agent memory** - The agents remember context across tasks, which helps them work together better
- **YAML configs** - Keeping agent and task definitions in YAML files makes it easy to tweak things without touching code

The tech stack:
- **crewAI** - The framework that makes all this possible
- **Pydantic** - For structured, validated data
- **SerperDev** - Web search API
- **Resend** - Email API

## Resources

If you want to learn more about crewAI:
- [Documentation](https://docs.crewai.com)
- [GitHub repo](https://github.com/joaomdmoura/crewAI)

---

This is definitely a work in progress and a learning project. Feel free to fork it, break it, fix it, and make it better! If you find any issues or have suggestions, let me know.
