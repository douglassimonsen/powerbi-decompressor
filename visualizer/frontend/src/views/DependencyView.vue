<script>
import * as d3Dag from "d3-dag";
import * as d3 from "d3";
import { mapState, mapStores } from 'pinia';
import { useReportStore } from "../stores/report";
export default {
  computed: {
    ...mapStores(useReportStore),
    ...mapState(useReportStore, 'report_dependencies'),
    dependency_tree: function(){
      let deps = this.reportStore.report_dependencies
      let pbiIds = [...new Set(deps.map(x => x.child_id).concat(deps.map(x => x.parent_id)))];
      pbiIds = pbiIds.map(x => {return {id: x.toString(), parentIds: []}});
      for(let i=0;i<deps.length;i++){
        let dep = deps[i];
        pbiIds.find(x => +x.id === dep.child_id).parentIds.push(dep.parent_id.toString());
      }
      return pbiIds;
    }
  },
  watch: {
    dependency_tree: function(){
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

      const colorMap = new Map();

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
        .attr("stroke", ({ source, target }) => {
          // encodeURIComponents for spaces, hope id doesn't have a `--` in it
          const gradId = encodeURIComponent(`${source.data.id}--${target.data.id}`);
          const grad = defs
            .append("linearGradient")
            .attr("id", gradId)
            .attr("gradientUnits", "userSpaceOnUse")
            .attr("x1", source.x)
            .attr("x2", target.x)
            .attr("y1", source.y)
            .attr("y2", target.y);
          grad
            .append("stop")
            .attr("offset", "0%")
            .attr("stop-color", colorMap.get(source.data.id));
          grad
            .append("stop")
            .attr("offset", "100%")
            .attr("stop-color", colorMap.get(target.data.id));
          return `url(#${gradId})`;
        });

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
        .attr("fill", (n) => colorMap.get(n.data.id));

      // Add text to nodes
      nodes
        .append("text")
        .text((d) => d.data.id)
        .attr("font-weight", "bold")
        .attr("font-family", "sans-serif")
        .attr("text-anchor", "middle")
        .attr("alignment-baseline", "middle")
        .attr("fill", "white");
    },
  },
}
</script>
<template>
  <div>
    <svg id="deps"></svg>
  </div>
</template>