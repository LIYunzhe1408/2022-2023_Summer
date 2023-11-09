<template>
  <div>
    <el-row class="top_style">

      <!-- 方式选择 -->
      <el-col align="center" v-show="choose===1" style="margin-top: 60px">
        <el-button type="text" style="font-size: 150px;margin-right: 200px">
          <i class="el-icon-upload" @click="toSingle">
            <div style="font-size: 20px;margin-top: 20px">单文件上传
              <div style="font-size: 18px;margin-top: 8px">Single-File Upload</div>
            </div>
          </i>
        </el-button>
        <el-button type="text" style="font-size: 150px">
          <i class="el-icon-document-copy" @click="toMulti">
            <div style="font-size: 20px;margin-top: 20px">多文件上传
              <div style="font-size: 18px;margin-top: 8px">Multi-Files Upload</div>
            </div>
          </i>
        </el-button>
      </el-col>

      <!-- 单文献 -------------------------------------------------------->
      <div v-show="isSingle==1">
        <single-file></single-file>
      </div>
      <!-- 多文献 -------------------------------------------------------->
      <div v-show="isSingle==0">
        <multi-files></multi-files>
      </div>


    </el-row>
  </div>
</template>

<script>
import singleFile from "./singleFile";
import multiFiles from "./multiFiles";

export default {
  name: "fileUpload",
  components:{
    singleFile,
    multiFiles
  },
  data:function (){
    return{
      active:0,
      choose:1,
      isSingle:2,
      btnName:"下一步",
      formLabelWidth: '120px',
    }
  },
  methods: {
    toSingle(){
      this.isSingle = 1;
      this.choose = 0;
    },
    toMulti(){
      this.isSingle = 0;
      this.choose = 0;
    },
  }
}
</script>

<style scoped>
.top_style {
  margin-top: 5px;
}
</style>
