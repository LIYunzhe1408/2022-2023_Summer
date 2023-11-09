// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import ElementUI from 'element-ui' //新添加
import echarts from "echarts";
import 'element-ui/lib/theme-chalk/index.css' //新添加，避免后期打包样式不同，要放在import App from './App';之前
import Vue from 'vue'
import App from './App'
import router from './router'  // 导入router
import axios from 'axios'
// import VueAxios from 'vue-axios'
import md5 from 'js-md5';
import VueResource from 'vue-resource'
import Viewer from "v-viewer"
import 'viewerjs/dist/viewer.css'

Vue.use(VueResource);
Vue.use(ElementUI);   //新添加，所有组件全局注册
Vue.use(Viewer);
axios.defaults.baseURL = '/api';  //vue文件里加了api就不用了
Vue.prototype.$md5 = md5;
Vue.prototype.$axios = axios;  //  不用做导入了，直接用this.$axios
Vue.prototype.$echarts = echarts;
Vue.config.productionTip = false;
axios.defaults.withCredentials = true; //请求发送cookie
Viewer.setDefaults({
  Options:{
    'inline': true,
    'button': true,
    'navbar': true,
    'title': true,
    'toolbar': true,
    'tooltip': true,
    'movable': true,
    'zoomable': true,
    'rotatable': true,
    'scalable': true,
    'transition': true,
    'fullscreen': true,
    'keyboard': true,
    'url': 'data-source'
  }
})
//请求拦截器
axios.interceptors.request.use(request=>{
  return request   //请求拦截器成功时返回值
},err=>{
  this.$notify.error({
    title: '错误',
    message: '系统异常，请重试或联系管理员'
  });
  return Promise.reject(err)   //请求错误时通过该方法返回配置信息
});

//响应拦截器
axios.interceptors.response.use(response =>{
  // 在接收响应做些什么，例如跳转到登录页
  if(response.data.code ===0 ||  response.data.code ===2){
    router.push({
      path:"/login",
      // querry:{redirect:router.currentRoute.fullPath}//从哪个页面跳转
    })
  }
  return response;
}, error => {
  // 对响应错误做点什么
  this.$notify.error({
    title: '错误',
    message: '系统异常，请重试或联系管理员'
  });
  // error是http状态4xx、5xx的响应结果，错误响应对象是error.response，错误响应数据是error.response.data，响应的数据就是一个页面，但是页面不一定要渲染出来
  return Promise.reject(error);
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
