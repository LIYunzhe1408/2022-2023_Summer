<template>
  <div>
    用户管理
    <el-row style="margin-top: 20px">
      <el-col :span="4" :offset="18">
        <el-button type="primary" @click="dialogNewUser=true">新增用户</el-button>
      </el-col>
    </el-row>
    <el-row style="margin-top: 20px">
      <el-col :span="20" :offset="2">
        <el-table :data="usersData" stripe border style="width: 100%">
          <el-table-column property="loginNo" label="统一认证号" width="200"></el-table-column>
          <el-table-column property="userName" label="用户名" width="200"></el-table-column>
          <el-table-column label="状态" width="200">
            <template slot-scope="scope">
              <p  v-if="scope.row.userActive===activeStatus">已激活</p>
              <p  v-if="scope.row.userActive===inActiveStatus">已停用</p>
            </template>
          </el-table-column>
          <el-table-column
            fixed="right"
            label="操作"
            width="200">
            <template slot-scope="scope">
              <el-button @click="getUserMenu(scope.row)" type="text" size="small">可访问模块</el-button>
              <el-button v-if="scope.row.userActive === activeStatus" @click="changeUserStatus(scope.row)" type="primary" size="mini">停用</el-button>
              <el-button v-if="scope.row.userActive === inActiveStatus" @click="changeUserStatus(scope.row)"  size="mini" type="danger">激活</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>
    <el-dialog title="新增用户" :visible.sync="dialogNewUser" :modal=false>
      <el-form :model="formNewUser">
        <!--todo 统一认证号唯一校验-->
        <el-form-item label="统一认证号" :label-width="formLabelWidth">
          <el-input v-model="formNewUser.loginNo" style="width: 80%"></el-input>
        </el-form-item>
        <el-form-item label="用户名" :label-width="formLabelWidth">
          <el-input v-model="formNewUser.userName" style="width: 80%"></el-input>
        </el-form-item>
        <el-form-item label="默认密码" :label-width="formLabelWidth">
          <label>123456</label>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogNewUser=false">取 消</el-button>
        <el-button type="primary" @click="addNewUser()">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="用户可访问模块信息" :visible.sync="dialogUserMenuVisible" :modal=false>
      <el-tree
        :data="institutionMenu"
        :check-strictly="true"
        ref="treeUser"
        show-checkbox
        node-key="order"
        :default-checked-keys="userMenu"
        :props="defaultProps">
      </el-tree>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogUserMenuVisible=false">取 消</el-button>
        <el-button type="primary" @click="updateUserMenu()">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "UserManage",
  data() {
    return {
      activeStatus:'1',
      inActiveStatus:'0',
      formLabelWidth: '120px',
      usersData: [],
      dialogNewUser:false,
      dialogUserMenuVisible:false,
      formNewUser:{
        loginNo:'',
        userName:'',
      },
      institutionMenu:[],
      userMenu:[],
      defaultProps:{
        children: 'children',
        label: 'name'
      },
      tmpUpdateUserMenu:'',
    }
  },
  mounted:function () {
    this.getUserList()
  },
  methods: {
    getUserList() {
      let params={};
      this.$axios.post('/user/getUserList',params).then(res => {
        if(res.data.code===1){
          let JsonParams=JSON.parse(res.data.data);
          this.usersData=JsonParams;
        }else{
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })
    },
    addNewUser(){
      let params={
        loginNo: this.formNewUser.loginNo,
        userName: encodeURIComponent(this.formNewUser.userName),
      };
      this.$axios.post('/user/addNewUser',params).then(res => {
        if(res.data.code===1){
          this.getUserList();
          this.$notify({
            title: '成功',
            message: res.data.msg,
            type: 'success'
          });
          this.dialogNewUser=false;
        }else{
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })
    },
    getUserMenu(row) {
      this.dialogUserMenuVisible=true;
      this.tmpUpdateUserMenu=row.loginNo;
      let params={
        loginNo:row.loginNo
      };
      this.$axios.post('/user/getUserMenu',params).then(res => {
        if(res.data.code===1){
          let JsonParams=JSON.parse(res.data.data);
          this.institutionMenu=JsonParams.institutionMenu;
          this.userMenu=JsonParams.userMenu;
        }else{
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })
    },
    updateUserMenu(){
      let params={
        loginNo:this.tmpUpdateUserMenu,
        newMenuList:this.$refs.treeUser.getCheckedKeys()
      };
      this.$axios.post('/user/updateUserMenu',params).then(res => {
        if(res.data.code===1){
          this.$notify({
            title: '成功',
            message: res.data.msg,
            type: 'success'
          });
          this.dialogUserMenuVisible=false;
        }else{
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })
    },
    changeUserStatus(row) {
        let params={
          loginNo:row.loginNo,
          activeStatus:row.userActive,
        };
        this.$axios.post('/user/changeUserStatus',params).then(res => {
          if(res.data.code===1){
            row.userActive=(row.userActive===this.inActiveStatus?this.activeStatus:this.inActiveStatus);
            this.$notify({
              title: '成功',
              message: res.data.msg,
              type: 'success'
            });
          }else{
            this.$notify({
              title: '警告',
              message: res.data.msg,
              type: 'warning'
            });
          }
        })

    },
  },
}
</script>

<style scoped>

</style>
