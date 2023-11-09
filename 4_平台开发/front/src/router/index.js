import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Login from '@/view/systemPage/Login.vue'
import Home from '@/view/systemPage/Home.vue'
import HomePage from '@/view/systemPage/HomePage.vue'
import InstitutionManage from '@/view/systemPage/InstitutionManage.vue'
import MenuManage from '@/view/systemPage/MenuManage.vue'
import OPManage from '@/view/systemPage/OPManage.vue'
import UserManage from '@/view/systemPage/UserManage.vue'
import UserInfo from '@/view/systemPage/UserInfo.vue'
import LogInfo from '@/view/systemPage/LogInfo.vue'
import AddPatent from '@/view/demo/AddPatent.vue'
import PatentInfo from '@/view/demo/PatentInfo.vue'
import RE from '@/view/demo/RelationExtract.vue'
import EE from '@/view/demo/PipelineControl.vue'


Vue.use(Router)

export default new Router({
  // mode: 'history',    //此行注释掉即hash模式 不用配置base
  // base:'/api',      // 配置单页应用的基路径 用history时与后端联合配置，打包history模式时用
  routes: [
    {
      path: '/HelloWorld',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '/home',
      name: 'Home',
      component: Home,
      children:[
        {
          path: '/homePage',
          name: '首页',
          component: HomePage,
        },
        {
          path: '/institutionManage',
          name: '机构管理',
          component: InstitutionManage,
        },
        {
          path: '/opManage',
          name: '操作管理',
          component: OPManage,
        },
        {
          path: '/menuManage',
          name: '菜单管理',
          component: MenuManage,
        },
        {
          path: '/userManage',
          name: '用户管理',
          component: UserManage,
        },
        {
          path: '/userInfo',
          name: '用户信息',
          component: UserInfo,
        },
        {
          path: '/logInfo',
          name: '系统日志',
          component: LogInfo,
        },
        // 子页面路由
        {
          path: '/addPatent',
          name: '专利新增',
          component: AddPatent,
        },
        {
          path: '/patentInfo',
          name: '专利信息',
          component: PatentInfo,
        },
        {
          path: '/relationExtract',
          name: '关系抽取',
          component: RE,
        },
        {
          path: '/pipelineControl',
          name: 'PipelineControl',
          component: EE,
        }
      ]
    }
  ]
})
