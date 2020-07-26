<template>
  <div>
    <!-- <b-button v-b-toggle.sidebar-1>Explore Files</b-button> -->
    <!-- <b-sidebar id="sidebar-1" title="Sidebar" shadow> -->
    <div class="sidebar-test">
      <p v-if="this.fetching">Fetching files...</p>
      <ul v-else>
        <li v-for="item in this.files" v-bind:key="item">
          <button @click="openFile(item)">{{item}}</button>
        </li>
      </ul>
    </div>
    <!-- </b-sidebar>  -->
  </div>
</template>

<script>
export default {
  name: "sidebar",
  data() {
    return {
      files: [],
      fetching: true,
    };
  },
  async created() {
    const response = await fetch("http://127.0.0.1:8000/dir");
    const data = await response.json();
    this.files = data.data;
    this.fetching = false;
  },
  methods: {
    async openFile(item) {
      const response = await fetch("http://127.0.0.1:8000/open_file/" + item);
      const data = await response.json();
      this.$parent.openFile(item);
      console.log(data);
    },
  },
};
</script>

<style scoped>
.sidebar-test {
  width: 14%;
  display: block;
  float: left;
  position: fixed;
  height: 100%;
  background: #f7f7f7;
  border-right: 1px solid #dae3e9;
  padding-top: 2em;
}
</style>