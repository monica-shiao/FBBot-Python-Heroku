from pymessager.message import GenericElement, ActionButton, ButtonType
from utils.ans import *
import requests

API = 'https://b02.api.theo.com.tw'
recommend = API + '/recommend'
houseDetail = API + '/house'
favorite = API + '/favorite'
addfavorite = API + '/favorite/add'
delfavorite = API + '/favorite/del'

houseDescribe = ['earthquake','flooding','mudslide','radiation','sand','soil','unlucky']

RECOMMENDQUERY = {
        'userid': '0123456789',
        'type': 'sale',
        'orderBy': 'score',
        'order': '1',
        'position': 'selected',
        'city': '臺北市',
        'area': '中正區',
        'lat': '25.223',
        'lng': '121.3043',
        'minBuy': '0',
        'maxBuy': '999',
        'minRent': '1',
        'maxRent': '99999',
        'house': '1',
        'function': '1',
        'environment': '1'
    }

DETAILQUERY = {
        'id': 0,
        'userid': '0123456789'
    }

FAVORATEQUERY = {
        'userid': '0123456789',
        'orderBy': 'score',
        'order': 0
    }

CHANGE_LOVE_QUERY = {
        'userid': '0123456789',
        'house_id': '123'
    }
    
REGION = {
    '臺北市': ['大安區','士林區','內湖區','文山區','北投區','中山區','信義區','松山區','萬華區','中正區','大同區','南港區'],   
    '新北市': ['板橋區','新莊區','中和區','三重區','新店區','土城區','永和區','蘆洲區','汐止區','樹林區','淡水區','三峽區','林口區','鶯歌區','五股區','泰山區','瑞芳區','八里區','深坑區','三芝區','萬里區','金山區','貢寮區','石門區','雙溪區','石碇區','坪林區','烏來區','平溪區'],
    '桃園市': ['桃園區','中壢區','平鎮區','八德區','楊梅區','蘆竹區','龜山區','龍潭區','大溪區','大園區','觀音區','新屋區','復興區'],
    '臺中市': ['北屯區','西屯區','大里區','太平區','豐原區','南屯區','北區','南區','西區','潭子區','大雅區','沙鹿區','清水區','龍井區','東區','大甲區','烏日區','神岡區','霧峰區','梧棲區','大肚區','后里區','東勢區','外埔區','新社區','大安區','中區','石岡區','和平區'],
    '臺南市': ['永康區','安南區','東區','北區','南區','新營區','中西區','仁德區','歸仁區','安平區','佳里區','善化區','麻豆區','新化區','新市區','關廟區','安定區','白河區','學甲區','鹽水區','西港區','下營區','後壁區','七股區','六甲區','柳營區','官田區','東山區','將軍區','玉井區','北門區','大內區','楠西區','南化區','山上區','左鎮區','龍崎區'],
    '高雄市': ['鳳山區','三民區','左營區','前鎮區','楠梓區','苓雅區','小港區','鼓山區','大寮區','岡山區','仁武區','林園區','路竹區','新興區','鳥松區','大樹區','美濃區','橋頭區','旗山區','梓官區','大社區','茄萣區','燕巢區','湖內區','阿蓮區','旗津區','前金區','鹽埕區','彌陀區','內門區','永安區','六龜區','杉林區','田寮區','甲仙區','桃源區','茂林區','那瑪夏區' ],
    '基隆市': ['仁愛區','中正區','信義區','中山區','安樂區','七堵區','暖暖區'],
    '新竹市': ['東區','北區','香山區'],
    '嘉義市': ['東區','西區'],
    '新竹線': ['竹北市','竹東鎮','新埔鎮','關西鎮','湖口鄉','新豐鄉','峨眉鄉','寶山鄉','北埔鄉','芎林鄉','橫山鄉','尖石鄉','五峰鄉'],
    '苗栗縣': ['苗栗市','頭份市','竹南鎮','後龍鎮','通霄鎮','苑裡鎮','卓蘭鎮','造橋鄉','西湖鄉','頭屋鄉','公館鄉','銅鑼鄉','三義鄉','大湖鄉','獅潭鄉','三灣鄉','南庄鄉','泰安鄉'],
    '彰化縣': ['彰化市','員林市','和美鎮','鹿港鎮','溪湖鎮','二林鎮','福興鄉','花壇鄉','社頭鄉','田中鎮','秀水鄉','永靖鄉','大村鄉','伸港鄉','埔心鄉','芳苑鄉','北斗鎮','埔鹽鄉','埤頭鄉','溪州鄉','田尾鄉','芬園鄉','大城鄉','線西鄉','二水鄉','竹塘鄉'],
    '南投縣': ['南投市','埔里鎮','草屯鎮','竹山鎮','集集鎮','名間鄉','鹿谷鄉','中寮鄉','魚池鄉','國姓鄉','水里鄉','仁愛鄉','信義鄉'],
    '雲林縣': ['斗六市','斗南鎮','虎尾鎮','西螺鎮','土庫鎮','北港鎮','古坑鄉','大埤鄉','莿桐鄉','林內鄉','二崙鄉','崙背鄉','麥寮鄉','東勢鄉','褒忠鄉','臺西鄉','元長鄉','四湖鄉','口湖鄉','水林鄉'],
    '嘉義縣': ['太保市','朴子市','布袋鎮','大林鎮','民雄鄉','溪口鄉','新港鄉','六腳鄉','東石鄉','義竹鄉','鹿草鄉','水上鄉','中埔鄉','竹崎鄉','梅山鄉','番路鄉','大埔鄉','阿里山鄉'],
    '屏東縣': ['屏東市','潮州鎮','東港鎮','恆春鎮','萬丹鄉','長治鄉','麟洛鄉','九如鄉','里港鄉','鹽埔鄉','高樹鄉','萬巒鄉','內埔鄉','竹田鄉','新埤鄉','枋寮鄉','新園鄉','崁頂鄉','林邊鄉','南州鄉','佳冬鄉','琉球鄉','車城鄉','滿州鄉','枋山鄉','三地門鄉','霧臺鄉','瑪家鄉','泰武鄉','來義鄉','春日鄉','獅子鄉','牡丹鄉'],
    '宜蘭縣': ['宜蘭市','羅東鎮','蘇澳鎮','頭城鎮','礁溪鄉','壯圍鄉','員山鄉','冬山鄉','五結鄉','三星鄉','大同鄉','南澳鄉'],
    '花蓮縣': ['花蓮市','鳳林鎮','玉里鎮','新城鄉','吉安鄉','壽豐鄉','光復鄉','豐濱鄉','瑞穗鄉','富里鄉','秀林鄉','萬榮鄉','卓溪鄉'],
    '臺東縣': ['臺東市','成功鎮','關山鎮','卑南鄉','大武鄉','太麻里鄉','東河鄉','長濱鄉','鹿野鄉','池上鄉','綠島鄉','延平鄉','海端鄉','達仁鄉','金峰鄉','蘭嶼鄉'],
    '澎湖縣': ['馬公市','湖西鄉','白沙鄉','西嶼鄉','望安鄉','七美鄉']
    }

# 搜尋區域的縣市
def askCity(input_area):

    '''
    # 這應該要寫在外面
    if area == ('東區'or'西區'or'南區'or'北區'):
        ans="請問是哪一個縣市的" + area + "呢？"
        print(ans)
        return 
    '''
    for city in REGION:
        for area in REGION[city]:
            if input_area == area:
                return(city, area)


# 判斷縣市區域配對有無錯誤
def regionMatch(city, input_area):
    check = False
    for area in REGION[city]:
        if input_area == area:
            check=True
            break
    
    return check

def createRecommend():
    
    return RECOMMENDQUERY

def createDetail():
    
    return DETAILQUERY

def createFavorite():
    
    return FAVORATEQUERY

def displayHouse(client, sender_id, rec_query):
    client.send_text(sender_id, "Please wait...")
    rec_query['userid'] = sender_id

    res = requests.post(recommend, data=rec_query)
    response_data = res.json()

    response_message = randomAnswer(sale_ans) if rec_query['type'] == 'sale' else randomAnswer(rent_ans)

    # Get House's result is not empty
    if (response_data['_status'] == 'OK') and (len(response_data['result']) > 0):
        
        results = response_data['result']
        # Show the template
        project_list = []
        for cnt in range(0,5):
            house_id = str(results[cnt]['house_id'])
            title = results[cnt]['title']
            address = results[cnt]['address']
            
            project_list.append(GenericElement(title, address, "http://g.udn.com.tw/upfiles/B_AD/ady1007/PSN_PHOTO/887/f_9359887_1.jpg",
                                [ActionButton(ButtonType.POSTBACK,"房屋詳細資料",payload=house_id),
                                ActionButton(ButtonType.POSTBACK,"新增我的最愛",payload=house_id)]))
            
            if cnt == len(results)-1:
                break

        client.send_generic(sender_id, project_list)

    else:
        response_message = "抱歉這裡沒有推薦房屋喔～"

    return response_message

def displayDetail(client, sender_id, detail_query):
    detail_query['userid'] = sender_id
    res = requests.post(houseDetail, data=detail_query)
    houseDetails = res.json()
    details = houseDetails["result"]
    
    describe_message = ''
    for element in houseDescribe:
        if details["describe"][element]["status"]:
            describe_message += "☑️" + details["describe"][element]["result"]

    response_message = """{title}
格局：{pattern}
地址：{address}
販售類型：{type}
{price_type}：{price}{price_unit}{favorite}

分數：
\t總分：{final}
\t環境分數：{env}
\t機能分數：{function}
\t房屋分數：{house}

機能評判：

☑️{consumption}☑️學校：{school}☑️交通：{transportation}{describe}
網頁介紹：{link}
資料來源：{source}""".format(
        title=details['title'], pattern=details["pattern"], address=details["address"],
        type='租屋' if details['type']=='rent' else '買屋',
        price_type='租金' if details['type']=='rent' else '售價',
        price=str(details["price"]), price_unit='元' if details['type']=='rent' else '萬元',
        favorite='\n已加入我的最愛❤️' if details['is_favorite'] == 1 else "",
        final=star(details["score"]["_final"]),
        env=star(details["score"]["environment"]),
        function=star(details["score"]["function"]),
        house=star(details["score"]["house"]),
        consumption=details["describe"]["consumption"],
        school=details["describe"]["school"],
        transportation=details["describe"]["transportation"],
        describe=describe_message,
        link=details["link"],
        source=details["source"]
    )

    client.send_text(sender_id, response_message)

def displayFavorate(client, sender_id, fav_query):
    client.send_text(sender_id, "Please wait...")
    fav_query['userid'] = sender_id
    res = requests.post(favorite, data=fav_query)
    response_data = res.json()
    response_message = ""

    # Get House's result is not empty
    if (response_data['_status'] == 'OK') and (len(response_data['result']) > 0):
        
        results = response_data['result']
        
        # project_list[0] is rent, project_list[1] is sale
        project_list=[[],[]]
        for cnt in range(0,10):
            house_id = str(results[cnt]['house_id'])
            title = results[cnt]['title']
            address = results[cnt]['address']

            p_list = project_list[0] if results[cnt]['type'] == 'rent' else project_list[1]
            p_list.append(GenericElement(title, address, "http://g.udn.com.tw/upfiles/B_AD/ady1007/PSN_PHOTO/887/f_9359887_1.jpg",
                            [ActionButton(ButtonType.POSTBACK,"房屋詳細資料",payload=house_id),
                            ActionButton(ButtonType.POSTBACK,"從我的最愛刪除",payload=house_id)]))
            
            if cnt == len(results)-1:
                break

        if(len(project_list[0]) > 0):
            client.send_generic(sender_id, project_list[0])
            client.send_text(sender_id, "上面是您加入我的最愛中的租屋。")

        if(len(project_list[1]) > 0):
            client.send_generic(sender_id, project_list[1])
            client.send_text(sender_id, "這些是在我的最愛中，您可能有意願購買的房子")

    else:
        response_message = "沒有我的最愛喔～"

    return response_message

def changefavorate(change_type, sender_id, house_id):
    CHANGE_LOVE_QUERY['userid'] = sender_id
    CHANGE_LOVE_QUERY['house_id'] = house_id

    res = requests.post(addfavorite if change_type == 'add' else delfavorite, data=CHANGE_LOVE_QUERY)

    response_data = res.json()
    print(str(response_data))

    return 
