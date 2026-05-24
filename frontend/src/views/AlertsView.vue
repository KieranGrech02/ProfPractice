<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">Alerts</h2>

    <div class="flex gap-3 mb-4">
      <input
        v-model="search"
        @input="fetchAlerts"
        type="text"
        placeholder="Search alerts..."
        class="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500"
      />
      <select
        v-model="filterSeverity"
        @change="fetchAlerts"
        class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-cyan-500"
      >
        <option value="">All Severities</option>
        <option value="critical">Critical</option>
        <option value="high">High</option>
        <option value="medium">Medium</option>
        <option value="low">Low</option>
      </select>
      <select
        v-model="filterStatus"
        @change="fetchAlerts"
        class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-cyan-500"
      >
        <option value="">All Statuses</option>
        <option value="open">Open</option>
        <option value="investigating">Investigating</option>
        <option value="resolved">Resolved</option>
        <option value="false_positive">False Positive</option>
      </select>
    </div>

    <div class="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-slate-800 text-slate-400 text-left">
            <th class="px-4 py-3 font-medium">Severity</th>
            <th class="px-4 py-3 font-medium">Title</th>
            <th class="px-4 py-3 font-medium">Source</th>
            <th class="px-4 py-3 font-medium">MITRE Technique</th>
            <th class="px-4 py-3 font-medium">Status</th>
            <th class="px-4 py-3 font-medium">Time</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="alert in alerts"
            :key="alert.id"
            @click="$router.push(`/alerts/${alert.id}`)"
            class="border-b border-slate-800/50 hover:bg-slate-800/50 cursor-pointer transition-colors"
          >
            <td class="px-4 py-3">
              <SeverityBadge :severity="alert.severity" />
            </td>
            <td class="px-4 py-3 text-slate-200 max-w-md truncate">
              {{ alert.title }}
            </td>
            <td class="px-4 py-3 text-slate-400">{{ alert.source }}</td>
            <td class="px-4 py-3">
              <span
                v-if="alert.mitre_technique_id"
                class="text-cyan-400 font-mono text-xs"
              >
                {{ alert.mitre_technique_id }}
              </span>
            </td>
            <td class="px-4 py-3">
              <StatusBadge :status="alert.status" />
            </td>
            <td class="px-4 py-3 text-slate-500 text-xs">
              {{ formatTime(alert.created_at) }}
            </td>
          </tr>
        </tbody>
      </table>

      <p
        v-if="!alerts.length"
        class="text-center text-slate-500 py-8"
      >
        No alerts found.
      </p>
    </div>
  </div>
</template>

<script setup>
import api from "../services/api";
import { onMounted, ref } from "vue";
import SeverityBadge from "../components/SeverityBadge.vue";
import StatusBadge from "../components/StatusBadge.vue";

const alerts = ref([]);
const search = ref("");
const filterSeverity = ref("");
const filterStatus = ref("");

function formatTime(iso) {
  return new Date(iso).toLocaleString();
}

async function fetchAlerts() {
  let params = {};
  if (search.value) params.search = search.value;
  if (filterSeverity.value) params.severity = filterSeverity.value;
  if (filterStatus.value) params.status = filterStatus.value;
  const res = await api.getAlerts(params);
  alerts.value = res.data;
}

onMounted(fetchAlerts);
</script>
