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
  name: "HelloWorld",
  // props: {
  //   msg: String
  // },
  components: {
    Content,
    Sidebar,
  },
  async created() {
    this.$parent.$on("open_file", this.openFile)
  },
  methods: {
    openFile(file) {
      this.$emit("open_file", file);
    },
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
