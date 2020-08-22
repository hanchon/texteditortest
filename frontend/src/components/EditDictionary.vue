<template>
<div>
    <b-table striped hover :fields="fields" :items="items">
     <template v-slot:cell(index)="data">
        <button @click="deleteKey(data.index)">Delete</button>
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
    //load
    this.items = []
    for (let i=0; i < localStorage.length; i++){
        let k = localStorage.key(i)
        this.items.push( {'key' : k , 'value' : localStorage[k]})
    }

  },
  methods: {
    deleteKey(index) {
      let k = this.items[index].key;
      console.log("delete ", this.items[index].key);
      this.items.splice(index, 1);
      delete localStorage[k]
      this.$parent.$parent.$parent.saveDict()
      
    }
  }
};
</script>

<style>

</style>