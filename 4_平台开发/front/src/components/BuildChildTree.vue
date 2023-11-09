<template>
  <div>
    <el-row>
      <el-col :span="20" offset="2">
        <div class="box-card">
          <el-row>
            <el-col :span="20" class="context" offset="2">
              <el-input suffix-icon="el-icon-search" placeholder="请输入根节点名称" style="width: 200px" v-model="myinput"></el-input>
              <el-button @click="runChildTree()">确定</el-button>
            </el-col>
            <el-col :span="20" class="context" offset="2" v-show="isPicDone === 1"> <!--  -->
              <viewer>
                <img src="../assets/tree.png" alt="rq" style="width: 90%; height: 90%; object-fit:contain; cursor:pointer"/>
                <!--el-image-viewer ></el-image-viewer-->
              </viewer>
              <!--el-image-viewer ></el-image-viewer-->
            </el-col>
          </el-row>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "buildchildtree",
  data() {
    return {
      tableData: [],
      formLabelWidth: '120px',
      active: 0,
      btnName: '下一步',
      patentName: '',
      isPicDone: 0,
      value: '',
      myinput: '',
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
    lastStep() {
      if (this.active < 1) {
        this.active = 0;
      } else {
        this.btnName = '下一步';
        this.active--;
      }
    },

    runChildTree(){
      let param = {name:this.myinput};
      console.log(param)
      this.$axios.post('/demo/runChildTree', param).then(res => {
        if (1 === 1) { //res.data.value
          this.$notify({
            title: '成功',
            message: res.data.msg,
            type: 'success'
          });
          this.isPicDone=1;
        } else {
          this.$notify({
            title: '警告',
            message: res.data.msg,
            type: 'warning'
          });
          this.isPicDone=0;
        }
      })
    },
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

.box-card{
  background-color: #fff;
}
.context {
  margin-top: 20px;
  margin-bottom: 20px;
}

</style>

