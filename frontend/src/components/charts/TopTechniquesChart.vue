<template>
  <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 h-full flex flex-col">
    <h3 class="text-sm font-medium text-slate-400 mb-4">
      Top MITRE ATT&CK Techniques
    </h3>
    <div class="flex-1 relative min-h-0">
      <Bar v-if="chartData" :data="chartData" :options="options" />
    </div>
  </div>
</template>

<script setup>
import {
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  Title,
  Tooltip,
} from "chart.js";
import { computed } from "vue";
import { Bar } from "vue-chartjs";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const props = defineProps({ data: Array });

const chartData = computed(() => {
  if (!props.data?.length) return null;
  return {
    labels: props.data.map(
      (d) => `${d.technique_id} ${d.technique_name}`.slice(0, 30),
    ),
    datasets: [
      {
        label: "Alerts",
        data: props.data.map((d) => d.count),
        backgroundColor: "#06b6d4",
        borderRadius: 4,
      },
    ],
  };
});

const options = {
  indexAxis: "y",
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
      ticks: { color: "#64748b" },
      beginAtZero: true,
    },
    y: {
      grid: { display: false },
      ticks: { color: "#94a3b8", font: { size: 11 } },
    },
  },
};
</script>
