<template>
  <div>
    <el-tag>多文献上传</el-tag>
    <div v-show="showData===0">
      <el-card style="  background-color:whitesmoke;font-family: 微软雅黑;margin-top: 20px">
        <h3 style="text-align: center">多文献上传提示</h3>
        <p style="text-indent: 32.4px; line-height: 25px;text-align: center">
          多文件上传采用Excel+PDF形式，请下载设置好的Excel表格，按照要求填写文献元信息，再上传PDF，PDF以文献标题命名
        </p>
        <div align="center"><el-button  @click="download">Excel下载</el-button></div>
      </el-card>

      <!--  上传excel  -->
      <el-form style="margin-top: 15px" enctype="multipart/form-data" ref="form" :model="form" :rules="rules">
        <el-form-item label="文献元信息Excel" :label-width="formLabelWidth" style="margin-left: 100px" prop="excel">
          <el-input v-model="uploadExcel.inputExcel" style="width: 50%" placeholder="请上传填写完整的Excel表格"></el-input>
          <el-upload
            class="upload-demo inline_block"
            ref="upload1"
            action=""
            :file-list="uploadExcel.fileList"
            :on-change="handleSelectExcel"
            :http-request="overSubmitExcel"
            :show-file-list="false"
            accept=".xlsx"
            :limit="1"
            :before-upload="beforeUpload"
            :auto-upload="false">
            <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
            <el-button style="margin-left: 10px;" size="small" type="success" @click="submitExcel">上传到服务器</el-button>
          </el-upload>
        </el-form-item>
      </el-form>


        <el-form ref="form" :model="form" :rules="rules">
          <el-form-item label="上传文献" :label-width="formLabelWidth" style="margin-left: 100px" prop="cover">
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
    </div>

    <!-- Display -------------------------------------------------------->
    <el-row>
      <el-col :span="20" class="context" offset="2" v-show="showData===1" style="margin-top: 20px">
        <el-table class="table_class"
                  border

                  :header-cell-style="{borderColor:'black'}"
                  :data="returnPatentData"
                  header-cell-style="background:#dfeef8;color:black">
          <el-table-column label="文献名称" align="center" property="titleE" :show-overflow-tooltip="true"></el-table-column>
          <el-table-column label="关键字" align="center" property="keywordsE"></el-table-column>
          <el-table-column label="作者" align="center" property="authorE"></el-table-column>
          <el-table-column label="出版日期" align="center" property="publish_date"></el-table-column>
          <el-table-column label="文章类型" align="center" property="reference_type"></el-table-column>
          <el-table-column label="研究机构" align="center" property="research_institute"></el-table-column>
          <el-table-column label="DOI" align="center" property="doi" :show-overflow-tooltip="true"></el-table-column>
        </el-table>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
name: "multiFiles",
  data () {
    return{
      showData:0,
      formLabelWidth: '200px',
      patent:'',
      uploadForm:{    //上传多文件
        inputFile: '',
        fileList: [],
      },
      uploadExcel:{   //上传excel
        inputExcel:'',
        fileList:[],
      },
      form:{
        excel:null,
        multiPdf:null,
      },
      rules:{
        excel:[
          {required:true,message:'excel为必填项',trigger:'blur'}
        ],
        multiPdf:[
          {required:true,message:'pdf为必填项',trigger:'blur'}
        ]
      },
      fd:null,       //多文件formdata
      fd1:null,      //excel formdata
      fileStatus:false,  //excel文件状态
      fileStatus1:false, //多文件文件状态
      returnPatentData:[],
    }

  },
  methods: {
    download(){
      let a = document.createElement('a');
      a.href = `./static/MultiPatentInfo.xlsx`;
      a.download = '[NASICON]MultiPatentInfo.xlsx';
      a.click();
    },
    // 上传excel
    handleSelectExcel(file,fileList){
      if (fileList.length > 1) {
        fileList.shift();
      }
      this.uploadExcel.inputExcel=file.name;

      this.fileStatus= true;
      const fileSuffix = file.name.substring(file.name.lastIndexOf(".") + 1);
      const whiteList = ["xlsx"];
      if (whiteList.indexOf(fileSuffix) === -1) {
        this.$message.error('上传文件只能是 xlsx 格式');
        this.fileStatus= false;
      }
      const isLt2M = file.size / 1024 / 1024 < 10;
      if (!isLt2M) {
        this.$message.error('上传文件大小不能超过 10MB');
        this.fileStatus= false;
      }
    },
    overSubmitExcel(param){
      this.fd1 = new FormData();
      this.fd1.append('file',param.file);
    },
    beforeUpload(file) {
    },
    submitExcel(){
      if(this.fileStatus) {
        this.$refs.upload1.submit();
        this.$axios.post('/demo/MultiPatentInfoSubmit', this.fd1).then(res => {
          if (res.data.code === 1) {
            this.$notify({
              title: '成功',
              message: res.data.msg,
              type: 'success'
            });
            this.fileStatus= false;
            this.uploadExcel.inputExcel='';
            this.showData = 1;
            this.getPatentData()
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


    //PDF
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
.box{
  border-style:solid;
  border-width:1px;
  margin-top: 10px;
  margin-right: 200px;
  margin-left: 200px;
  -webkit-line-clamp: 3;
  text-align: center;
}
.el_button_center{
  margin-top: 15px;
  text-align: center;
}
.inline_block{
  display: inline-block;
}
</style>
