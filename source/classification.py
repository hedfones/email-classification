import json
from pathlib import Path
import re
from langchain_core.runnables import RunnableSerializable
from pydantic import BaseModel
from langchain_aws.chat_models import ChatBedrockConverse
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class EmailClassication(BaseModel):
    model_id: str = "us.meta.llama3-3-70b-instruct-v1:0"
    email: str

    @property
    def instructions(self):
        path = Path("resources/classification.md")
        with path.open("r") as f:
            return f.read()

    def classify(self) -> dict[str, str]:
        llm = ChatBedrockConverse(model=self.model_id)
        prompt = ChatPromptTemplate([("system", "{instructions}"), {"user": "{email}"}], partial_variables={"instructions": self.instructions})
        chain: RunnableSerializable[dict[str, str], str] = prompt | llm | StrOutputParser()

        result = chain.invoke({"email": self.email})

        pattern = r"```json\s*([\s\S]*?)\s*```"
        match = re.search(pattern, result)
        if not match:
            raise ValueError("No JSON found in the response")

        json_result: dict[str, str] = json.loads(match.group(1))

        return json_result
