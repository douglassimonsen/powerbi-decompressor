<script>
import * as d3Dag from "d3-dag";
import * as d3 from "d3";
import { mapState, mapStores } from 'pinia';
import { useReportStore } from "../stores/report";
export default {
  computed: {
    ...mapStores(useReportStore),
    ...mapState(useReportStore, ['report_dependencies', 'selectedVisual']),
    dependency_tree: function(){
      if(this.selectedVisual === null){
        return [];
      }
      let deps = this.reportStore.report_dependencies;
      let pbiIds = [...new Set(deps.map(x => `${x.child_type}-${x.child_id}`).concat(deps.map(x => `${x.parent_type}-${x.parent_id}`)))];
      pbiIds = pbiIds.map(x => {return {id: x.toString(), parentIds: []}});
      for(let i=0;i<deps.length;i++){
        let dep = deps[i];
        pbiIds.find(x => x.id === `${dep.child_type}-${dep.child_id}`).parentIds.push(`${dep.parent_type}-${dep.parent_id}`);
      }
      let selectedVisual = pbiIds.find(x => x.id === this.selectedVisual);
      pbiIds = pbiIds.filter(x => 
        x.id === this.selectedVisual || 
        x.parentIds.includes(this.selectedVisual) || 
        selectedVisual.parentIds.includes(x.id)
      );
      return pbiIds;
    }
  },
  methods: {
    updateVisual: function(){
      if(this.dependency_tree.length === 0){
        return;
      }
      const dag = d3Dag.dagStratify()(this.dependency_tree);
      const nodeRadius = 20;
      const layout = d3Dag
        .sugiyama() // base layout
        //.decross(d3Dag.decrossOpt()) // minimize number of crossings
        .nodeSize((node) => [(node ? 3.6 : 0.25) * nodeRadius, 3 * nodeRadius]); // set node size instead of constraining to fit
      const { width, height } = layout(dag);

      // --------------------------------
      // This code only handles rendering
      // --------------------------------
      const svgSelection = d3.select("#deps");
      svgSelection.attr("viewBox", [0, 0, width, height].join(" "));
      const defs = svgSelection.append("defs"); // For gradients
      const colorMap = {
        "column": "red",
        "visual": "orange",
        "page": "yellow",
        "measure": "green",
        "column": "blue",
      };
      // How to draw edges
      const line = d3
        .line()
        .curve(d3.curveCatmullRom)
        .x((d) => d.x)
        .y((d) => d.y);

      // Plot edges
      svgSelection
        .append("g")
        .selectAll("path")
        .data(dag.links())
        .enter()
        .append("path")
        .attr("d", ({ points }) => line(points))
        .attr("fill", "none")
        .attr("stroke-width", 3)
        .attr("stroke", "black");

      // Select nodes
      const nodes = svgSelection
        .append("g")
        .selectAll("g")
        .data(dag.descendants())
        .enter()
        .append("g")
        .attr("transform", ({ x, y }) => `translate(${x}, ${y})`);

      // Plot node circles
      nodes
        .append("circle")
        .attr("r", nodeRadius)
        .attr("fill", (n) => colorMap[n.data.id.split('-')[0]]);

      // Add text to nodes
      nodes
        .append("text")
        .text((d) => d.data.id)
        .attr("font-weight", "bold")
        .attr("font-family", "sans-serif")
        .attr("text-anchor", "middle")
        .attr("alignment-baseline", "middle")
        .attr("font-size", ".5em")
        .attr("fill", "white");
    },
  },
}
</script>
<template>
  <div>
    hello
    <svg id="deps"></svg>
    <button @click="updateVisual">update</button>
  </div>
</template>