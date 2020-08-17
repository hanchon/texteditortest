<template>
<div>
    <b-table striped hover :items="items">
    </b-table>

</div>
</template>

<script>
export default {
  data() {
    return {
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
  }
};
</script>

<style>

</style>