<template>
  <div class="main-content" >
    <button @click="push">Push</button>
    <div v-for="item in data" :key="item.id">
      <Files :id=item.id />
      <Texto :id=item.id @input='update' v-show='item.text === 1'/>
      <EditDict v-show='item.text === 2'/>
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
    return { data: [{id:1, content:"", file:"", text:1}], active: 1  };
  },
  created: async function () {
    this.$parent.$parent.$on("open_file_files", this.openFile);
    this.$parent.$parent.$on("open_edit_dictionary", this.openDictionaryEditor);
    this.active = 1
  },
  methods: {
    async push(){
      this.data.push({id:this.data.length+1, content:"", file:"", text:1})
      this.active = this.data.length
    },
    async openFile(obj, save) {
      if (obj.panel)
        this.active = obj.panel
      let file = obj.item
      if (file!=""){
        if (save){
          await this.saveCurrentFile()
        }
        const response = await fetch("http://127.0.0.1:8000/get_file/" + file);
        const data = await response.json();
        
        this.$emit("update_text", { panel: this.active, text: data.raw, file: file });
        this.$emit("opening_file", { panel: this.active, file: file })
        this.data.content = data.raw
        this.data.file = file
        this.data[this.active-1].text = 1
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
      this.data[this.active-1].content = text.content
    },
    openDictionaryEditor(){
      this.$emit("reloaddict")
      this.data[this.active-1].text = 2
    },
    noFileOpen(panel){
      console.log(panel)
      if (this.data.length == 1)
        this.data[panel-1].text = 3
      else {
        this.active = this.data.length
        this.data.splice(panel-1, 1);
      }
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