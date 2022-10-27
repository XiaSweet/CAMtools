function gettime() {
	$.ajax({
		url: '/gettime', //从gettime这个视图函数获取数据，一会编写
		type: 'post' , //采用get方法
		timeout: 10000, //超时时间设置为10秒
		success: function(t) { //成功之后的结果，这里的t是从'/gettime'视图函数获得的返回值，如果返回值有多个，可以用json
			$('#timenow').html("当前时间为" + t) //用“当前时间为：t”代替timenow也就是上面的“当前时间?"
		}
	});
} 
function connect_devices() {
	$.ajax({
		url: '/devices',
		//从gettime这个视图函数获取数据，一会编写
		type: 'post',
		//采用get方法
		timeout: 10000,
		//超时时间设置为10秒
		success: function(t) { //成功之后的结果，这里的t是从'/gettime'视图函数获得的返回值，如果返回值有多个，可以用json
			if (t === "0") {
				$('#connect_devices').html("ADB设备还没有链接，客官请先喝口茶(＞﹏＜)"),
				$('#con_devices_len').html(t)
			} else {
				$('#con_devices_len').html(t),
				$('#connect_devices').html("温馨提示：当前链接的设备是" + t + "台") //用“当前时间为：t”代替timenow也就是上面的“当前时间?"
			}
		}
	});
}
setInterval(connect_devices, 2985) //每3秒刷新一次
function exist(id){
	var s=document.getElementById(id);
	if(s){
	return true
	}
	else{
	return false
}
}
function get_localip(deviceid,ysid) {
	$.ajax({
		url: '/devices/'+deviceid+'/localip/',
		//deviceid动态变量获取ip
		type: 'post',
		//采用post方法
		timeout: 10000,
		//超时时间设置为10秒
		success: function(t) { //成功之后的结果，这里的t是从'/gettime'视图函数获得的返回值，如果返回值有多个，可以用json
			if (t === "False") {
				$('#'+ysid).html("咩有联网"),
				console.info(ysid+"：IP似乎没有链接")
			} else {
				$('#'+ysid).html(t),
				console.info(deviceid+"的本地IP地址："+t)
			}
		}
	});
}