<template>
  <div class="main-content" v-bind:style="{ width: width + '%' }">
    <button @click="openDictionaryEditor"> Edit Dictionary </button>
    <Files />
    <Texto v-model="editorData" @input='update' v-show='text === 1'/>
    <EditDict v-show='text === 2'/>
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
    return { data: {content:"", file:""}, editorData:'a', width: 85.5, text:1 };
  },
  created: async function () {
    this.$parent.$parent.$on("open_file", this.openFile);
  },
  methods: {
    async openFile(file) {
      if (file!=""){
        console.log('openingfile')
        this.$emit("opening_file", file);
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
        const data1 = await response1.json();
        console.log(data1)
      }
      const response = await fetch("http://127.0.0.1:8000/get_file/" + file);
      const data = await response.json();
      
      this.$emit("update_text", { text: data.raw, file: file });
      this.data.content = data.raw
      this.data.file = file
      this.text = 1
      
    },
    update(text){
      this.data.content = text.content
      console.log('content     ', text)
    },
    openDictionaryEditor(){
      this.text = 2
    },
    noFileOpen(){
      this.text = 3
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