var vm = new Vue({
    el: '#app',
    data: {
        host: host,
        error_username: false,
        error_pwd: false,
        error_pwd_message: '请填写密码',
        username: '',
        password: '',
        remember: false
    },
    methods: {
        // 获取url路径中查询字符串里面的指定名称的值
        get_query_string: function(name){ // name = "next"
            var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
            // window.location.search 获取地址栏上面的查询字符串
            var r = window.location.search.substr(1).match(reg);
            if (r != null) {
                return decodeURI(r[2]);
            }
            return null;
        },
        // 检查数据
        check_username: function(){
            if (!this.username) {
                this.error_username = true;
            } else {
                this.error_username = false;
            }
        },
        check_pwd: function(){
            if (!this.password) {
                this.error_pwd_message = '请填写密码';
                this.error_pwd = true;
            } else {
                this.error_pwd = false;
            }
        },
        // 表单提交
        on_submit: function(){
            this.check_username();
            this.check_pwd();

            if (this.error_username == false && this.error_pwd == false) {
                axios.post(this.host+'/authorizations/', {
                        username: this.username,
                        password: this.password
                    }, {
                        responseType: 'json',
                        // 设置vue.js附带cookie
                        withCredentials: true,
                    })
                    .then(response => {
                        // 使用浏览器本地存储保存token
                        if (this.remember) {
                            // 记住登录
                            sessionStorage.clear();
                            localStorage.token = response.data.token;
                            localStorage.user_id = response.data.user_id;
                            localStorage.username = response.data.username;
                        } else {
                            // 未记住登录
                            localStorage.clear();
                            sessionStorage.token = response.data.token;
                            sessionStorage.user_id = response.data.user_id;
                            sessionStorage.username = response.data.username;
                        }

                        // 跳转页面
                        var return_url = this.get_query_string('next');
                        if (!return_url) {
                            return_url = '/index.html';
                        }
                        // 页面跳转
                        location.href = return_url;
                    })
                    .catch(error => {
                        this.error_pwd_message = '用户名或密码错误';
                        this.error_pwd = true;
                    })
            }
        },
        // QQ登陆
        qq_login: function(){
            // 把地址栏上面的next参数获取到
            var state = this.get_query_string('next') || '/';
            // 发送get请求，获取qq登陆地址
            axios.get(this.host + '/oauth/qq/authorization/?next=' + state, {
                    responseType: 'json'
                })
                .then(response => {
                    // 获取到地址，跳转到qq登陆页面
                    location.href = response.data.auth_url;
                })
                .catch(error => {
                    console.log(error.response.data);
                })
        }
    }
});