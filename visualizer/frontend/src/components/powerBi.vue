<script>
export default {
  props: ['visuals'],
  data: function(){
    return {
      a: 0
    };
  },
  computed: {
    pageNames: function(){
      debugger;
      return ['a', 'b']
    }
  },
  watch: {
  },
}
</script>
<template>
  <div class="pbi-container">
    
  </div>
</template>
<style scoped>
.pbi-container {
  background-color: grey;
  height: 720px;
  width: 1280px;
}
</style>