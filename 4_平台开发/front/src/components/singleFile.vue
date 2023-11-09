<template>
  <div>
    <el-tag>单文献上传</el-tag>
    <el-row class="top_style">
      <el-col :span="20" class="context" offset="2">
        <el-steps :active="active" finish-status="success">
          <el-step title="文献内容" icon="el-icon-reading"></el-step>
          <el-step title="文献属性" icon="el-icon-edit"></el-step>
          <el-step title="文献PDF" icon="el-icon-s-data"></el-step>
        </el-steps>
      </el-col>
      <!-- 文献内容 -->
      <el-col :span="20" class="context"   v-show="active === 0" style="margin-top: 20px;margin-left: 5%">
        <el-form :model="patentData">
          <el-form-item label="标题(英文)" :label-width="formLabelWidth" >
            <el-input v-model="patentData.titleE" style="width: 80%"></el-input>
          </el-form-item>
          <el-form-item label="PDF命名" :label-width="formLabelWidth" >
            <el-input v-model="patentData.PDFName" style="width: 20%"></el-input>.pdf
          </el-form-item>
          <el-form-item label="作者(英文)" :label-width="formLabelWidth">
            <el-input v-model="patentData.authorE" style="width: 80%"></el-input>
          </el-form-item>
          <el-form-item label="摘要(英文)" :label-width="formLabelWidth">
            <el-input type="textarea" rows="4" v-model="patentData.l_abstractE" style="width: 80%"></el-input>
          </el-form-item>
          <el-form-item label="关键字(英文)" :label-width="formLabelWidth">
            <el-input v-model="patentData.keywordsE" style="width: 80%"></el-input>
          </el-form-item>
        </el-form>
      </el-col>
      <!-- 文献属性 -->
      <el-col :span="20" class="context" v-show="active === 1" style="margin-top: 20px;margin-left: 5%">
        <el-form :model="patentData" :rules="rules" ref="patentData">
          <el-form-item label="发表日期" :label-width="formLabelWidth">
            <el-date-picker v-model="patentData.publish_date"
                            value-format="yyyy-MM-dd"></el-date-picker>
          </el-form-item>
          <el-form-item label="文章类型" :label-width="formLabelWidth" >
            <el-select v-model="patentData.reference_type" >
              <el-option v-for="item in articleTypes" :key="item.id" :label="item.value" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="研究机构" :label-width="formLabelWidth">
            <el-input v-model="patentData.research_institute" style="width: 80%"></el-input>
          </el-form-item>
          <el-row>
            <el-col :span="8">
              <el-form-item label="卷" :label-width="formLabelWidth">
                <el-input v-model="patentData.volume" style="width: 80%" ></el-input>
              </el-form-item></el-col>
            <el-col :span="8"><el-form-item label="期" :label-width="formLabelWidth">
              <el-input v-model="patentData.issue" style="width: 80%" ></el-input>
            </el-form-item></el-col>
          </el-row>
          <el-form-item label="DOI" :label-width="formLabelWidth" prop="doi">
            <el-input v-model="patentData.doi" style="width: 80%" ></el-input>
          </el-form-item >
          <el-row>
            <el-col :span="8">
              <el-form-item label="起始页" :label-width="formLabelWidth">
                <el-input v-model="patentData.start_page" style="width: 80%"></el-input>
              </el-form-item></el-col>
            <el-col :span="8"><el-form-item label="结束页" :label-width="formLabelWidth">
              <el-input v-model="patentData.end_page" style="width: 80%" ></el-input>
            </el-form-item></el-col>
          </el-row>
        </el-form>
      </el-col>
      <!-- 文献PDF -->
      <el-col :span="20" class="context" v-show="active === 2" style="margin-top: 20px;margin-left: 5%">
        <el-form ref="form" :model="form" :rules="rules">
          <el-form-item label="上传文献" :label-width="formLabelWidth" prop="cover">
            <el-input v-model="uploadForm.inputFile" style="width: 50%" placeholder="（仅支持PDF格式上传，文件以文献标题命名）"></el-input>
            <el-upload
              class="upload-demo"
              ref="upload"
              action=""
              :file-list="uploadForm.fileList"
              :on-change="handleSelectFile"
              :http-request="overSubmit"
              :show-file-list="true"
              accept=".pdf"
              :limit="1"
              :before-upload="beforeUpload"
              :auto-upload="false"
              :model="form.cover">
              <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
              <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传到服务器</el-button>
              <div slot="tip" class="el-upload__tip">只能上传pdf文件，上传文件大小不能超过 100MB</div>
            </el-upload>
          </el-form-item>
        </el-form>
      </el-col>


      <!-- Display -------------------------------------------------------->
      <el-col :span="20" class="context" offset="2" v-show="active===3" style="margin-top: 20px">
          <el-table class="table_class"
                    border

                    :header-cell-style="{borderColor:'black'}"
                    :data="returnPatentData"
                    header-cell-style="background:#dfeef8;color:black">
            <el-table-column label="文献名称" align="center" property="titleE" :show-overflow-tooltip="true"></el-table-column>
            <el-table-column label="关键字" align="center" property="keywordsE" :show-overflow-tooltip="true"></el-table-column>
            <el-table-column label="作者" align="center" property="authorE"></el-table-column>
            <el-table-column label="出版日期" align="center" property="publish_date"></el-table-column>
            <el-table-column label="文章类型" align="center" property="reference_type"></el-table-column>
            <el-table-column label="研究机构" align="center" property="research_institute"></el-table-column>
            <el-table-column label="DOI" align="center" property="doi" :show-overflow-tooltip="true"></el-table-column>
          </el-table>
      </el-col>


      <el-col :span="8" class="context" offset="8" style="margin-top: 20px">
        <div align="center">
          <el-button @click="lastStep()" v-show="active!==0 && active<3">上一步</el-button>
          <el-button @click="save();nextStep()" v-show="active!==3">{{btnName}}</el-button>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "singleFile",
  data (){
    return{
      active: 0,
      headPipe:0,
      choose:1,
      isSingle:2,
      btnName:"下一步",
      formLabelWidth: '120px',

      articleTypes: [
        // {
        // value: '高温合金',
        // id: '1'
        // },
        {
          value: 'Nascion 固态电解质',
          id: '2'
        }],
      patentData: {
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
        end_page:'',
        PDFName:''
      },
      form:{
        cover:'',
      },
      uploadForm:{
        inputFile: '',
        fileList: [],
      },
      rules:{
        title:[
          {required:true,message:'title为必填项',trigger:'blur'}
        ],
        doi:[
          {required:true,message:'DOI为必填项',trigger:'blur'}
        ],
        cover:[
          {required:true,message:'pdf文件为必填项',trigger:'blur'}
        ]
      },
      returnPatentData:[],
    }
  },
  methods:{
    lastStep () {
      if (this.active < 1) {
        this.active = 0;
      } else{
        this.btnName = '下一步';
        this.active--;
      }
    },
    nextStep () {
      this.active++;
      if(this.active === 1){
        this.btnName = "提交文献基本信息"
      }
      if (this.active === 2) {
        this.btnName = '提交';
      }
      if(this.active >= 3 ){
        // this.headPipe = 0
        this.active = 3
        this.getPatentData()
        this.btnName = '完成';
      }
    },
  // 属性、内容写入数据库
    save() {
      console.log(this.active)
      //理论上要用valid的，但是好像是因为两个标签下，刷新了，所以导致出现了问题
      if (this.btnName === "提交文献基本信息"){
        console.log(this.active)
        if(this.patentData.titleE!==''&&this.patentData.doi!==''){
          this.addNewPatent();
        }else {
          this.$notify({
            title: '警告',
            message: "标题或DOI必填项未填写",
            type: 'warning'
          });
        }
      }
    },
    addNewPatent() {
      let params = {
        titleE: this.patentData.titleE,
        authorE: this.patentData.authorE,
        l_abstractE: this.patentData.l_abstractE,
        keywordsE: this.patentData.keywordsE,
        publish_date: this.patentData.publish_date,
        reference_type: this.patentData.reference_type,
        research_institute: this.patentData.research_institute,
        volume: this.patentData.volume,
        issue: this.patentData.issue,
        doi: this.patentData.doi,
        start_page: this.patentData.start_page,
        end_page: this.patentData.end_page,
        PDFName: this.patentData.PDFName
      };
      console.log(this.active)
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

    // PDF上传
    handleSelectFile(file, fileList) {   // 文件上传成功或者失败时调用，提示一些基本的错误：文件格式和文件大小
      if (fileList.length > 1) {
        fileList.shift();
      }
      this.uploadForm.inputFile=file.name;

      this.fileStatus= true;
      const fileSuffix = file.name.substring(file.name.lastIndexOf(".") + 1);
      const whiteList = ["pdf"];
      if (whiteList.indexOf(fileSuffix) === -1) {
        this.$message.error('上传文件只能是 pdf 格式');
        this.fileStatus= false;
      }

      const isLt2M = file.size / 1024 / 1024 < 10;
      if (!isLt2M) {
        this.$message.error('上传文件大小不能超过 10MB');
        this.fileStatus= false;
      }

    },
    overSubmit(param){
      this.fd = new FormData();
      let otherParams={
        aa:'aaa',
        bb:'bbb',
      };
      this.fd.append('otherParams',JSON.stringify(otherParams));
      this.fd.append('file',param.file);

    },
    beforeUpload(file) {
    },
    submitUpload(){     //  真正上传
      if(this.fileStatus) {
        this.$refs.upload.submit();
        this.$axios.post('/demo/selectFileUpload', this.fd).then(res => {
          if (res.data.code === 1) {
            this.$notify({
              title: '成功',
              message: res.data.msg,
              type: 'success'
            });
            this.fileStatus= false;
            this.uploadForm.inputFile='';
            this.active = 3
            this.getPatentData()
            this.btnName = '完成';
          } else {
            this.$notify({
              title: '警告',
              message: res.data.msg,
              type: 'warning'
            });
          }
        })
      }else {
        this.$message.error('请先上传合适的文件');
      }

    },


    //  展示上传
    getPatentData () {
      this.$axios.get('/demo/getPatentData').then(res => {
        if (res.data.code == 1) {
          this.returnPatentData = JSON.parse(res.data.data);
        } else {
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
        }
      })
    }
  }
}
</script>

<style scoped>

</style>
