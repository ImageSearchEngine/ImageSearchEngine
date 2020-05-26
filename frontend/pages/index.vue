<template>
  <v-container
    class="fill-height"
    fluid
  >
    <v-row justify="center">
      <v-col
        cols="12"
        sm="8"
        md="4"
        style="text-align:center"
      >
        <logo />
        <v-combobox
          outlined
          rounded
          single-lined
          prepend-inner-icon="mdi-magnify"
          full-width
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
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Logo from '~/components/Logo.vue'
import myUpload from 'vue-image-crop-upload'
export default {
  components: {
    Logo,
    "my-upload": myUpload,
  },
  data () {
    return {
      imageName: "",
      imageID: "",
      showDialog: false,
      imageUrl: ''
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
    search: function () {
      if (this.imageName != "") {
        this.$router.push({
          path: "/search/",
          query: {
            'id': this.imageID,
          }
        })
      }
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
      this.imageID = jsonData.id
      this.imageUrl = `${this.backend}/upload/${this.imageID}`
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
