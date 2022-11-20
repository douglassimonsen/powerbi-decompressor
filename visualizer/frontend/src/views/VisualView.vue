<script>
import powerBi from '../components/powerBi.vue';
import { useReportStore } from '../stores/report';
import { mapStores, mapState } from "pinia";

export default {
  components: { powerBi },
  computed: {
    ...mapStores(useReportStore),
    ...mapState(useReportStore, ['reports', 'visuals']),
    selectedReport: {
      get: function(){return this.reportStore.selectedReport},
      set: function(val){
        this.reportStore.selectedReport = val;
        this.reportStore.getData();
      },
    },
  },
  mounted: function(){
    this.reportStore.getData();
  },
  methods: {
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