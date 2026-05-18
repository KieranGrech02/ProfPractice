<template>
  <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
    <p class="text-sm text-slate-400">{{ label }}</p>
    <p class="text-3xl font-bold mt-1" :class="valueClass">{{ value }}</p>
  </div>
</template>

<script setup>
defineProps({
  label: String,
  value: [Number, String],
  valueClass: { type: String, default: "text-slate-100" },
});
</script>
