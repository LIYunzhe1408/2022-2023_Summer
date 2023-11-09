<template>
  <el-row class="top_style">
    <el-col :span="20" offset="2">
      <div class="box_head">
        <h2 class="box_head_title">NASICON固态电解质描述符自动获取</h2>
      </div>
      <el-tabs type="border-card">
        <el-tab-pane label="文献上传">
            <file-upload></file-upload>
        </el-tab-pane>
        <el-tab-pane label="预处理">
            <pre-process></pre-process>
        </el-tab-pane>
        <el-tab-pane label="实体抽取">
          <entity></entity>
        </el-tab-pane>
        <el-tab-pane label="关系抽取">
          <relation></relation>
        </el-tab-pane>
        <el-tab-pane label="知识图谱构建">
          <buildmap></buildmap>
        </el-tab-pane>
        <el-tab-pane label="描述符树构建">
          <buildchildtree></buildchildtree>
        </el-tab-pane>
      </el-tabs>
    </el-col>
  </el-row>
</template>

<script>
import entity from "../../components/entity";
import Relation from "../../components/relation";
import fileUpload from "../../components/fileUpload";
import preProcess from "../../components/preProcess";
import Buildchildtree from "../../components/BuildChildTree";
import Buildmap from "../../components/BuildMap";
export default {
  name: "EntityExtract",
  components:{
    Buildmap,
    Buildchildtree,
    Relation,
    entity,
    fileUpload,
    preProcess
  },
  data () {
    return {
    }
  },
  mounted: function () {

  },

  methods: {


  },
}
</script>

<style scoped>
.top_style {
  margin-top: 5px;
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
</style>
