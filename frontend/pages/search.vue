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
  data () {
    return {
      page: 1,
      focusImgURL: "",
      dialog: false,
      imgURLs: [],
      relateImgURLs: [],
      totalPage: 1,
    }
  },
  mounted () {
    this.init()
  },
  watch: {
    "$route.query": function (newQuery) {
      this.init()
    },
    "page": function (newPage) {
      //console.log(this.$route.query)
      let queryObj = Object.assign({}, this.$route.query, { page: newPage - 1 })
      if (newPage == 1)
        delete queryObj.page
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
  },
  methods: {
    init: function () {
      let queryObj = Object.assign({ page: 0, pagesize: 20 }, this.$route.query)
      this.$axios.post('/api/search', queryObj).then(
        res => {
          let data = res.data

          this.totalPage = Math.floor(data.total / data.pagesize) + 1,
            this.page = queryObj.page ? parseInt(queryObj.page) + 1 : 1,
            this.imgURLs = data.imgURLs
        },
        () => {
          context.error({
            statusCode: 404,
            message: "参数存在问题"
          })
        }
      )
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
