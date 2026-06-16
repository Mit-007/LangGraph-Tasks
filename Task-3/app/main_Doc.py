from app.utils.subgraph.graph_doc_researcher import Doc_researcher_agent
import uuid
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

    config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    print("\n---------------")
    print("|🆔 thread_id |")
    print("---------------")
    print(config['configurable']['thread_id'])

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