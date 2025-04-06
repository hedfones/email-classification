import json
import re
from pathlib import Path
from typing import override

from langchain_aws.chat_models import ChatBedrockConverse
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSerializable
from pydantic import BaseModel
import structlog


log = structlog.stdlib.get_logger()

class Email(BaseModel):
    sender: str
    subject: str
    body: str

    @override
    def __str__(self):
        return f"From: {self.sender}\nSubject: {self.subject}\n\n{self.body}"


class EmailClassication(BaseModel):
    model_id: str = "us.meta.llama3-3-70b-instruct-v1:0"
    email: Email

    @property
    def instructions(self):
        path = Path("resources/prompt.md")
        with path.open("r") as f:
            return f.read()

    def classify(self) -> dict[str, str]:
        log.info("classify_email", email=self.email)
        llm = ChatBedrockConverse(model=self.model_id)
        prompt = ChatPromptTemplate(
            [("system", "{instructions}"), ("user", "{email}")], partial_variables={"instructions": self.instructions}
        )
        chain: RunnableSerializable[dict[str, str], str] = prompt | llm | StrOutputParser()

        result = chain.invoke({"email": str(self.email)})
        log.debug("classify_email_result", result=result)

        pattern = r"(?:```json)?\s*({[\s\S]*?})\s*(?:```)?"
        match = re.search(pattern, result)
        if not match:
            raise ValueError("No JSON found in the response")
        log.debug("classify_email_match", match=match.group(1))

        json_result: dict[str, str] = json.loads(match.group(1))

        log.debug("classify_email_json_result", json_result=json_result)

        return json_result
