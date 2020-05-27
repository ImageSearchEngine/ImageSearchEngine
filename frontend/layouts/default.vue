<template>
  <v-app dark>
    <div>
      <v-app-bar
        color="#212121"
        dark
        v-if="$route.path=='/search/' || $route.path=='/search'"
      >
        <img
          class="DoodleLogo"
          alt="Doodle Logo"
          src="/logo.png"
          style="height:60px;width:132px"
          @click="$router.push({path:'/'})"
        >
        <div style="height:100%">
          <v-combobox
            outlined
            class='mx-4'
            single-lined
            prepend-inner-icon="mdi-magnify"
            v-model="imageName"
            @keydown.prevent="keyDownListener"
            @focus.prevent="showDialog = imageName? false:true"
            autocomplete="off"
            ref="inputBox"
          >
            <template v-slot:selection="data">
              <v-chip
                pill
                close
                @click:close="remove()"
              >
                <v-avatar left>
                  <img :src="imageUrl"></v-avatar>
                {{ data.item }}
              </v-chip>
            </template>
          </v-combobox>
        </div>
        <v-dialog
          v-model="dialog"
          max-width="340"
        >
          <template v-slot:activator="{ on }">

            <v-btn
              icon
              v-on="on"
            >
              <v-icon>mdi-filter-outline</v-icon>
            </v-btn>
          </template>

          <v-card>
            <v-card-title primary-title>
              Filter
              <v-spacer />
              <v-switch
                v-model="showColorPicker"
                label="color"
              ></v-switch>
            </v-card-title>
            <v-container>
              <v-row>
                <v-col>
                  <v-select
                    class="ma-2"
                    :items="['any','large','medium','small']"
                    label="Image size"
                    v-model="size"
                    outlined
                  ></v-select>
                </v-col>
              </v-row>
              <v-row v-if="showColorPicker">
                <v-spacer />
                <v-col>
                  <v-color-picker
                    class="ma-2"
                    v-model="color"
                  ></v-color-picker>
                </v-col>
                <v-spacer />
              </v-row>
            </v-container>
            <v-divider></v-divider>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                text
                @click="dialog = false;filter()"
              >
                Apply
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-spacer></v-spacer>
        <v-btn
          text
          to='/aboutus/'
        >
          About us
        </v-btn>

      </v-app-bar>
    </div>
    <v-content style="width:100%">

      <nuxt />
      <my-upload
        field="image"
        :width="500"
        :height="500"
        url="/api/upload"
        withCredentials
        v-model="showDialog"
        @crop-success="cropSuccess"
        @crop-upload-success="cropUploadSuccess"
        @crop-upload-fail="cropUploadFail"
        img-format="png"
      />
    </v-content>
  </v-app>
</template>

<script>
import myUpload from 'vue-image-crop-upload'
const backendAddr = 'http://39.96.36.54:8388'
export default {
  components: {
    "my-upload": myUpload,
  },
  data () {
    return {
      showDialog: false,
      dialog: false,
      size: "any",
      color: "",
      imageName: "",
      imageUrl: "",
      imageID: "",
      showColorPicker: false,
      backend: backendAddr
    }
  },
  mounted () {
    if (this.$route.path == "/search/") {
      this.init()
    }
  },
  watch: {
    "$route.path": function (path) {
      if (this.$route.path == "/search/") {
        this.init()
      }
    },
    "$route.query": function (path) {
      if (this.$route.path == "/search/") {
        this.init()
      }
    }
  },
  methods: {
    keyDownListener (e) {
      if (e.key == 'Backspace')
        this.remove()
      else if (e.key == 'Enter')
        this.search()
    },
    remove () {
      this.imageName = ''
      this.imageUrl = ''
      this.imageID = ''
      this.showDialog = false
      this.$refs.inputBox.blur()
    },
    init: function () {
      if (this.$route.query.id) {
        this.imageID = this.$route.query.id
        this.imageName = '搜索图片'
        this.imageUrl = `${backendAddr}/upload/${this.imageID}?s=100y100`
      }
      console.log(this.$route.query)
      this.size = this.$route.query.size ? this.$route.query.size : "any"
      this.color = this.$route.query.color ? this.$route.query.color : ""
      if (this.color == "")
        this.showColorPicker = false
      else
        this.showColorPicker = true
    },
    filter: function () {

      //console.log(this.size, this.color)
      let queryObj = Object.assign({}, this.$route.query, {
        size: this.size == 'any' ? null : this.size,
        color: this.showColorPicker ? this.color : null
      })
      if (!queryObj.size)
        delete queryObj.size
      if (!queryObj.color)
        delete queryObj.color
      delete queryObj.page
      console.log('filter', queryObj)
      this.$router.push({
        path: "/search/",
        query: queryObj
      })
    },
    search: function () {
      let queryObj = Object.assign({}, this.$route.query, { 'id': this.imageID })
      delete queryObj.page
      this.$router.push({
        path: "/search/",
        query: queryObj
      })
    },
    cropSuccess (imgDataUrl, field) {
      console.log('-------- crop success --------')
      this.imageUrl = imgDataUrl
    },
    /**
     * upload success
     *
     * [param] jsonData   服务器返回数据，已进行json转码
     * [param] field
     */
    cropUploadSuccess (jsonData, field) {
      console.log('-------- upload success --------')
      this.imageName = '搜索图片'
      this.imageID = jsonData.img
      this.imageUrl = `${backendAddr}/upload/${this.imageID}?s=100y100`
    },
    /**
     * upload fail
     *
     * [param] status    server api return error status, like 500
     * [param] field
     */
    cropUploadFail (status, field) {
      console.log('-------- upload fail --------')
      this.imageID = ''
      this.imageUrl = ''
      this.imageName = ''
    }
  }
}
</script>
