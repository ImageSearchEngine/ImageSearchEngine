<template>
  <div style="width:100%">
    <v-row
      v-for="n in 6"
      :key="n"
      style="width:100%;margin:0 auto;"
    >
      <v-col
        v-for="nn in 5"
        :key="nn"
        style="width:20%;margin:0 auto;"
      >
        <v-dialog
          v-model="dialog"
          width="700px"
        >
          <template v-slot:activator="{ on }">
            <v-img
              src="https://cdn.vuetifyjs.com/images/cards/sunshine.jpg"
              height="200px"
              class="touchable"
              v-on='on'
            ></v-img>
          </template>
          <v-card>
            <v-img
              src="https://cdn.vuetifyjs.com/images/cards/house.jpg"
              width=100%
            ></v-img>
            <v-card-title class="ma-2">
              <span class="headline">Use Google's location service?</span>
            </v-card-title>
            <v-card-subtitle class="ma-2">Related images
            </v-card-subtitle>
            <Waterfall style="width:100%">
              <WaterfallItem
                v-for="(imgURL,idx) in imgURLs"
                :key="idx"
              >
                <v-img :src="imgURL"></v-img>
              </WaterfallItem>
            </Waterfall>
          </v-card>
        </v-dialog>

        <div
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
        </div>
      </v-col>
    </v-row>
    <div class="text-center ma-10">
      <v-pagination
        v-model="page"
        :length="15"
        circle
        :total-visible="9"
      ></v-pagination>
    </div>
  </div>
</template>
<script>
const Waterfall = require("vue2-waterfall").Waterfall;
const WaterfallItem = require("vue2-waterfall").WaterfallItem;
export default {
  components: {
    Waterfall: Waterfall,
    WaterfallItem: WaterfallItem
  },
  data () {
    return {
      page: 1,
      imgURLs: [
        "https://cdn.vuetifyjs.com/images/cards/sunshine.jpg",
        "https://cdn.vuetifyjs.com/images/cards/house.jpg",
        "https://cdn.vuetifyjs.com/images/cards/sunshine.jpg",
        "https://cdn.vuetifyjs.com/images/cards/house.jpg",
        "https://cdn.vuetifyjs.com/images/cards/house.jpg",
        "https://cdn.vuetifyjs.com/images/cards/house.jpg",
        "https://cdn.vuetifyjs.com/images/cards/sunshine.jpg",
        "https://cdn.vuetifyjs.com/images/cards/house.jpg",
        "https://cdn.vuetifyjs.com/images/cards/sunshine.jpg",
        "https://cdn.vuetifyjs.com/images/cards/house.jpg",
        "https://cdn.vuetifyjs.com/images/cards/house.jpg",
        "https://cdn.vuetifyjs.com/images/cards/house.jpg",
      ]
    }
  },
  mounted () {
    console.log(this.$route.path)
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
