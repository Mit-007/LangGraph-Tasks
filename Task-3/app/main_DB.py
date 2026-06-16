from app.utils.subgraph.graph_DB_researcher import DB_researcher_agent
from app.core.config import DB_PATH_OF_COLLECTION
import uuid
while(True):

    print("============================================== Start =================================================================================")
    
    user_input = input("👨 User : ")

    input_state = {
        "query" : user_input,
        "db_path" :DB_PATH_OF_COLLECTION,
        "sub_querys" : [],
        "schema_of_collection" : {},
        "workers_output" :[],
        "final_result" : ""
    }

    if user_input.lower() == "exit":
        break

    config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    print("\n---------------")
    print("|🆔 thread_id |")
    print("---------------")
    print(config['configurable']['thread_id'])

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