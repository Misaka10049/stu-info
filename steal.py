from threading import Thread, Lock, current_thread
import time
import requests
import os
url="https://oa.cqyz.cn/Web Services/student.asmx/NewStudents_Get2"
head={
	"method":"POST",
	"Content-Type": "application/json;utf-8"
}
body={
	"name":"",
	"noticeId":"HB"
}
body["name"]=input("学生姓名是：")
loop=1000
looplock=Lock()
found=False
def func():
	global loop,found
	while(not found):
		looplock.acquire()
		loop+=1
		body["noticeId"]="HB"+str(loop)
		print("[{}] 正在对比".format(current_thread().name)+body["noticeId"])
		looplock.release()
		res=requests.post(url,headers=head,data=str(body).encode("utf-8"))
		if res.json()["d"]["type"]!=None:
			found=True
			print("查询完成！用时："+str(time.time()-start)+"s")
			print(res.json())
			os.system("pause")
			break
pro=[]
start=time.time()
for i in range(0,20,1):
		pro.append(Thread(target=func,name=str(i)))
		pro[i].start()
