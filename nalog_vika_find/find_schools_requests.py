#!/usr/bin/python

import requests
import pandas as pd
import time
import pprint

#Settings to change
number_of_results = 3
sleepBetweenRequests = 1

#Settings not to change
headers = {
    'Host': 'egrul.nalog.ru',
}
url1 = 'https://egrul.nalog.ru'                     #URL, по которому обращаться с POST запросом для генерации результатов поиска
url2 = 'https://egrul.nalog.ru/search-result/'      #URL, по которому можно получить результаты поиска

#Функция, реализующяя, собственно, обращение
def search(query: str):
    r = requests.post(url1, headers=headers, data={'query': query, 'region': 77})
    result_id = r.json()['t']
    print(r)
    time.sleep(sleepBetweenRequests)
    result = requests.get(url2+result_id).json()['rows']
    list_to_return = []
    for entity in result[0:number_of_results]:
        list_to_return.append(
                {
                    'query': query,
                    'school_name': entity['n'],
                    'school_name2': entity['c'],
                    'director': entity['g']
                    }
                )
    return list_to_return


def main():
    results = []
    onelist = []
    pp = pprint.PrettyPrinter()
    with open('schools.txt') as file:
        schools = file.read().splitlines()
    for school in schools:
        results.append(search(school))
    for result in results:
        onelist += [*result]

    frame = pd.DataFrame(onelist)
    # print(frame)
    frame.to_excel (r'schools_nalog.xlsx')

if __name__ == "__main__":
    main()

