<template>
<div @click="imActive">
    <b-table striped hover :fields="fields" :items="items">
     <template v-slot:cell(index)="data">
        <button @click="deleteKey(data.index)">Delete</button>
      </template>

      <template v-slot:cell(key)="data">
        <form @submit.prevent>
          <input type="text" v-model="data.item.key" v-on:keydown.enter="submitKey(data.item.original, data.item.key, data.index)">
        </form>
      </template>


      <template v-slot:cell(path)="data">
        <form @submit.prevent>
          <input type="text" v-model="data.item.value" v-on:keydown.enter="submitPath(data.item.key, data.item.value)">
        </form>
      </template>

    </b-table>

</div>
</template>

<script>
// 
// 
// 

export default {
  data() {
    return {
      fields: [
          // A column that needs custom formatting
          'key',
          // A regular column
          'path',
          'index',
          ],        
      
      items: [],
      parentContent: "",
      mainApp: ""
    };
  },
  async created() {
    this.parentContent = this.$parent.$parent.$parent
    this.mainApp = this.parentContent.$parent.$parent
    this.parentContent.$on("reloaddict", this.reload)
    this.reload()
  },
  async mounted() {
  },
  methods: {
    deleteKey(index) {
      let k = this.items[index].key;
      console.log("delete ", this.items[index].key);
      this.items.splice(index, 1);
      delete localStorage[k]
      this.mainApp.saveDict()
    },
    submitKey(key, newkey, index){
      console.log("Submit key ", key, newkey, index)
      let path = localStorage[key]
      delete localStorage[key]
      localStorage[newkey] = path
      this.reload()
    },
    submitPath(key, newPath){
      console.log("Submit path ", key, newPath)
      localStorage[key] = newPath
      this.mainApp.saveDict()
      this.reload()
    },
    reload(){
      this.items = []
      for (let i=0; i < localStorage.length; i++){
          let k = localStorage.key(i)
          this.items.push( {'key' : k , 'original':k, 'value' : localStorage[k]})
      }
    },
    imActive (){
      this.$emit("active", this.id)
    },
  }
};
</script>

<style>

</style>