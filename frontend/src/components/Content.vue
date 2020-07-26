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
    return { data: "" };
  },
  created: async function () {
    this.$parent.$on("open_file", this.openFile);
  },
  methods: {
    async openFile(file) {
      const response = await fetch("http://127.0.0.1:8000/get_file/" + file);
      const data = await response.json();
      if (data.raw) {
        this.$emit("update_text", { text: data.raw, file: file });
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