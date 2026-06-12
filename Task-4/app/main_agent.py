from app.agent import agent
from langgraph.types import Command


while True:
    print("============================================== Start =================================================================================")
    user_transScript = input("\nUser : ")

    input_state = {
        "call_transcript" : user_transScript,
        "issues" : [],
        "severity" : [],
        "fixes" : [],
        "report" :"",
        "final_answer" :""
    }

    if user_transScript.lower() == "exit":
        break

    config = {"configurable": {"thread_id": "thread-1"}}

    res = agent.invoke(input_state,config=config)

    # print("\n====================")
    # print(" : ",event['call_llm']['tool_call'])
    # print("tool_name : ",event['call_llm']['tool_name'])
    # print("Through : ",event['call_llm']['through'])
    # print("tool_args : ",event['call_llm']['tool_args'])
    # print("----------")

    current_state = agent.get_state(config=config)


    # second while loop for handle multiple interrupts 
    while current_state.interrupts:
        print("\n--------------------------------------------------------")
        print("\n",current_state.interrupts[0].value)
        user_input = input("Your Response :")
        print("\n--------------------------------------------------------")

        current_state = agent.get_state(config=config)


    # print result After graph Execution
    print("\n\n----------------")
    print("| Output :-    |")
    print("----------------")
    print("final_answer : ",current_state.values['final_answer'])

    print("\n============================================== End =================================================================================")
