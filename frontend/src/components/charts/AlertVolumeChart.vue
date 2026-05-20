<template>
  <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 h-full flex flex-col">
    <h3 class="text-sm font-medium text-slate-400 mb-4">
      Alert Volume (30 Days)
    </h3>
    <div class="flex-1 relative min-h-0">
      <Line v-if="chartData" :data="chartData" :options="options" />
    </div>
  </div>
</template>

<script setup>
import {
  CategoryScale,
  Chart as ChartJS,
  Filler,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  Title,
  Tooltip,
} from "chart.js";
import { computed } from "vue";
import { Line } from "vue-chartjs";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
);

const props = defineProps({ data: Array });

const chartData = computed(() => {
  if (!props.data?.length) return null;
  return {
    labels: props.data.map((d) => d.date.slice(5)),
    datasets: [
      {
        label: "Alerts",
        data: props.data.map((d) => d.count),
        borderColor: "#06b6d4",
        backgroundColor: "rgba(6, 182, 212, 0.1)",
        fill: true,
        tension: 0.3,
        pointRadius: 0,
        pointHitRadius: 10,
      },
    ],
  };
});

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: "#1e293b",
      borderColor: "#334155",
      borderWidth: 1,
      titleColor: "#e2e8f0",
      bodyColor: "#94a3b8",
    },
  },
  scales: {
    x: {
      grid: { color: "rgba(51, 65, 85, 0.3)" },
      ticks: { color: "#64748b", maxTicksLimit: 10 },
    },
    y: {
      grid: { color: "rgba(51, 65, 85, 0.3)" },
      ticks: { color: "#64748b" },
      beginAtZero: true,
    },
  },
};
</script>
