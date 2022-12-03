import { defineStore } from 'pinia'
import axios from "axios";
const ENDPOINT = `http://${window.location.hostname}:5000/`
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
      dbCreds: {},
    }
  },
  getters: {
    updateDependencyFocus: function(state){
      return function(id){
        this.selectedVisual = id;
      }.bind(this);
    },
  },
  actions: {
    getCreds: function(){
      axios.post(ENDPOINT + "admin/creds", {}, {headers: HEADERS}).then(function(response){
        this.dbCreds = response.data;
      }.bind(this));
    },
    getEndpoint: function(apiEndpoint){
      axios.post(ENDPOINT + `api/query/${apiEndpoint}`, {
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
