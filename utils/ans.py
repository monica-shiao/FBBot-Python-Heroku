from random import randint

greeting_ans = [
	'您想看哪邊的房子呢？',
	'您對哪邊的房子有興趣呢？',
	'想看哪～ 我可以推薦幾間好房給您！',
	'你好～ 我可以幫你推薦房子喔＾＾'
]

sale_ans=[
	'來來來～ 這些是推薦給您不錯買的房子！',
	'看看這些房子怎麼樣～',
	'這是我們推薦分數不錯可以買的房子'
]


rent_ans=[
	'看看這些房子怎麼樣～',
	'這是我們推薦分數不錯可以租的房子喔＾＾',
	'租房這些都不錯喔！ 慢慢看。'
]

def randomAnswer(f_name):
	return f_name[randint(0,len(f_name)-1)]

def star(num):
    message=''
    for n in range(0,5):
        if n < num:
            message += '⭐️'
        else:
            message += '☆'
    return message







