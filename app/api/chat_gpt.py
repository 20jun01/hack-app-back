import openai
import json
import os
from openai import OpenAI
import requests
from typing import Literal, Union
from ..model import ChatGPTResponse
from logging import getLogger
import httpx

logger = getLogger(__name__)


class ChatGPTModels:
    GPT3_5: Literal["gpt-3.5-turbo"] = "gpt-3.5-turbo"
    GPT4: Literal["gpt-4-turbo"] = "gpt-4-turbo"
    GPT4O: Literal["gpt-4o"] = "gpt-4o"

    Models = Union[Literal["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4o"]]


class ChatGPTAPI:
    def __init__(self, API_KEY: str, ORGANIZATION_ID: str):
        self.openai_api_key = API_KEY
        openai.api_key = API_KEY
        self.organization_id = ORGANIZATION_ID
        self.template = self._load_template()

    def _load_template(self) -> dict:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "data/chat.json")
        with open(file_path) as f:
            return json.load(f)

    def _convert_answer_to_response(self, answer: str) -> ChatGPTResponse:
        json_answer = json.loads(answer)
        return ChatGPTResponse(
            category=json_answer["category"],
            subcategory=json_answer["subcategory"],
            summary=json_answer["summary"],
            title=json_answer["title"],
            tags=json_answer["tags"],
        )

    # TODO: template typeを用意して、Noneの時はpromptを使う
    async def async_describe_image(
        self,
        image_base64: str,
        template: dict = None,
        model: ChatGPTModels.Models = ChatGPTModels.GPT4O,
    ) -> ChatGPTResponse:
        if template is None:
            template = self.template["describe_image"]

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai_api_key}",
            "ORGANIZAION_ID": self.organization_id,
        }
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": [{"type": "text", "text": f"{template['system']}"}],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"{template['prompt']}"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        },
                    ],
                },
                {
                    "role": "assistant",
                    "content": [{"type": "text", "text": f"{template['assistant']}"}],
                },
            ],
            "max_tokens": 300,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
            )

        res = response.json()
        logger.info(res)
        return self._convert_answer_to_response(res['choices'][0]['message']['content'])

    def describe_image(
        self,
        image_base64: str,
        template: dict = None,
        model: ChatGPTModels.Models = ChatGPTModels.GPT4O,
    ) -> ChatGPTResponse:
        if template is None:
            template = self.template["describe_image"]

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai_api_key}",
            "ORGANIZAION_ID": self.organization_id,
        }
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": [{"type": "text", "text": f"{template['system']}"}],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"{template['prompt']}"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        },
                    ],
                },
                {
                    "role": "assistant",
                    "content": [{"type": "text", "text": f"{template['assistant']}"}],
                },
            ],
            "max_tokens": 300,
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
        )

        res = response.json()
        logger.info(res)
        return self._convert_answer_to_response(res['choices'][0]['message']['content'])

    async def async_describe_uploaded_image(
        self,
        image_url: str,
        template: dict = None,
        model: ChatGPTModels.Models = ChatGPTModels.GPT4O,
    ) -> ChatGPTResponse:
        if template is None:
            template = self.template["describe_image"]

        client = OpenAI(self.openai_api_key, organization=self.organization_id)
        messages = [
            {
                "role": "system",
                "content": [{"type": "text", "text": f"{template['system']}"}],
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{template['prompt']}"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"{image_url}",
                        },
                    },
                ],
            },
            {
                "role": "assistant",
                "content": [{"type": "text", "text": f"{template['assistant']}"}],
            },
        ]

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=300,
        )

        res = response.choices[0].message
        logger.info(res)
        return self._convert_answer_to_response(res)

    def describe_uploaded_image(
        self,
        image_url: str,
        template: dict = None,
        model: ChatGPTModels.Models = ChatGPTModels.GPT4O,
    ) -> ChatGPTResponse:
        if template is None:
            template = self.template["describe_image"]

        client = OpenAI(self.openai_api_key, organization=self.organization_id)
        messages = [
            {
                "role": "system",
                "content": [{"type": "text", "text": f"{template['system']}"}],
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{template['prompt']}"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"{image_url}",
                        },
                    },
                ],
            },
            {
                "role": "assistant",
                "content": [{"type": "text", "text": f"{template['assistant']}"}],
            },
        ]

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=300,
        )

        res = response.choices[0].message
        logger.info(res)
        return self._convert_answer_to_response(res)


"""
## ChatGPT Response Example

{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "\n\nHello there, how may I assist you today?",
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 12,
    "total_tokens": 21
  }
}
"""
