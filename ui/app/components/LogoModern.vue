<template>
  <NuxtLink :to="to" class="flex items-center gap-2 group">
    <!-- Abstract Icon -->
    <div class="relative">
      <div class="w-9 h-9 rounded-lg bg-gradient-to-br from-primary-500 to-primary-600 flex items-center justify-center shadow-md group-hover:shadow-lg transition-all">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 3L14 8L12 13L10 8L12 3Z" fill="white" />
          <path d="M12 21L8 12H16L12 21Z" fill="white" fill-opacity="0.8" />
          <circle cx="12" cy="8" r="1.5" fill="white" />
        </svg>
      </div>
      <div class="absolute inset-0 rounded-lg bg-primary-500 opacity-0 group-hover:opacity-20 transition-opacity"></div>
    </div>
    
    <!-- Text -->
    <div class="flex flex-col items-start">
      <div class="flex items-baseline gap-0.5">
        <span class="text-lg font-bold text-gray-900 dark:text-white">AI</span>
        <span class="text-lg font-bold text-primary-600 dark:text-primary-400">Activity</span>
      </div>
      <span class="text-[10px] font-medium text-gray-500 dark:text-gray-400 -mt-0.5 tracking-wide">
        SMART PLANNER
      </span>
    </div>
  </NuxtLink>
</template>

<script lang="ts" setup>
defineProps({
  to: {
    type: String,
    default: '/v1'
  }
})
</script>