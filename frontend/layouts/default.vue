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
            </v-card-title>
            <v-container>
              <v-row>
                <v-col>
                  <v-select
                    class="ma-2"
                    :items="['Any Size','Large','Medium','Mini']"
                    label="Image size"
                    outlined
                  ></v-select>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-color-picker
                    class="ma-2"
                    hide-canvas
                    width="100%"
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
                @click="dialog = false"
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
      keyWord: ""
    }
  },
  mounted () {
    if (this.$route.path == "/search/") {
      this.keyWord = this.$route.query.keyword
    }
  },
  watch: {
    "$route.path": function (path) {
      if (this.$route.path == "/search/") {
        this.keyWord = this.$route.query.keyword
      }
    }
  },
  methods: {
    search: function () {
      if (this.keyWord != "") {
        this.$router.push({
          path: "/search/",
          query: {
            'keyword': this.keyWord
          }
        })
      } else {
        this.$router.push({
          path: "/"
        })
      }
    }
  }
}
</script>
