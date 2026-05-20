<template>
  <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 h-full flex flex-col">
    <h3 class="text-sm font-medium text-slate-400 mb-4">
      Severity Breakdown
    </h3>
    <div class="flex-1 relative min-h-0">
      <Doughnut v-if="chartData" :data="chartData" :options="options" />
    </div>
  </div>
</template>

<script setup>
import {
  ArcElement,
  Chart as ChartJS,
  Legend,
  Title,
  Tooltip,
} from "chart.js";
import { computed } from "vue";
import { Doughnut } from "vue-chartjs";

ChartJS.register(ArcElement, Title, Tooltip, Legend);

const props = defineProps({ data: Array });

const colorMap = {
  critical: "#ef4444",
  high: "#f97316",
  medium: "#eab308",
  low: "#3b82f6",
  informational: "#64748b",
};

const chartData = computed(() => {
  if (!props.data?.length) return null;
  return {
    labels: props.data.map((d) => d.severity),
    datasets: [
      {
        data: props.data.map((d) => d.count),
        backgroundColor: props.data.map((d) => colorMap[d.severity] || "#64748b"),
        borderWidth: 0,
      },
    ],
  };
});

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: "bottom",
      labels: { color: "#94a3b8", padding: 16 },
    },
    tooltip: {
      backgroundColor: "#1e293b",
      borderColor: "#334155",
      borderWidth: 1,
      titleColor: "#e2e8f0",
      bodyColor: "#94a3b8",
    },
  },
};
</script>
