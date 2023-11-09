<template>
  <el-row class="top_style">
    <el-col :span="20" offset="2">
      <div class="box_head">
        <h2 class="box_head_title">关系抽取</h2>
      </div>
      <el-tabs type="border-card">
        <el-tab-pane label="抽取提示">
          <p align="center">抽取方法概述</p>
          <el-empty description="description" />

          <div class="demo-progress">
            <el-progress :percentage="100" :format="format"  />
          </div>
          <el-col :span='20' offset="10">
            <el-button @click="active">抽取</el-button>
            <el-button @click="active">完成</el-button>
          </el-col>
        </el-tab-pane>
        <el-tab-pane label="结果展示">
              <el-tabs type="border-card" tab-position="left" >
                <el-tab-pane label="Article 1">
                  <el-row>
                    <el-col :span="10">
                      <p>关系抽取结果</p>
                    </el-col>
                    <div style="padding: 10px 0">
                      <el-input suffix-icon="el-icon-search" placeholder="请输入文献名" style="width: 200px"></el-input>
                      <el-button type="primary">搜索</el-button>
                    </div>
                    <el-col :span="20">
                      <el-table :data="tableData" border style="width: 100%">
                        <el-table-column fixed prop="sentence" label="sentence"/>
                        <el-table-column prop="entity_1" label="entity_1" width="80"/>
                        <el-table-column prop="relation" label="relation" width="130"/>
                        <el-table-column prop="entity_2" label="entity_2" width="120"/>
                        <el-table-column label="Operation">
                          <!--template slot-scope="scope"></template-->
                            <el-button type="success">编辑<i class="el-icon-edit"></i></el-button>
                            <el-popover
                              placement="top"
                              width="160"
                              v-model="visible">
                              <p>确定删除本条语句吗？</p>
                              <div style="text-align: right; margin: 0">
                                <el-button size="mini" type="text" @click="visible = false">取消</el-button>
                                <el-button type="primary" size="mini" @click="visible = false">确定</el-button>
                              </div>
                              <el-button type="danger" slot="reference">删除<i class="el-icon-remove-outline"></i></el-button>
                            </el-popover>
                        </el-table-column>
                      </el-table>
                    </el-col>
                  </el-row>
                </el-tab-pane>
                <el-tab-pane label="Article 2"></el-tab-pane>
                <el-tab-pane label="Article 3"></el-tab-pane>
                <el-tab-pane label="Article 4"></el-tab-pane>
                <el-tab-pane label="Article 5"></el-tab-pane>
                <el-tab-pane label="Article 6"></el-tab-pane>
                <div class="block" style="margin-left:200px; padding: 10px 0">
                  <el-pagination
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="currentPage4"
                    :page-sizes="[5, 10, 20, 30]"
                    :page-size="10"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="49">
                  </el-pagination>
                </div>
              </el-tabs>

              <el-col :span="8" class="context" offset="10">
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
      visible: false,

      format : (percentage) => (percentage === 100 ? 'Full' : `${percentage}%`),
      patentData: {
        title: '',
        titleE: '',
        author: '',
        authorE: '',
        l_abstract: '',
        l_abstractE: '',
        keywords: '',
        keywordsE: '',
      },
      tableData : [          //TODO to be add from back
        {
          sentence: 'The full cells were galvanostatically cycled at a temperature of 60 degree C with voltage limits of 2.5 V and 4.2 V.',
          entity_1: 'cycled',
          relation: 'Condition-On',
          entity_2:'60 degree C',
        },
        {
          sentence: 'The full cells were galvanostatically cycled at a temperature of 60 degree C with voltage limits of 2.5 V and 4.2 V.',
          entity_1: '4.2v',
          relation: 'Instance-Of',
          entity_2:'voltage',
        },
        {
          sentence: 'The full cells were galvanostatically cycled at a temperature of 60 degree C with voltage limits of 2.5 V and 4.2 V.',
          entity_1: '2.5v',
          relation: 'Instance-Of',
          entity_2:'voltage',
        },
      ]
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
.el-header{
  margin-top: 10px;
}
.demo-progress{
  margin-left: 200px;
  margin-right: 200px;
}
</style>
