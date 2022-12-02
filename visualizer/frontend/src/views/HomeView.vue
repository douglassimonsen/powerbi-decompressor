<script>
import { useReportStore } from '../stores/report';
import { mapStores, mapState } from "pinia";

export default {
  computed: {
    ...mapState(useReportStore, ['dbCreds']),
    ...mapStores(useReportStore),
  },
  mounted: function(){
    this.reportStore.getCreds();
  },
}

</script>

<template>
  <div>
    <div>To request a new feature, open an issue <a href="https://github.com/douglassimonsen/powerbi-decompressor/issues">here</a></div>
    <div>To directly access the database, use the following credentials</div>
    <table>
      <thead>
        <tr><th colspan=2>Creds</th></tr>
      </thead>
      <tbody>
        <tr v-for="(value, key) in dbCreds" :key="key">
          <td>{{key}}</td>
          <td>{{value}}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>

table {
  border: solid 1px #DDEEEE;
  border-collapse: collapse;
  border-spacing: 0;
  font: normal 13px Arial, sans-serif;
}
thead th {
  background-color: #DDEFEF;
  border: solid 1px #DDEEEE;
  color: #336B6B;
  padding: 10px;
  text-align: left;
  text-shadow: 1px 1px 1px #fff;
}
tbody td {
  border: solid 1px #DDEEEE;
  color: #333;
  padding: 10px;
  text-shadow: 1px 1px 1px #fff;
}
span {
  font-weight: bold;
}
</style>