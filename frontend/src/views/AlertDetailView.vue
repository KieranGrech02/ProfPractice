<template>
  <div v-if="alert">
    <button
      @click="$router.push('/alerts')"
      class="text-sm text-slate-400 hover:text-cyan-400 mb-4 inline-flex items-center gap-1"
    >
      &larr; Back to Alerts
    </button>

    <div class="grid grid-cols-3 gap-6">
      <div class="col-span-2 space-y-6">
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <div class="flex items-start justify-between mb-4">
            <div>
              <h2 class="text-xl font-bold text-slate-100">
                {{ alert.title }}
              </h2>
              <p class="text-xs text-slate-500 mt-1">
                Alert #{{ alert.id }} &middot;
                {{ new Date(alert.created_at).toLocaleString() }}
              </p>
            </div>
            <div class="flex items-center gap-2">
              <SeverityBadge :severity="alert.severity" />
              <StatusBadge :status="alert.status" />
            </div>
          </div>

          <p class="text-sm text-slate-300 leading-relaxed mb-6">
            {{ alert.description }}
          </p>

          <div class="grid grid-cols-2 gap-4 text-sm">
            <div v-if="alert.source" class="bg-slate-800 rounded-lg p-3">
              <span class="text-slate-500">Source</span>
              <p class="text-slate-200">{{ alert.source }}</p>
            </div>
            <div v-if="alert.source_ip" class="bg-slate-800 rounded-lg p-3">
              <span class="text-slate-500">Source IP</span>
              <p class="text-slate-200 font-mono">{{ alert.source_ip }}</p>
            </div>
            <div
              v-if="alert.destination_ip"
              class="bg-slate-800 rounded-lg p-3"
            >
              <span class="text-slate-500">Destination IP</span>
              <p class="text-slate-200 font-mono">
                {{ alert.destination_ip }}
              </p>
            </div>
            <div v-if="alert.hostname" class="bg-slate-800 rounded-lg p-3">
              <span class="text-slate-500">Hostname</span>
              <p class="text-slate-200 font-mono">{{ alert.hostname }}</p>
            </div>
            <div v-if="alert.username" class="bg-slate-800 rounded-lg p-3">
              <span class="text-slate-500">Username</span>
              <p class="text-slate-200">{{ alert.username }}</p>
            </div>
            <div v-if="alert.file_hash" class="bg-slate-800 rounded-lg p-3">
              <span class="text-slate-500">File Hash</span>
              <p class="text-slate-200 font-mono text-xs break-all">
                {{ alert.file_hash }}
              </p>
            </div>
            <div
              v-if="alert.mitre_technique_id"
              class="bg-slate-800 rounded-lg p-3"
            >
              <span class="text-slate-500">MITRE ATT&CK</span>
              <p class="text-cyan-400">
                {{ alert.mitre_technique_id }} -
                {{ alert.mitre_technique_name }}
              </p>
              <p class="text-slate-400 text-xs">{{ alert.mitre_tactic }}</p>
            </div>
          </div>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <h3 class="text-sm font-medium text-slate-400 mb-3">
            Update Status
          </h3>
          <div class="flex gap-2">
            <button
              v-for="s in statuses"
              :key="s.value"
              @click="updateStatus(s.value)"
              :disabled="alert.status === s.value"
              class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors disabled:opacity-30"
              :class="
                alert.status === s.value
                  ? 'bg-cyan-600 text-white'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
              "
            >
              {{ s.label }}
            </button>
          </div>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <h3 class="text-sm font-medium text-slate-400 mb-3">
            Analyst Notes
          </h3>
          <textarea
            v-model="notes"
            rows="4"
            class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500 resize-none"
            placeholder="Add investigation notes..."
          ></textarea>
          <button
            @click="saveNotes"
            class="mt-2 px-4 py-1.5 bg-cyan-600 hover:bg-cyan-500 text-white text-sm rounded-lg transition-colors"
          >
            Save Notes
          </button>
        </div>
      </div>

      <div class="space-y-6">
        <EnrichmentPanel
          :enrichments="alert.enrichments"
          :loading="enriching"
          @enrich="runEnrichment"
        />

        <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h3 class="text-sm font-medium text-slate-400 mb-4">
            Alert Timeline
          </h3>
          <div class="space-y-3">
            <div
              v-for="event in alert.timeline_events"
              :key="event.id"
              class="flex gap-3"
            >
              <div class="flex flex-col items-center">
                <div
                  class="w-2 h-2 rounded-full mt-1.5"
                  :class="timelineColor(event.event_type)"
                ></div>
                <div class="w-px flex-1 bg-slate-800"></div>
              </div>
              <div class="pb-3">
                <p class="text-xs text-slate-300">{{ event.description }}</p>
                <p class="text-xs text-slate-500">
                  {{ new Date(event.created_at).toLocaleString() }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import api from "../services/api";
import EnrichmentPanel from "../components/EnrichmentPanel.vue";
import SeverityBadge from "../components/SeverityBadge.vue";
import StatusBadge from "../components/StatusBadge.vue";

const route = useRoute();
const alert = ref(null);
const notes = ref("");
const enriching = ref(false);

const statuses = [
  { value: "open", label: "Open" },
  { value: "investigating", label: "Investigating" },
  { value: "resolved", label: "Resolved" },
  { value: "false_positive", label: "False Positive" },
];

function timelineColor(type) {
  const map = {
    alert_created: "bg-cyan-400",
    status_change: "bg-yellow-400",
    note_added: "bg-blue-400",
    enrichment_completed: "bg-green-400",
  };
  return map[type] || "bg-slate-400";
}

async function fetchAlert() {
  const res = await api.getAlert(route.params.id);
  alert.value = res.data;
  notes.value = res.data.analyst_notes || "";

  if (!res.data.enrichments.length) {
    runEnrichment();
  }
}

async function updateStatus(status) {
  await api.updateAlert(alert.value.id, { status });
  await fetchAlert();
}

async function saveNotes() {
  await api.updateAlert(alert.value.id, { analyst_notes: notes.value });
  await fetchAlert();
}

async function runEnrichment() {
  enriching.value = true;
  try {
    await api.enrichAlert(alert.value.id);
    await fetchAlert();
  } finally {
    enriching.value = false;
  }
}

onMounted(fetchAlert);
</script>
