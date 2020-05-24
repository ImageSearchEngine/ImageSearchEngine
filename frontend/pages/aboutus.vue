<template>
  <v-layout
    column
    justify-center
    align-center
  >
    <v-flex
      xs12
      sm8
      md6
    >
      <div class="text-center">
        <nuxt-link to="/">
          <logo />
        </nuxt-link>

        <nuxt-logo />
      </div>
      <v-card>
        <v-card-title class="headline">
          欢迎使用由徐天行和郑林楷小组开发的INRIA Holidays数据集上进行图片检索的网站Doodle。
        </v-card-title>
        <v-card-text>
          <p>Doodle是一个开源的项目，使用Facebook提出的multigrain模型进行基于内容的图片检索。</p>
          <p>
            如果您有任何的问题，请联系我们 <a
              href="https://github.com/fnoi2014xtx"
              target="_blank"
              title="contribute"
            >
              fnoi2014xtx
            </a>, <a
              href="https://github.com/Konano"
              target="_blank"
              title="contribute"
            >
              Konano
            </a>
          </p>
          <p>
            如果您发现任何bug，欢迎在Github上提出 <a
              href="https://github.com/ImageSearchEngine/ImageSearchEngine/issues"
              target="_blank"
              title="contribute"
            >
              issue board
            </a>
          </p>
          <p>本网站前端使用Nuxt.js + Vuetify搭建，后端使用Flask搭建，在此感谢三个项目对网站开发做出的贡献</p>
          <hr class="my-3">
          <a
            href="https://nuxtjs.org/"
            target="_blank"
          >
            Nuxt Documentation
          </a>
          <br>
          <a
            href="https://vuetifyjs.com/en/"
            target="_blank"
          >
            Vuetify Documentation
          </a>
          <br>
          <a
            href="https://dormousehole.readthedocs.io/en/latest/"
            target="_blank"
          >
            Flask Documentation
          </a>
        </v-card-text>
        <!--v-card-actions>
          <v-spacer />
          <v-btn
            color="primary"
            nuxt
            to="/inspire"
          >
            Continue
          </v-btn>
        </v-card-actions-->
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import Logo from '~/components/Logo.vue'
import NuxtLogo from '~/components/NuxtLogo.vue'

export default {
  auth: false,
  components: {
    Logo,
    NuxtLogo
  }
}
</script>
