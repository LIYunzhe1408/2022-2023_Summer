<template>
  <div>
    机构管理
    <el-row style="margin-top: 20px">
      <el-col :span="4" :offset="18">
        <el-button type="primary" @click="dialogNewInstitution=true">新增机构</el-button>
      </el-col>
    </el-row>
    <el-row style="margin-top: 20px">
      <el-col :span="20" :offset="2">
        <el-table :data="institutiontableData" stripe border style="width: 100%">
          <el-table-column prop="institutionName" label="机构名称" width="200"></el-table-column>
          <el-table-column prop="institutionDetail" label="机构描述" width="200"></el-table-column>
          <el-table-column
            label="机构状态"
            width="120">
            <template slot-scope="scope">
              <p  v-if="scope.row.inActive===activeStatus">已激活</p>
              <p  v-if="scope.row.inActive===inActiveStatus">已停用</p>
            </template>
          </el-table-column>
          <el-table-column
            fixed="right"
            label="操作"
            width="400">
            <template slot-scope="scope">
              <el-button @click="institutionManagers(scope.row)" type="text" size="small">查看机构管理员</el-button>
              <el-button @click="changeInstitutionDetail(scope.row)" type="text" size="small">编辑机构信息</el-button>
              <el-button @click="getInstitutionMenu(scope.row)" type="primary" size="mini">可访问模块</el-button>
              <el-button v-if="scope.row.inActive === activeStatus" @click="changeInstitutionStatus(scope.row)" type="primary" size="mini" :disabled="scope.row.institutionId==='0'">停用</el-button>
              <el-button v-if="scope.row.inActive === inActiveStatus" @click="changeInstitutionStatus(scope.row)"  size="mini" type="danger" :disabled="scope.row.institutionId==='0'">激活</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>


    <el-dialog title="机构管理员信息" :visible.sync="dialogManagersTableVisible" :modal=false>
      <el-button type="primary" @click="dialogNewManager=true">新增机构管理员</el-button>
      <el-table :data="managersData" height="250" border>
        <el-table-column property="loginNo" label="统一认证号" width="150"></el-table-column>
        <el-table-column property="userName" label="用户名" width="200"></el-table-column>
        <el-table-column label="状态" width="100">
          <template slot-scope="scope">
            <p  v-if="scope.row.userActive===activeStatus">已激活</p>
            <p  v-if="scope.row.userActive===inActiveStatus">已停用</p>
          </template>
        </el-table-column>
        <el-table-column
          fixed="right"
          label="操作"
          width="100">
          <template slot-scope="scope">
            <el-button v-if="scope.row.userActive === activeStatus" @click="changeUserStatus(scope.row)" type="primary" size="mini">停用</el-button>
            <el-button v-if="scope.row.userActive === inActiveStatus" @click="changeUserStatus(scope.row)"  size="mini" type="danger">激活</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
    <el-dialog title="修改机构信息" :visible.sync="dialogChangeInstitutionInfo" :modal=false>
      <el-form :model="formChangeInstitutionInfo">
        <el-form-item label="新机构信息" :label-width="formLabelWidth">
          <el-input v-model="formChangeInstitutionInfo.newInstitutionInfo" style="width: 80%"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="cID2">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="机构可访问模块信息" :visible.sync="dialogInstitutionMenuVisible" :modal=false>
      <el-tree
        :data="menuData"
        :check-strictly="true"
        ref="tree"
        show-checkbox
        node-key="order"
        :default-checked-keys="institutionMenu"
        :props="defaultProps">
      </el-tree>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogInstitutionMenuVisible=false">取 消</el-button>
        <el-button type="primary" @click="updateInstitutionMenu()">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="新增机构" :visible.sync="dialogNewInstitution" :modal=false>
      <el-form :model="formNewInstitution">
        <el-form-item label="新增机构名称" :label-width="formLabelWidth">
          <el-input v-model="formNewInstitution.institutionName" style="width: 80%"></el-input>
        </el-form-item>
        <el-form-item label="新增机构信息" :label-width="formLabelWidth">
          <el-input v-model="formNewInstitution.institutionDetail" style="width: 80%"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogNewInstitution=false">取 消</el-button>
        <el-button type="primary" @click="addNewInstitution()">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="新增机构管理员" :visible.sync="dialogNewManager" :modal=false>
      <el-form :model="formNewManager">
        <!--todo 统一认证号唯一校验-->
        <el-form-item label="统一认证号" :label-width="formLabelWidth">
          <el-input v-model="formNewManager.loginNo" style="width: 80%"></el-input>
        </el-form-item>
        <el-form-item label="用户名" :label-width="formLabelWidth">
          <el-input v-model="formNewManager.userName" style="width: 80%"></el-input>
        </el-form-item>
        <el-form-item label="默认密码" :label-width="formLabelWidth">
          <label>123456</label>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogNewManager=false">取 消</el-button>
        <el-button type="primary" @click="addNewManager()">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import ElRow from "element-ui/packages/row/src/row";
import ElCol from "element-ui/packages/col/src/col";

export default {
  components: {
    ElCol,
    ElRow},
  name: "InstitutionManage",
  data() {
    return {
      activeStatus:'1',
      inActiveStatus:'0',
      institutiontableData: [],
      dialogManagersTableVisible:false,
      dialogChangeInstitutionInfo:false,
      dialogNewInstitution:false,
      dialogNewManager:false,
      dialogInstitutionMenuVisible:false,
      managersData:[],
      formChangeInstitutionInfo:{
        newInstitutionInfo:'',
        institutionId:'',
      },
      formLabelWidth: '120px',
      formNewInstitution:{
        institutionName:'',
        institutionDetail:'',
      },
      formNewManager:{
        institutionStatus:'',
        institutionId:'',
        loginNo:'',
        userName:'',
      },
      menuData:[],
      institutionMenu:[],
      defaultProps:{
        children: 'children',
        label: 'name'
      },
      tmpUpdateInstitutionMenu:'',
    }
  },
  mounted:function () {
    this.getInstitutionInfo()
  },

  methods: {
    getInstitutionInfo() {
      let params={};
      this.$axios.post('/user/getInstitutionInfo',params).then(res => {
        if(res.data.code===1){
          let JsonParams=JSON.parse(res.data.data);
          this.institutiontableData=JsonParams;
        }else{
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })
    },
    getInstitutionMenu(row) {
      this.dialogInstitutionMenuVisible=true;
      this.tmpUpdateInstitutionMenu=row.institutionId;
      let params={
        institutionId:row.institutionId
      };
      this.$axios.post('/user/getInstitutionMenu',params).then(res => {
        if(res.data.code===1){
          let JsonParams=JSON.parse(res.data.data);
          this.menuData=JsonParams.menuData;
          this.institutionMenu=JsonParams.institutionMenu;
        }else{
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })
    },
    updateInstitutionMenu(){
//      console.log(this.$refs.tree.getCheckedKeys())
      let params={
        institutionId:this.tmpUpdateInstitutionMenu,
        newMenuList:this.$refs.tree.getCheckedKeys()
      };
      this.$axios.post('/user/updateInstitutionMenu',params).then(res => {
        if(res.data.code===1){
          this.$notify({
            title: '成功',
            message: res.data.msg,
            type: 'success'
          });
          this.dialogInstitutionMenuVisible=false;
        }else{
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })
    },
    institutionManagers(row) {
      this.formNewManager.institutionStatus=row.inActive;
      this.formNewManager.institutionId=row.institutionId;
      this.dialogManagersTableVisible=true;
      let params={institutionId:row.institutionId};
      this.$axios.post('/user/institutionManagers',params).then(res => {
        if(res.data.code===1){
          let JsonParams=JSON.parse(res.data.data);
          this.managersData=JsonParams;
        }else{
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })
    },
    changeInstitutionDetail(row) {
      this.formChangeInstitutionInfo.newInstitutionInfo=row.institutionDetail;
      this.formChangeInstitutionInfo.institutionId=row.institutionId;
      this.dialogChangeInstitutionInfo=true;
    },
    cID2() {
      let params={
        newInstitutionDetail: encodeURIComponent(this.formChangeInstitutionInfo.newInstitutionInfo),
        institutionId:this.formChangeInstitutionInfo.institutionId,
      };
      this.$axios.post('/user/changeInstitutionDetail',params).then(res => {
        if(res.data.code===1){
          this.$notify({
            title: '成功',
            message: res.data.msg,
            type: 'success'
          });
          // 表格数据修改,仅适用于较少数据
          let item;
          for(item in this.institutiontableData){
            if(this.institutiontableData[item].institutionId===this.formChangeInstitutionInfo.institutionId){
              this.institutiontableData[item].institutionDetail=this.formChangeInstitutionInfo.newInstitutionInfo;
              break;
            }
          }
          this.dialogChangeInstitutionInfo=false
        }else{
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })
    },
    changeInstitutionStatus(row) {
      let params={
        institutionId:row.institutionId,
        activeStatus:row.inActive,
      };
      this.$axios.post('/user/changeInstitutionStatus',params).then(res => {
        if(res.data.code===1){
          row.inActive=(row.inActive===this.inActiveStatus?this.activeStatus:this.inActiveStatus);
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
    addNewInstitution(){
      let params={
        institutionName: encodeURIComponent(this.formNewInstitution.institutionName),
        institutionDetail: encodeURIComponent(this.formNewInstitution.institutionDetail),
      };
      this.$axios.post('/user/addNewInstitution',params).then(res => {
        if(res.data.code===1){
          this.getInstitutionInfo()
          this.$notify({
            title: '成功',
            message: res.data.msg,
            type: 'success'
          });
          this.dialogNewInstitution=false;
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
      if(this.formNewManager.institutionStatus===this.inActiveStatus){
        this.$notify({
          title: '警告',
          message: '请先激活当前机构',
          type: 'warning'
        });
      }else{
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
      }
    },
    addNewManager(){
      let params={
        loginNo: this.formNewManager.loginNo,
        userName: encodeURIComponent(this.formNewManager.userName),
        institutionId: this.formNewManager.institutionId,
        institutionStatus: this.formNewManager.institutionStatus,
      };
      this.$axios.post('/user/addNewManager',params).then(res => {
        if(res.data.code===1){
          this.$notify({
            title: '成功',
            message: res.data.msg,
            type: 'success'
          });
          this.dialogNewManager=false;
          this.dialogManagersTableVisible=false;
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
