from app.agent import chat_agent
from app.core.constant import MOOD_HISTORY_COUNTER 

user_state = {
    "messages" : [],
    "summary" : "",
    "turn_count":0,
    "mood": [],
    "summary_status" : False
}

print("===============================================[Start the Converstion]=========================================================")
while(True):
    print("\n\n")
    user_input = input("👨 user : ")

    if(user_input == "exit"):
        break

    user_state['messages'].append(user_input)

    user_state = chat_agent.invoke(user_state)

    if user_state['messages'][-1] != 'error occurred':
        print("🤖 AI : ",user_state['messages'][-1])
        print("Mood : ",user_state['mood'][-1])
    else : 
        print("🤖 AI : Somthing Wrong , LLm Could not Generate Answer.")

    print("summary : ",user_state['summary'])
    print("turn_count : " ,user_state['turn_count'])
    if user_state['turn_count'] % MOOD_HISTORY_COUNTER ==0:
        print("mood list :",user_state['mood'])


print("===============================================[End Of Converstion]=========================================================")

