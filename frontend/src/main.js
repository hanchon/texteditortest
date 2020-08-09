import Vue from "vue";
import App from "./App.vue";
import { BootstrapVue, IconsPlugin } from "bootstrap-vue";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import CKEditor from '@ckeditor/ckeditor5-vue';
import slVueTree from 'sl-vue-tree';
import 'sl-vue-tree/dist/sl-vue-tree-dark.css';
Vue.component('sl-vue-tree', slVueTree);

import 'vue-awesome/icons';
import Icon from 'vue-awesome/components/Icon';
Vue.component('icon', Icon);

Vue.use( CKEditor );
Vue.use(BootstrapVue);
Vue.use(IconsPlugin);

Vue.config.productionTip = false;

new Vue({
  render: (h) => h(App),
}).$mount("#app");
