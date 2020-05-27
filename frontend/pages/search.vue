<template>
  <div style="width:100%">
    <v-row
      v-for="n in Math.ceil(imgIDs.length/4) "
      :key="n"
      style="width:100%;margin:0 auto;"
    >
      <v-col
        v-for="nn in 4"
        :key="nn"
        style="width:20%;margin:0 auto;"
      >
        <div v-if="(nn-1)+(n-1)*4<imgIDs.length">
          <v-dialog
            v-model="dialog"
            width="700px"
          >
            <template v-slot:activator="{ on }">
              <v-img
                :src="`${backend}/img/${imgIDs[(nn-1)+(n-1)*4]}?s=300y300`"
                height="200px"
                class="touchable"
                @click="focusImgID=imgIDs[(nn-1)+(n-1)*4]"
                v-on='on'
              ></v-img>
            </template>
            <v-card>
              <a
                :href="`${backend}/img/${focusImgID}`"
                target="_blank"
              >
                <v-img
                  :src="`${backend}/img/${focusImgID}?s=500y500`"
                  width=100%
                ></v-img>
              </a>
              <v-card-title class="ma-2">
                <span class="headline">Related images</span>
              </v-card-title>
              <Waterfall style="width:100%">
                <WaterfallItem
                  v-for="(imgID,idx) in relateImgIDs"
                  :key="idx"
                >
                  <v-img :src="`${backend}/img/${imgID}?s=300y300`"></v-img>
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
const Waterfall = require("vue2-waterfall").Waterfall
const WaterfallItem = require("vue2-waterfall").WaterfallItem
const clone = require('clone-deep')
const backendAddr = 'http://39.96.36.54:8388'
export default {
  components: {
    Waterfall: Waterfall,
    WaterfallItem: WaterfallItem
  },
  data () {
    return {
      page: 1,
      focusImgID: "",
      dialog: false,
      imgIDs: [],
      relateImgIDs: [],
      totalPage: 1,
      backend: backendAddr
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
      this.relateImgIDs = []
      this.$axios.post('/api/relate', {
        img: this.focusImgID,
        num: 20,
      }).then(
        res => {
          let data = res.data
          this.relateImgIDs = data.imgs
        },
        () => {
        }
      )
      //console.log(this.focusImgURL)
    }
  },
  methods: {
    init: function () {
      let queryObj = Object.assign({ page: 0, num: 20 }, this.$route.query)
      this.$axios.post('/api/search', queryObj).then(
        res => {
          let data = res.data

          this.totalPage = Math.floor(data.total / data.num) + 1
          this.page = queryObj.page ? parseInt(queryObj.page) + 1 : 1
          this.imgIDs = data.imgs
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
