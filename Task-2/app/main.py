from app.agent import agent
from langgraph.types import Command


# -------- > Start Graph Execution :


# first while loop for handle multiple user query 
while True:
    print("============================================== Start =================================================================================")
    user_question = input("\n👨 User : ")

    input_state = {
        'question' : user_question,
        "iteration_count" : 0,
        'tool_call_log' : []
    }

    if user_question.lower() == "exit":
        break

    config = {"configurable": {"thread_id": "thread-1"}}

    for event in agent.stream(
        input_state,
        config=config,
        stream_mode="updates"
    ):
        if "call_llm" in event:    
            print("\n====================")
            print("Tool_call_Require : ",event['call_llm']['tool_call'])
            print("tool_name : ",event['call_llm']['tool_name'])
            print("Through : ",event['call_llm']['through'])
            print("tool_args : ",event['call_llm']['tool_args'])
            print("----------")

    current_state = agent.get_state(config=config)


    # second while loop for handle multiple interrupts 
    while current_state.interrupts:
        print("\n🛑 Interrupt : ",current_state.interrupts[0].value)
        user_input = input("enter the approval :")
        for event in agent.stream(
            Command(resume=user_input),
            config=config,
            stream_mode="updates"
        ):
            if "call_llm" in event:    
                print("\n====================")
                print("Tool_call_Require : ",event['call_llm']['tool_call'])
                print("tool_name : ",event['call_llm']['tool_name'])
                print("Through : ",event['call_llm']['through'])
                print("tool_args : ",event['call_llm']['tool_args'])
                print("----------")

            if "tool_node" in event:
                print("\n----------")    
                print("🔧 tool_result : ",event['tool_node']['tool_result'])
                print("====================")

        current_state = agent.get_state(config=config)


    # print result After graph Execution
    print("\n\n----------------")
    print("|✅ Output :-  |")
    print("----------------")
    print("Question : ",current_state.values['question'])
    print("final_answer : ",current_state.values['final_answer'])


    # print tool call summary 
    print("\n\n----------------------------")
    print("| Tool - Call -Summary :-  |")
    print("----------------------------")

    if len(current_state.values['tool_call_log']) == 0:
        print("\n No Call An External Tool -- ")

    for i,doc in enumerate(current_state.values['tool_call_log'] ,start=1):
        print("\n")
        print(f"[{i}].")
        print("Tool_Name : ",doc['tool_name'])
        print("Tool_Args : ",doc['tool_args'])
        print("Tool_Result : ",doc['tool_answer'])


    print("\n============================================== End =================================================================================")
