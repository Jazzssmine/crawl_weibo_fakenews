from bs4 import BeautifulSoup
import pandas as pd
import re
import unidecode
import time

path = []
for i in range(1, 51):
    path.append('text_data/' + str(i) + '.txt')

for i in range(0, 50):
    crawl_path = 'crawl_data/text_data' + str(i) + '.csv'
    html = open(path[i], 'r', encoding='utf-8')
    htmlhandle = html.read()
    soup = BeautifulSoup(htmlhandle, 'lxml')

    result = pd.DataFrame()
    result.drop(result.index, inplace=True)
    view = []
    inform = []
    reported_id = []
    reported_address = []
    reported_gender = []
    reported_credit = []
    post_time = []
    cn_links = []
    ## 访问次数
    li = soup.find_all(text=re.compile("访问次数"))
    pattern = re.compile(r'\d+')
    for item in li:
        string = unidecode.unidecode(item.string)
        view.append(re.findall(pattern, string)[0])
    ## 举报人数
    list_report = soup.select('input[node-type="uids_num"] ')
    for item in list_report:
        inform.append(item['value'])

    for item in soup.find_all("div", class_="user bg_orange2 clearfix"):
        ## 被举报人id
        link_u = item.select('p a')
        reported_id.append(str(link_u)[29:39])

        ## 被举报人位置
        string = str(item.contents[5])[-15:]
        add = re.sub("[A-Za-z0-9\<\>\"\/\\t]", "", string)
        reported_address.append(add)

        ## 被举报人信用等级
        x = item.select('p a[target="_blank"] ')
        credit_u_i = re.findall(r'信用等级：(.+)"', str(x))
        reported_credit.append(credit_u_i)

    ## 原微博发布时间
    '''for item in soup.find_all(text=re.compile("发布时间")):
        match=re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', item)
        if match==None:
            post_time.append('nn')
        else:
            post_time.append(time.strptime(match.group(), '%Y-%m-%d %H:%M:%S'))'''
    for item in soup.find_all('div', {'class': 'item top'}):
        if item.p.a == None:
            post_time.append('None')
        else:
            match = re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', str(item.p))
            post_time.append(match[0])
            # post_time.append(time.strptime(match.group(), '%Y-%m-%d %H:%M:%S'))

    ## 原微博链接
    for item in soup.select('div[class="W_main_half_r"] div div div div[class="item top"]'):
        if item.p.a == None:
            cn_links.append('nn')
        else:
            weibo_cn = re.findall(r'(?<=\/)[\w]*(?=\"\s)', str(item.p.a))
            cn_links.append('https://weibo.cn/comment/' + weibo_cn[0])
    result['view_num'] = view
    result['inform_num'] = inform
    result['reported_id'] = reported_id
    '''result['reported_gender'] = reported_gender'''
    result['reported_address'] = reported_address
    result['post_time'] = post_time
    result['link_to_post'] = cn_links
    result['reported_credit'] = reported_credit
    print(result)
    result.to_csv(crawl_path, index=None, header=True)