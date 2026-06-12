from app.utils.subgraph.graph_doc_researcher import Doc_researcher_agent

while(True):

    print("============================================== Start =================================================================================")
    
    user_input = input("👨 User : ")

    input_state = {
        'topic' : " ",
        'sub_querys' : [],
        'workers_output' : [],
        'final_result' : ""
    }

    if user_input.lower() == "exit":
        break

    config = {"configurable": {"thread_id": "thread-1"}}

    result = Doc_researcher_agent.invoke(input_state,config)

    print("\n----------------About Research-------------------------")

    print("\n-----------------")
    print("| 🎯 Topic      |")
    print("-----------------")
    print(result["topic"])

    print("\n------------------")
    print("| 📋 Sub Queries |")
    print("------------------")
    print(result["sub_querys"])

    # print("\n--------------------")
    # print("| 👷 Worker Output |")
    # print("--------------------")
    # print(result["workers_output"])

    print("\n-------------------")
    print("| ✅ Final Answer |")
    print("-------------------")
    print(result["final_result"])

    print("\n---------------- End Research -------------------------")

    print("============================================== End ===================================================================================")