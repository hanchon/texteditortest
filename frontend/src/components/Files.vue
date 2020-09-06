<template>
  <div id="filehandler" v-on:change="openFileDic" v-on:drop="dropBar($event, id)" v-on:dragover="allowDrop">
    <b-nav tabs >
      <b-nav-item class='filetab' v-for="file in this.files" v-bind:key="file" @click="openFile(file)"   v-bind:class="{'active':(tab === file)}"
      :draggable="true"  v-on:dragstart="drag($event, file, id)"  
      v-on:drop="drop($event, file, id)" v-on:dragover="allowDrop">
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
    id:Number,
    files: Array
  },
  data() {
    return {
      tab: "",
      parentContent: "",
      mainApp: ""
    };
  },
  async created() {
    this.parentContent = this.$parent.$parent.$parent
    this.mainApp = this.parentContent.$parent.$parent
    this.parentContent.$on("opening_file", this.openingFile);
    this.parentContent.$on("close_file", this.file_is_closing);
    this.mainApp.$on("deleting_file", this.deletedFile);
    console.log("Created panel ", this.id, "open file ", this.files)
    if (this.files.length > 0)
        this.openFile(this.files[0])
  },
  methods: {
    allowDrop:function(event) {
      event.preventDefault();
    },

    drop(event, file, id){
      event.stopPropagation();
      var f = event.dataTransfer.getData("file");
      var p = event.dataTransfer.getData("panel");
      console.log(f, " from ", p, " to ",file, " on ", id)
      if (p == id) {
        let origin = this.files.indexOf(f)
        let destiny = this.files.indexOf(file)
        this.files.splice(origin, 1)
        this.files.splice(destiny, 0, f)
        this.openFile(f)
      } else {
        console.log("Close ", f, "on panel ", p)
        this.parentContent.closeFile(f, p)
        let destiny = this.files.indexOf(file)
        this.files.splice(destiny, 0, f)
        this.openFile(f)
      }
      
    },
    dropBar(event, id){
      var f = event.dataTransfer.getData("file");
      var p = event.dataTransfer.getData("panel");
      console.log(f, " from ", p,  " on ", id)
      if (p == id) {
        let destiny = this.files.length
        let origin = this.files.indexOf(f)
        this.files.splice(origin, 1)
        this.files.splice(destiny, 0, f)
        this.openFile(f)
      }  else {
        console.log("Close ", f, "on panel ", p)
        this.parentContent.closeFile(f, p)
        let destiny = this.files.length
        this.files.splice(destiny, 0, f)
        this.openFile(f)
      }
    },
    drag(event, file, id){
      event.dataTransfer.setData("file", file);
      event.dataTransfer.setData("panel", id);
      console.log(event)
    },
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
      console.log("Close file ", file)
      let index = this.files.indexOf(file)
      if (index){
        this.files.splice(index, 1);
        const response = await fetch("http://127.0.0.1:8000/close_file/" + file);
        const data = await response.json();
        console.log("open files now ", this.files)
        if (this.files.length > 0)
          this.openFile(this.files[0])
        else this.parentContent.noFileOpen(this.id);
        return data;
      }
    },
    async openFile(item) {
      console.log(item)
      this.parentContent.openFile({"panel":this.id, "item":item}, true)
      this.mainApp.openFileFromFiles(item);
      this.tab = item
    },
    async openFileDic(item) {
      console.log("OPen File Dic", item.detail)
      const name = item.detail.name
      this.parentContent.openFileDict({"item":name}, true)
      console.log("name", name)
      this.mainApp.openFileFromFiles(name);
    },
    openingFile(obj) {
      console.log("Active is ", obj.panel)
      let file = obj.file
      let short = file.replace('./','')
      if (obj.panel != this.id) {
        if (this.files.includes(short)){
          let index = this.files.indexOf(short)
          this.files.splice(index, 1);
          if (this.files.length == 0)
            this.parentContent.noFileOpen(this.id);
        }
      } else {      
        if (!this.files.includes(short)){
          this.files.push(short)
          this.active = true
        }
        this.tab = short
      }
    },
    createFile(){
      this.mainApp.createFile({'name':"", 'complete':false})
    },
    file_is_closing(panelid, file){
      if (panelid == this.id){
        this.closeFile(file)
      }
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
  z-index: 0; 
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