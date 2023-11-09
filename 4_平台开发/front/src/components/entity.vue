<template>
  <div>
    <el-row>
      <el-col :span="20" class="context" offset="2">
        <el-steps :active="active" finish-status="success">
          <el-step title="抽取提示" icon="el-icon-reading"></el-step>
          <el-step title="结果预览" icon="el-icon-edit"></el-step>
          <el-step title="抽取统计" icon="el-icon-s-data"></el-step>
        </el-steps>
      </el-col>

      <!-- 抽取提示-->
      <el-col :span="20" class="context" offset="2" v-show="active === 0">
        <el-card style="  background-color:whitesmoke;font-family: 微软雅黑;">
          <h3 style="text-align: center">实体抽取概述</h3>
          <p style="text-indent: 32.4px; line-height: 25px">
            实体识别旨在将现实生活中具有实体类信息的名称识别提取出来，可以是具体的客观存在的事物，也可以是某种抽象概念，具体到不同的领域也有不同的定义，在通用领域有人名、地名、机构名；在医疗领域可以将疾病名称，症状，治疗方式，药物名称等定义为实体类别；在军事领域有武器名、组织名、地区名等。这些实体非常清楚的表达了这句话的意思，准确识别出这些实体，对一些下游任务有很大帮助，可以应用在提升信息检索的质量，构建知识图谱等下游任务。
          </p>
          <p style="text-indent: 32.4px;line-height: 25px">
            国外在对于命名实体识别任务的研究起步较早，研究经历主要经历了基于规则的方法，基于统计学的机器方法学，基于深度学习的方法。英文只需关注单词本身含义，不需考虑词语边界问题，实现难度相对较低，准确率也相对较高。早在1991年L.Rau就在金融新闻领域提取公司名称，并随后在100万多字的财经新闻中做了测试，准确率超过95%，表现效果比人为标注索引的公司实体名多出25%，并在1996年MUC-6会议上被正式列为信息抽取的一项子任务。Nadeau，David等学者在2007年总结了近15年内命名实体识别与分类任务的研究进展和方法，调查结果显示，当时的NERC系统实现了从最初的手工规则提取到机器学习技术的广泛使用。近年来，深度学习通过将文本向量化表示和一些非线性处理的语义组合，在命名实体任务上有了非常可观的进展。
          </p>
        </el-card>
        <div align="center" style="margin-top: 20px">
          <el-button align="center" v-show="started===0" type="primary" @click="getLitName();started=1">开始实体抽取</el-button>
        </div>
        <div align="center" style="margin-top: 20px" v-show="started===1">
          <el-select  v-model="extractLitName" placeholder="请选择需要抽取的论文" ref="myselect">
            <el-option v-for="item in LitName" :value="item.topic" :key="item.topic"/>
          </el-select>
          <el-button type="primary" @click="runExtraction()">抽取</el-button>
          <div v-show="showClue===1" align="center" ><el-tag >转换中，请稍后 <i class="el-icon-loading"></i></el-tag></div>
        </div>
      </el-col>

      <!-- 结果预览 -->
      <el-col :span="20" class="context" offset="2" v-show="active === 1">
        <el-table
          :data="NERExtractData"
          height="400px"
          header-cell-style="background:#dfeef8;color:black">
          <el-table-column prop="entity_content" align="center" label="实体" width="200px"></el-table-column>
          <el-table-column prop="predicate" align="center" label="类型" width="200px"></el-table-column>
          <el-table-column prop="sentence_content" align="center" label="句子" :show-overflow-tooltip="true"></el-table-column>
          <el-table-column align="center" label="操作" width="210px" #default="scope">
            <el-button type="success" @click="dialogFormVisible = true;setValue(scope)">编辑<i class="el-icon-edit"></i></el-button>
            <el-button type="warning" @click="dialog2FormVisible = true;setValue(scope)">溯源<i class="el-icon-info"></i></el-button>
          </el-table-column>

        </el-table>
      </el-col>

      <el-dialog title="文献句子信息"  :visible.sync="dialogFormVisible" width="600px" :append-to-body="true">
        <el-form :model="NERExtractDataForm" ref="NERExtractDataForm" status-icon="true">
          <el-form-item prop="entity_content" label = "实体" label-width=60px>
            <el-col>
              <el-input v-model="NERExtractDataForm.entity_content"></el-input>
            </el-col>
          </el-form-item>
          <el-form-item prop="entity_content" label = "类型" label-width=60px>
            <el-col>
              <el-input v-model="NERExtractDataForm.predicate"></el-input>
            </el-col>
          </el-form-item>
          <el-form-item prop="sentence_content" label = "句子"  label-width=60px>
            <el-col>
              <el-input type="textarea" v-model="NERExtractDataForm.sentence_content" disabled="true" autosize></el-input>
            </el-col>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer" style="text-align: center">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="submitForm('NERExtractDataForm');">保存</el-button>
        </div>
      </el-dialog>


      <el-dialog title="文献句子溯源"  :visible.sync="dialog2FormVisible" width="600px" :append-to-body="true">
        <el-form :model="traceData" status-icon="true">
          <el-form-item prop="title" label = "标题"  label-width=60px>
            <el-col>
              <el-input  v-model="traceData.topic" disabled="true" autosize></el-input>
            </el-col>
          </el-form-item>
          <el-form-item prop="author" label = "作者" label-width=60px>
            <el-col>
              <el-input v-model="traceData.author" disabled="true"></el-input>
            </el-col>
          </el-form-item>
          <el-form-item prop="keywords" label = "关键词"  label-width=60px>
            <el-col>
              <el-input  v-model="traceData.keywords" disabled="true" autosize></el-input>
            </el-col>
          </el-form-item>
          <el-form-item prop="id" label = "句子ID"  label-width=60px>
            <el-col>
              <el-input  v-model="traceData.sentence_id" disabled="true" autosize></el-input>
            </el-col>
          </el-form-item>
          <el-form-item prop="abstract" label = "摘要"  label-width=60px>
            <el-col>
              <el-input  type="textarea" v-model="traceData.abstract" disabled="true" autosize></el-input>
            </el-col>
          </el-form-item>
          <el-form-item prop="abstract" label = "doi"  label-width=60px>
            <el-col>
              <el-input  type="textarea" v-model="traceData.doi" disabled="true" autosize></el-input>
            </el-col>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer" style="text-align: center">
          <el-button @click="dialog2FormVisible = false">确定</el-button>
        </div>
      </el-dialog>

      <!-- 抽取统计 -->
      <el-col :span="20" class="context" offset="2" v-show="active === 2">
        <el-table
              :data = "resultData"
              stripe="true"
              header-cell-style="background:#dfeef8;color:black"
              highlight-current-row ="true">
          <el-table-column align="center" prop="totalNumber" label="实体总数"></el-table-column>
          <el-table-column align="center" prop="Composition" label = "Composition"></el-table-column>
          <el-table-column align="center" prop="Structure" label="Structure"></el-table-column>
          <el-table-column align="center" prop="Property" label="Property"></el-table-column>
          <el-table-column align="center" prop="Application" label="Application"></el-table-column>
          <el-table-column align="center" prop="Processing" label="Processing"></el-table-column>
          <el-table-column align="center" prop="Condition" label="Condition"></el-table-column>
          <el-table-column align="center" prop="Feature" label="Feature"></el-table-column>
          <el-table-column align="center" prop="Characterization" label="Characterization"></el-table-column>
        </el-table>
        <div id="main" style="width: 1000px; height: 600px; margin-top: 40px;margin-left: 20px;text-align: center" align="center"></div>

        <div align="center"><el-button type="primary" align="center" @click="downloadFile">下载文件</el-button></div>
      </el-col>

      <el-col :span="20" class="context" offset="2" v-show="active === 3">
        <div style="font-size: 24px; text-align: center"><i class="el-icon-finished">实体抽取完成</i></div>
      </el-col>

    </el-row>



    <el-col :span="8" class="context" offset="8">
      <div align="center">
        <el-button @click="lastStep()" v-show="active!==0">上一步</el-button>
        <el-button @click="nextStep()" v-show="isExtracted==1&&active!=3">{{btnName}}</el-button>
      </div>

    </el-col>

  </div>

</template>


<script>
export default {
  name: "entity",
  mounted: function () {
    this.getLitName()
  },

  data:function (){
    return{
      started:0,
      showClue:0,
      dialogFormVisible:false,
      dialog2FormVisible:false,
      formLabelWidth: '120px',
      active: 0,
      btnName: '下一步',
      LitName: '',
      extractLitName:'',
      long_lasted_Name:'',
      isExtracted: 0,
      NERExtractData:[{
        entity_content:'',
        sentence_content:'',
        doi:'',
        sentence_id:'',
        entity_id:'',
        topic:'',
        predicate:'',
        author:'',
        abstract:'',
        keywords:''
      }],
      NERExtractDataForm:{
        entity_content:'',
        sentence_content:'',
        predicate:'',
        entity_id:'',
        sentence_id:''
      },
      resultData:[{
        totalNumber:'0.0',
        Characterization:'0',
        Composition:'0',
        Structure:'0',
        Property:'0',
        Feature:'0',
        Application:'0',
        Processing:'0',
        Condition:"0"+[]
      }],
      echartsData:[],
      traceData: {
        topic: '',
        // titleE: '',
        author: '',
        // authorE: '',
        // l_abstract: '',
        abstract: '',
        keywords: '',
        // keywordsE: '',
        sentence_id:'',
        entity_id:'',
        doi:''
      }
    }
  },
  methods:{
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
      if (this.active === 1)
      {
        this.getTableData()
      }
      if (this.btnName == '完成'){
        this.active = 3;
      }

      if (this.active === 2) {
        this.getStatics()
        this.drawChart()
        this.btnName = '完成';

        this.drawChart()
      }else if(this.active > 2 && this.active != 3){
        this.active = 2;
      }
    },
    runExtraction(){
      this.showClue = 1
      this.long_lasted_Name = this.extractLitName
      let param = {
        fileName: this.extractLitName
      }
      this.$axios.post('/demo/entityExtraction',param).then(res => {
        console.log(res.data.code)
        if (res.data.code === 1) {
          this.$notify({
            title: '成功',
            message: res.data.msg,
            type: 'success'
          });
          this.writeEntity();
          this.isExtracted = 1;
          this.showClue = 0;
        } else {
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })
    },
    downloadFile() {
      let param = {
        fileName: this.extractLitName
      }
      this.$axios({
        url: '/demo/downloadFile',
        method: 'post',
        responseType: 'blob'
      }).then(res => {
        const url = window.URL.createObjectURL(new Blob([res.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', this.extractLitName + '_NER_result.xlsx'); // 文件名
        document.body.appendChild(link);
        link.click();
        this.$notify({
          title: '成功',
          message: '文件下载成功',
          type: 'success'
        })
      }).catch(error => {
        console.error(error)
        this.$notify({
          title: '错误',
          message: '文件下载失败',
          type: 'error'
        })
      })
    },
    getTableData () {
      let table_params = {
        topic: String(this.extractLitName)
      }
      this.$axios.post('/demo/getNERResults', table_params).then(res => {
        if (res.data.code === 1) {
          this.NERExtractData = JSON.parse(res.data.data)
          this.getStatics()
        } else {
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })

    },

    getStatics () {
      let table_params = {
        topic: String(this.extractLitName)
      }
      this.$axios.post('/demo/getStatics', table_params).then(res => {
        if (res.data.code === 1) {
          this.resultData = JSON.parse(res.data.data)
          this.resultData[0].totalNumber = (this.resultData[0].Composition-0)+
            (this.resultData[0].Structure-0)+
            (this.resultData[0].Property-0)+
            (this.resultData[0].Application-0)+
            (this.resultData[0].Processing-0)+
            (this.resultData[0].Condition-0)+
            (this.resultData[0].Feature-0)+
            (this.resultData[0].Characterization-0)
          this.echartsData = [this.resultData[0].Composition,
            this.resultData[0].Structure,
            this.resultData[0].Property,
            this.resultData[0].Application,
            this.resultData[0].Processing,
            this.resultData[0].Condition,
            this.resultData[0].Feature,
            this.resultData[0].Characterization]
          console.log(this.echartsData)
          this.drawChart()
        } else {
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })
    },

    writeEntity () {
      let table_params = {
        topic: String(this.extractLitName)
      }
      this.$axios.post('/demo/WriteResults', table_params).then(res => {
        if (res.data.code === 1) {
          console.log(this.echartsData)
        } else {
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })
    },
    getLitName () {
      let params = {source:"RE"};
      this.$axios.post('/demo/getLitName', params).then(res => {
        if (res.data.code === 1) {
          this.LitName = JSON.parse(res.data.data);
        } else {
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })
    },
    setValue(scope) {
      this.NERExtractDataForm.entity_content = scope.row.entity_content;
      this.NERExtractDataForm.sentence_content = scope.row.sentence_content;
      this.NERExtractDataForm.predicate = scope.row.predicate;
      this.NERExtractDataForm.entity_id = scope.row.entity_id
      this.NERExtractDataForm.sentence_id = scope.row.sentence_id
      this.traceData.topic = scope.row.topic;
      this.traceData.sentence_id = scope.row.sentence_id;
      this.traceData.entity_id = scope.row.entity_id;
      this.traceData.doi = scope.row.doi;
      this.traceData.author = scope.row.author;
      this.traceData.keywords = scope.row.keywords;
      this.traceData.abstract = scope.row.abstract;
      // console.log(this.traceData.entity_id)
      // console.log(this.traceData.abstract)
    },
    updateNERResult(){
      let table_params = {
        entity_content:this.NERExtractDataForm.entity_content,
        sentence_content:this.NERExtractDataForm.sentence_content,
        predicate:this.NERExtractDataForm.predicate,
        entity_id:this.NERExtractDataForm.entity_id,
        sentence_id:this.NERExtractDataForm.sentence_id
      }
      console.log(this.NERExtractDataForm.entity_content)
      this.$axios.post('/demo/updateNERResult',table_params).then(res=>{
        if (res.data.code === 1)
        {
          console.log(res.data)
          this.$message({
            type:"success",
            message:"修改成功"
          })
        }
        else{
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })
    },
    submitForm(formName) {  // TODO 全要改
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.updateNERResult();
          return true;
        } else {
          this.$message({
            duration:3000,
            message:'更新失败',
            type:"error"
          });
          console.log('error submit!!');
          return false;
        }
      });
      this.dialogFormVisible = false
      this.getTableData()
    },
  drawChart() {
      console.log(this.echartsData)
    // 基于准备好的dom，初始化echarts实例  这个和上面的main对应
    let myChart = this.$echarts.init(document.getElementById("main"));
    // 指定图表的配置项和数据
    let option = {
      title: {
        text: "NER数据统计",
      },
      tooltip: {},
      legend: {
        data: ["个数"],
      },
      xAxis: {
        data: ["Composition", "Structure", "Property", "Application", "Processing", "Condition", "Feature", "Characterization"],
        axisLabel: {
          fontSize: 8
        }
      },
      yAxis: {},
      series: [
        {
          name: "个数",
          type: "bar",
          seriesLayoutBy: "column",
          data: this.echartsData,
        }

      ]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
  }
  }
}
</script>

<style scoped>
.context {
  margin-top: 20px;
  margin-bottom: 20px;
}

</style>
