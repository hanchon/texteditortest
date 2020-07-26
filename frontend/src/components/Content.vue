<template>
  <div class="main-content">
    <Files />
    <Texto v-model="data" />
  </div>
</template>

<script>
import Texto from "./Texto.vue";
import Files from "./Files.vue";
export default {
  name: "Content",
  components: {
    Texto,
    Files,
  },
  data: function () {
    return { data: {content:"", file:""} };
  },
  created: async function () {
    this.$parent.$on("open_file", this.openFile);
  },
  methods: {
    async openFile(file) {
      if (file!=""){
        console.log("asdasdasd"+ this.data.content)
        const response = await fetch("http://127.0.0.1:8000/store_file/" + file + "/" + this.data.content);
        const data = await response.json();
        console.log(data)
      }
      const response = await fetch("http://127.0.0.1:8000/get_file/" + file);
      const data = await response.json();
      if (data.raw) {
        this.$emit("update_text", { text: data.raw, file: file });
        this.data.content = data.raw
        this.data.content = file
      }
    },
  },
};
</script>


<style scoped>
.main-content {
  width: 85.5%;
  display: block;
  float: left;
  margin-left: 14.5%;
}
</style>