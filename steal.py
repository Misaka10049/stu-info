import requests
import json
import asyncio
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'application/json',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=,0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json;utf-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Length': '34',
    'Origin': 'https://oa.cqyz.cn',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://oa.cqyz.cn/ns/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'TE': 'trailers',
}
n = 2
name = ""
task_list = []
url = "https://oa.cqyz.cn/Web%20Services/student.asmx/NewStudents_Get2"
finded_id = ''


async def find_id(name, start_num, end_num):
    global finded_id
    for num in range(start_num, end_num):
        id = 'HB{}'.format(str(num))
        post_json = json.dumps({'name': name, 'noticeId': id})
        response = requests.post(url=url, headers=headers, data=post_json)
        content = response.text
        if "Error" not in content:
            if "safedog" not in content:
                finded_id = id
                raise ValueError(id)
            elif "JumpSelf" in content:
                finded_id = "blocked"
                raise ValueError("blocked")
            else:
                finded_id = "blocked"
                raise ValueError("blocked")
        print(str(start_num)+": "+id)


async def main():
    for i in range(0, n):
        start_num = 1000+9000//n*i
        task = find_id(name, start_num, start_num+9000//n)
        task_list.append(asyncio.ensure_future(task))
    if 9000 % n != 0:
        last_task = find_id(name, 9999-9000 % n+1, 9999)
        task_list.append(asyncio.ensure_future(last_task))
    results = await asyncio.wait(task_list, return_when=asyncio.FIRST_EXCEPTION)
    print(finded_id)
    print("main finish")
if __name__ == '__main__':
    asyncio.run(main())
