<template>
  <div>
    <button @click="push">Push</button>
    <splitpanes class="main-content default-theme" >
      <pane v-for="item in data" :key="item.id" v-on:drop="drop($event, item.id)" v-on:dragover="allowDrop" min-size="15">
        <Files :files=item.files :id=item.id />
        <Texto :id=item.id @input='update' v-show='item.text === 1' @active="setActive"/>
        <EditDict v-show='item.text === 2' @active="setActive"/>
      </pane>
    </splitpanes>
  </div>
</template>

<script>

import Texto from "./Texto.vue";
import Files from "./Files.vue";
import EditDict from "./EditDictionary.vue";
import { Splitpanes, Pane } from 'splitpanes'
import 'splitpanes/dist/splitpanes.css'

export default {
  name: "Content",
  components: {
    Texto,
    Files,
    EditDict,
    Splitpanes, 
    Pane
  },
  data: function () {
    return { data: [], active: 1, overrideNextActive: false  };
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
  mounted: function(){
    window.setInterval(async () => {
      this.data.forEach(element => {
        this.saveCurrentFile(element.id)
      });
    }, 30000);
  },
  methods: {
    allowDrop:function(event) {
      event.preventDefault();
    },

    drop(event, id){
      var f = event.dataTransfer.getData("file");
      var p = event.dataTransfer.getData("panel");
      console.log(f, " from ", p, " to ",id)
    },

    async push(){
      console.log("Pre push", this.data)
      if (this.data.length == 1 && this.data[0].text != 1 )
        return;
      if (this.data[this.active].files.length == 1)
        return;
      let newid = this.data[this.data.length-1].id + 1
      
      let toOpen = ''
      let push = this.data[this.active].file;
      console.log("file to push", this.data[this.active].file)
      if (this.data[this.active].files[0] != push)
        toOpen = this.data[this.active].files[0]
      else 
        toOpen = this.data[this.active].files[1]
      console.log("File to leave open ", toOpen)
      await this.openFile({'panel':this.active, 'item': toOpen}, true)
      this.data.push({id:newid, content:"", file:"", text:1, files: [push]})
      this.active = newid
      console.log("POST push", this.data)
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
    async openFileDict(obj, save){
      this.openFile(obj, save)
      this.overrideNextActive = true
    },
    async openFile(obj, save) {
      if (obj.panel === 0 || obj.panel) {
        this.setActive(obj.panel)
      } else {
        var isOpenOn = this.checkFileisOpen(obj.item)
        if (isOpenOn != -1){
          console.log("File is already open on ", isOpenOn)
          this.setActive(isOpenOn)
        } else console.log("File was not open ")
      }
      console.log("Active panel is", this.active)

      let file = obj.item
      console.log ("open File ", file, " ",  save)
      if (file!=""){
        if (save){
          await this.saveCurrentFile()
        }
        const response = await fetch("http://127.0.0.1:8000/get_file/" + file);
        const data = await response.json();
        
        this.$emit("update_text", { panel: this.data[this.active].id, text: data.raw, file: file });
        this.$emit("opening_file", { panel: this.data[this.active].id, file: file })
        this.data[this.active].content = data.raw
        this.data[this.active].file = file
        console.log("Current open file ", )
        this.data[this.active].text = 1
      }
    },
    async saveCurrentFile(panel_id=-1){
      let panel_index
      if (panel_id == -1 )
        panel_index = this.active
      else panel_index = this.panel_index(panel_id)
      console.log("Save ", this.data[panel_index].file, " on ", this.data[panel_index].content)
      let filepost = {name:this.data[panel_index].file,content:this.data[panel_index].content}
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
      //this.data[this.active].file=''
      //this.data[this.active].content=''
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
      if(index == 0 || index) {
        if (this.data.length == 1)
          this.data[index].text = 3
        else {
          this.data.splice(index, 1);
          this.active = this.data.length-1
          console.log("Deleted panel ", panel, " with index ", index)
          console.log("New active is", this.active)
          console.log("POST DELETE", this.data)
        }
      }
    },
    setActive(panel){
      if (!this.overrideNextActive) {
        var index;
        this.data.forEach(element => {
            if (element.id == panel) {
              index = this.data.indexOf(element);
            }
        });
        this.active = index;
        console.log("New active is ", panel, " on index ", this.active)
      } else console.log("OVerride active")
      this.overrideNextActive = false
      if (typeof this.active == 'undefined')
        this.active = this.data[0].id
    },
    async closeFile(file, panelid){
      var index;
      this.data.forEach(element => {
        if (element.id == panelid) {
        index = this.data.indexOf(element);
        }
      });
      if (index) {
        await this.saveCurrentFile()
        let f_index = this.data[index].files.indexOf(file)
        console.log("content, ", this.data[index].files)
        
        console.log("content, ", this.data[index].files)
        await this.$emit('close_file', panelid, file)
        this.data[index].files.splice(f_index, 1)
        if (this.data[index].files.length == 0)
          this.noFileOpen(panelid)
      }      
    },
    panel_index(id){
      return id;
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