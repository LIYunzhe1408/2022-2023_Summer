<template>
  <el-row class="top_style">
    <el-col :span="20" offset="2">
      <div class="box_head">
        <h2 class="box_head_title">数据上传</h2>
      </div>
      <el-tabs type="border-card">
        <el-tab-pane label="数据"></el-tab-pane>
        <el-tab-pane label="计算方法"></el-tab-pane>
        <el-tab-pane label="文献"></el-tab-pane>
        <el-tab-pane label="专利">
          <el-row>
            <el-col :span="20" class="context" offset="2">
              <el-steps :active="active" finish-status="success">
                <el-step title="专利内容信息" icon="el-icon-edit"></el-step>
                <el-step title="专利属性信息" icon="el-icon-edit"></el-step>
                <el-step title="专利文件上传" icon="el-icon-upload"></el-step>
              </el-steps>
            </el-col>
            <el-col :span="20" class="context" offset="2" v-show="active === 0">
              <el-form :model="patentData">
                <el-form-item label="标题(中文)" :label-width="formLabelWidth">
                  <el-input v-model="patentData.title" style="width: 80%"></el-input>
                </el-form-item>
                <el-form-item label="标题(英文)" :label-width="formLabelWidth">
                  <el-input v-model="patentData.titleE" style="width: 80%"></el-input>
                </el-form-item>
                <el-form-item label="作者(中文)" :label-width="formLabelWidth">
                  <el-input v-model="patentData.author" style="width: 80%"></el-input>
                </el-form-item>
                <el-form-item label="作者(英文)" :label-width="formLabelWidth">
                  <el-input v-model="patentData.authorE" style="width: 80%"></el-input>
                </el-form-item>
                <el-form-item label="摘要(中文)" :label-width="formLabelWidth">
                  <el-input v-model="patentData.l_abstract" style="width: 80%"></el-input>
                </el-form-item>
                <el-form-item label="摘要(英文)" :label-width="formLabelWidth">
                  <el-input v-model="patentData.l_abstractE" style="width: 80%"></el-input>
                </el-form-item>
                <el-form-item label="关键字(中文)" :label-width="formLabelWidth">
                  <el-input v-model="patentData.keywords" style="width: 80%"></el-input>
                </el-form-item>
                <el-form-item label="关键字(英文)" :label-width="formLabelWidth">
                  <el-input v-model="patentData.keywordsE" style="width: 80%"></el-input>
                </el-form-item>
              </el-form>
            </el-col>
          </el-row>
          <el-col :span="8" class="context" offset="8">
            <el-button @click="lastStep()">上一步</el-button>
            <el-button @click="nextStep()">{{btnName}}</el-button>
          </el-col>
        </el-tab-pane>
      </el-tabs>
    </el-col>
  </el-row>
</template>

<script>
import ElRow from "element-ui/packages/row/src/row";
import ElCol from "element-ui/packages/col/src/col";

export default {
  name: "AddPatent",
  data () {
    return {
      formLabelWidth: '120px',
      active: 0,
      btnName: '下一步',

      patentData: {
        title: '',
        titleE: '',
        author: '',
        authorE: '',
        l_abstract: '',
        l_abstractE: '',
        keywords: '',
        keywordsE: '',
      }

    }
  },
  mounted: function () {

  },

  methods: {
    lastStep () {
      if (this.active < 1) {
        this.active = 0;
      } else {
        this.btnName = '下一步';
        this.active--;
      }
    },
    nextStep () {
      this.active++;
      if (this.active === 2) {
        this.btnName = '提交';
      }else if(this.active >2 ){
        this.active =2;
        this.addNewPatent();
      }
    },
    //新增一条专利信息
    addNewPatent(){
      let params = {
        title: this.patentData.title,
        titleE: this.patentData.titleE,
        author: this.patentData.author,
        authorE: this.patentData.authorE,
        l_abstract: this.patentData.l_abstract,
        l_abstractE: this.patentData.l_abstractE,
        keywords: this.patentData.keywords,
        keywordsE: this.patentData.keywordsE,
      };
      this.$axios.post('/demo/addNewPatent', params).then(res => {
        if (res.data.code === 1) {
          this.$notify({
            title: '成功',
            message: res.data.msg,
            type: 'success'
          });
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
.top_style {
  margin-top: 5px;
}
.dataHead {
  position: absolute;
  top: 54%;
  left: 55%;
  transform: translate(-50%, -50%);
  width: 70%;
  height: 80%;
  border: 2px solid #adcadd;
  border-top: none;
  border-radius: 5px;
  background-color: #fff;
}
.box_head {
  position: relative;
  width: 100%;
  height: 45px;
  border-bottom: 1px solid #adcadd;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  background-color: #dfeef8;
}
.box_head_title {
  height: 45px;
  line-height: 45px;
  margin-left: 10px;
  font-size: 14px;
  /* color: #fff; */
}

.context {
  margin-top: 20px;
  margin-bottom: 20px;
}
</style>
