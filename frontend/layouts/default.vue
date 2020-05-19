<template>
  <v-app dark>
    <div>
      <v-app-bar
        color="#212121"
        dark
        v-if="$route.path!='/'"
      >
        <img
          class="DoodleLogo"
          alt="Doodle Logo"
          src="/logo.png"
          style="height:60px;width:132px"
          @click="$router.push({path:'/'})"
        >
        <div style="height:100%">
          <v-text-field
            class="mx-4"
            v-model="keyWord"
            outlined
            single-lined
            prepend-inner-icon="mdi-magnify"
            @keydown.enter="search()"
          />
        </div>
        <v-dialog
          v-model="dialog"
          width="40%"
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
                    :items="['Any Size','Large','Medium','Mini']"
                    label="Image size"
                    v-model="size"
                    outlined
                  ></v-select>
                </v-col>
              </v-row>
              <v-row v-if="showColorPicker">
                <v-col>
                  <v-color-picker
                    class="ma-2"
                    hide-canvas
                    width="100%"
                    v-model="color"
                  ></v-color-picker>
                </v-col>
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
        <v-btn text>
          About us
        </v-btn>

      </v-app-bar>
    </div>
    <v-content style="width:100%">

      <nuxt />
    </v-content>
  </v-app>
</template>

<script>
export default {
  data () {
    return {
      dialog: false,
      size: "Any Size",
      color: "",
      keyWord: "",
      showColorPicker: false,
    }
  },
  mounted () {
    if (this.$route.path == "/search/") {
      this.keyWord = this.$route.query.keyword ? this.$route.query.keyword : ""
      this.size = this.$route.query.size ? this.$route.query.size : "Any Size"
      this.color = this.$route.query.color ? this.$route.query.color : ""
      if (this.color == "")
        this.showColorPicker = false
      else
        this.showColorPicker = true
    }
  },
  watch: {
    "$route.path": function (path) {
      if (this.$route.path == "/search/") {
        this.keyWord = this.$route.query.keyword ? this.$route.query.keyword : ""
        this.size = this.$route.query.size ? this.$route.query.size : "Any Size"
        this.color = this.$route.query.color ? this.$route.query.color : ""
        if (this.color == "")
          this.showColorPicker = false
        else
          this.showColorPicker = true
      }
    }
  },
  methods: {
    filter: function () {

      //console.log(this.size, this.color)
      let queryObj = Object.assign({}, this.$route.query, {
        size: this.size == 'Any Size' ? null : this.size.toLowerCase(),
        color: this.showColorPicker ? this.color : null
      })
      if (!queryObj.size)
        delete queryObj.size
      if (!queryObj.color)
        delete queryObj.color
      delete queryObj.page
      this.$router.push({
        path: "/search/",
        query: queryObj
      })
    },
    search: function () {
      let queryObj = Object.assign({}, this.$route.query, { 'keyword': this.keyWord })
      delete queryObj.page
      this.$router.push({
        path: "/search/",
        query: queryObj
      })
    }
  }
}
</script>
