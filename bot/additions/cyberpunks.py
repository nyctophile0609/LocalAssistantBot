
def generate_text1(data:list,):
    message=""
    for j,i in enumerate(data):
        message+=f"{j+1}. {i[1]}\n"
    return message


    
def paginate_data(data:list,pn:int):
    qw=value=None
    if len(data[pn-12:])>=12:
        qw=data[pn-12:pn]
    else:
        qw=data[pn-12:]
    
    if pn==12 and len(data)>12:
        value=[0,1]
    elif 12<len(data)<=pn:
        value=[1,0]
    elif len(data)<12 and pn==12:
        value=[0,0]
    elif 12<pn<len(data):
        value=[1,1]
    return [qw,value]
    


def make_dict(data:list):
    u_type,u_info=data
    admin=["id","telegram_id","joined_date"]
    service=["id","telegram_id","name","number","telegram_username","description","joined_date"]
    customer=["id","telegram_id","name","number","telegram_username","joined_date"]
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



def format_the_message(data:dict,username,description):
    m=""
    n1=data["name"]
    n2=data["contact_info"][0][1]
    n4=data["region"][1]
    n5=data["districts"]
    n6=data["skills"]
    districts=generate_text1(n5)
    skills=generate_text1(n6)
    m=f"""
<b>Name:</b> {n1}
<b>Phone number:</b> {n2}
<b>Telegram username:</b> @{username}
==============================================
<b>Region:</b> {n4}
==============================================
<b>Districts:</b>\n{districts}
==============================================
<b>Skills:</b>\n{skills}
==============================================
<b>Description:</b> {description}
    """

    return m

def format_the_message1(data):
    name=data[0][2]
    number=data[0][3]
    username=data[0][4]
    districts=generate_text1(data[2])
    skills=generate_text1(data[1])
    description=data[0][5]
    date=data[0][6]
    m=f"""
<b>Name:</b> {name}
<b>Phone number:</b> {number}
<b>Telegram username:</b> @{username}
<b>Serving since:</b>{date} 
===================================
<b>Districts:</b>\n{districts}
=================================
<b>Skills:</b>\n{skills}
================================
<b>Description:</b> {description}
    """
    return m

def make_it_list(data:list):
    r=[]
    for i in data:
        r.append(i[0])

    return r
