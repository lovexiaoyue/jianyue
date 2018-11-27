var vm = new Vue({
    el: '#app',
    data: {
        host,
        username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        cart: [], // 购物车商品列表
        // 选择的商品总数量
        total_selected_count: 0,
        origin_input: 0 // 用于记录手动输入前的值
    },
    // 钩子[后执行]
    computed: {
        total_count: function(){
            var total = 0;
            for(var i=0; i<this.cart.length; i++){
                total += parseInt(this.cart[i].count);
                this.cart[i].amount = (parseFloat(this.cart[i].price) * parseFloat(this.cart[i].count)).toFixed(2);
            }
            return total;
        },
        total_selected_amount: function(){
            var total = 0;
            this.total_selected_count = 0;
            for(var i=0; i<this.cart.length; i++){
                if(this.cart[i].selected) {
                    total += (parseFloat(this.cart[i].price) * parseFloat(this.cart[i].count));
                    this.total_selected_count += parseInt(this.cart[i].count);
                }
            }
            return total.toFixed(2);
        },
        selected_all: function(){
            var selected=true;
            for(var i=0; i<this.cart.length; i++){
                if(this.cart[i].selected==false){
                    selected=false;
                    break;
                }
            }
            return selected;
        }
    },
    // 钩子[先执行]
    mounted: function(){
        // 获取购物车数据
        axios.get(this.host+'/carts/', {
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
                // 设置vue是否允许发送cookie，True表示允许
                withCredentials: true
            })
            .then(response => {
                this.cart = response.data;
                for(var i=0; i<this.cart.length; i++){
                    this.cart[i].amount = (parseFloat(this.cart[i].price) * this.cart[i].count).toFixed(2);
                }
            })
            .catch(error => {
                console.log(error.response.data);
            })
    },
    methods: {
        // 退出
        logout: function(){
            sessionStorage.clear();
            localStorage.clear();
            location.href = '/login.html';
        },
        // 减少操作
        on_minus: function(index){
            if (this.cart[index].count > 1) {
                var count = this.cart[index].count - 1;
                this.update_count(index, count);
            }
        },
        on_add: function(index){
            var count = this.cart[index].count + 1;
            this.update_count(index, count);
        },
        on_selected_all: function(){
            var selected = !this.selected_all;
            for (var i=0; i<this.cart.length;i++){
                this.cart[i].selected = selected;
            }
        },
        // 删除购物车数据
        on_delete: function(index){
            axios.delete(this.host+'/carts/', {
                    data: {
                        sku_id: this.cart[index].id
                    },
                    headers:{
                        'Authorization': 'JWT ' + this.token
                    },
                    responseType: 'json',
                    withCredentials: true
                })
                .then(response => {
                    this.cart.splice(index, 1);
                })
                .catch(error => {
                    console.log(error.response.data);
                })
        },
        on_input: function(index){
            var val = parseInt(this.cart[index].count);
            if (isNaN(val) || val <= 0) {
                this.cart[index].count = this.origin_input;
            } else {
                // 更新购物车数据
                axios.put(this.host+'/carts/', {
                        sku_id: this.cart[index].id,
                        count: val,
                        selected: this.cart[index].selected
                    }, {
                        headers:{
                            'Authorization': 'JWT ' + this.token
                        },
                        responseType: 'json',
                        withCredentials: true
                    })
                    .then(response => {
                        this.cart[index].count = response.data.count;
                    })
                    .catch(error => {
                        alert(error.response.data.message);
                        this.cart[index].count = this.origin_input;
                    })
            }
        },
        // 更新购物车数据
        update_count: function(index, count){
            axios.put(this.host+'/carts/', {
                    sku_id: this.cart[index].id,
                    count,
                    selected: this.cart[index].selected
                }, {
                    headers:{
                        'Authorization': 'JWT ' + this.token
                    },
                    responseType: 'json',
                    withCredentials: true
                })
                .then(response => {
                    this.cart[index].count = response.data.count;
                })
                .catch(error => {
                    alert(error.response.data.message);
                })
        },
        // 更新购物车数据
        update_selected: function(index) {
            axios.put(this.host+'/carts/', {
                    sku_id: this.cart[index].id,
                    count: this.cart[index].count,
                    selected: this.cart[index].selected
                }, {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    responseType: 'json',
                    withCredentials: true
                })
                .then(response => {
                    this.cart[index].selected = response.data.selected;
                })
                .catch(error => {
                    alert(error.response.data.message);
                })
        }
    }
});