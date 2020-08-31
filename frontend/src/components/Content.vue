<template>
  <div class="main-content" >
    <button @click="push">Push</button>
    <div v-for="item in data" :key="item.id" v-on:drop="drop($event, item.id)" v-on:dragover="allowDrop">
      <Files :files=item.files :id=item.id />
      <Texto :id=item.id @input='update' v-show='item.text === 1' @active="setActive"/>
      <EditDict v-show='item.text === 2' @active="setActive"/>
    </div>
  </div>
</template>

<script>

import Texto from "./Texto.vue";
import Files from "./Files.vue";
import EditDict from "./EditDictionary.vue";
export default {
  name: "Content",
  components: {
    Texto,
    Files,
    EditDict
  },
  data: function () {
    return { data: [], active: 1  };
  },
  created: async function () {
    this.$parent.$parent.$on("open_file_files", this.openFile);
    this.$parent.$parent.$on("open_edit_dictionary", this.openDictionaryEditor);
    this.active = 0
    this.data.push({id:0, content:"", file:"", text:1, files: []})
    const response = await fetch("http://127.0.0.1:8000/opened_files");
    const data = await response.json();
    let files = data.files;
    this.data[0].files = files
  },
  methods: {
    allowDrop:function(event) {
      event.preventDefault();
    },

    drop(event, id){
       var data = event.dataTransfer.getData("Text");
      console.log(data, id)
    },

    async push(){
      if (this.data.length == 1 && this.data[0].text != 1 )
        return;
      if (this.data[this.active].files.length == 1)
        return;
      let newid = this.data[this.data.length-1].id + 1
      this.data.push({id:newid, content:"", file:"", text:1, files: [this.data.file]})
      this.active = newid
    },
    checkFileisOpen(file){
      var index = -1;
      this.data.forEach(element => {
        element.files.forEach(f => {
          if (f == file){
            index = element.id
          }
        })
      });
      return index;
    },
    async openFile(obj, save) {
      console.log("Complete data opeening file ", obj.item)
      console.log(this.data)
      console.log("openfile ", obj)
      console.log("File is open on ", this.checkFileisOpen(obj.item))
      if (obj.panel === 0 || obj.panel) {
        this.setActive(obj.panel)
        console.log("Opening file on ", obj.panel)
      } else {
        var isOpenOn = this.checkFileisOpen(obj.item)
        if (isOpenOn != -1)
          this.setActive(isOpenOn)
      }

      let file = obj.item
      if (file!=""){
        if (save){
          await this.saveCurrentFile()
        }
        const response = await fetch("http://127.0.0.1:8000/get_file/" + file);
        const data = await response.json();
        
        this.$emit("update_text", { panel: this.data[this.active].id, text: data.raw, file: file });
        this.$emit("opening_file", { panel: this.data[this.active].id, file: file })
        this.data.content = data.raw
        this.data.file = file
        this.data[this.active].text = 1
      }
    },
    async saveCurrentFile(){
      let filepost = {name:this.data.file,content:this.data.content}
      let settings = {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
        },
        body:JSON.stringify(filepost)
      }
      const response1 = await fetch("http://127.0.0.1:8000/save_filepost/", settings);
      await response1.json();
      this.data.file=''
      this.data.content=''
    },
    update(text){
      this.data[this.active].content = text.content
    },
    openDictionaryEditor(){
      this.$emit("reloaddict")
      this.data[this.active].text = 2
    },
    noFileOpen(panel){
      var index;
      this.data.forEach(element => {
        if (element.id == panel) {
        index = this.data.indexOf(element);
        }
      });
      console.log("No files open in id=", panel, " INDEX ",index)
      if (this.data.length == 1)
        this.data[index].text = 3
      else {
        this.data.splice(index, 1);
        this.active = this.data.length-1
        console.log("Deleted panel ", panel, " with index ", index)
        console.log("New active is", this.active)
      }
    },
    setActive(panel){
      var index;
      this.data.forEach(element => {
          if (element.id == panel) {
            index = this.data.indexOf(element);
          }
      });
      this.active = index;
      console.log("New active is ", panel, " on index ", this.active)
    }
  },
};
</script>


<style>
.main-content {
  position: relative;
  width: 85.5%;
  margin-left: 14.5%;
  z-index:1;
}


</style>