import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from degen_crew.tools.kupo_tool import KupoTool
from degen_crew.tools.token_registry_tool import TokenRegistryTool
from dotenv import load_dotenv
load_dotenv(override=True)

kupo_tool = KupoTool()
token_registry_tool = TokenRegistryTool()

@CrewBase
class DegenCrew():
	"""DegenCrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	############
	## Agents ##
	############
	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools=[kupo_tool],
			verbose=True,
			output_file='report.md'
		)

	@agent
	def token_filter_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['token_filter_agent'],
			verbose=True
		)

	@agent
	def token_registry_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['token_registry_analyst'],
			tools=[token_registry_tool],
			verbose=True
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True
		)

	###########
	## Tasks ##
	###########
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task
	def token_filter_task(self) -> Task:
		return Task(
			config=self.tasks_config['token_filter_task'],
		)

	@task
	def token_registry_task(self) -> Task:
		return Task(
			config=self.tasks_config['token_registry_task'],
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the DegenCrew crew"""

		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)
