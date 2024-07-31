from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import ChatPromptTemplate

from langchain_community.chat_models import BedrockChat

from langchain_core.messages import HumanMessage

import boto3

MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"
bedrock_runtime_client = boto3.client("bedrock-runtime")

model_kwargs =  {
    "max_tokens": 4000,
    "temperature": 0.0,
    "top_k": 250,
    "top_p": 1,
    "stop_sequences": ["\n\nHuman"],
}


def summarize_agent_trace(trace_file_base_path= "trace_files/", lab_number="2b", turn_number="1"):

    complete_log_path = trace_file_base_path + f"full_trace_lab{lab_number}_agent_trace_{turn_number}.log"
    print(f">>>>>>>> complete_log_path to summarize==> {complete_log_path}")
    trace_content_text = None
    with open(complete_log_path, "r") as trace_fp:
        trace_content_text = trace_fp.read().replace("\n", "")

    # print(f"trace_content_text[:20] == {trace_content_text[:20]}")
    
    llm = BedrockChat(client=bedrock_runtime_client, model_id=MODEL_ID, model_kwargs=model_kwargs)
    messages = [HumanMessage(content=f"Summarize in natural language the agent workflow in the trace file contents that follow. Remove XML tags in the output. TRACE FILE CONTENTS: {trace_content_text[:40000]}")]
    response = llm(messages)
    # print(f"raw response ==> {response}")

    if str(type(response)) == "<class 'langchain_core.messages.ai.AIMessage'>":
            response = response.content
            response = response.strip()
            #print(f"Parsed response ==> {response}")

    return response

# for unit-testing
# summarize_agent_trace(trace_file_base_path= "../trace_files/", lab_number="2b", turn_number="1")
