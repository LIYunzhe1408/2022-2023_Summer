<template>
  <div>
    <el-row>
      <el-col :span="20" :offset="2">
        <h1 class="info_title">专利信息</h1>
      </el-col>
      <el-col :span="20" :offset="2">
        <el-table :data="PatentData" stripe border style="width: 100%">
          <el-table-column prop="title" label="标题(中文)"></el-table-column>
          <el-table-column prop="titleE" label="标题(英文)"></el-table-column>
          <el-table-column prop="author" label="作者(中文)"></el-table-column>
          <el-table-column prop="authorE" label="作者(英文)"></el-table-column>
          <el-table-column prop="l_abstract" label="摘要(中文)"></el-table-column>
          <el-table-column prop="l_abstractE" label="摘要(英文)"></el-table-column>
          <el-table-column prop="keywords" label="关键字(中文)"></el-table-column>
          <el-table-column prop="keywordsE" label="关键字(英文)"></el-table-column>
        </el-table>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import ElRow from "element-ui/packages/row/src/row";
import ElCol from "element-ui/packages/col/src/col";

export default {
  components: {
    ElCol,
    ElRow
  },
  name: "PatentInfo",
  data () {
    return {
      PatentData: [],

    }
  },
  mounted: function () {
    this.getPatentData()
  },

  methods: {
    //查询专利表数据信息
    getPatentData () {
      let params = {};
      this.$axios.post('/demo/getPatentData', params).then(res => {
        if (res.data.code === 1) {
          this.PatentData = JSON.parse(res.data.data);
        } else {
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
.info_title {
  font-size: 20px;
  padding: 5px 0;
}
</style>
