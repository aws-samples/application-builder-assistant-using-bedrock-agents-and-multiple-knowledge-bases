import ipywidgets as widgets
from IPython.display import JSON
import logging

# action on tab click for agent trace
out = widgets.Output(layout=widgets.Layout(border = '1px solid black', width = '100%',))

# lab2a out variables
out_2a_tabs_1 = widgets.Output(layout=widgets.Layout(border = '1px solid black', width = '100%',))
out_2a_tabs_2 = widgets.Output(layout=widgets.Layout(border = '1px solid black', width = '100%',))
out_2a_tabs_3 = widgets.Output(layout=widgets.Layout(border = '1px solid black', width = '100%',))

#lab2b out variables
out_2b_tabs_1 = widgets.Output(layout=widgets.Layout(border = '1px solid black', width = '100%',))

# lab3 out variables
out_3_tabs_1 = widgets.Output(layout=widgets.Layout(border = '1px solid black', width = '100%',))
out_3_tabs_2 = widgets.Output(layout=widgets.Layout(border = '1px solid black', width = '100%',))
out_3_tabs_3 = widgets.Output(layout=widgets.Layout(border = '1px solid black', width = '100%',))
out_3_tabs_4 = widgets.Output(layout=widgets.Layout(border = '1px solid black', width = '100%',))

# setting logger
logging.basicConfig(format='[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# action on tab click for agent trace

def click_button(obj):
    with out:
        out.clear_output()
        logger.info(f'Expand JSON elements (if available) in {obj.new}')
        if obj.new == "Pre-Processing":
             with open("trace_files/preProcessingTrace_" + trace_filename_prefix + "_" + str(turn_number) + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Orchestration":
             with open("trace_files/orchestrationTrace_" + trace_filename_prefix + "_" + str(turn_number) + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Knowledge-Base":
             with open("trace_files/knowledgeBaseLookupOutput_" + trace_filename_prefix + "_" + str(turn_number) + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Post-Processing":
             with open("trace_files/postProcessingTrace_" + trace_filename_prefix + "_" + str(turn_number) + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "ActionInvocation-Output":
            with open("trace_files/actionGroupInvocationOutput_" + trace_filename_prefix + "_" + str(turn_number) + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))


def click_button_lab2a_turn1(obj):
    with out_2a_tabs_1:
        out_2a_tabs_1.clear_output()
        logger.info(f'Expand JSON elements (if available) in {obj.new}')
        
        if obj.new == "Pre-Processing":
             with open("trace_files/preProcessingTrace_" + 'lab2a_agent_trace' + "_" + '1' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Orchestration":
             with open("trace_files/orchestrationTrace_" + 'lab2a_agent_trace' + "_" + '1' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Knowledge-Base":
             with open("trace_files/knowledgeBaseLookupOutput_" + 'lab2a_agent_trace' + "_" + '1' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Post-Processing":
             with open("trace_files/postProcessingTrace_" + 'lab2a_agent_trace' + "_" + '1' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "ActionInvocation-Output":
            with open("trace_files/actionGroupInvocationOutput_" + 'lab2a_agent_trace' + "_" + str(turn_number) + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
                


def click_button_lab2a_turn2(obj):
    with out_2a_tabs_2:
        out_2a_tabs_2.clear_output()
        logger.info(f'Expand JSON elements (if available) in {obj.new}')
        
        if obj.new == "Pre-Processing":
             with open("trace_files/preProcessingTrace_" + 'lab2a_agent_trace' + "_" + '2' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Orchestration":
             with open("trace_files/orchestrationTrace_" + 'lab2a_agent_trace' + "_" + '2' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Knowledge-Base":
             with open("trace_files/knowledgeBaseLookupOutput_" + 'lab2a_agent_trace' + "_" + '2' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Post-Processing":
             with open("trace_files/postProcessingTrace_" + 'lab2a_agent_trace' + "_" + '2' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "ActionInvocation-Output":
            with open("trace_files/actionGroupInvocationOutput_" + 'lab2a_agent_trace' + "_" + '2' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))



def click_button_lab2a_turn3(obj):
    with out_2a_tabs_3:
        out_2a_tabs_3.clear_output()
        logger.info(f'Expand JSON elements (if available) in {obj.new}')
        
        if obj.new == "Pre-Processing":
             with open("trace_files/preProcessingTrace_" + 'lab2a_agent_trace' + "_" + '3' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Orchestration":
             with open("trace_files/orchestrationTrace_" + 'lab2a_agent_trace' + "_" + '3' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Knowledge-Base":
             with open("trace_files/knowledgeBaseLookupOutput_" + 'lab2a_agent_trace' + "_" + '3' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Post-Processing":
             with open("trace_files/postProcessingTrace_" + 'lab2a_agent_trace' + "_" + '3' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "ActionInvocation-Output":
            with open("trace_files/actionGroupInvocationOutput_" + 'lab2a_agent_trace' + "_" + '3' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))



def click_button_lab2b_turn1(obj):
    with out_2b_tabs_1:
        out_2b_tabs_1.clear_output()
        logger.info(f'Expand JSON elements (if available) in {obj.new}')
        
        if obj.new == "Pre-Processing":
             with open("trace_files/preProcessingTrace_" + 'lab2b_agent_trace' + "_" + '1' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Orchestration":
             with open("trace_files/orchestrationTrace_" + 'lab2b_agent_trace' + "_" + '1' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Knowledge-Base":
             with open("trace_files/knowledgeBaseLookupOutput_" + 'lab2b_agent_trace' + "_" + '1' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Post-Processing":
             with open("trace_files/postProcessingTrace_" + 'lab2b_agent_trace' + "_" + '1' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "ActionInvocation-Output":
            with open("trace_files/actionGroupInvocationOutput_" + 'lab2b_agent_trace' + "_" + '1' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
                


def click_button_lab3_turn1(obj):
    with out_3_tabs_1:
        out_3_tabs_1.clear_output()
        logger.info(f'Expand JSON elements (if available) in {obj.new}')
        
        if obj.new == "Pre-Processing":
             with open("trace_files/preProcessingTrace_" + 'lab3_agent_trace' + "_" + '1' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Orchestration":
             with open("trace_files/orchestrationTrace_" + 'lab3_agent_trace' + "_" + '1' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Knowledge-Base":
             with open("trace_files/knowledgeBaseLookupOutput_" + 'lab3_agent_trace' + "_" + '1' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Post-Processing":
             with open("trace_files/postProcessingTrace_" + 'lab3_agent_trace' + "_" + '1' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "ActionInvocation-Output":
            with open("trace_files/actionGroupInvocationOutput_" + 'lab3_agent_trace' + "_" + '1' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))


         
def click_button_lab3_turn2(obj):
    with out_3_tabs_2:
        out_3_tabs_2.clear_output()
        logger.info(f'Expand JSON elements (if available) in {obj.new}')
        
        if obj.new == "Pre-Processing":
             with open("trace_files/preProcessingTrace_" + 'lab3_agent_trace' + "_" + '2' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Orchestration":
             with open("trace_files/orchestrationTrace_" + 'lab3_agent_trace' + "_" + '2' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Knowledge-Base":
             with open("trace_files/knowledgeBaseLookupOutput_" + 'lab3_agent_trace' + "_" + '2' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Post-Processing":
             with open("trace_files/postProcessingTrace_" + 'lab3_agent_trace' + "_" + '2' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Lambda-Output":
            with open("trace_files/actionGroupInvocationOutput_" + 'lab3_agent_trace' + "_" + '2' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "ActionInvocation-Output":
            with open("trace_files/actionGroupInvocationOutput_" + 'lab3_agent_trace' + "_" + '2' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))



def click_button_lab3_turn3(obj):
    with out_3_tabs_3:
        out_3_tabs_3.clear_output()
        logger.info(f'Expand JSON elements (if available) in {obj.new}')
        
        if obj.new == "Pre-Processing":
             with open("trace_files/preProcessingTrace_" + 'lab3_agent_trace' + "_" + '3' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Orchestration":
             with open("trace_files/orchestrationTrace_" + 'lab3_agent_trace' + "_" + '3' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Knowledge-Base":
             with open("trace_files/knowledgeBaseLookupOutput_" + 'lab3_agent_trace' + "_" + '3' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Post-Processing":
             with open("trace_files/postProcessingTrace_" + 'lab3_agent_trace' + "_" + '3' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "ActionInvocation-Output":
            with open("trace_files/actionGroupInvocationOutput_" + 'lab3_agent_trace' + "_" + '3' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))



def click_button_lab3_turn4(obj):
    with out_3_tabs_4:
        out_3_tabs_4.clear_output()
        logger.info(f'Expand JSON elements (if available) in {obj.new}')
        
        if obj.new == "Pre-Processing":
             with open("trace_files/preProcessingTrace_" + 'lab3_agent_trace' + "_" + '4' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Orchestration":
             with open("trace_files/orchestrationTrace_" + 'lab3_agent_trace' + "_" + '4' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Knowledge-Base":
             with open("trace_files/knowledgeBaseLookupOutput_" + 'lab3_agent_trace' + "_" + '4' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "Post-Processing":
             with open("trace_files/postProcessingTrace_" + 'lab3_agent_trace' + "_" + '4' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))
        elif obj.new == "ActionInvocation-Output":
            with open("trace_files/actionGroupInvocationOutput_" + 'lab3_agent_trace' + "_" + '4' + ".log", "r") as agent_trace_fp:
                display(JSON(agent_trace_fp.read()))



def show_tabs(trace_filename_prefix, turn_number):
    
    toggles = widgets.ToggleButtons(
    options=['Click-tabs >>','Pre-Processing', 'Orchestration', 'Knowledge-Base', 'ActionInvocation-Output', 'Post-Processing'],
    description='Agent Trace: (Last Logged trace only) Full trace available inside trace_files/ folder ',
    disabled=False,
    button_style='success', 
    tooltips=['Click all tabs to view last output trace of that step', 'Pre-Processing Trace', 'Orchestration Trace', 'Knowledge-Base Trace', 'ActionInvocationOutput Trace', 'Post-Processing Trace'],
)
    print(f"trace_filename_prefix = {trace_filename_prefix} and turn_number = {turn_number}")
    ## lab2a
    if trace_filename_prefix == 'lab2a_agent_trace' and turn_number == 1:
        toggles.observe(click_button_lab2a_turn1, 'value')
    elif trace_filename_prefix == 'lab2a_agent_trace' and turn_number == 2:
        toggles.observe(click_button_lab2a_turn2, 'value')
    elif trace_filename_prefix == 'lab2a_agent_trace' and turn_number == 3:
        toggles.observe(click_button_lab2a_turn3, 'value')
        
    ## lab2b
    elif trace_filename_prefix == 'lab2b_agent_trace' and turn_number == 1:
        toggles.observe(click_button_lab2b_turn1, 'value')
    
    ## lab3
    elif trace_filename_prefix == 'lab3_agent_trace' and turn_number == 1:
        toggles.observe(click_button_lab3_turn1, 'value')
    elif trace_filename_prefix == 'lab3_agent_trace' and turn_number == 2:
        toggles.observe(click_button_lab3_turn2, 'value')
    elif trace_filename_prefix == 'lab3_agent_trace' and turn_number == 3:
        toggles.observe(click_button_lab3_turn3, 'value')
    elif trace_filename_prefix == 'lab3_agent_trace' and turn_number == 4:
        toggles.observe(click_button_lab3_turn4, 'value')
    
    display(toggles)
