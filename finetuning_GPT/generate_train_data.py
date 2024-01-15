import json
import os
import jsonlines

train_data_path = "D:\学习资料\大三上\冯如杯\llm_robot\llm_robot\\test_data"
train_file_name = "mydata.jsonl"

prompt = "i"

messages_prefix = "{\"messages\": "
messages_suffix = "}"

def dict2jsonl_str(each_file_dict):
    messages = [{"role": "system", "content": prompt}]
    user_question =  each_file_dict[0]['question']
    assistant_reply = each_file_dict[1]['answer']
    messages.append({"role": "user", "content": user_question})
    messages.append({"role": "assistant", "content": assistant_reply})




    return {"messages": messages}





def dataset2data():


    fils = os.listdir(train_data_path)
    file_count = len(fils)


    for i in range(0,file_count):
        each_file_name = os.path.join(train_data_path, "test"+str(i)+".json")
        with open(each_file_name, 'r', encoding='utf-8') as each_file:
            each_file_content = each_file.read()
            each_file_dict = json.loads(each_file_content)
            messages = dict2jsonl_str(each_file_dict)


            with jsonlines.open(train_file_name, mode='a') as writer:
                writer.write(messages)




if __name__ == '__main__':
    dataset2data()





