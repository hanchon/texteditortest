<template>
  <div id="filehandler" v-on:change="openFileDic">
    <b-nav tabs>
      <b-nav-item>Create new file</b-nav-item>
      <b-nav-item v-for="file in this.files" v-bind:key="file">
        <span @click="openFile(file)">{{file}}</span>
        <button @click="closeFile(file)">(close)</button>
      </b-nav-item>
    </b-nav>
  </div>
</template>


<script>
export default {
  data() {
    return {
      files: [],
    };
  },
  async created() {
    const response = await fetch("http://127.0.0.1:8000/opened_files");
    const data = await response.json();
    this.files = data.files;
    this.fetching = false;
  },
  methods: {
    async closeFile(file) {
      const response = await fetch("http://127.0.0.1:8000/close_file/" + file);
      const data = await response.json();
      return data;
    },
    async openFile(item) {
      console.log(item)
      const response = await fetch("http://127.0.0.1:8000/open_file/" + item);
      const data = await response.json();
      this.$parent.openFile(item);
      console.log(data);
    },
      async openFileDic(item) {
      const name = item.detail.name
      console.log(name)
      
      const response = await fetch("http://127.0.0.1:8000/open_file/" + name );
      const data = await response.json();
      this.$parent.openFile(name);
      console.log(data);
    },
  },
  mounted: async function () {
    window.setInterval(async () => {
      const response = await fetch("http://127.0.0.1:8000/opened_files");
      const data = await response.json();
      this.files = data.files;
    }, 1000);
  },
};
</script>