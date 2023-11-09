<template>
  <div>
    <el-row class="top_style">
      <div align="center" style="margin-top: 20px">
        <el-button align="center" v-show="started===0" type="primary" @click="getLitName();started=1">开始预处理</el-button>
      </div>
      <el-col :span="20" :offset="2" v-show="isPreProcessed===0 && started === 1">
        <el-tabs >
          <el-form >
            <el-form-item label="文献标题" :label-width="formLabelWidth" style="margin-left: 200px">
              <el-select v-model="article" filterable placeholder="请选择">
                <el-option v-for="item in articles" :value="item.topic" :key="item.topic"></el-option>
              </el-select>
              <el-button @click="run">PDF转文本</el-button>

<!--              <el-button @click="show">信息展示</el-button>-->
<!--              <el-button @click="download">下载</el-button>-->
            </el-form-item>
            <div v-show="showClue===1" align="center" ><el-tag >转换中，请稍后 <i class="el-icon-loading"></i></el-tag></div>
          </el-form>
        </el-tabs>
      </el-col>
    </el-row>

      <el-col :span="20" class="context" offset="2" v-show="isPreProcessed===1">
        <el-table
          :data="NERExtractData"
          height="400px"
          header-cell-style="background:#dfeef8;color:black">
          <el-table-column prop="sentence_content" align="center" label="句子" :show-overflow-tooltip="true"></el-table-column>
          <el-table-column align="center" label="操作" width="210px" #default="scope">
            <el-button type="success" @click="dialogFormVisible = true;setValue(scope)">编辑<i class="el-icon-edit"></i></el-button>
            <el-button type="danger" @click="setValue(scope);open()">删除<i class="el-icon-info"></i></el-button>
          </el-table-column>
        </el-table>
      </el-col>

      <el-dialog title="文献句子信息"  :visible.sync="dialogFormVisible" width="600px" :append-to-body="true">
        <el-form :model="NERExtractDataForm" ref="NERExtractDataForm" status-icon="true">
          <el-form-item prop="entity_content" label = "句子" label-width=60px>
            <el-col>
              <el-input type = "textarea" v-model="NERExtractDataForm.sentence_content"></el-input>
            </el-col>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer" style="text-align: center">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="submitForm('NERExtractDataForm');">保存</el-button>
        </div>
      </el-dialog>

      <el-col v-show="isPreProcessed===1" style="margin-top: 20px">
        <div align="center"><el-tag>预处理完成</el-tag></div>
      </el-col>
  </div>
</template>

<script>
export default {
  name: "preProcess",
  data () {
    return {
      dialogFormVisible: false,
      dialog2FormVisible: false,
      formLabelWidth: '120px',
      active: 0,
      isPreProcessed:0,
      showClue:0,
      started:0,
      btnName: '下一步',
      flag:0, // 用于提示信息
      article:'',
      articles:'',
      sentence:[],
      ref:[],
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
      patentData:[{
        titleE: '',
        authorE: '',
        l_abstractE: '',
        keywordsE: '',
        publish_date:'',
        reference_type:'',
        research_institute:'',
        volume:'',
        issue:'',
        doi:'',
        start_page:'',
        end_page:''
      }]
    }
  },
  mounted: function () {
    this.getLitName();
  },

  methods: {
    getLitName () {
      let params = {source:"Pre"};
      this.$axios.post('/demo/getLitName', params).then(res => {
        if (res.data.code === 1) {
          this.articles = JSON.parse(res.data.data);
        } else {
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })
    },

    run(){
      this.showClue = 1
      let params={
        article:this.article
      };
      this.$axios.post("/demo/pdfToTxt",params).then(res=>{
        if (res.data.code === 1) {
          this.$notify({
            title: '成功',
            message: res.data.msg,
            type: 'success'
          });
          this.flag +=1 ;
          this.isPreProcessed = 1
          this.showClue = 0
          this.getTableData()
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
    },
    display(){
      let params={
        article:this.article
      };
      this.$axios.post("/demo/display",params).then(res=>{
        if(res.data.code===1){
          this.sentence=JSON.parse(res.data.data)
          this.$notify({
            title:'已完成预处理',
            message:res.data.msg,
            type:'success'
          });
        }else {
          this.$notify({
            title:"请等待预处理完成后查看",
            message:res.data.msg,
            type:'warning'
          })
        }
      })
    },
    reference(){
      let params={
        article:this.article
      };
      this.$axios.post("/demo/reference",params).then(res=>{
        if(res.data.code===1){
          this.ref=JSON.parse(res.data.data)
          this.$notify({
            title:'已完成预处理',
            message:res.data.msg,
            type:'success'
          });
        }else {
          this.$notify({
            title:"请等待预处理完成后查看",
            message:res.data.msg,
            type:'warning'
          })
        }
      })
    },
    metaInfo(){
      let params={
        article:this.article
      };
      this.$axios.post("/demo/metaInfo",params).then(res=>{
        if(res.data.code===1){
          this.patentData=JSON.parse(res.data.data)
          this.$notify({
            title:'已完成预处理',
            message:res.data.msg,
            type:'success'
          });
        }else {
          this.$notify({
            title:"请等待预处理完成后查看",
            message:res.data.msg,
            type:'warning'
          })
        }
      })
    },

    show(){
      if (this.flag===0) {
        // this.display();
        // this.reference();
        this.metaInfo();
      }else {
        this.$notify({
          title: '警告',
          message: "请先完成pdf文本转换",
          type: 'warning'
        });
      }
    },
    getTableData () {
      let table_params = {
        topic: String(this.article)
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
    updatePreProcessResult () {
      let table_params = {
        sentence_content:this.NERExtractDataForm.sentence_content,
        sentence_id:this.NERExtractDataForm.sentence_id
      }
      console.log(this.NERExtractDataForm.sentence_id)
      this.$axios.post('/demo/updatePreProcessResult', table_params).then(res => {
        if (res.data.code === 1) {
          this.NERExtractData = JSON.parse(res.data.data)
        } else {
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })

    },
    deleteSentence () {
      let table_params = {
        sentence_id:this.NERExtractDataForm.sentence_id
      }
      console.log(this.NERExtractDataForm.sentence_id)
      this.$axios.post('/demo/deleteSentence', table_params).then(res => {
        if (res.data.code === 1) {
          this.$message({
            type: 'success',
            message: '删除成功!'
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
    submitForm(formName) {  // TODO 全要改
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.updatePreProcessResult();
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
    open() {
      this.$confirm('此操作将永久删除该句子, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.deleteSentence()
        this.getTableData()
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        });
      });
    },
    download(){
      let params={
        article:this.article
      };
      this.$axios.post("/demo/download",params).then(res=>{
        if (res.data.code === 1 &&this.flag===1) {
          let a = document.createElement('a');
          a.href = `./static/`+this.article+`.xlsx`;
          a.download = this.article+ '.xlsx';
          a.click();
          this.$notify({
            title: '成功',
            message: res.data.msg,
            type: 'success'
          });
        } else {
          this.$notify({
            title: '警告',
            message: "excel下载失败，请检查是否完成PDF转文本及其他错误",
            type: 'warning'
          });
        }
      })
    }
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
</style>
