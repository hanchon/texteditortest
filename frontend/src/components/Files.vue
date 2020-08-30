<template>
  <div id="filehandler" v-on:change="openFileDic">
    <b-nav tabs >
      <b-nav-item class='filetab' v-for="file in this.files" v-bind:key="file" @click="openFile(file)"   v-bind:class="{'active':(tab === file)}">
                <a> {{file.replace(/^.*[\\\/]/, '')}} </a>
        <button class='filetab' @click="closeFile(file)" v-on:click.stop>x</button>
      </b-nav-item>
      <b-nav-item class="filetab" @click="createFile">+</b-nav-item>
    </b-nav>
  </div>
</template>


<script>

//  :active='file === tab'
//v-bind:style='{"background-color" : (file === tab? "orange" : "red" )}'
//var filename = fullPath.replace(/^.*[\\\/]/, '')
export default {
  props: {
    id:Number
  },
  data() {
    return {
      files: [],
      tab: "",
    };
  },
  async created() {
    this.$parent.$on("opening_file", this.openingFile);
    this.$parent.$parent.$parent.$on("deleting_file", this.deletedFile);
    const response = await fetch("http://127.0.0.1:8000/opened_files");
    const data = await response.json();
    this.files = data.files;
    if (this.files.length > 0)
        this.openFile(this.files[0])
  },
  methods: {
    deletedFile(file){
      let short = file.replace('./','')
      console.log("deleted ", file)
      let index = this.files.indexOf(short)
      if (index > -1) {
        this.files.splice(index, 1);
        if (this.tab === short) {
          if (this.files.length > 0){
            this.openFile(this.files[0], false)
          }
        }
      }
    },
    async closeFile(file) {
      let index = this.files.indexOf(file)
      this.files.splice(index, 1);
      const response = await fetch("http://127.0.0.1:8000/close_file/" + file);
      const data = await response.json();
      if (this.files.length > 0)
        this.openFile(this.files[0])
      else this.$parent.noFileOpen(this.id);
      return data;
    },
    async openFile(item) {
      this.$parent.openFile({"panel":this.id, "item":item})
      this.$parent.$parent.$parent.openFileFromFiles(item);
      this.tab = item
    },
    async openFileDic(item) {
      const name = item.detail.name
      this.$parent.openFile(name)
       this.$parent.openFile({"panel":this.id, "item":name})
      console.log("name", name)
      this.$parent.$parent.$parent.openFileFromFiles(name);
    },
    openingFile(obj) {
      console.log("Active is ", obj.panel)
      if (obj.panel != this.id)
        return;
      let file = obj.file
      let short = file.replace('./','')
      if (!this.files.includes(short)){
        this.files.push(short)
        this.active = true
      }
      this.tab = short
    },
    createFile(){
      this.$parent.$parent.$parent.createFile({'name':"", 'complete':false})
    }
  },
  mounted: async function () {
    /*window.setInterval(async () => {
      const response = await fetch("http://127.0.0.1:8000/opened_files");
      const data = await response.json();
      this.files = data.files;
    }, 1000);*/
  },
};
</script>

<style>
/* Color not working, not overriding boostrap*/
.filetab {
  background-color: white;
  color: black; 
}

.active {
  background-color: lightgrey;
  color: black;

}

.nav-item > a:hover {
  color: grey;
  background-color: white;
}

</style>