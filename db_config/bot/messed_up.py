def make_dict(data:list):
    print(f'\n\n\n{data}\n\n\n\n')
    u_type,u_info=data
    
    admin=["id","telegram_id","joined_date"]
    service=["id","name","telegram_id","number","telegram_username", "region","description","joined_date"]
    customer=["id","name","telegram_id","number","telegram_username"]
    dict_keys=[admin,service,customer][u_type]
    dic={}
    for i in range(len(dict_keys)):
        dic[dict_keys[i]]=u_info[i]

    return dic

def for_loop(data):
    data=data.split(",")
    looped=""
    for i in range(0,len(data),3):
        looped+=f"{data[i-2]}, "
    return looped
def format_the_data(data:list):
    districts=for_loop(data[10])
    skills=for_loop(data[11])
    user_info=data[0:7]
    region=data[7:10]
    return [user_info,region,districts,skills]
