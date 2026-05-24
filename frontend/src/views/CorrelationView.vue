<template>
  <div>
    <h2 class="text-2xl font-bold mb-2">Alert Correlation Graph</h2>
    <p class="text-sm text-slate-400 mb-4">
      Alerts connected by shared indicators — IP addresses, hostnames,
      usernames, and file hashes.
    </p>

    <div class="flex gap-4 mb-4">
      <div class="flex items-center gap-4 text-xs text-slate-400">
        <span class="flex items-center gap-1.5">
          <span class="w-3 h-3 rounded-full bg-red-500 inline-block"></span>
          Critical
        </span>
        <span class="flex items-center gap-1.5">
          <span class="w-3 h-3 rounded-full bg-orange-500 inline-block"></span>
          High
        </span>
        <span class="flex items-center gap-1.5">
          <span class="w-3 h-3 rounded-full bg-yellow-500 inline-block"></span>
          Medium
        </span>
        <span class="flex items-center gap-1.5">
          <span class="w-3 h-3 rounded-full bg-blue-500 inline-block"></span>
          Low
        </span>
      </div>
      <div class="flex items-center gap-4 text-xs text-slate-500 ml-auto">
        <span>Scroll to zoom</span>
        <span>Drag nodes to rearrange</span>
        <span>Click node for details</span>
      </div>
    </div>

    <div
      class="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden relative"
      style="height: 600px"
    >
      <svg ref="svgRef" class="w-full h-full"></svg>

      <div
        v-if="tooltip.visible"
        class="absolute pointer-events-none bg-slate-800 border border-slate-700 rounded-lg p-3 shadow-xl z-10 max-w-xs"
        :style="{ left: tooltip.x + 'px', top: tooltip.y + 'px' }"
      >
        <p class="text-sm font-medium text-slate-100">{{ tooltip.title }}</p>
        <div class="mt-1.5 space-y-1 text-xs text-slate-400">
          <p>
            Severity:
            <span :class="severityTextClass(tooltip.severity)">{{
              tooltip.severity
            }}</span>
          </p>
          <p v-if="tooltip.technique">
            MITRE:
            <span class="text-cyan-400">{{ tooltip.technique }}</span>
          </p>
          <p v-if="tooltip.source_ip">
            Source IP:
            <span class="text-slate-300 font-mono">{{
              tooltip.source_ip
            }}</span>
          </p>
          <p v-if="tooltip.hostname">
            Host:
            <span class="text-slate-300">{{ tooltip.hostname }}</span>
          </p>
          <p>
            Connections:
            <span class="text-slate-300">{{ tooltip.connections }}</span>
          </p>
        </div>
      </div>
    </div>

    <div class="mt-6">
      <h3 class="text-lg font-semibold mb-3">Correlated Clusters</h3>
      <div class="grid grid-cols-1 gap-3">
        <div
          v-for="cluster in clusters"
          :key="cluster.id"
          class="bg-slate-900 border border-slate-800 rounded-xl p-4"
        >
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center gap-2">
              <span
                class="px-2 py-0.5 rounded-full text-xs font-medium"
                :class="severityBadgeClass(cluster.max_severity)"
              >
                {{ cluster.max_severity }}
              </span>
              <span class="text-sm text-slate-200">
                {{ cluster.alert_count }} correlated alerts
              </span>
            </div>
          </div>
          <div class="flex flex-wrap gap-1.5 mb-2">
            <span
              v-for="indicator in cluster.shared_indicators"
              :key="indicator"
              class="px-2 py-0.5 bg-slate-800 text-slate-400 text-xs rounded font-mono"
            >
              {{ indicator }}
            </span>
          </div>
          <div class="space-y-1">
            <button
              v-for="alert in cluster.alerts"
              :key="alert.id"
              @click="$router.push(`/alerts/${alert.id}`)"
              class="block w-full text-left px-2 py-1 text-xs text-slate-300 hover:bg-slate-800 rounded transition-colors"
            >
              #{{ alert.id }} — {{ alert.title }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import * as d3 from "d3";
import { onBeforeUnmount, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";

const router = useRouter();
const svgRef = ref(null);
const clusters = ref([]);
const tooltip = ref({
  visible: false,
  x: 0,
  y: 0,
  title: "",
  severity: "",
  technique: "",
  source_ip: "",
  hostname: "",
  connections: 0,
});

let simulation = null;

const SEVERITY_COLORS = {
  critical: "#ef4444",
  high: "#f97316",
  medium: "#eab308",
  low: "#3b82f6",
  informational: "#64748b",
};

const EDGE_COLORS = {
  source_ip: "#06b6d4",
  destination_ip: "#8b5cf6",
  hostname: "#10b981",
  username: "#f59e0b",
  file_hash: "#ef4444",
};

function severityTextClass(sev) {
  const map = {
    critical: "text-red-400",
    high: "text-orange-400",
    medium: "text-yellow-400",
    low: "text-blue-400",
  };
  return map[sev] || "text-slate-400";
}

function severityBadgeClass(sev) {
  const map = {
    critical: "bg-red-500/20 text-red-400",
    high: "bg-orange-500/20 text-orange-400",
    medium: "bg-yellow-500/20 text-yellow-400",
    low: "bg-blue-500/20 text-blue-400",
  };
  return map[sev] || "bg-slate-500/20 text-slate-400";
}

function buildGraph(graphData) {
  const svg = d3.select(svgRef.value);
  svg.selectAll("*").remove();

  const rect = svgRef.value.getBoundingClientRect();
  const width = rect.width;
  const height = rect.height;

  const g = svg.append("g");

  const zoom = d3
    .zoom()
    .scaleExtent([0.3, 4])
    .on("zoom", (event) => g.attr("transform", event.transform));
  svg.call(zoom);

  const nodes = graphData.nodes.map((n) => ({ ...n }));
  const edges = graphData.edges.map((e) => ({
    ...e,
    source: e.source,
    target: e.target,
  }));

  simulation = d3
    .forceSimulation(nodes)
    .force(
      "link",
      d3
        .forceLink(edges)
        .id((d) => d.id)
        .distance(60),
    )
    .force("charge", d3.forceManyBody().strength(-150))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collision", d3.forceCollide().radius(30));

  const link = g
    .append("g")
    .selectAll("line")
    .data(edges)
    .join("line")
    .attr("stroke", (d) => EDGE_COLORS[d.type] || "#334155")
    .attr("stroke-opacity", 0.4)
    .attr("stroke-width", 1.5);

  const nodeGroup = g
    .append("g")
    .selectAll("g")
    .data(nodes)
    .join("g")
    .call(
      d3
        .drag()
        .on("start", (event, d) => {
          if (!event.active) simulation.alphaTarget(0.3).restart();
          d.fx = d.x;
          d.fy = d.y;
        })
        .on("drag", (event, d) => {
          d.fx = event.x;
          d.fy = event.y;
        })
        .on("end", (event, d) => {
          if (!event.active) simulation.alphaTarget(0);
          d.fx = null;
          d.fy = null;
        }),
    );

  nodeGroup
    .append("circle")
    .attr("r", (d) => 8 + Math.min(d.connections * 2, 16))
    .attr("fill", (d) => SEVERITY_COLORS[d.severity] || "#64748b")
    .attr("fill-opacity", 0.8)
    .attr("stroke", (d) => SEVERITY_COLORS[d.severity] || "#64748b")
    .attr("stroke-width", 2)
    .attr("stroke-opacity", 0.4)
    .style("cursor", "pointer");

  nodeGroup
    .append("circle")
    .attr("r", (d) => 8 + Math.min(d.connections * 2, 16) + 4)
    .attr("fill", "transparent")
    .attr("stroke", (d) => SEVERITY_COLORS[d.severity] || "#64748b")
    .attr("stroke-width", 1)
    .attr("stroke-opacity", 0.15);

  nodeGroup
    .append("text")
    .text((d) => `#${d.id}`)
    .attr("text-anchor", "middle")
    .attr("dy", (d) => -(12 + Math.min(d.connections * 2, 16)))
    .attr("fill", "#94a3b8")
    .attr("font-size", "10px");

  nodeGroup
    .on("mouseover", (event, d) => {
      // console.log("hover", d.id, d.title);
      const svgRect = svgRef.value.getBoundingClientRect();
      tooltip.value = {
        visible: true,
        x: event.clientX - svgRect.left + 12,
        y: event.clientY - svgRect.top - 10,
        title: d.title,
        severity: d.severity,
        technique: d.mitre_technique_id
          ? `${d.mitre_technique_id} ${d.mitre_technique_name}`
          : "",
        source_ip: d.source_ip,
        hostname: d.hostname,
        connections: d.connections,
      };

      d3.select(event.currentTarget)
        .select("circle")
        .transition()
        .duration(150)
        .attr("fill-opacity", 1)
        .attr("stroke-opacity", 0.8);

      link
        .attr("stroke-opacity", (l) =>
          l.source.id === d.id || l.target.id === d.id ? 0.9 : 0.1,
        )
        .attr("stroke-width", (l) =>
          l.source.id === d.id || l.target.id === d.id ? 3 : 1,
        );
    })
    .on("mousemove", (event) => {
      const svgRect = svgRef.value.getBoundingClientRect();
      tooltip.value.x = event.clientX - svgRect.left + 12;
      tooltip.value.y = event.clientY - svgRect.top - 10;
    })
    .on("mouseout", () => {
      tooltip.value.visible = false;
      nodeGroup
        .select("circle")
        .transition()
        .duration(150)
        .attr("fill-opacity", 0.8)
        .attr("stroke-opacity", 0.4);
      link.attr("stroke-opacity", 0.4).attr("stroke-width", 1.5);
    })
    .on("click", (_, d) => {
      router.push(`/alerts/${d.id}`);
    });

  simulation.on("tick", () => {
    link
      .attr("x1", (d) => d.source.x)
      .attr("y1", (d) => d.source.y)
      .attr("x2", (d) => d.target.x)
      .attr("y2", (d) => d.target.y);

    nodeGroup.attr("transform", (d) => `translate(${d.x},${d.y})`);
  });

  svg.call(zoom.transform, d3.zoomIdentity.translate(0, 0).scale(0.9));
}

onMounted(async () => {
  const [graphRes, clusterRes] = await Promise.all([
    api.getCorrelationGraph(),
    api.getCorrelationClusters(),
  ]);
  clusters.value = clusterRes.data;
  buildGraph(graphRes.data);
});

onBeforeUnmount(() => {
  if (simulation) simulation.stop();
});
</script>
