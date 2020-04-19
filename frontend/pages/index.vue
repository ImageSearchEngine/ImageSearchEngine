<template>
  <v-container
    class="fill-height"
    fluid
  >
    <v-row justify="center">
      <v-col
        cols="12"
        sm="8"
        md="6"
        style="text-align:center"
      >
        <logo />
        <v-text-field
          v-model="keyWord"
          outlined
          rounded
          single-lined
          prepend-inner-icon="mdi-magnify"
          full-width
          @keydown.enter="search()"
        >

        </v-text-field>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Logo from '~/components/Logo.vue'
//import VuetifyLogo from '~/components/VuetifyLogo.vue'

export default {
  components: {
    Logo
  },
  data () {
    return {
      keyWord: ""
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
      }
    }
  }
}
</script>
