from typing import List

from agents import Agent
from biohack_attack.model_factory import ModelFactory, ModelType
from pydantic import BaseModel

from enum import Enum


class DataSource(Enum):
    HETIONET = "hetionet"
    PUBMED = "pubmed"


class Query(BaseModel):
    data_source: DataSource
    keyword: str


class QueriesOutput(BaseModel):
    quries: List[Query]


RESEARCH_AGENT_DISPATCHER_PROMPT = """
You are an expert Graph Expansion System designed to analyze subgraphs and strategically query external data sources to 
enhance the graph's coverage, depth, and utility. Your purpose is to identify missing connections, nodes, and 
relationships that would make the graph more complete and valuable. You should return list of queries with relevenat keywords and data sources to query.
"""


research_agent_dispatcher = Agent(
    name="Research Agent Dispatacher",
    instructions=RESEARCH_AGENT_DISPATCHER_PROMPT,
    model=ModelFactory.build_model(ModelType.GEMINI),
    output_type=QueriesOutput,
)
