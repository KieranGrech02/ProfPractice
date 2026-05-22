<template>
  <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-sm font-medium text-slate-400">
        Threat Intelligence Enrichment
      </h3>
      <button
        v-if="!enrichments.length"
        @click="$emit('enrich')"
        :disabled="loading"
        class="px-3 py-1.5 bg-cyan-600 hover:bg-cyan-500 disabled:bg-slate-700 text-white text-xs rounded-lg transition-colors"
      >
        {{ loading ? "Enriching..." : "Enrich Indicators" }}
      </button>
    </div>

    <div v-if="enrichments.length" class="space-y-3">
      <div
        v-for="e in enrichments"
        :key="e.id"
        class="bg-slate-800 rounded-lg p-3"
      >
        <div class="flex items-center justify-between mb-2">
          <div>
            <span class="text-xs text-slate-500 uppercase">{{
              e.source
            }}</span>
            <p class="text-sm font-mono text-slate-200">{{ e.indicator }}</p>
          </div>
          <span
            class="px-2 py-0.5 rounded text-xs font-medium"
            :class="
              e.malicious
                ? 'bg-red-500/20 text-red-400'
                : 'bg-green-500/20 text-green-400'
            "
          >
            {{ e.malicious ? "Malicious" : "Clean" }}
          </span>
        </div>
        <div class="grid grid-cols-2 gap-2 text-xs text-slate-400">
          <div>
            Type:
            <span class="text-slate-300">{{ e.indicator_type }}</span>
          </div>
          <div v-if="e.reputation_score != null">
            Reputation:
            <span
              class="text-slate-300"
              :class="e.reputation_score < 0 ? 'text-red-400' : 'text-green-400'"
              >{{ e.reputation_score }}</span
            >
          </div>
        </div>
      </div>
    </div>

    <p
      v-else-if="!loading"
      class="text-sm text-slate-500 text-center py-4"
    >
      No enrichment data yet. Click the button to enrich indicators.
    </p>
  </div>
</template>

<script setup>
defineProps({
  enrichments: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
});
defineEmits(["enrich"]);
</script>
