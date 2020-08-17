<template>
  <div class="hello">
    <Sidebar class="side"/>
    <Content class="cont"/>
  </div>
</template>

<script>
import Content from "./Content.vue";
import Sidebar from "./Tree.vue";
export default {
  name: "CentralPanel",
  // props: {
  //   msg: String
  // },
  components: {
    Content,
    Sidebar,
  },
  async created() {
  },
  methods: {
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}

.side {
  z-index: 1000;
}
.cont {
  z-index: 1;
}

</style>
