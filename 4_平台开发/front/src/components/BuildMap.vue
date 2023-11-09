<template>
  <div>
    <el-row>
      <el-col :span="20" offset="2">
        <div class="box-card">
          <el-row>
            <div align="center" style="margin-top: 20px">
              <el-button align="center" v-show="started===0" type="primary" @click="runMap();started=1">构建知识图谱</el-button>
            </div>
            <el-col :span="20" class="context" offset="2" v-show="started===1">
              <p class="profile" v-show="isPicDone===0" >请稍候 </p>
              <div v-once>{{runMap()}}</div>
              <detail-pannel ref="detailPannel"></detail-pannel>
              <div id="map_building" style="height: 600px;"></div>
            </el-col>
          </el-row>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import Vis from 'vis';
import DetailPannel from "./DetailPannel";
import * as d3 from 'd3';
export default {
  name: "buildmap",
  components: {DetailPannel},
  data() {
    return {
      started:0,
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
      },
      map_nodes : '',
      map_edges : '',
    }
  },
  mounted: function () {
    this.runMap();
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
    drawMap(){
        var container = document.getElementById("map_building");

        var data = {
          nodes: this.map_nodes,
          edges: this.map_edges,
        };

        var options = {
          nodes: {
            shape: 'box', // custom circles using ctxRender: https://visjs.github.io/vis-network/docs/network/nodes.html
            size: 18,
            margin: 6,
            font: {
              size: 12,
              align: 'middle',
              face: 'Time New Romans',

              //vadjust: 0,
            }
          },
          edges: {
            font: {
              size: 10,
              align: 'middle',
              face: 'Time New Romans',

              //vadjust: 0,
            },
            endPointOffset: {
              from: 50,
              to: 50,
            },
            color: 'gray',
            arrows: {
              to: {
                enabled: true,
                scaleFactor: 0.5
              }
            },
            smooth: {
              enabled: true
            }
          },

          physics: {
            enabled: true
          }
        };
        var network = new Vis.Network(container, data, options);
    },
    runMap(){
      let param = {name:this.myinput}; //node_name:this.myinput
      this.$axios.post('/demo/runMap', param).then(res => {
        if (1 === 1) { //res.data.value
          // console.log(res.data);
          let strlist = res.data.split("\n");
          this.map_nodes = JSON.parse(strlist[0]);
          this.map_edges = JSON.parse(strlist[1]);
          console.log(strlist[0]);
          console.log(strlist[1]);
          console.log(this.map_nodes);
          console.log(this.map_edges);
          this.$notify({
            title: '成功',
            message: res.data.msg,
            type: 'success'
          });
          this.drawMap();
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
.profile{
  margin-left: 30px;
  margin-right: 30px;
  text-align: left;
  line-height: 32px;
  text-indent: 20px;
  word-spacing: 1px;
  letter-spacing: 0.8px;
  font-family: 'Nunito', sans-serif;
//font-family: "Times New Roman";
  font-size: 14px;
}

/* cyrillic-ext */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofIOOaBXso.woff2) format('woff2');
  unicode-range: U+0460-052F, U+1C80-1C88, U+20B4, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F;
}
/* cyrillic */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofIMeaBXso.woff2) format('woff2');
  unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;
}
/* vietnamese */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofIOuaBXso.woff2) format('woff2');
  unicode-range: U+0102-0103, U+0110-0111, U+0128-0129, U+0168-0169, U+01A0-01A1, U+01AF-01B0, U+1EA0-1EF9, U+20AB;
}
/* latin-ext */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofIO-aBXso.woff2) format('woff2');
  unicode-range: U+0100-024F, U+0259, U+1E00-1EFF, U+2020, U+20A0-20AB, U+20AD-20CF, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
/* latin */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofINeaB.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
/* cyrillic-ext */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofIOOaBXso.woff2) format('woff2');
  unicode-range: U+0460-052F, U+1C80-1C88, U+20B4, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F;
}
/* cyrillic */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofIMeaBXso.woff2) format('woff2');
  unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;
}
/* vietnamese */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofIOuaBXso.woff2) format('woff2');
  unicode-range: U+0102-0103, U+0110-0111, U+0128-0129, U+0168-0169, U+01A0-01A1, U+01AF-01B0, U+1EA0-1EF9, U+20AB;
}
/* latin-ext */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofIO-aBXso.woff2) format('woff2');
  unicode-range: U+0100-024F, U+0259, U+1E00-1EFF, U+2020, U+20A0-20AB, U+20AD-20CF, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
/* latin */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofINeaB.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
/* cyrillic-ext */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofIOOaBXso.woff2) format('woff2');
  unicode-range: U+0460-052F, U+1C80-1C88, U+20B4, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F;
}
/* cyrillic */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofIMeaBXso.woff2) format('woff2');
  unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;
}
/* vietnamese */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofIOuaBXso.woff2) format('woff2');
  unicode-range: U+0102-0103, U+0110-0111, U+0128-0129, U+0168-0169, U+01A0-01A1, U+01AF-01B0, U+1EA0-1EF9, U+20AB;
}
/* latin-ext */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofIO-aBXso.woff2) format('woff2');
  unicode-range: U+0100-024F, U+0259, U+1E00-1EFF, U+2020, U+20A0-20AB, U+20AD-20CF, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
/* latin */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofINeaB.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
/* cyrillic-ext */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 800;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofIOOaBXso.woff2) format('woff2');
  unicode-range: U+0460-052F, U+1C80-1C88, U+20B4, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F;
}
/* cyrillic */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 800;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofIMeaBXso.woff2) format('woff2');
  unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;
}
/* vietnamese */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 800;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofIOuaBXso.woff2) format('woff2');
  unicode-range: U+0102-0103, U+0110-0111, U+0128-0129, U+0168-0169, U+01A0-01A1, U+01AF-01B0, U+1EA0-1EF9, U+20AB;
}
/* latin-ext */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 800;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofIO-aBXso.woff2) format('woff2');
  unicode-range: U+0100-024F, U+0259, U+1E00-1EFF, U+2020, U+20A0-20AB, U+20AD-20CF, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
/* latin */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 800;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofINeaB.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
/* cyrillic-ext */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 900;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofIOOaBXso.woff2) format('woff2');
  unicode-range: U+0460-052F, U+1C80-1C88, U+20B4, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F;
}
/* cyrillic */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 900;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofIMeaBXso.woff2) format('woff2');
  unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;
}
/* vietnamese */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 900;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofIOuaBXso.woff2) format('woff2');
  unicode-range: U+0102-0103, U+0110-0111, U+0128-0129, U+0168-0169, U+01A0-01A1, U+01AF-01B0, U+1EA0-1EF9, U+20AB;
}
/* latin-ext */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 900;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofIO-aBXso.woff2) format('woff2');
  unicode-range: U+0100-024F, U+0259, U+1E00-1EFF, U+2020, U+20A0-20AB, U+20AD-20CF, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
/* latin */
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 900;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofINeaB.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
</style>

