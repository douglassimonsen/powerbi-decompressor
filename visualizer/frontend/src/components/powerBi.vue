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
      pageAspectRatio: {},
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
      this.pageAspectRatio = {
        height: pageVisuals[0]?.page_height,
        width: pageVisuals[0]?.page_width,
      }
      let aspectRatio = this.getAspectRatio()
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
            height: `${x.height * aspectRatio.height / window.innerHeight * 100}vh`,
            width: `${x.width * aspectRatio.width / window.innerWidth * 100}vw`,
            top: `${x.y * aspectRatio.height / window.innerHeight * 100}vh`,
            left: `${x.x * aspectRatio.width / window.innerWidth * 100}vw`,
          }
        };
      })
    },
  },
  methods: {
    visualClick: function(id){
      this.$emit('visualClick', {id: id});
    },
    getAspectRatio: function(){
      let finalSize = {
        height: window.innerHeight * .6,
        width: window.innerWidth * .8,
      }
      return {
        height: finalSize.height / (this.pageAspectRatio.height || finalSize.height),
        width: finalSize.width / (this.pageAspectRatio.width || finalSize.width),
      }
    }
  },
}
</script>
<template>
  <div>
    <div>Original Size: {{pageAspectRatio.height}}x{{pageAspectRatio.width}}</div>
    <div class="pbi-container">
      <div 
        v-for="visual in pageVisuals" 
        :style="visual.style" 
        class="pbi-visual" 
        :key="visual.id"
        @click="visualClick(visual.id)"
      >{{visual.visual_type}}</div>
    </div>
    <div class="pbi-tabs">
      <div v-for="pageName in pageNames" class="pbi-tab" :class="+selectedPage === +pageName[0] ? 'selected': null" :key="pageName[0]" @click="selectedPage = pageName[0]">{{pageName[1]}}</div>
    </div>
  </div>
</template>
<style scoped>
.pbi-container {
  background-color: #ddd;
  height: 60vh;
  width: 80vw;
  position: relative;
}
.pbi-tabs {
  height: 80px;
  width: 80vw;
  background-color: blue;
  box-sizing: border-box;
    overflow-y: hidden;
    overflow-x: auto;
    white-space: nowrap;
    background: red;
}
.selected {
  background-color: rgb(17, 159, 175) !important;
}
.pbi-tabs div {
  height: 80px;
    width: auto;
    background-color: red;
    padding: 5px 10px;
    border: 1px solid black;
    font-size: 20px;
    margin: auto;
    display: inline-block;
}
.pbi-tab:hover {
  opacity: .8;
}
.pbi-visual:hover {
  opacity: .6;
}
</style>