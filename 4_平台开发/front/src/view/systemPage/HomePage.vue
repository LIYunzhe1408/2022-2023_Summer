<template xmlns:el-row="http://www.w3.org/1999/html">
  <el-row class="box_head">
    <!--h1>{{msg}}</h1-->
    <el-tabs   tab-position="right" class="top-card">
        <el-tab-pane label="Developer Team">

          <b><div class="module-topic" style="font-size: 24px;margin-top: 20px">开发者团队</div></b>
          <div style="margin-bottom: 20px">Wechat Profile Photo</div>
          <el-row class="demo-avatar demo-basic">
            <el-col :span="8">
              <!-- For Jonas -->
              <!-- For Jonas -->
              <!-- For Jonas -->
              <div class="demo-basic--circle">
                <div class="block">
                  <el-avatar shape="square" :size="200" :src="squareUrl">
                    <img src="../../assets/lyz.jpg" alt="lyz"/>
                  </el-avatar>
                </div>
                <div v-for="size in sizeList" :key="size" class="block">
                  <el-avatar shape="square" :size="size" :src="squareUrl" />
                </div>
              </div>
              <div class="sub-title">李昀哲 Jonas Li</div>
<!--              <div class="sub-title">李昀哲</div>-->
<!--              <el-col :span="12" offset='5' class="sub-col">-->
<!--                <ul>-->
<!--                  <li>Project 1</li>-->
<!--                  <li>Project 2</li>-->
<!--                  <li>......</li>-->
<!--                </ul>-->
<!--              </el-col>-->
            </el-col>




            <!-- For Leo -->
            <!-- For Leo -->
            <!-- For Leo -->
            <el-col :span="8">
              <div class="demo-basic--circle">
                <div class="block">
                  <el-avatar shape="square" :size="200" :src="squareUrl">
                    <img src="../../assets/IMG_0239.jpg" alt="IMG_0239" />
                  </el-avatar>
                </div>
              </div>
              <div class="sub-title">郑力铖 Leo Zheng</div>
<!--              <el-col :span="12" offset='5' class="sub-col">-->
<!--                <ul>-->
<!--                  <li>Project 1</li>-->
<!--                  <li>Project 2</li>-->
<!--                  <li>......</li>-->
<!--                </ul>-->
<!--              </el-col>-->
            </el-col>
            <!-- For zjy -->
            <!-- For zjy -->
            <!-- For zjy -->
            <el-col :span="8">
              <div class="demo-basic--circle">
                <div class="block">
                  <el-avatar shape="square" :size="200" :src="squareUrl">
                    <img src="../../assets/JoyCheung.jpg" alt="IMG_0239" />
                  </el-avatar>
                </div>
                <div v-for="size in sizeList" :key="size" class="block">
                  <el-avatar shape="square" :size="size" :src="squareUrl" />
                </div>
              </div>
              <div class="sub-title">张佳瑶 Joy Cheung</div>
              <!--              <el-col :span="12" offset='5' class="sub-col">-->
              <!--                <ul>-->
              <!--                  <li>Project 1</li>-->
              <!--                  <li>Project 2</li>-->
              <!--                  <li>......</li>-->
              <!--                </ul>-->
              <!--              </el-col>-->
            </el-col>

          </el-row>
        </el-tab-pane>
        <el-tab-pane label="What we do">
          <h2 class="module-topic">What we do</h2>
            <p class="profile">NASICON型(Na Super-Ion Conductors)复合物在十九世纪六十年代首次被发现，在1976年类材料被开发后，由Hong和Goodenough命名为“NASICON”。NASICON型材料目前被认为是适合高压固态电池的固体电解质。</p>
            <p class="profile"> NASICON型固态电解质因其原料成本低，安全性高，化学性质稳定、电导率高、电化学窗口宽等特点，成为了最具潜力的钠离子无机固态电解质[1]。鉴于开放的3D结构和高离子导电率，NASICON结构的化合物已经广泛开发应用于二次电池的电极材料和固体电解质材料。固态电池的离子导电性能取决于离子在固态电解质中的扩散，迁移离子的激活能是衡量NASICON型固态电解质材料离子输运性能的关键指标之一。因此，通过对NASICON型固态电解质材料激活能的准确预测，能够在一定程度上加速新型高性能固态电解质材料的发现过程。</p>
            <p class="profile">在预测激活能的过程中，描述符是一种有利的特征。大量有关预测激活能的描述符存在于NASICON型固态电解质相关的文献中。目前，绝大部分领域专家只能依靠亲自阅读相关文献，结合自身领域知识，手动提取描述符，然后再进行预测工作。这样的过程存在以下问题：其一，NASICON型固态电解质相关文献规模大、来源广泛，手动提取会消耗极大的时间、人力成本；其二，个体知识存在差别，考虑到描述符的选择至关重要，所以只是依靠人力难以及时获取最新的知识，导致提取描述符的准确度降低。</p>
            <p class="profile">本项目针对目前NASICON型固态电解质描述符的获取方式进行创新，提出面向NASICON型固态电解质的描述符自动获取的方法。</p>
            <p class="profile">主要流程是先对NASICON型固态电解质的文献预处理，再进行文献命名实体识别和关系抽取，最后基于预处理文献中提取的描述符，构建机器学习模型，实现NASICON型固态电解质描述符的自动获取。此方法目前在这个领域还未有团队深入研究，具有良好的发展前景和现实意义。</p>
        </el-tab-pane>
    </el-tabs>
  </el-row>

</template>


<script>
export default {
  name: 'HomePage',
  data () {
    return {
      msg: 'Welcome to platform for NASICON'
    }
  }
}
</script>


<style scoped>

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

.top-card{
  text-align: center;
}

.sub-title{
  margin-top: 30px;
  margin-bottom: 10px;
  font-size: 17px;

}

.demo-basic--circle{
  margin-top: 10px;
}

.box_head {
  position: relative;
  width: 100%;
  height: 45px;
  border-bottom: 1px solid #adcadd;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  /*background-color: #dfeef8;*/
}

.top-card{
  background-color: #dfeef8;
}

p,h1,h2,h3,h4,h5,h6,li,div{
  font-family: 'Nunito', sans-serif;
}
.sub-col{
  text-align: unset;
  background-color: #dfeef8;
  margin-bottom: 10px;
}

.module-topic{
  /*border-bottom: 2px solid #adcadd;*/
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
</style>
