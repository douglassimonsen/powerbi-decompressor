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
    this.getData();
    this.getReport();
  },
  methods: {
    getData: function(){
      axios.post(ENDPOINT + 'query/reports', {
        headers: HEADERS,
      }).then(function(response){
        this.reports = response.data;
      }.bind(this));
    },
    getReport: function(){
      axios.post(ENDPOINT + 'query/visuals', {
        id: this.selectedReport
      }, {
        headers: HEADERS,
      }).then(function(response){
        this.visuals = response.data;
      }.bind(this));
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
    <power-bi :visuals="visuals"></power-bi>
  </div>
</template>