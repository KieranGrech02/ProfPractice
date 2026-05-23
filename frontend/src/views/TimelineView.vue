<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">Investigation Timeline</h2>

    <div class="flex gap-3 mb-6">
      <select
        v-model="filterType"
        @change="fetchTimeline"
        class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-cyan-500"
      >
        <option value="">All Events</option>
        <option value="alert_created">Alert Created</option>
        <option value="status_change">Status Change</option>
        <option value="note_added">Note Added</option>
        <option value="enrichment_completed">Enrichment</option>
      </select>
    </div>

    <div class="bg-slate-900 border border-slate-800 rounded-xl p-6">
      <div class="space-y-0">
        <div
          v-for="(event, idx) in filteredEvents"
          :key="event.id"
          class="flex gap-4"
        >
          <div class="flex flex-col items-center">
            <div
              class="w-3 h-3 rounded-full mt-1 flex-shrink-0"
              :class="dotColor(event.event_type)"
            ></div>
            <div
              v-if="idx < filteredEvents.length - 1"
              class="w-px flex-1 bg-slate-800 my-1"
            ></div>
          </div>
          <div class="pb-6 flex-1">
            <div class="flex items-center justify-between">
              <span
                class="text-xs px-2 py-0.5 rounded-full font-medium"
                :class="badgeClass(event.event_type)"
              >
                {{ eventLabel(event.event_type) }}
              </span>
              <span class="text-xs text-slate-500">
                {{ new Date(event.created_at).toLocaleString() }}
              </span>
            </div>
            <p class="text-sm text-slate-300 mt-1">{{ event.description }}</p>
            <button
              @click="$router.push(`/alerts/${event.alert_id}`)"
              class="text-xs text-cyan-400 hover:text-cyan-300 mt-1"
            >
              View Alert #{{ event.alert_id }}
            </button>
          </div>
        </div>
      </div>

      <p
        v-if="!filteredEvents.length"
        class="text-center text-slate-500 py-8"
      >
        No timeline events found.
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import api from "../services/api";

const allAlerts = ref([]);
const filterType = ref("");

const filteredEvents = computed(() => {
  let events = allAlerts.value.flatMap((a) =>
    (a.timeline_events || []).map((e) => ({ ...e, alert_id: a.id })),
  );
  if (filterType.value) {
    events = events.filter((e) => e.event_type === filterType.value);
  }
  return events.sort(
    (a, b) => new Date(b.created_at) - new Date(a.created_at),
  );
});

function dotColor(type) {
  const map = {
    alert_created: "bg-cyan-400",
    status_change: "bg-yellow-400",
    note_added: "bg-blue-400",
    enrichment_completed: "bg-green-400",
  };
  return map[type] || "bg-slate-400";
}

function badgeClass(type) {
  const map = {
    alert_created: "bg-cyan-500/20 text-cyan-400",
    status_change: "bg-yellow-500/20 text-yellow-400",
    note_added: "bg-blue-500/20 text-blue-400",
    enrichment_completed: "bg-green-500/20 text-green-400",
  };
  return map[type] || "bg-slate-500/20 text-slate-400";
}

function eventLabel(type) {
  const map = {
    alert_created: "Created",
    status_change: "Status Change",
    note_added: "Note",
    enrichment_completed: "Enrichment",
  };
  return map[type] || type;
}

async function fetchTimeline() {
  const res = await api.getAlerts();
  const detailed = await Promise.all(
    res.data.map((a) => api.getAlert(a.id).then((r) => r.data)),
  );
  allAlerts.value = detailed;
}

onMounted(fetchTimeline);
</script>
