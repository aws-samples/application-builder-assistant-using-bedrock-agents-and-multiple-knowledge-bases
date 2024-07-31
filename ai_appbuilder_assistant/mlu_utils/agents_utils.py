from IPython.display import display, HTML
import pandas as pd

import pprint
import logging
import json
from IPython.display import JSON
import os, shutil

logging.basicConfig(format='[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def clean_up_trace_files(trace_file_path):
    # cleanup trace files to avoid issues
    if os.path.isdir(trace_file_path):
        shutil.rmtree(trace_file_path)
    os.mkdir(trace_file_path)


def pretty_print(df):
    return display(HTML( df.to_html().replace("\\n","<br>"))) # .replace("\\n","<p>") 


def format_final_response(question, final_answer, lab_number, turn_number, gen_sql):
    # Print the final response for turn-2
    final_answer = final_answer.replace('$', r'\$')

    final_answer_list = [final_answer]
    question_list = [question]

    if gen_sql is True:
        
        generated_sql = list()
        trace_file_name = f"trace_files/actionGroupInvocationOutput_lab{lab_number}_agent_trace_{turn_number}.log"
        with open(trace_file_name, "r") as agent_trace_fp:
            file_json = json.load(agent_trace_fp)
            start_pos = str(file_json["text"]).index('SELECT')
            end_pos = str(file_json["text"]).index(';')
            #print(str(start_pos) + " >> " + str(end_pos))
            generated_sql = str(file_json["text"])[start_pos:end_pos]
            #print(gen_sql)


        # Store and print as a dataframe
        response_df = pd.DataFrame( list(zip(question_list, [generated_sql], final_answer_list )), 
                                      columns=["User Question","Agent Generated SQL", "Agent Answer"],)
        response_df.style.set_properties(**{'text-align': 'left', 'border': '1px solid black'})
        with pd.option_context("display.max_colwidth", None):
            pretty_print(response_df)
    else:
        # Store and print as a dataframe
        response_df = pd.DataFrame( list(zip(question_list,  final_answer_list )), 
                                      columns=["User Question", "Agent Answer"],)
        response_df.style.set_properties(**{'text-align': 'left', 'border': '1px solid black'})
        with pd.option_context("display.max_colwidth", None):
            pretty_print(response_df)


def invoke_agent_generate_response(bedrock_agent_runtime_client,
                                   input_text, 
                                   agent_id, 
                                   agent_alias_id, 
                                   session_id, 
                                   enable_trace,
                                   end_session,
                                   trace_filename_prefix,
                                   turn_number):

    # invoke the agent API
    agentResponse = bedrock_agent_runtime_client.invoke_agent(
        inputText=input_text,
        agentId=agent_id,
        agentAliasId=agent_alias_id, 
        sessionId=session_id,
        enableTrace=enable_trace, 
        endSession= end_session
    )

    #logger.info(pprint.pprint(agentResponse))
    event_stream = agentResponse['completion']
    final_answer = None
    try:
        for event in event_stream:
            if 'chunk' in event:
                data = event['chunk']['bytes']
                final_answer = data.decode('utf8')
                logger.info(f"Final answer ->\n{final_answer}") 
                end_event_received = True
                # End event indicates that the request finished successfully
            elif 'trace' in event:
                #logger.info(json.dumps(event['trace'], indent=2))
                with open("trace_files/full_trace_" + trace_filename_prefix + "_" + str(turn_number) + ".log", "a") as agent_trace_fp:
                    agent_trace_fp.writelines(json.dumps(event['trace'], indent=2))
                   
                logger.debug(f"entering if loop>>>> {type(event['trace'])} and keys ::: {event['trace']['trace'].keys()}")
                # only save the last trace output for clear display
                if 'preProcessingTrace' in event['trace']['trace']:
                    logger.debug("saving pre-processing log")
                    with open("trace_files/preProcessingTrace_" + trace_filename_prefix + "_" + str(turn_number) + ".log", "w") as agent_trace_fp:
                        agent_trace_fp.writelines(json.dumps(event['trace']['trace']['preProcessingTrace'], indent=2))

                elif 'orchestrationTrace' in event['trace']['trace'] and 'observation' in event['trace']['trace']['orchestrationTrace'] and 'knowledgeBaseLookupOutput' in event['trace']['trace']['orchestrationTrace']['observation']:
                    logger.debug("saving knowledgeBaseLookupOutput log")
                    with open("trace_files/knowledgeBaseLookupOutput_" + trace_filename_prefix + "_" + str(turn_number) + ".log", "w") as agent_trace_fp:
                        agent_trace_fp.writelines(json.dumps(event['trace']['trace']['orchestrationTrace']['observation']['knowledgeBaseLookupOutput'], indent=2))
                        
                        
                elif 'orchestrationTrace' in event['trace']['trace'] and 'observation' in event['trace']['trace']['orchestrationTrace'] and 'actionGroupInvocationOutput' in event['trace']['trace']['orchestrationTrace']['observation']:
                    logger.debug("saving actionGroupInvocationOutput log")
                    with open("trace_files/actionGroupInvocationOutput_" + trace_filename_prefix + "_" + str(turn_number) + ".log", "w") as agent_trace_fp:
                        agent_trace_fp.writelines(json.dumps(event['trace']['trace']['orchestrationTrace']['observation']['actionGroupInvocationOutput'], indent=2))

                elif 'orchestrationTrace' in event['trace']['trace']:
                    logger.debug("saving orchestrationTrace log")
                    with open("trace_files/orchestrationTrace_" + trace_filename_prefix + "_" + str(turn_number) + ".log", "w") as agent_trace_fp:
                        agent_trace_fp.writelines(json.dumps(event['trace']['trace']['orchestrationTrace'], indent=2))
            else:
                raise Exception("unexpected event.", event)
                
    except Exception as e:
        raise Exception("unexpected event.", e)

    return final_answer


