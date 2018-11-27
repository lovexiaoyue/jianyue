var vm = new Vue({
	el: '#app',
	data: {
		host:host, // 在host.js中统一配置一个后端服务器的地址，实现一改全改
		// 表单字段的错误状态[false表示没有错误]
		error_name: false,
		error_password: false,
		error_check_password: false,
		error_phone: false,
		error_allow: false,
		error_image_code: false,
		error_sms_code: false,

		// 表单字段值[默认没有填写]
		username: '',
		password: '',
		password2: '',
		mobile: '', 
		image_code: '',     // 用户填写的图片验证码
		image_code_url: '', // 图片url地址
        image_code_uuid: '',// 图片编号
		sms_code: '',
		allow: false,

        // 错误提示
        error_image_code_message: "请填写图片验证码",
        error_name_message:"请输入5-20个字符的用户",
        sending_flag:false, // 表示是否发送了短信验证码
        sms_code_tip:"获取短信验证码", // 倒计时提示
	},
    mounted: function () {
	    // 生成图片验证码
        this.generate_code_url();
    },
	methods: {
		// 生成图片验证码的图片地址
		generate_code_url: function(){
			// 拼接后端接口提供的url地址
            this.image_code_uuid = this.generate_uuid();
            this.image_code_url = this.host + "/image_codes/" + this.image_code_uuid + "/" ;
		},

        // 生成uuid
		generate_uuid: function(){
			var d = new Date().getTime();
			if(window.performance && typeof window.performance.now === "function"){
				d += performance.now(); //use high-precision timer if available
			}
			var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
				var r = (d + Math.random()*16)%16 | 0;
				d = Math.floor(d/16);
				return (c =='x' ? r : (r&0x3|0x8)).toString(16);
			});
			return uuid;
		},
		// 发送短信
        send_sms: function(){
		    // 校验下是否填写手机号码
            this.check_phone();
            this.check_image_code();

            if( this.error_phone || this.error_image_code ){ // 如果error_phone为true表示有错误
                return;
            }

            // 判断是否有发送短信
            if( this.sending_flag == true ){ // True表示发送
                return;
            }

			// 使用axios发送get请求
			url = this.host + "/sms_codes/" + this.mobile + "/?image_code_id=" + this.image_code_uuid + "&text=" + this.image_code
			axios.get(url).then(response=>{
                this.sending_flag = true; // 表示60秒内发送了短信
			    // 表示后端发送短信成功
                // 倒计时60秒，60秒后允许用户再次点击发送短信验证码的按钮
                var num = 60;
                // 设置一个计时器
                var t = setInterval(() => {
                    // console.log(num);
                    if (num == 1) {
                        // 如果计时器到最后, 清除计时器对象
                        clearInterval(t);
                        // 将点击获取验证码的按钮展示的文本回复成原始文本
                        this.sms_code_tip = '获取短信验证码';
                        // 将点击按钮的onclick事件函数恢复回去
                        this.sending_flag = false;
                    } else {
                        num -= 1;
                        // 展示倒计时信息
                        // console.log(this)
                        this.sms_code_tip = num + '秒';
                    }
                }, 1000)


			}).catch(error=>{
			    // 响应状态码
                if (error.response.status == 400) {
                    this.error_image_code_message = '图片验证码有误';
                    this.error_image_code = true;
                } else {
                    console.log(error.response.data);
                }
                this.sending_flag = false;
			});
        },
		check_username: function (){
			var len = this.username.length;
			if(len<5||len>20) {
				this.error_name = true;
			} else {
				this.error_name = false;
			}

			if(this.error_name == false){
				// 校验账号的唯一性
				axios.get(this.host + "/usernames/"+ this.username + "/count/",{
				    responseType: "json",
                }).then(response => {
						if (response.data.count > 0) {
							this.error_name_message = '用户名已存在';
							this.error_name = true;
						} else {
							this.error_name = false;
						}
					})
					.catch(error => {
						console.log(error.response.data);
					})

			}

		},
		check_pwd: function (){
			var len = this.password.length;
			if(len<8||len>20){
				this.error_password = true;
			} else {
				this.error_password = false;
			}		
		},
		check_cpwd: function (){
			if(this.password!=this.password2) {
				this.error_check_password = true;
			} else {
				this.error_check_password = false;
			}		
		},
		check_phone: function (){
			var re = /^1[345789]\d{9}$/;
			if(re.test(this.mobile)) {
				this.error_phone = false;
			} else {
				this.error_phone = true;
			}
		},
		check_image_code: function (){
			if(!this.image_code) {
				this.error_image_code = true;
			} else {
				this.error_image_code = false;
			}	
		},
		// 短信验证码
		check_sms_code: function(){
			if(!this.sms_code){
				this.error_sms_code = true;
			} else {
				this.error_sms_code = false;
			}
		},
		check_allow: function(){
			if(!this.allow) {
				this.error_allow = true;
			} else {
				this.error_allow = false;
			}
		},
		// 注册
		on_submit: function(){
			this.check_username();
			this.check_pwd();
			this.check_cpwd();
			this.check_phone();
			this.check_sms_code();
			this.check_allow();

			if(this.error_name == false && this.error_password == false && this.error_check_password == false
				&& this.error_phone == false && this.error_sms_code == false && this.error_allow == false) {
				axios.post(this.host+'/users/', {
						username: this.username,
						password: this.password,
						password2: this.password2,
						mobile: this.mobile,
						sms_code: this.sms_code,
						allow: this.allow.toString()
					}, {
						responseType: 'json'
					})
					.then(response => {
					    // 注册成功以后，默认当前新用户已经登陆了。
                        // console.log(response.data)
						// 保存后端返回的token数据
						localStorage.token = response.data.token;
						localStorage.username = response.data.username;
						localStorage.user_id = response.data.id;

                        // 跳转到用户中心
						location.href = '/user_center_info.html';
					})
					.catch(error=> {
						if (error.response.status == 400) {
							this.error_sms_code_message = '短信验证码错误';
							this.error_sms_code = true;
						} else {
							console.log(error.response.data);
						}
					})
			}

		}
	}
});
