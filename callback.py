from dto import ChatbotRequest
from samples import list_card
import aiohttp
import time
import logging
import openai
import os
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    SystemMessage
)

# 환경 변수 처리 필요!
openai.api_key = os.environ["OPENAI_API_KEY"]
SYSTEM_MSG = "당신은 카카오 서비스 제공자입니다."

instructions = None
with open('./data/kakao_doc.txt') as f:
    instructions = f.read()

system_message = f"assistant는 챗봇으로 동작한다. 챗봇은 아래 내용을 참고하여, user의 질문 혹은 요청에 따라 적절한 답변을 제공합니다."
system_message_prompt = SystemMessage(content=system_message)
llm = ChatOpenAI(temperature=0.8)



logger = logging.getLogger("Callback")

async def callback_handler(request: ChatbotRequest) -> dict:

    # ===================== start =================================
    print('hi')
    print(request)

    human_template = ("제품정보: {product_data}\n" +
                      request.userRequest.utterance )
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    chain = LLMChain(llm=llm, prompt=chat_prompt)

    output_text = chain.run(product_data=instructions)

    # 참고링크 통해 payload 구조 확인 가능
    payload = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": output_text
                    }
                }
            ]
        }
    }
    # ===================== end =================================
    # 참고링크1 : https://kakaobusiness.gitbook.io/main/tool/chatbot/skill_guide/ai_chatbot_callback_guide
    # 참고링크1 : https://kakaobusiness.gitbook.io/main/tool/chatbot/skill_guide/answer_json_format

    time.sleep(1.0)

    url = request.userRequest.callbackUrl
    print(f'output_text1: {output_text}')


    if url:
        print(f'output_text2: {output_text}')
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, json=payload, ssl=False) as resp:
                await resp.json()
