<script>
const VISUAL_COLORS = {
  'slicer': 'green',
  'card': 'red',
  'textbox': 'grey',
  'card': 'blue',
  'barChart': '#aadd00',
  'scatterChart': '#aadd00',
  'scatterChart': '#aadd00',
  'lineStackedColumnComboChart': '#aadd00',
  'basicShape': 'grey',
}
export default {
  props: ['visuals'],
  data: function(){
    return {
      selectedPage: 0,
    };
  },
  mounted: function(){
    window.addEventListener('keydown', function(evt){
      if(evt.key === 'ArrowRight'){
        this.selectedPage = Math.min(this.selectedPage + 1, this.pageNames.length - 1);
      }
      if(evt.key === 'ArrowLeft'){
        this.selectedPage = Math.max(this.selectedPage - 1, 0);
      }
    }.bind(this));    
  },
  computed: {
    pageNames: function(){
      return Object.entries(Object.fromEntries(this.visuals.map(x => [x.ordinal, x.page_name]))).sort((a, b) => +a[0] > +b[0] ? 1 : -1)
    },
    pageVisuals: function(){
      let pageVisuals = this.visuals.filter(x => x.ordinal === +this.selectedPage).sort((a, b) => a.z < b.z ? 1 : -1);
      return pageVisuals.map(x => {
        return {
          id: x.id,
          visual_type: x.visual_type,
          style: {
            position: 'absolute',
            display: 'grid',
            placeItems: 'center',
            fontSize: '20px',
            backgroundColor: VISUAL_COLORS[x.visual_type] || 'grey',
            height: `${x.height}px`,
            width: `${x.width}px`,
            top: `${x.y}px`,
            left: `${x.x}px`,
          }
        };
      })
    },
  },
}
</script>
<template>
  <div>
    <div class="pbi-container">
      <div v-for="visual in pageVisuals" :style="visual.style" class="pbi-visual" :key="visual.id">{{visual.visual_type}}</div>
    </div>
    <div class="pbi-tabs">
      <div v-for="pageName in pageNames" class="pbi-tab" :key="pageName[0]" @click="selectedPage = pageName[0]">{{pageName[1]}}</div>
    </div>
  </div>
</template>
<style scoped>
.pbi-container {
  background-color: #ddd;
  height: 720px;
  width: 1280px;
  position: relative;
}
.pbi-tabs {
  height: 80px;
  width: 1280px;
  background-color: blue;
}
.pbi-tab {
  height: 80px;
    width: auto;
    background-color: red;
    float: left;
    padding: 5px 10px;
    border: 1px solid black;
    font-size: 20px;
}
.pbi-tab:hover {
  opacity: .8;
}
.pbi-visual:hover {
  opacity: .6;
}
</style>