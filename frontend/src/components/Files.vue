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
  data() {
    return {
      files: [],
      tab: "",
      active:false
    };
  },
  async created() {
    this.$parent.$on("opening_file", this.openingFile);
    /*const response = await fetch("http://127.0.0.1:8000/opened_files");
    const data = await response.json();
    this.files = data.files;
    console.log ('opned files ', this.files)
    this.fetching = false;*/
  },
  methods: {
    async closeFile(file) {
      let index = this.files.indexOf(file)
      this.files.splice(index, 1);
      const response = await fetch("http://127.0.0.1:8000/close_file/" + file);
      const data = await response.json();
      if (this.files.length > 0)
        this.openFile(this.files[0])
      return data;
    },
    async openFile(item) {
      console.log('open file files', item)
      const response = await fetch("http://127.0.0.1:8000/open_file/" + item);
      const data = await response.json();
      this.$parent.openFile(item);
      this.tab = item
      console.log("new tab", this.tab)
      console.log(data);
    },
    async openFileDic(item) {
      const name = item.detail.name
      console.log(name)
      
      const response = await fetch("http://127.0.0.1:8000/open_file/" + name );
      const data = await response.json();
      this.$parent.openFile(name);
      console.log(data);
    },
    openingFile(file) {
      console.log("openining", file)
      console.log(this.files)
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