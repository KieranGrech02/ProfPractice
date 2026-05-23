<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">MITRE ATT&CK Coverage</h2>

    <div class="grid grid-cols-1 gap-4">
      <div
        v-for="tactic in coverage"
        :key="tactic.tactic_id"
        class="bg-slate-900 border border-slate-800 rounded-xl p-5"
      >
        <div class="flex items-center justify-between mb-3">
          <div>
            <h3 class="text-sm font-semibold text-slate-200">
              {{ tactic.tactic_name }}
            </h3>
            <span class="text-xs text-slate-500">{{ tactic.tactic_id }}</span>
          </div>
          <span
            class="text-xs px-2 py-1 rounded-full"
            :class="
              tactic.alert_count > 0
                ? 'bg-cyan-500/20 text-cyan-400'
                : 'bg-slate-800 text-slate-500'
            "
          >
            {{ tactic.alert_count }} alert{{
              tactic.alert_count !== 1 ? "s" : ""
            }}
          </span>
        </div>

        <div class="flex flex-wrap gap-2">
          <div
            v-for="tech in tactic.techniques"
            :key="tech.id"
            class="px-3 py-2 rounded-lg text-xs border cursor-default transition-colors"
            :class="
              tech.alert_count > 0
                ? 'bg-cyan-500/10 border-cyan-500/30 text-cyan-300'
                : 'bg-slate-800/50 border-slate-700/50 text-slate-500'
            "
            :title="`${tech.id}: ${tech.name} (${tech.alert_count} alerts)`"
          >
            <span class="font-mono">{{ tech.id }}</span>
            {{ tech.name }}
            <span
              v-if="tech.alert_count > 0"
              class="ml-1 text-cyan-400 font-medium"
            >
              ({{ tech.alert_count }})
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import api from "../services/api";

const coverage = ref([]);

onMounted(async () => {
  const res = await api.getMitreCoverage();
  coverage.value = res.data;
});
</script>
