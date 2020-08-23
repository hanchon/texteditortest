<template>
<div>
    <b-table striped hover :fields="fields" :items="items">
     <template v-slot:cell(index)="data">
        <button @click="deleteKey(data.index)">Delete</button>
      </template>

      <template v-slot:cell(key)="data">
        <form>
          <input type="text" v-model="data.item.key" v-on:keyup.enter="submitKey(data.item.original, data.item.key, data.index)">
        </form>
      </template>


      <template v-slot:cell(value)="data">
        <form>
          <input type="text" v-model="data.item.value" v-on:keyup.enter="submitPath(data.item.key, data.item.value)">
        </form>
      </template>

    </b-table>

</div>
</template>

<script>
export default {
  data() {
    return {
      fields: [
          // A column that needs custom formatting
          'key',
          // A regular column
          'value',
          'index',
          ],         
      
      items: []
    };
  },
  async created() {
    this.reload()
  },
  methods: {
    deleteKey(index) {
      let k = this.items[index].key;
      console.log("delete ", this.items[index].key);
      this.items.splice(index, 1);
      delete localStorage[k]
      this.$parent.$parent.$parent.saveDict()
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
      this.$parent.$parent.$parent.saveDict()
      this.reload()
    },
    reload(){
      this.items = []
      for (let i=0; i < localStorage.length; i++){
          let k = localStorage.key(i)
          this.items.push( {'key' : k , 'original':k, 'value' : localStorage[k]})
    }
    }
  }
};
</script>

<style>

</style>