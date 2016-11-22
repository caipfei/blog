function check_register(){
	var username = $.trim($('#username').val())
	if (! username)
	{
		$('#username_error').html('用户名不能为空')
		return false
	}
	if (username.length<3)
	{
		$('#username_error').html('用户名不能少于3个字符')
		return false
	}
	if ($.isNumeric(username))
	{
		$('#username_error').html('用户名不能全为数字组成')
		return false
	}
	var nick = $.trim('#nick').val()
	if (! nick)
	{
		$('#nick_error').html('昵称不能为空')
		return false
	}
	if (nick.length<3)
	{
		$('#nick_error').html('昵称不能少于三个字符')
		return false
	}
	var password1 = $.trim($('#password1').val())
	if (! password1)
	{
		$('#password1_error').html('密码不能为空')
		return false
	}
	if (password1.length<6)
	{
		$('#password1_error').html('密码不能小于6个字符')
		return false
	}
	if ($.isNumeric(password1))
	{
		$('#password1_error').html('密码不能全为数字')
		return false
	}
	var password2 = $.trim($('#password2').val())
	if (password2 != password1)
	{
		$('#password2_error').html('两次输入的密码不一致')
		return false
	}
	var reg = new RegExp('^(.+?)@(.+?)\\.(.+?)$')
	var email = $.trim($('#email').val())
	if (！ email)
	{
		$('#email_error').html('邮箱不能为空')
		return false
	}
	if (! email.match(reg))
	{
		$('#email_error').html('邮箱格式不正确')
		return false
	}
}

var field = $('.field input')
var field_error = $('.field_error')
field.each(function(i){
	$(this).focus(function(){
		field_error.eq(i).html('')
	})
})

document.getElementById('username').onblur = function(){
	var username = this.value
	if (! username)
	{
		document.getElementById('username_error').innerHTML = '用户名不能为空'
	}
	else{
		var xhr
		if (window.XMLHttpRequest)
		{
			xhr = new XMLHttpRequest()
		}else{
			xhr = new ActiveXObject('Microsoft.XMLHTTP')	
		}
		xhr.onreadystatechange=function(){
			if (xhr.readyState==4 && xhr.status==200)
			{
				var result = JSON.parse(xhr.responseText)
				var exist = result['user_exist']
				if (exist == 'exist')
				{
					$('#username_error').html('该用户已存在')
				}
			}
		}
		var data = {'username':username}
		var csrftoken = getCookie('csrftoken')
		xhr.open('POST',"../check_user/",true)
		xhr.setRequestHeader('Content-type','application/json')
		xhr.setRequestHeader('X-CSRFToken',csrftoken)
		xhr.send(JSON.stringify(data))
	}
}


function getCookie(name) {  
    var cookieValue = null;  
    if (document.cookie && document.cookie != '') {  
        var cookies = document.cookie.split(';');  
        for (var i = 0; i < cookies.length; i++) {  
            var cookie = cookies[i].trim();  
            // Does this cookie string begin with the name we want?  
            if (cookie.substring(0, name.length + 1) == (name + '=')) {  
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));  
                break;  
            }  
        }  
    }  
    return cookieValue;  
}  



