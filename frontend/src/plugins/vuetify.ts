import Vue from 'vue';
import Vuetify from 'vuetify';
import colors from "vuetify/es5/util/colors";

Vue.use(Vuetify, {
  iconfont: 'md',
  theme: {
    primary: '#05B07A',
    secondary: colors.grey.darken1,
    accent: colors.shades.black,
    error: colors.red.accent3
  }
});
