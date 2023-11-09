<template>
  <div>
    <el-row>
      <el-col :span="20" class="context" offset="2">
        <el-steps :active="active" finish-status="success">
          <el-step title="抽取提示" icon="el-icon-reading"></el-step>
          <el-step title="结果预览" icon="el-icon-edit"></el-step>
<!--          <el-step title="抽取统计" icon="el-icon-s-data"></el-step>-->
        </el-steps>
      </el-col>
      <!-- 抽取提示-->
      <el-col :span="20" class="context" offset="2" v-show="active === 0">
        <el-card style="  background-color:whitesmoke;font-family: 微软雅黑;">
          <h3 style="text-align: center">关系抽取概述</h3>
          <p style="text-indent: 32.4px; line-height: 25px">
            关系抽取是在实体识别的基础上，将其中有关系的两个实体进行分类以帮助人们得到文本中更为重要的信息，是知识库构建，只能问答，语义分析的重要技术支撑。一个完整的关系抽取系统包含实体识别，实体对齐，关系分类三部分，第一部分是基础，第三部分是核心，不管是国内还是国外，其实现方式不外乎两种，一种是以管道的当时抽取，先做一部分提取出实体，然后在识别出的实体上做抽取任务。另一种方式是做联合抽取，输入文本，直接输出实体关系对。大量实验表明同等数据集和算法下，联合抽取的性能要比管道方式性能好。
          </p>
          <p style="text-indent: 32.4px;line-height: 25px">
            实体关系抽取任务在1998年MUC-7会议上被首次正式提出，当时主要用模板匹配的方式在英文纽约时代新翁服务语料库完成关系分类。随后在机器学习和深度学习方面都有相应的发展，通过分析句法语法结构，得到句子的某些特征，利用这些特征结合机器学习的相关算法去做关系抽取任务。随着SVM的发展，核函数设计的多样化也促进了关系抽取任务的发展。像Bunescu R和Mooney R提出的依赖树核和子序列核。Miwa M， Bansal M[7]在序列和树结构上用长短时记忆网络做到端到端的关系抽取。近些年来，神经网络模型被应用到更多的关系抽取任务，有递归神经网络，卷积神经网络，循环神经网络，图神经网络，transformer等。
          </p>
          <p style="text-indent: 32.4px;line-height: 25px">
            与国外相比，中文实体标注的研究进展有限。无词界，无形态变化的特点使抽取困难大大增加。Wenjie Li, Peng Zhang等人提出一种新型基于语法特征的中文关系抽取模型，不仅利用了实体本身语义信息，还定义了实体之间的九种位置结构，在ACE2005数据集上表现良好。Zheng, Suncong等人提出了一种混合神经网络模型，不需要任何手工特征，实体检测部分用来双向LSTM模块，关系分类用CNN模块并在ACE2005数据集上有了最新成果。Tseng, Yuen-Hsien等人开发了一种新型的开放式信息抽取系统，该系统不需要任何特定于关系的人工输入和预先指定的关系合计就可以提取出一组不同的关系，适合目标关系未知的大规模文本语料库。
          </p>
        </el-card>


        <div align="center" style="margin-top: 20px">
          <el-button align="center" v-show="started===0" type="primary" @click="getLitName()">开始关系抽取</el-button>
        </div>

        <div v-show="started===1">
          <div align="center" style="margin-top: 20px">
            <el-select  v-model="extractLitName" placeholder="请选择已完成NER的论文" ref="myselect">
              <el-option v-for="item in LitName" :value="item.topic" :key="item.topic"/>
            </el-select>
            <el-button type="primary" v-show ="isChecked===false" @click="checkInputPreProcess()">检查输入预处理</el-button>
            <el-button type="primary" v-show ="isChecked===true" @click="runREExtraction()">抽取</el-button>
            <div v-show="showClue===1" align="center" ><el-tag >转换中，请稍后 <i class="el-icon-loading"></i></el-tag></div>
          </div>
        </div>
      </el-col>

      <el-col :span="20" class="context" offset="2" v-show="active === 1">
        <el-table
          :data="REExtractData"
          height="400px"
          header-cell-style="background:#dfeef8;color:black">
          <el-table-column prop="relation" align="center" label="关系" width="200px"></el-table-column>
          <el-table-column prop="sentence" align="center" label="句子" :show-overflow-tooltip="true"></el-table-column>
          <el-table-column align="center" label="操作" width="210px" #default="scope">
            <el-button type="success" @click="dialogFormVisible = true;setValue(scope)">编辑<i class="el-icon-edit"></i></el-button>
<!--            <el-button type="warning" @click="dialog2FormVisible = true;">溯源<i class="el-icon-info"></i></el-button>-->
          </el-table-column>

        </el-table>
        <div v-show = "active===1" align="center"><el-button type="primary" align="center" @click="downloadFile">下载文件</el-button></div>
        <el-dialog title="文献句子信息"  :visible.sync="dialogFormVisible" width="600px" :append-to-body="true">
          <el-form :model="REExtractDataForm" status-icon="true">
            <el-form-item prop="relation" label = "关系" label-width=60px>
              <el-col>
                <el-input v-model="REExtractDataForm.relation"></el-input>
              </el-col>
            </el-form-item>
            <el-form-item prop="sentence" label = "句子"  label-width=60px>
              <el-col>
                <el-input type="textarea" rows = "6" v-model="REExtractDataForm.sentence" disabled="true" autosize></el-input>
              </el-col>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer" style="text-align: center">
            <el-button @click="dialogFormVisible = false">取 消</el-button>
            <el-button type="primary" @click="submitForm('REExtractDataForm');">保存</el-button>
          </div>
        </el-dialog>

        <el-dialog title="文献句子溯源"  :visible.sync="dialog2FormVisible" width="600px" :append-to-body="true">
          <el-form :model="patentData" status-icon="true">
            <el-form-item prop="title" label = "标题"  label-width=60px>
              <el-col>
                <el-input  v-model="patentData.title" disabled="true" autosize></el-input>
              </el-col>
            </el-form-item>
            <el-form-item prop="author" label = "作者" label-width=60px>
              <el-col>
                <el-input v-model="patentData.author" disabled="true"></el-input>
              </el-col>
            </el-form-item>
            <el-form-item prop="keywords" label = "关键词"  label-width=60px>
              <el-col>
                <el-input  v-model="patentData.keywords" disabled="true" autosize></el-input>
              </el-col>
            </el-form-item>
            <el-form-item prop="id" label = "句子ID"  label-width=60px>
              <el-col>
                <el-input  v-model="patentData.keywords" disabled="true" autosize></el-input>
              </el-col>
            </el-form-item>
            <el-form-item prop="abstract" label = "摘要"  label-width=60px>
              <el-col>
                <el-input  type="textarea" v-model="patentData.l_abstract" disabled="true" autosize></el-input>
              </el-col>
            </el-form-item>

          </el-form>
          <div slot="footer" class="dialog-footer" style="text-align: center">
            <el-button @click="dialog2FormVisible = false">确定</el-button>
          </div>
        </el-dialog>
      </el-col>
<!--      &lt;!&ndash; 抽取统计 &ndash;&gt;-->
<!--      <el-col :span="20" class="context" offset="2" v-show="active === 2">-->

<!--        <el-table-->
<!--          :data = "resultData"-->
<!--          stripe="true"-->
<!--          header-cell-style="background:#dfeef8;color:black"-->
<!--          highlight-current-row ="true">-->
<!--          <el-table-column align="center" prop="totalNumber" label="关系总数"></el-table-column>-->
<!--          <el-table-column align="center" prop="compNumber" label = "Cause-Effect"></el-table-column>-->
<!--          <el-table-column align="center" prop="strNumber" label="Component-Whole"></el-table-column>-->
<!--          <el-table-column align="center" prop="propNumber" label="Condition-On"></el-table-column>-->
<!--          <el-table-column align="center" prop="condNumber" label="Feature-Of"></el-table-column>-->
<!--          <el-table-column align="center" prop="proceNumber" label="Instance-Of"></el-table-column>-->
<!--          <el-table-column align="center" prop="appliNumber" label="Located-Of"></el-table-column>-->
<!--          <el-table-column align="center" prop="featNumber" label="Other"></el-table-column>-->
<!--        </el-table>-->
<!--        <div id="main2" style="width: 1000px; height: 400px; margin-top: 40px;margin-left: 0px;text-align: center" align="center"></div>-->
<!--      </el-col>-->

    </el-row>
    <el-col :span="20" class="context" offset="2" v-show="active === 2">
      <div style="font-size: 24px; text-align: center"><i class="el-icon-finished">关系抽取完成</i></div>
    </el-col>
    <el-col :span="8" class="context" offset="8">
      <div align="center">
        <el-button @click="lastStep()" v-show="active!==0">上一步</el-button>
        <el-button @click="nextStep()" v-show="isExtracted==1">{{btnName}}</el-button>
      </div>

    </el-col>


  </div>

</template>

<script>
export default {
  name: "relation",
  mounted() {
  },
  data:function (){
    return{
      showClue:0,
      extractBtnName:"检查输入预处理",
      LitName: '',
      started:0,
      active: 0,
      isChecked:false,
      isExtracted:0,
      dialogFormVisible:false,
      dialog2FormVisible:false,
      btnName:'下一步',
      REExtractData:[{
        relation:'',
        sentence:''
      }],
      extractLitName:'',
      REExtractDataForm:{
        relation:'',
        sentence:''
      },
      patentData: {
        title: 'Internal short circuit detection in Li-ion batteries using supervised machine learning',
        titleE: '',
        author: 'Ashish Vaswani',
        authorE: '',
        l_abstract: '',
        l_abstractE: '',
        keywords: '',
        keywordsE: '',
      },
      resultData:[{
        totalNumber:97,
        strNumber:12,
        compNumber:10,
        propNumber:40,
        condNumber:10,
        appliNumber:5,
        proceNumber:10,
        featNumber:10
      }],
      echartsData:[
        12,
        10,
        40,
        5,
        10,
        10,
        10
      ],
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
      this.getTableData()
      if (this.active === 1) {
        this.btnName = '完成';
      }else if(this.active >1 ){
        this.active =1;
      }
    },
    /***************************************************/
    getLitName () {
      this.started=1
      this.$axios.post('/demo/getLitName', {source:"RE"}).then(res => {
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
    checkInputPreProcess(){
      let table_params = {
        topic: String(this.extractLitName)
      }
      console.log(String(this.extractLitName))
      this.$axios.post('/demo/checkREInput', table_params).then(res => {
        if (res.data.code === 1) {
          this.isChecked = true;
          this.$message({
            message:"验证成功",
            type:"success"
          })
          this.extractBtnName = "抽取关系"
        } else {
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })

    },
    runREExtraction(){
      this.showClue = 1
      // this.$axios.get('/demo/REExtraction').then(res => {
      //   if (res.data.code === 1) {
      //     console.log(res.data)
      //     this.$message({
      //       message:"验证成功",
      //       type:"success"
      //     })
      //     this.isExtracted = 1
      //     this.isChecked = true;
      //     this.showClue = 0
      //     this.runJoin()
      //
      //   } else {
      //     this.$notify({
      //       title: '警告',
      //       message: res.data.msg,
      //       type: 'warning'
      //     });
      //   }
      // })

      this.isExtracted = 1
      this.isChecked = true;
      this.showClue = 0
    },
    runJoin(){
      this.$axios.get('/demo/runJoin').then(res => {
        if (res.data.code === 1) {
          console.log(res.data)
          this.$message({
            message:"验证成功",
            type:"success"
          })
         this.joinInOut()
        } else {
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })
    },
    joinInOut(){
      this.$axios.get('/demo/joinInOutToDB').then(res => {
        if (res.data.code === 1) {
          console.log(res.data)
          this.$message({
            message:"验证成功",
            type:"success"
          })
          this.isChecked = true;
          this.getTableData();
        } else {
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })
    },
    getTableData () {   // TODO backend改doi
      let table_params = {
        topic:String(this.extractLitName)
      }
      this.$axios.post('/demo/REResults', table_params).then(res => {
        if (res.data.code === 1) {
          this.REExtractData = JSON.parse(res.data.data)
          // console.log()

          // this.tableData = JSON.parse(res.data.data);
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
      this.REExtractDataForm.relation = scope.row.relation;
      this.REExtractDataForm.sentence = scope.row.sentence;
    },
    updateREResult(){
      let table_params = {
        relation:this.REExtractDataForm.relation,
        sentence:this.REExtractDataForm.sentence
      }
      console.log(this.REExtractDataForm.sentence)
      this.$axios.post('/demo/updateREResult',table_params).then(res=>{
        if (res.data.code === 1)
        {
          console.log(res.data)
          this.$message({
            type:"success",
            message:"修改成功"
          })
          this.getTableData()
          this.dialogFormVisible = 0
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
      this.updateREResult();
      this.$refs[formName].validate((valid) => {
        if (valid) {
          console.log(this.isExtracted)
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
    downloadFile() {
      let param = {
        fileName: this.extractLitName
      }
      this.$axios({
        url: '/demo/downloadREFile',
        method: 'post',
        responseType: 'blob'
      }).then(res => {
        const url = window.URL.createObjectURL(new Blob([res.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', this.extractLitName + '_RE_result.xlsx'); // 文件名
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
    drawChart() {
      // 基于准备好的dom，初始化echarts实例  这个和上面的main对应
      let myChart = this.$echarts.init(document.getElementById("main2"));
      // 指定图表的配置项和数据
      let option = {
        title: {
          text: "RE数据统计",
        },
        tooltip: {},
        legend: {
          data: ["个数"],
        },
        xAxis: {
          data: ["Cause-Effect", "Component-Whole", "Condition-On", "Feature-Of", "Instance-Of", "Located-Of", "Other"],
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
