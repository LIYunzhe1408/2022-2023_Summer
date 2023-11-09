<template xmlns:cursor="http://www.w3.org/1999/xhtml">
  <el-container class="container">
    <el-header class="header">
      <el-row>
        <el-col :span="4">
          <div class="logo">
            <img src="../../assets/logo.png" alt="logo" @click="toHomePage()">
            </img>
          </div>
        </el-col>
        <el-col :span="14">
          <el-menu class="el-menu-new" mode="horizontal">
            <el-submenu  class="el-submenu-new" :index="item.order" :key="item.order" v-for="item in menuData">
                <div slot="title" class="el-menu-title">{{item.name}}</div>
                <el-menu-item :index="item2.order" v-for="item2 in item.children" :key="item2.order" @click="changePage(item2.path)">{{item2.name}}</el-menu-item>
            </el-submenu>
          </el-menu>
        </el-col>
        <el-col :span="6">
          <div class="rightsection">
            <span class="clickstyle" @click="signOut">退出</span>
          </div>
        </el-col>
      </el-row>
    </el-header>
    <el-main style="height:0; flex-grow:1; padding:0">
       <el-row >
         <el-col :span="20" :offset="2" style="margin-top:50px">
           <router-view></router-view>
         </el-col>
       </el-row>
    </el-main>
        <el-footer height="40px" color="fff" opacity="0.0">
          <div style="text-align: right;margin-top: 10px">liyunzhe903@gmail.com</div>
        </el-footer>
  </el-container>
</template>



<script>
export default {
  name: "Home",
  data () {
    return {
      menuData: [],
      //      menuData: [
      //        {
      //          name: "系统管理",
      //          order: "1",
      //          path:'',
      //          children: [
      //            {
      //              name: "机构管理",
      //              order: "11",
      //              path:'/institutionManage',
      //            },
      //            {
      //              name: "用户管理",
      //              order: "12",
      //              path:'/userManage',
      //            },
      //            {
      //              name: "用户信息",
      //              order: "13",
      //              path:'/userInfo',
      //            },
      //            {
      //              name: "系统日志",
      //              order: "14",
      //              path:'/logInfo',
      //            },
      //          ],
      //        },
      //        {
      //          name: "业务管理",
      //          order: "2",
      //          path:'',
      //          children: [
      //            {
      //              name: "样例1",
      //              order: "21",
      //              path:'/demo1',
      //            },
      //          ],
      //        },
      //      ],
      userData: {},
      userName: '',
      isShow: []
    }
  },
  created(){
      this.changePage('/')
  },
  mounted: function () {
    this.getMenuTree();
    this.getUserInfo();
    this.$router.push({ path: "/homePage" });
  },
  methods: {
    changePage(path){
      this.$router.replace(path)
    },
    toHomePage () {
      this.$router.push({ path: "/homePage" });
    },
    signOut () {
      this.$confirm("退出登录, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).then(() => {
        let params = {};
        this.$axios.post('/user/signOut', params).then(res => {
          if (res.data.code === 1) {
            this.$router.push({ path: "/login" });
          } else {
            this.$notify({
              title: '警告',
              message: res.data.msg,
              type: 'warning'
            });
          }
        })
      });
    },
    getMenuTree () {
      //      this.menuData=[{order: "3",name: "研究生入学测试",children: [{name: "回归",order: "31",path: "/regression"},{name: "聚类",order: "32",path: "/clustering"}]}]
      let params = {
        //        loginNo: localStorage.getItem("loginNo"),
      };
      this.$axios.post('/user/getMenuData', params).then(res => {
        let this_ = this
        if (res.data.code === 1) {
          this_.menuData = JSON.parse(res.data.data);
          this_.isShow.length = this_.menuData.length
          for(let i=0; i < this_.menuData.length; i++){
            this_.isShow[i] = false
          }
        } else {
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })

      //        .catch(error => {
      //        this.$notify.error({
      //          title: '错误',
      //          message: '系统异常，请重试或联系管理员'
      //        });
      //        // error是http状态4xx、5xx的响应结果，错误响应对象是error.response，错误响应数据是error.response.data，响应的数据就是一个页面，但是页面不一定要渲染出来
      //      })
    },
    getUserInfo () {
      let params = {};
      this.$axios.post('/user/getUserInfo', params).then(res => {
        if (res.data.code === 1) {
          this.userData = JSON.parse(res.data.data);
          this.userName = this.userData.userName;
        } else {
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })
    },
    goBack () {
      if (window.history.length > 1) {
        this.$router.go(-1);
      }
    },
    showSubmenu(index, flag){
      this.isShow[index] = flag
    }
  }
}
</script>



<style>
.container {
  height: 100%;
  font-size: 15px;
  background-color: #f6eee8;
}
.header {
  color: #f6eee8;
  position: relative;
  width: 100%;
  height: 104px !important;
  background-image: url('../../assets/head.jpg');
}
.el-main {
  height: 100%;
  background-color: transparent;
}
.logo {
  position: absolute;
  top: 22px;
  left: 100px;
  width: 290px;
  height: 60px;
}
.logo img {
  width: 100%;
  height: 100%;
}
.el-menu-new {
  position: fixed;
  top: 82px;
  right: 30%;
  height: 20px;
  background-color: transparent;
  border-bottom: none;
}
.el-submenu-new {
  height: 20px;
  width: 100px;
}

.el-menu--horizontal>.el-submenu .el-submenu__title{
  height: 20px;
  line-height: 20px;
  text-align: center;
}

.el-submenu__title i {
  display: none;
}

.el-submenu__title {
  background-image: url('../../assets/navUnin.png');
  background-size: 100px;
}

.el-submenu__title:hover {
  background-color: transparent;
  background-image: url('../../assets/navIn.png');
  background-size: 100px;
}

.el-menu--horizontal .el-menu {
  width: 100px;
  margin-top: -5px;
  background-color: transparent;
  border: none;
  box-shadow: none;
}

.el-menu--horizontal .el-menu .el-menu-item, .el-menu--horizontal .el-menu .el-submenu__title {
  padding: 0;
  width: 100px;
  height: 20px;
  line-height: 20px;
  font-size: 14px;
  text-align: center;
  background-color: #fff;
  border: 1px solid #eee;
}
.el-menu-title {
  background-color: transparent;
}
.el-menu--horizontal .el-menu .el-menu-item:hover {
  background-color: #ecf5ff;
}
.el-menu--horizontal>.el-menu-item:not(.is-disabled):focus, .el-menu--horizontal>.el-menu-item:not(.is-disabled):hover, .el-menu--horizontal>.el-submenu .el-submenu__title:hover{
}
.el-menu--horizontal>.el-submenu .el-submenu__title {
  background-color: transparent;
  color: #303133;
}
.el-menu--horizontal>.el-submenu .el-submenu__title:hover {
  background-color: transparent;
}

.el-menu-item, .el-submenu__title{
  padding: 0;
  height: 20px;
  line-height: 20px;
}


.rightsection {
  position: absolute;
  right: 0;
  top: 20px;
  line-height: 103px;
  text-align: center;
}
.rightsection span {
  padding: 0 20px;
}
.clickstyle {
  font-size: 12px;
  cursor: pointer;
}
</style>
