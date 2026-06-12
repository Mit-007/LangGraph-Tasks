from app.utils.subgraph.graph_web_researcher import web_researcher_agent

while(True):

    print("============================================== Start =================================================================================")
    
    user_input = input("User : ")

    input_state = {
        'topic' : user_input,
        'sub_topics' : [],
        'workers_output' : [],
        'final_result' : ""
    }

    if user_input.lower() == "exit":
        break

    config = {"configurable": {"thread_id": "thread-1"}}

    result = web_researcher_agent.invoke(input_state,config)

    print("\n----------------About Research-------------------------")

    print("\n----------------")
    print("| 🎯 Topic      |")
    print("----------------")
    print(result["topic"])

    print("\n----------------")
    print("| 🧩 Sub Topics |")
    print("----------------")
    print(result["sub_topics"])

    print("\n----------------")
    print("| ✅ Final Answer |")
    print("----------------")
    print(result["final_result"])

    print("\n---------------- End Research -------------------------")

    print("============================================== End ===================================================================================")