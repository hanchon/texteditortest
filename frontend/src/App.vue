<template>
  <div>
    <div>
      <b-navbar type="dark">
        <b-dropdown id="dropdown" text="File" >
          <b-dropdown-item class="context" href="#" @click="createProject">Create New Project</b-dropdown-item>
        </b-dropdown>
        <b-dropdown id="dropdown"  text="Projects" >
            <li v-for="item in items" :key="item.message">
               <b-dropdown-item class="context" href="#" @click="openProject(item)">{{ item }}</b-dropdown-item>
            </li>
        </b-dropdown>
      </b-navbar>
    </div>
    <div id="app" @updateDict='updateDict' @click="closeContext">
      <CentralPanel />
    </div>
  </div>
</template>

<script>
import CentralPanel from './components/CentralPanel.vue'
//import CreateDictionary from './plugins/addtodict/createDictionary';

export default {
  name: 'App',
  components: {
    CentralPanel
  },
  data () {
    return {
     items: []
    }
  },
  async created() {
    const response = await fetch("http://127.0.0.1:8000/init/");
    const data = await response.json();
    console.log(data.raw)

    const response1 = await fetch("http://127.0.0.1:8000/list_projects/");
    const data1 = await response1.json();
    console.log(data1.projects)
    this.items = data1.projects
  },
  async mounted() {
    this.openProject()
  },
  methods: {
    async createProject(){
      let dir = prompt("Project Name","");
      if (dir == null || dir == "") {
        return;
      }
      console.log("App ", dir)
      const response = await fetch("http://127.0.0.1:8000/create_new_project/"+dir);
      const res = await response.json();
      if (res.result) {
        this.openProject(dir)
      }
      this.items.push(dir)
    },
    async openProject(projectName='project'){
      console.log("Opening", projectName)
      const response = await fetch("http://127.0.0.1:8000/open_project/"+projectName);
      const data = await response.json();
      var dict = {}
      if (data.raw)
        dict =  JSON.parse(data.raw);
      
      for (var key in dict) {
        localStorage[key] = dict[key]
        console.log(key, dict[key])
      }
      this.$emit("reload");
    },
    async saveDict(){
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
      await response1.json();
    },
    async updateDict(file){
      this.saveDict()
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
        file.name = file.name +"/";
      }
      console.log("App ", file, person)
      const response = await fetch("http://127.0.0.1:8000/create_file/"+file.name+person);
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
      this.$emit("deleting_file", file);
      this.$emit("reload");

    },
    async removeDir(dir){
      const response = await fetch("http://127.0.0.1:8000/remove_directory/"+dir);
      await response.json();
      this.$emit("reload");
    },
    async closeContext(){
      this.$emit("closecontext");
    },
    async previewFiles(qwe){
      console.log("butttt", qwe)
    },
    async openFileFromFiles(file, shouldSave=true){
      const response = await fetch("http://127.0.0.1:8000/open_file/"+file);
      await response.json();
      this.$emit("open_file_tree", file, shouldSave)
    },
    async openFileFromTree(file, shouldSave=true){
      const response = await fetch("http://127.0.0.1:8000/open_file/"+file);
      await response.json();
      this.$emit("open_file_files", file, shouldSave)
    },
    openDictionaryEditor(){
      this.$emit("open_edit_dictionary")
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
  margin-top: 0px;
}

.context {
  z-index: 10000;
}

</style>
