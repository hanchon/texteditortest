<template>
  <div id="treefile" class="sidebar-test" @contextmenu.prevent="" @click="contextMenuIsVisible = false">

    <sl-vue-tree v-model="nodes" @nodeclick="nodeClick" @nodecontextmenu="nodecontextmenu" @drop="drop" >

      <template slot="toggle" slot-scope="{ node }">
          <span v-if="!node.isLeaf">
            <icon name="caret-right" v-if="!node.isExpanded"></icon>
            <icon name="caret-down"  v-if="node.isExpanded"></icon>
          </span>
      </template>

      <template slot="title" slot-scope="{ node }">
          <icon name="file" v-if="node.isLeaf"></icon> {{ node.title }} </template>

      <template slot="sidebar" slot-scope="{ node }">
          <icon name="circle" v-if="node.data.isModified"></icon>
      </template>
    </sl-vue-tree>
  <div class="contextmenu" ref="contextmenu" v-show="contextMenuIsVisible">
      <div @click="createFile">Create File</div>
      <div @click="createDirectory">Create Directory</div>
  </div>
  
  </div>

</template>

<script>

export default {
  name: 'app',
  data () {
    return {
     nodes: [],
     contextMenuIsVisible: false
    }
  },
  async mounted() {
    await this.reload()

    this.$parent.$parent.$on("reload", this.reload);
  },
  methods: {
    async nodeClick(node) {
      this.contextMenuIsVisible = false;
      this.node = node
      if (node.isLeaf) {
        console.log(node)
      // console.log(node.data.pathname);
        this.$parent.openFile(node.data.fullPath);
        const response = await fetch(
          "http://127.0.0.1:8000/open_file/" + node.data.fullPath
        );
        await response.json();
        console.log("path", node.data.fullPath)
        
      }
    },
    async nodecontextmenu(node) {
      this.node = node
      this.contextMenuIsVisible = true;
      const $contextMenu = this.$refs.contextmenu;
      $contextMenu.style.left = (event.clientX) + 'px';
      $contextMenu.style.top = (event.clientY) + 'px';
    },
    async drop(draggingNodes, position, event) {
      console.log(this.nodes)
      console.log("path", draggingNodes, position, event)
    },

    async createFile(){
      this.contextMenuIsVisible = false;
      console.log('createFile', this.node.data.fullPath)
      var path = this.node.data.fullPath
      if (this.node.isLeaf)
        path = path.substring(0, path.lastIndexOf("/"));
      this.$parent.$parent.createFile(path);

    },
    async createDirectory(){
      this.contextMenuIsVisible = false;
      console.log('createDirectory', this.node.data.fullPath)
      var path = this.node.data.fullPath
      if (this.node.isLeaf)
        path = path.substring(0, path.lastIndexOf("/"));
      this.$parent.$parent.createDirectory(path);
    },
    async reload(){
      this.contextMenuIsVisible = false;
      console.log("reload ")
      const response = await fetch("http://127.0.0.1:8000/dir");
      const data = await response.json();
      this.nodes = data.data;
    }
  }
}
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

  .contextmenu {
    position: fixed;
    background-color: white;
    color: black;
    border-radius: 2px;
    border-color: indigo;
    cursor: pointer;
  }

  .contextmenu > div {
    padding: 10px;
  }

  .contextmenu > div:hover {
    background-color: rgba(100, 100, 255, 0.5);
  }

</style>