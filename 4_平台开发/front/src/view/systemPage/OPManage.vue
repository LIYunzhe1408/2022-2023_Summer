<template>
  <div>
    操作管理
    <el-row style="margin-top: 20px">
      <el-col :span="4" :offset="18">
        <el-button type="primary" @click="dialogNewOP=true">新增操作条目</el-button>
      </el-col>
    </el-row>
    <el-row style="margin-top: 20px">
      <el-col :span="20" :offset="2">
        <el-table :data="OPData.slice((this.currentPage-1)*this.pageSize,this.currentPage*this.pageSize)" stripe border style="width: 100%">
          <el-table-column prop="opURL" label="操作url" width="200"></el-table-column>
          <el-table-column label="操作归属模块" width="200">
            <template slot-scope="scope">
              <p  v-if="scope.row.opType==='user'">系统管理</p>
            </template>
          </el-table-column>
          <el-table-column prop="opDescribe" label="操作描述"></el-table-column>
        </el-table>
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[5, 10, 20, 40]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="OPData.length">
        </el-pagination>
      </el-col>
    </el-row>
    <el-dialog title="新增机构" :visible.sync="dialogNewOP" :modal=false>
      <el-form :model="formNewOP">
        <el-form-item label="新增操作url" :label-width="formLabelWidth">
          <el-input v-model="formNewOP.opURL" style="width: 80%"></el-input>
        </el-form-item>
        <el-form-item label="新增操作归属模块" :label-width="formLabelWidth">
          <el-select v-model="formNewOP.opType" placeholder="请选择">
            <el-option
              v-for="item in opTypeData"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="新增操作描述" :label-width="formLabelWidth">
          <el-input v-model="formNewOP.opDescribe" style="width: 80%"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogNewOP=false">取 消</el-button>
        <el-button type="primary" @click="addNewOP()">确 定</el-button>
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
  name: "OPManage",
  data() {
    return {
      dialogNewOP:false,
      OPData:[],
      formNewOP:{
        opURL:'',
        opType:'',
        opDescribe:'',
      },
      formLabelWidth: '120px',
      opTypeData: [{
        value: 'user',
        label: '系统管理'
      }],
      currentPage:1, //初始页
      pageSize:10,    //    每页的数据　　　　　　
    }
  },
  mounted:function () {
    this.getOPInfo()
  },

  methods: {
    getOPInfo() {
      let params={};
      this.$axios.post('/user/getOPInfo',params).then(res => {
        if(res.data.code===1){
          let JsonParams=JSON.parse(res.data.data);
          this.OPData=JsonParams;
        }else{
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })
    },

    addNewOP(){
      let params={
        opURL: encodeURIComponent(this.formNewOP.opURL),
        opDescribe: encodeURIComponent(this.formNewOP.opDescribe),
        opType: this.formNewOP.opType,
      };
      this.$axios.post('/user/addNewOP',params).then(res => {
        if(res.data.code===1){
          this.getOPInfo()
          this.$notify({
            title: '成功',
            message: res.data.msg,
            type: 'success'
          });
          this.dialogNewOP=false;
        }else{
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })
    },
    handleSizeChange(val) {
      this.pageSize = val;
      this.currentPage = 1;
    },
    handleCurrentChange(val) {
      //点击改变当前页
      this.currentPage = val;
    },

  },
}
</script>

<style scoped>

</style>
