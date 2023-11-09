<template>
  <div class="home">
    <Menu />
    <h2>Vuecli4 力向导图示例</h2>
    <ForceDirected id="mytest" width="1200" height="600" :nodes="nodes" :edges="edges"></ForceDirected>
  </div>
</template>

<script>
// @ is an alias to /src
import ForceDirected from "./Force-Directed"

export default {
  name: "Home",
  components: {
    ForceDirected,
  },
  data() {
    return {
      // 节点集
      nodes : [
        { name: "天津大学" },
        { name: "智能与计算学部" },
        { name: "小超" },
        { name: "小丽" },
        { name: "小华" },
      ],
      // 边集
      edges : [
        { source: 0, target: 4, relation: "学生", value: 1.7 },
        { source: 0, target: 2, relation: "学生", value: 1.7 },
        { source: 0, target: 3, relation: "学生", value: 1.7 },
        { source: 0, target: 1, relation: "分院", value: 1.7 },
        { source: 2, target: 3, relation: "国顺aaa", value: 1.9 },
        { source: 2, target: 0, relation: "国顺bbb", value: 10 },
      ]
    };
  },
  methods:{
    charts(){
      const width = 928;
      const height = 680;

      const simulation = d3.forceSimulation()
        .force("charge", d3.forceManyBody())
        .force("link", d3.forceLink().id(d => d.id))
        .force("x", d3.forceX())
        .force("y", d3.forceY())
        .on("tick", ticked);

      const svg = d3.create("svg")
        .attr("viewBox", [-width / 2, -height / 2, width, height])
        .attr("width", width)
        .attr("height", height)
        .attr("style", "max-width: 100%; height: auto;");

      let link = svg.append("g")
        .attr("stroke", "#999")
        .attr("stroke-opacity", 0.6)
        .selectAll("line");

      let node = svg.append("g")
        .attr("stroke", "#fff")
        .attr("stroke-width", 1.5)
        .selectAll("circle");

      function ticked() {
        node.attr("cx", d => d.x)
          .attr("cy", d => d.y);

        link.attr("x1", d => d.source.x)
          .attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x)
          .attr("y2", d => d.target.y);
      }

      invalidation.then(() => simulation.stop());

      return Object.assign(svg.node(), {
        update({nodes, links}) {

          // Make a shallow copy to protect against mutation, while
          // recycling old nodes to preserve position and velocity.
          const old = new Map(node.data().map(d => [d.id, d]));
          nodes = nodes.map(d => ({...old.get(d.id), ... d}));
          links = links.map(d => ({...d}));

          node = node
            .data(nodes, d => d.id)
            .join(enter => enter.append("circle")
              .attr("r", 5)
              .call(drag(simulation))
              .call(node => node.append("title").text(d => d.id)));

          link = link
            .data(links, d => [d.source, d.target])
            .join("line");

          simulation.nodes(nodes);
          simulation.force("link").links(links);
          simulation.alpha(1).restart().tick();
          ticked(); // render now!
        }
      });
    }
  }
};
</script>

