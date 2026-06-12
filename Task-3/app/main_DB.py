from app.utils.subgraph.graph_DB_researcher import DB_researcher_agent

while(True):

    print("============================================== Start =================================================================================")
    
    user_input = input("👨 User : ")

    input_state = {
        "query" : user_input,
        "db_path" :"app/db/Task_3_data.db",
        "sub_querys" : [],
        "schema_of_collection" : {},
        "workers_output" :[],
        "final_result" : ""
    }

    if user_input.lower() == "exit":
        break

    config = {"configurable": {"thread_id": "thread-1"}}

    result = DB_researcher_agent.invoke(input_state,config)

    print("\n----------------About Research-------------------------")

    print("\n-----------------")
    print("| 👨 Query      |")
    print("-----------------")
    print(result["query"])

    # print("\n-----------------")
    # print("| 🗂️ Schema     |")
    # print("-----------------")
    # print(result["schema_of_collection"])

    print("\n------------------")
    print("| 📋 Sub Queries |")
    print("------------------")
    print(result["sub_querys"])

    print("\n--------------------")
    print("| 👷 Worker Output |")
    print("--------------------")
    print(result["workers_output"])

    print("\n-------------------")
    print("| ✅ Final Answer |")
    print("-------------------")
    print(result["final_result"])

    print("\n---------------- End Research -------------------------")

    print("============================================== End ===================================================================================")