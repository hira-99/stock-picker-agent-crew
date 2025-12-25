from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from pydantic import BaseModel, Field
from crewai_tools import SerperDevTool
from .tools.email_tool import EmailTool

class TrendingCompany(BaseModel):
    name: str = Field(description="Company name")
    ticker: str = Field(description="Stock ticker symbol")
    reason: str = Field(description="Reason this company is trending in the news")

class TrendingCompaniesList(BaseModel):
    companies: List[TrendingCompany] = Field(description="List of trending companies")

class TrendingCompanyResearch(BaseModel):
    name: str = Field(description="Company name")
    market_position: str = Field(description="Current market position and competitive analysis")
    future_outlook: str = Field(description="Future outlook and growth prospects")
    investment_potential: str = Field(description="Investment potential and suitability for investment")

class TrendingCompaniesResearchList(BaseModel):
    research_list: List[TrendingCompanyResearch] = Field(description="Comprehensive research on all trending companies")

@CrewBase
class TwoStockPicker():
    """TwoStockPicker crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    @agent
    def trending_companies_finder(self):
        return Agent(config=self.agents_config['trending_companies_finder'], verbose=True, tools=[SerperDevTool()])

    @agent
    def financial_researcher(self):
        return Agent(config=self.agents_config['financial_researcher'], verbose=True, tools=[SerperDevTool()])

    @agent
    def stock_picker(self):
        return Agent(config=self.agents_config['stock_picker'], verbose=True, tools=[EmailTool()])

    @task
    def find_trending_companies(self):
        return Task(config=self.tasks_config['find_trending_companies'], output_pydantic=TrendingCompaniesList)

    @task
    def research_trending_companies(self):
        return Task(config=self.tasks_config['research_trending_companies'], output_pydantic=TrendingCompaniesResearchList)

    @task
    def pick_best_company(self):
        return Task(config=self.tasks_config['pick_best_company'])

    @crew
    def crew(self):
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
            manager_agent=Agent(config=self.agents_config['manager'], verbose=True),
            process=Process.hierarchical,
            memory=True
        )