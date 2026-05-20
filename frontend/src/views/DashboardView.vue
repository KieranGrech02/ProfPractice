<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">Dashboard</h2>

    <div class="grid grid-cols-4 gap-4 mb-6">
      <StatsCard
        label="Total Alerts"
        :value="stats.total_alerts"
        value-class="text-slate-100"
      />
      <StatsCard
        label="Open"
        :value="stats.open_alerts"
        value-class="text-red-400"
      />
      <StatsCard
        label="Investigating"
        :value="stats.investigating_alerts"
        value-class="text-yellow-400"
      />
      <StatsCard
        label="Resolved"
        :value="stats.resolved_alerts"
        value-class="text-green-400"
      />
    </div>

    <div class="grid grid-cols-4 gap-4 mb-6">
      <StatsCard
        label="Critical"
        :value="stats.critical_alerts"
        value-class="text-red-400"
      />
      <StatsCard
        label="High"
        :value="stats.high_alerts"
        value-class="text-orange-400"
      />
      <StatsCard
        label="Medium"
        :value="stats.medium_alerts"
        value-class="text-yellow-400"
      />
      <StatsCard
        label="Low"
        :value="stats.low_alerts"
        value-class="text-blue-400"
      />
    </div>

    <div class="grid grid-cols-3 gap-4">
      <div class="col-span-2 h-72">
        <AlertVolumeChart :data="alertVolume" />
      </div>
      <div class="h-72">
        <SeverityChart :data="severityBreakdown" />
      </div>
    </div>

    <div class="mt-4" style="height: 320px">
      <TopTechniquesChart :data="topTechniques" />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import AlertVolumeChart from "../components/charts/AlertVolumeChart.vue";
import SeverityChart from "../components/charts/SeverityChart.vue";
import TopTechniquesChart from "../components/charts/TopTechniquesChart.vue";
import StatsCard from "../components/StatsCard.vue";
import api from "../services/api";

const stats = ref({
  total_alerts: 0,
  open_alerts: 0,
  investigating_alerts: 0,
  resolved_alerts: 0,
  critical_alerts: 0,
  high_alerts: 0,
  medium_alerts: 0,
  low_alerts: 0,
});
const severityBreakdown = ref([]);
const topTechniques = ref([]);
const alertVolume = ref([]);

onMounted(async () => {
  const [statsRes, sevRes, techRes, volRes] = await Promise.all([
    api.getStats(),
    api.getSeverityBreakdown(),
    api.getTopTechniques(),
    api.getAlertVolume(),
  ]);
  stats.value = statsRes.data;
  severityBreakdown.value = sevRes.data;
  topTechniques.value = techRes.data;
  alertVolume.value = volRes.data;
});
</script>
