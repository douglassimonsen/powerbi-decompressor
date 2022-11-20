<script>
import axios from "axios";
import powerBi from '../components/powerBi.vue';
const HEADERS = {
  'Access-Control-Allow-Origin': '*',
};
const ENDPOINT = 'http://127.0.0.1:5000/api/'
export default {
  components: { powerBi },
  data: function(){
    return {
      reports: [],
      selectedReport: 2,
      visuals: [],
    };
  },
  mounted: function(){
    this.getData('reports');
    this.getData('visuals');
  },
  methods: {
    getData: function(apiEndpoint){
      axios.post(ENDPOINT + `query/${apiEndpoint}`, {
        id: this.selectedReport
      }, {
        headers: HEADERS,
      }).then(function(apiEndpoint, response){
        this.$data[apiEndpoint] = response.data;
      }.bind(this, apiEndpoint));
    },
    visualClick: function(evt){
      debugger;
    },
  },
}
</script>
<template>
  <div>
    <select v-model="selectedReport">
      <option v-for="report in reports" :value="report.id">{{report.name}}</option>
    </select>
    <button @click="getReport">Open</button>
    <power-bi :visuals="visuals" @visual-click="visualClick"></power-bi>
  </div>
</template>