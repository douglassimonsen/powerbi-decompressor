import { defineStore } from 'pinia'
import axios from "axios";
const ENDPOINT = 'http://127.0.0.1:5000/api/'
const HEADERS = {
  'Access-Control-Allow-Origin': '*',
};
export const useReportStore = defineStore('report', {
  state() {
    return {
      reports: [],
      selectedReport: 2,

      visuals: [],
      selectedVisual: null,

      report_dependencies: [],
    }
  },
  actions: {
    getEndpoint: function(apiEndpoint){
      axios.post(ENDPOINT + `query/${apiEndpoint}`, {
        id: this.selectedReport
      }, {
        headers: HEADERS,
      }).then(function(apiEndpoint, response){
        this[apiEndpoint] = response.data;
      }.bind(this, apiEndpoint));
    },
    getData: function(){
      this.getEndpoint('reports');
      this.getEndpoint('visuals');
      this.getEndpoint('report_dependencies');
    },
  }
})
