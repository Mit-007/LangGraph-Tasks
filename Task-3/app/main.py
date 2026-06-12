from app.agent import researcher_agent

while(True):

    print("============================================== Start =================================================================================")
    
    user_input = input("User : ")

    input_state = {
        'user_input' : user_input,
        'researchers_list' : [],
        'researchers_output' : [],
        'final_report' : "******"
    }

    if user_input.lower() == "exit":
        break

    config = {"configurable": {"thread_id": "thread-1"}}

    result = researcher_agent.invoke(input_state,config)

    print("\n--------------")
    print("|👨 question |")
    print("--------------")
    print(result["user_input"])

    print("\n----------------------")
    print("|🧠 researchers_list |")
    print("----------------------")
    print(result["researchers_list"])

    print("\n------------------------")
    print("|⚙️ researchers_output |")
    print("------------------------")
    print(result["researchers_output"])

    print("\n--------------------")
    print("|📄 Final-Research |")
    print("--------------------")
    print(result["final_report"])

    print("============================================== End ===================================================================================")