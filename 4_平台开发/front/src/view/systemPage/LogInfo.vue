<template>
  <div>
    系统日志
    <el-row style="margin-top: 20px">
      <el-col :span="20" :offset="2">
        <el-table :data="opLogtableData" stripe border style="width: 100%">
          <el-table-column prop="opTime" label="操作时间" width="200"></el-table-column>
          <el-table-column prop="opLoginNo" label="操作统一认证号" width="200"></el-table-column>
          <el-table-column prop="opUser" label="操作用户名" width="200"></el-table-column>
          <el-table-column label="操作模块" width="200">
            <template slot-scope="scope">
              <p  v-if="scope.row.opType==='user'">系统管理</p>
              <!--todo 按需添加-->
              <!--<p  v-if="scope.row.opType===inActiveStatus">已停用</p>-->
            </template>
          </el-table-column>
          <el-table-column prop="opDescribe" label="操作描述" width="300"></el-table-column>
        </el-table>
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currPage"
          :page-sizes="[10, 20, 50]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total">
        </el-pagination>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "LogInfo",
  data(){
    return{
      opLogtableData:[],
      total:0,
      currPage: 1,  //默认第一页
      pageSize: 10, //默认展示10条数据
    }
  },
  mounted:function () {
    this.getOpLogInfo()
  },
  methods:{
    getOpLogInfo() {
      let params={
        offset:(this.currPage-1)*this.pageSize,//每次传过去的页数
        limit:this.pageSize, //每页需要展示的条数
      };
      this.$axios.post('/user/getOpLogInfo',params).then(res => {
        if(res.data.code===1){
          let JsonParams=JSON.parse(res.data.data);
          this.total=JsonParams.total;
          this.opLogtableData=JsonParams.opLogtableData;
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
      //改变每页显示数量重新请求数据，重置当前页为第一页
      this.pageSize = val;
      this.currPage = 1;
      this.getOpLogInfo();
    },
    handleCurrentChange(val) {
      //点击改变当前页
      this.currPage = val;
      this.getOpLogInfo()
    },

  }
}
</script>

<style scoped>

</style>
