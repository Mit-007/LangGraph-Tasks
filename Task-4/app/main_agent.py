from app.agent import agent
import uuid

while True:
    print("============================================== Start =================================================================================")
    user_transScript = input("\nUser : ")

    input_state = {
        "call_transcript" : user_transScript,
        "issues" : [],
        "severity" : [],
        "fixes" : [],
        "draft_report" :"",
        "overall_score" :0.0
    }

    if user_transScript.lower() == "exit":
        break

    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    res = agent.invoke(input_state,config=config)

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
    print("final_answer : ",current_state.values['draft_report'])

    print("\n============================================== End =================================================================================")
