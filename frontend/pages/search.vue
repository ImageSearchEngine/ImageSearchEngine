<template>
  <div style="width:100%">
    <v-row
      v-for="n in Math.ceil(imgURLs.length/4) "
      :key="n"
      style="width:100%;margin:0 auto;"
    >
      <v-col
        v-for="nn in 4"
        :key="nn"
        style="width:20%;margin:0 auto;"
      >
        <div v-if="(nn-1)+(n-1)*4<imgURLs.length">
          <v-dialog
            v-model="dialog"
            width="700px"
          >
            <template v-slot:activator="{ on }">
              <v-img
                :src="imgURLs[(nn-1)+(n-1)*4]"
                height="200px"
                class="touchable"
                @click="focusImgURL=imgURLs[(nn-1)+(n-1)*4]"
                v-on='on'
              ></v-img>
            </template>
            <v-card>
              <v-img
                :src="imgURLs[(nn-1)+(n-1)*4]"
                width=100%
              ></v-img>
              <v-card-title class="ma-2">
                <span class="headline">Related images</span>
              </v-card-title>
              <Waterfall style="width:100%">
                <WaterfallItem
                  v-for="(imgURL,idx) in relateImgURLs"
                  :key="idx"
                >
                  <v-img :src="imgURL"></v-img>
                </WaterfallItem>
              </Waterfall>
            </v-card>
          </v-dialog>

          <!--div
            class="single-line"
            style="margin-top:1em;"
          >
            1,000 miles of wonder 1,000 miles of wonder 1,000 miles of wonder 1,000 miles of wonder
          </div>
          <div
            class="single-line"
            style="color:grey;font-size:0.8em;"
          >
            Top western road
          </div-->
        </div>
      </v-col>
    </v-row>
    <div class="text-center ma-10">
      <v-pagination
        v-model="page"
        :length="totalPage"
        circle
        :total-visible="9"
      ></v-pagination>
    </div>
  </div>
</template>
<script>
const Waterfall = require("vue2-waterfall").Waterfall;
const WaterfallItem = require("vue2-waterfall").WaterfallItem;
const clone = require('clone-deep');
export default {
  components: {
    Waterfall: Waterfall,
    WaterfallItem: WaterfallItem
  },
  asyncData (context) {
    let queryObj = Object.assign({ page: 0, pagesize: 20 }, context.query)
    console.log("query backend!")
    console.log(queryObj)
    return context.app.$axios.post('/api/search', queryObj).then(
      res => {
        let data = res.data
        /*
          {
              total: 119, //总共找到119条结果
              page: 0, //这是第0页的结果列表
              pagesize: 20, //每页返回20个
              imgURLs:[
                  '.....1.png',
                  '.....2.png',
              ]
          }
        */
        return {
          totalPage: Math.floor(data.total / data.pagesize) + 1,
          page: context.query.page ? parseInt(context.query.page) + 1 : 1,
          imgURLs: data.imgURLs
        }
      },
      () => {
        context.error({
          statusCode: 404,
          message: "参数存在问题"
        })
      }
    )
  },
  data () {
    return {
      page: 1,
      focusImgURL: "",
      dialog: false,
      imgURLs: [],
      relateImgURLs: []
    }
  },
  mounted () {
    console.log(this.$route.path)
  },
  watch: {
    "$route.query": function (newQuery) {
      let queryObj = Object.assign({}, newQuery)
      console.log(queryObj)
      this.$axios.post('/api/search', queryObj).then(
        res => {
          let data = res.data
          /*
            {
                total: 119, //总共找到119条结果
                page: 0, //这是第0页的结果列表
                pagesize: 20, //每页返回20个
                imgURLs:[
                    '.....1.png',
                    '.....2.png',
                ]
            }
          */
          this.totalPage = Math.floor(data.total / data.pagesize) + 1
          this.page = this.$route.query.page ? parseInt(this.$route.query.page) + 1 : 1
          this.imgURLs = data.imgURLs
        },
        () => {
        }
      )
    },
    "page": function (newPage) {
      //console.log(this.$route.query)
      let queryObj = Object.assign({}, this.$route.query, { page: newPage - 1 })
      this.$router.push({
        path: "/search/",
        query: queryObj
      })
    },
    "dialog": function (newDialog) {
      //console.log(newDialog)
      this.relateImgURLs = []
      this.$axios.post('/api/relate', {
        imgURL: this.focusImgURL,
        maxsize: 40,
      }).then(
        res => {
          let data = res.data
          this.relateImgURLs = data.imgURLs
        },
        () => {
        }
      )
      //console.log(this.focusImgURL)
    }
  }
}
</script>
<style>
.single-line {
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}
.touchable:hover {
  cursor: pointer;
}
.single-line:hover {
  text-decoration: underline;
  cursor: pointer;
}
</style>
