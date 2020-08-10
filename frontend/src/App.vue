<template>
  <div id="app" @updateDict='updateDict'>
    <HelloWorld />
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
//import CreateDictionary from './plugins/addtodict/createDictionary';

export default {
  name: 'App',
  components: {
    HelloWorld
  },
  async created() {
    const response = await fetch("http://127.0.0.1:8000/open_project");
    const data = await response.json();
    var dict = {}
    if (data.raw)
      dict =  JSON.parse(data.raw);
    
    for (var key in dict) {
      localStorage[key] = dict[key]
      console.log(key, dict[key])
    }
  },
  methods: {
    async updateDict(file){
      var dict = {}
      for (let i=0; i < localStorage.length; i++){
        let k = localStorage.key(i)
        dict[k] = localStorage[k]
      }
      let filepost = {name:'.dict', content:JSON.stringify(dict)}
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
      console.log(data1, file.detail.name)

      await this.createFile(file.detail);
    },
    async createFile(file) {
      var person = ''
      if (!file.complete) {
        person = prompt("File name","");
        if (file.name == "")
          file.name = "."
        if (person == null || person == "") {
          return;
        }
      }
      console.log("App ", file, person)
      const response = await fetch("http://127.0.0.1:8000/create_file/"+file.name+"/"+person);
      await response.json();
      this.$emit("reload");
    },
    async createDirectory(dir){
      var person = prompt("Dir name", "");
      if (person == null || person == "") {
        return;
      }
      const response = await fetch("http://127.0.0.1:8000/create_directory/"+dir+"/"+person);
      await response.json();
      this.$emit("reload");
    },
    async removeFile(file){
      const response = await fetch("http://127.0.0.1:8000/remove_file/"+file);
      await response.json();
      this.$emit("reload");
    },
    async removeDir(dir){
      const response = await fetch("http://127.0.0.1:8000/remove_directory/"+dir);
      await response.json();
      this.$emit("reload");
    }


  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
