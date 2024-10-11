import requests
import json
from typing import Any, Dict

import config
from clients.mongo_client import MongoClient
from clients.clip_client import ClipClient
from clients.pinecone_client import PineconeClient
from clients.gpt_client import ChatGPTClient, create_message
import re

from clients.meilisearch_client import MeiliSearchClient


class GPTService:
    def __init__(self):
        self.client = ChatGPTClient(config.GPT_API_KEY, config.GPT_BASE_URL)

    def extract_search_rates_from_user_prompt(self, user_prompt: str) -> Dict[str, Any]:
        messages = [
            create_message(
                "system",
                "You are an assistant that is going to help for a search engine on products data. "
                "the engine has two search modes. semantic search through images and meiliesearch through keywords. "
                "the semantic is good for cases that user searches by attributes and features, the other one is used "
                "for keywords in title, brand and etc. the result of engine is an aggregated response from each mode. "
                "Your task is to determine the ratio of the query that must be sent to each search mode to maximize "
                "the search result quality. for example having this query: {black women bag} should have more shares "
                "in semantic search. your output should be a json file with two keys(semantin, keword) and obviously "
                "the sum of them should be 1 because their values are the percentage of total result.",
            ),
            create_message(
                "user",
                f"Given the user statement: '{user_prompt}', identify the percentage of each mode mentioned "
                "Respond only with JSON including 'semantic' and 'keyword'.",
            ),
        ]

        try:
            response = self.client.query(messages)
            return self.parse_response(response)
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
        except ValueError as e:
            print(f"Response error: {e}")

    def parse_response(self, response: str) -> Dict[str, Any]:
        match = re.search(r"\{.*?\}", response, re.DOTALL)
        if match:
            json_response = match.group(0)
            return json.loads(json_response)

        raise ValueError("Could not find a valid JSON response in GPT's output")


class ProductsFetchService:
    def __init__(self):
        self.pinecone_client = PineconeClient()
        self.clip_client = ClipClient()
        self.meilisearch_client = MeiliSearchClient()
        self.mongo_client = MongoClient()
        self.gpt_client = GPTService()

    def get_products(self, query: str, mode: str):
        total_share = 24
        semantic_share, keyword_share = total_share // 2, total_share // 2
        semantic_ids, keyword_ids = [], []
        if mode == "semantic":
            semantic_share = total_share
            keyword_share = 0
        elif mode == "keyword":
            semantic_share = 0
            keyword_share = total_share
        else:
            shares = self.gpt_client.extract_search_rates_from_user_prompt(query)
            if "semantic" in shares and "keyword" in shares:
                semantic_share = int(total_share * shares.get("semantic"))
                keyword_share = int(total_share - semantic_share)

        if semantic_share > 0:
            semantic_ids = self._get_semantic_products(query, semantic_share)

        if keyword_share > 0:
            keyword_ids = self._get_keyword_products(query, keyword_share)

        if semantic_share >= keyword_share:
            return self.mongo_client.get_products_by_ids(
                list(set(semantic_ids + keyword_ids))
            )
        else:
            return self.mongo_client.get_products_by_ids(
                list(set(keyword_ids + semantic_ids))
            )

    def _get_semantic_products(self, query, semantic_share):
        encoded_query = self.clip_client.encode_query_text(query)
        semantic_ids = set()
        semantic_results = self.pinecone_client.search_by_query(
            encoded_query, semantic_share * 5
        ).get("matches", [])
        for row in semantic_results:
            semantic_ids.add(int(row["id"].split("_")[0]))
        return list(semantic_ids)[:semantic_share]

    def _get_keyword_products(self, query, keyword_share):
        keyword_ids = set()
        keyword_results = self.meilisearch_client.get_products(
            query, keyword_share
        ).get("hits", [])
        for row in keyword_results:
            keyword_ids.add(int(row["id"]))
        return list(keyword_ids)[:keyword_share]


products_fetch_service = ProductsFetchService()
