import requests
from bs4 import BeautifulSoup
import math
#from data import urls, service_table, meta_data, all_photoes, feedbacks
import re
import json




def cards_url_list_get():

    cards_url_list = []

    for i in range(1, 104):
        url = f'https://www.bodo.ua/?page={i}'
        print(url)

        q = requests.get(url)
        result = q.content


        soup = BeautifulSoup(result, 'lxml')
        cards = soup.find_all(class_='product-item__hover-container')

        for card in cards:
            card_page_url = card.get('href')
            cards_url_list.append(card_page_url)

    with open('data/cards_url_list_www.bodo.ua.txt', 'w') as file:
        file.write(json.dumps(cards_url_list))







def feedbacks_list_get():
    with open(f'data/cards_url_list_www.bodo.ua.txt') as file:
        # lines = [line.strip() for line in file.readlines()]
        cards_url_list = json.loads(file.read())

    count = 0
    feedbacks_list = []
    errors = []
    for k in cards_url_list[217:]:
        page = f'{k}/?_pjax=%23experience-feedback&page=1'
        print(f'{count} - {page}')
        count += 1



        r = requests.get(page)
        result = r.content
        try:
            soup = BeautifulSoup(result, 'lxml')
            number = soup.find(class_='col-9 section-headline__col')
            number_page = str(number.find('h3').text)
            num = clean_int(number_page)
            print(num)
            counter = math.ceil(int(num) / 4)

            print(counter)
            counter1 = 0


            for i in range(1, counter+1):

                url = f'{k}/?_pjax=%23experience-feedback&page={i}'



                q = requests.get(url)
                result1 = q.content


                soup = BeautifulSoup(result1, 'lxml')
                feedbacks_page = soup.find_all(class_='comment-item')
                counter1+=1

                for feedback in feedbacks_page:
                    feedback_page_name = feedback.find(class_='comment-item__name').text
                    feedback_page_date = feedback.find(class_='comment-item__date').text
                    feedback_page_comment = feedback.find(class_='comment-text').text

                    feedback_page_url = k
                    feedback_data = []
                    feedback_data.append(feedback_page_url)
                    feedback_data.append(feedback_page_name)
                    feedback_data.append(feedback_page_date)
                    feedback_data.append(feedback_page_comment)


                    print(counter1)

                    feedbacks_list.append(feedback_data)
        except AttributeError:
            errors.append(page)
            return

        print (f'ok {count}')



    print(feedbacks_list)
    print(errors)

    with open('data/all_feedbacks_list_www.bodo.ua2.txt', 'w') as file:
        file.write(json.dumps(feedbacks_list))



def clean_int(line):

    return int(re.sub("[^0-9]", "", line))




def get_all_photo():
    with open(f'data/cards_url_list_www.bodo.ua.txt') as file:
        # lines = [line.strip() for line in file.readlines()]
        cards_url_list = json.loads(file.read())

    count = 0
    all_photo =[]

    print('fdf')
    for k in cards_url_list:
        photoes_list = []


        q = requests.get(k)
        result = q.content

        soup = BeautifulSoup(result, 'lxml')
        photoes = soup.find(class_='product-video__img js-experience-img').get('src')
        photoes_list.append(k)
        photoes_list.append(photoes)
        print(f'ok {count}')
        print(photoes_list)
        count +=1
        all_photo.append(photoes_list)




    print(all_photo)

    with open('data/all_photo_www.bodo.ua.txt', 'w') as file:
        file.write(json.dumps(all_photo))


def main_parser():

    with open(f'data/cards_url_list_www.bodo.ua.txt') as file:
        # lines = [line.strip() for line in file.readlines()]
        cards_url_list = json.loads(file.read())

    count = 0
    convert = 2.71

    all_main_info = []

    print('work')

    try:
        for k in cards_url_list:

            #cделать прослойку, проверить наличие файла

            url = k
            print(url)

            q = requests.get(url)
            result = q.content

            soup = BeautifulSoup(result, 'lxml')
            card_url = url
            card_name = soup.find(class_='product-video__headline').text
            card_name = re.sub(r"[\n]", "", card_name)
            card_price = soup.find(class_='price-list__item').get('data-price')
            card_price = re.sub(r"[\n]", "", card_price)
            card_price = float(card_price) * convert
            card_duration = soup.find(class_='price-list__item').get('data-duration')
            card_duration = re.sub(r"\n", "", card_duration)
            card_human_number = soup.find(class_='price-list__item').get('data-participants')
            card_human_number = re.sub(r"\n", "", card_human_number)
            card_description = soup.find(class_='product-description__text').text
            card_description = re.sub(r"\n", "", card_description)
            card_need_to_know = soup.find(class_='product-info__container').text
            card_need_to_know = re.sub(r"\n", "", card_need_to_know)
            card_meta = soup.find_all('meta')  # .find(name_='description')
            card_meta_description = 'None'
            card_meta_keywords = 'None'
            for meta in card_meta:
                meta_name = meta.get('name')
                if meta_name == 'description':
                    card_meta_description = meta.get('content')
                    card_meta_description = re.sub(r"\n", "", card_meta_description)
                else:
                    pass

                if meta_name == 'keywords':
                    card_meta_keywords = meta.get('content')
                    card_meta_keywords = re.sub(r"\n", "", card_meta_keywords)
                else:
                    pass

            print(f'юрл {card_url}\n название {card_name}\n цена {card_price}\n продолжительность {card_duration}\n кол-во людей {card_human_number}\n описание {card_description}\n доп. инфо {card_need_to_know}\n мета описание {card_meta_description}\n мета ключи {card_meta_keywords}')


            card_main_info = []
            card_main_info.append(card_url)  # 0
            card_main_info.append(card_name)  # 1
            card_main_info.append(card_price)  # 2
            card_main_info.append(card_duration)  # 3
            card_main_info.append(card_human_number)  # 4
            card_main_info.append(card_need_to_know)  # 5
            card_main_info.append(card_meta_description)  # 6
            card_main_info.append(card_meta_keywords)  # 7
            card_main_info.append(card_description)  # 8

            print(card_main_info)

            all_main_info.append(card_main_info)
            count += 1
            print(f'ok {count}')

    except Exception as ex:
        print(ex)

    print(all_main_info)

    with open('data/main_info_list_www.bodo.ua.txt', 'w') as file:
        file.write(json.dumps(all_main_info))




def meta():
    count = 0
    meta_data = []
    for k in urls:
        one_file_meta_data = []

        q = requests.get(k)
        result = q.content




        soup = BeautifulSoup(result, 'lxml')
        metas = soup.find_all('meta')
        meta_description = 'None'
        meta_keywords = 'None'
        for meta in metas:
            meta_name = meta.get('name')
            if meta_name == 'description':
                meta_description = meta.get('content')
            else:
                pass

            if meta_name == 'keywords':
                meta_keywords = meta.get('content')
            else:
                pass

        one_file_meta_data.append(k)
        one_file_meta_data.append(meta_description)
        one_file_meta_data.append(meta_keywords)
        print(one_file_meta_data)
        meta_data.append(one_file_meta_data)

        count +=1
        print(f'ok {count}')

    print(meta_data)


def need_to_know():
    count = 0
    need_to_know_data = []


    for k in urls:
        one_card_info = []

        q = requests.get(k)
        result = q.content

        soup = BeautifulSoup(result, 'lxml')
        info = soup.find_all(class_='product-info__item-text')
        #print(info)
        one_card_info.append(k)
        for i in range(0, len(info)):
            product = info[i].text

            one_card_info.append(product)
        need_to_know_data.append(one_card_info)
        count +=1

        print(one_card_info)
        print(f'ok {count}')

    print(need_to_know_data)

#main_parser()
#cards_url_list_get()
#get_all_photo()
#need_to_know()
feedbacks_list_get()
#meta()



