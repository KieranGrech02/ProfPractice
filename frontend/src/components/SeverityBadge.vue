<template>
  <span
    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
    :class="classes"
  >
    {{ severity }}
  </span>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({ severity: String });

const classes = computed(() => {
  const map = {
    critical: "bg-red-500/20 text-red-400 border border-red-500/30",
    high: "bg-orange-500/20 text-orange-400 border border-orange-500/30",
    medium: "bg-yellow-500/20 text-yellow-400 border border-yellow-500/30",
    low: "bg-blue-500/20 text-blue-400 border border-blue-500/30",
    informational: "bg-slate-500/20 text-slate-400 border border-slate-500/30",
  };
  return map[props.severity] || map.informational;
});
</script>
