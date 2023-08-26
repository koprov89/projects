#!/usr/bin/python
import json
import time
import pprint
import pandas as pd
from aiohttp import ClientSession, ClientTimeout
import asyncio

headers = {
    'Host': 'egrul.nalog.ru',
    # 'Origin': 'https://egrul.nalog.ru'
    # 'Referer: https://egrul.nalog.ru/index.html'
}

url1 = 'https://egrul.nalog.ru'
url2 = 'https://egrul.nalog.ru/search-result/'

async def search(query: str, session: ClientSession):
    async with session.request('POST', url1, headers=headers, data={'query': query, 'region': 77}) as response:
        r = await response.json()
        print(r)
        result_id = r['t']
        await asyncio.sleep(1)
    async with session.request('GET', url2+result_id, headers=headers) as response:
        result = (await response.json())['rows']
    # print(result)
    list_to_return = []
    for entity in result[0:3]:
        list_to_return.append(
                {
                    'query': query,
                    'school_name': entity['n'],
                    'school_name2': entity['c'],
                    'director': entity['g']
                    }
                )
    formatted_result = {
            query: result
            }
    # return formatted_result
    return list_to_return


async def multiple_requests(schools: list):
    async with ClientSession() as session:
        results = []
        onelist = []
        for i in range(0,len(schools), 1):
            tasks = []
            for school in schools[i:i+1]:
                task = asyncio.create_task(search(school, session))
                tasks.append(task)
            results.extend(await asyncio.gather(*tasks))
            time.sleep(1)
        for result in results:
            onelist+=[*result]
    return onelist

async def main():
    pp = pprint.PrettyPrinter()
    with open('schools.txt') as file:
        schools = file.read().splitlines()
    result = await multiple_requests(schools)
    frame = pd.DataFrame(result)
    print(frame)
    frame.to_excel (r'exported.xlsx')
    # pp.pprint(result)

if __name__ == "__main__":
    asyncio.run(main())





