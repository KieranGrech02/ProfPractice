<template>
  <span
    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
    :class="classes"
  >
    {{ label }}
  </span>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({ status: String });

const classes = computed(() => {
  const map = {
    open: "bg-red-500/20 text-red-400",
    investigating: "bg-yellow-500/20 text-yellow-400",
    resolved: "bg-green-500/20 text-green-400",
    false_positive: "bg-slate-500/20 text-slate-400",
  };
  return map[props.status] || map.open;
});

const label = computed(() => {
  const map = {
    open: "Open",
    investigating: "Investigating",
    resolved: "Resolved",
    false_positive: "False Positive",
  };
  return map[props.status] || props.status;
});
</script>
