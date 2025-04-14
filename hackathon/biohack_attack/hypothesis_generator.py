import asyncio
from typing import Any, List

from agents import Agent, Runner
from biohack_attack.hackathon_agents.research_agents import ResearchAgentOutput
from biohack_attack.hackathon_agents.research_agents.research_agent_dispatcher import (
    DataSource,
    QueriesOutput,
    research_agent_dispatcher,
)
from biohack_attack.model_factory import ModelFactory, ModelType
from dotenv import load_dotenv
from pydantic import BaseModel

from ard.hypothesis import Hypothesis, HypothesisGeneratorProtocol
from ard.subgraph import Subgraph
from hackathon.biohack_attack.hackathon_agents.research_agents.hetionet_agent import (
    KnowledgeGraph,
    hetionet_agent,
)


class HypothesisOutput(BaseModel):
    title: str
    statement: str
    reasoning_steps: list[str]


async def run_agents(subgraph: Subgraph) -> Hypothesis:
    # hypothesis_agent = Agent(
    #     name="Hypothesis create",
    #     instructions=f"Build novel scientific hypothesis based on the provided cypher path",
    #     model=ModelFactory.build_model(ModelType.OPENAI),
    #     output_type=HypothesisOutput
    # )
    print(subgraph)
    path = subgraph.to_cypher_string(full_graph=True)
    print(path)

    queries: QueriesOutput = await Runner.run(research_agent_dispatcher, path)

    # TODO: Add async.
    for query in queries:
        if query.data_source == DataSource.HETIONET:
            result: KnowledgeGraph = await Runner.run(hetionet_agent, query.keyword)
        elif query.data_source == DataSource.PUBMED:
            pass

    results: ResearchAgentOutput = ResearchAgentOutput(sources=[], graphs=[])

    # Hypothesis generation Agent

    # result = await Runner.run(hypothesis_agent, path)
    # hypothesis_output: HypothesisOutput = result.final_output

    # return Hypothesis(
    #     title=hypothesis_output.title,
    #     statement=hypothesis_output.statement,
    #     source=subgraph,
    #     method=HypothesisGenerator(),
    # )


class HypothesisGenerator(HypothesisGeneratorProtocol):
    def run(self, subgraph: Subgraph) -> Hypothesis:
        return asyncio.run(run_agents(subgraph))

    def __str__(self) -> str:
        return "HypeGen Generator"

    def to_json(self) -> dict[str, Any]:
        return {"type": "HypothesisGenerator"}
