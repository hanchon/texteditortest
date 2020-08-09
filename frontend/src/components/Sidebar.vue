<template>
  <div  @contextmenu.prevent="">
    <!-- <b-button v-b-toggle.sidebar-1>Explore Files</b-button> -->
    <!-- <b-sidebar id="sidebar-1" title="Sidebar" shadow> -->
    <div class="sidebar-test" >
      <p v-if="this.fetching">Fetching files...</p>
      <!-- <ul v-else>
        <li v-for="item in this.files" v-bind:key="item">
          <button @click="openFile(item)">{{item}}</button>
        </li>
      </ul>-->

      <!-- @nodeClick="nodeClick"
      @nodeDoubleClick="nodeDoubleClick"
      @nodeDrop="nodeDrop"-->
      <!-- <div @click="doDashboard">Dashboard</div>
      <div @click="doCustomers">Customers</div>-->

      <file-browser-tree id="file-tree" ref="filetree" class="column" @nodeClick="openFile" >
        <template slot="context-menu">
          <div @click='createFile'>Create File</div>
          <div @click='createDirectory'>Create Directory</div>
        </template>
      </file-browser-tree>
    </div>
  </div>
</template>

<script>
import FileBrowserTree from "vue-file-tree";
export default {
  name: "sidebar",
  components: {
    "file-browser-tree": FileBrowserTree,
  },
  data() {
    return {
      files: [],
      fetching: true,
      node: null,
      componentKey:0
    };
  },
  async mounted() {
    const response = await fetch("http://127.0.0.1:8000/dir");
    const data = await response.json();
    this.files = data.data;

    for (var f in this.files)
      console.log(this.files[f]);

    this.fetching = false;

    // directory
    // https://github.com/robogeek/vue-file-tree
    //this.$refs.filetree.addPathToTree("Directory", "dir", true);
    this.files.forEach((element) => {
      this.$refs.filetree.addPathToTree(element.data.fullPath, "", false);
    });

    this.$parent.$parent.$on("reload", this.reload);
  },
  methods: {
    async openFile(event, node) {
      // console.log(event);
      this.node = node
      if (node.isLeaf) {
      // console.log(node.title);
      // console.log(node.data.pathname);
        this.$parent.openFile(node.data.pathname);
        const response = await fetch(
          "http://127.0.0.1:8000/open_file/" + node.data.pathname
        );
        await response.json();
        console.log("path", node.data.pathname)
        
      }
    },

    async createFile(){
      console.log('createFile', this.node)
      this.$parent.$parent.createFile(this.node.data.pathname);

    },
    async createDirectory(){
      console.log('createDirectory', this.node.data.pathname)
      this.$parent.$parent.createDirectory(this.node.data.pathname);
    },
    async reload(){
      console.log("reload ")
    }
  },
};
</script>

<style>
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
