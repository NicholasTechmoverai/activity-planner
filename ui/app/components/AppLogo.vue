<template>
  <NuxtLink :to="to" class="flex items-center gap-3 group">
    <!-- Animated Logo Icon -->
    <div class="relative">
      <div class="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center shadow-lg group-hover:shadow-xl transition-all duration-300">
        <svg
          class="w-6 h-6 text-white transition-transform duration-300 group-hover:scale-110"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M12 2L15 8L12 14L9 8L12 2Z"
            fill="currentColor"
            fill-opacity="0.9"
          />
          <path
            d="M12 22L7 12H17L12 22Z"
            fill="currentColor"
            fill-opacity="0.7"
          />
          <circle cx="12" cy="8" r="2" fill="currentColor" fill-opacity="1" />
          <path
            d="M5 18L8 15L11 18L8 21L5 18Z"
            fill="currentColor"
            fill-opacity="0.6"
          />
          <path
            d="M19 18L16 15L13 18L16 21L19 18Z"
            fill="currentColor"
            fill-opacity="0.6"
          />
        </svg>
      </div>
      <!-- Animated pulse ring -->
      <div class="absolute inset-0 rounded-xl bg-primary-500 opacity-0 group-hover:opacity-20 animate-ping pointer-events-none"></div>
    </div>
    
    <!-- Text Logo with Gradient -->
    <div class="flex flex-col">
      <div class="flex items-baseline gap-1">
        <span class="text-xl font-bold tracking-tight bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-300 bg-clip-text text-transparent">
          AI
        </span>
        <span class="text-xl font-bold text-primary-600 dark:text-primary-400">
          Activity
        </span>
        <span class="text-xl font-bold bg-gradient-to-r from-primary-600 to-primary-500 dark:from-primary-400 dark:to-primary-300 bg-clip-text text-transparent">
          Planner
        </span>
      </div>
      <span class="text-xs text-gray-500 dark:text-gray-400 -mt-0.5 flex items-center gap-1">
        <span class="inline-block w-1 h-1 rounded-full bg-primary-500"></span>
        Smart Decisions
        <span class="inline-block w-1 h-1 rounded-full bg-primary-500"></span>
        AI Powered
      </span>
    </div>
  </NuxtLink>
</template>

<script lang="ts" setup>
defineProps({
  to: {
    type: String,
    default: '/v1'
  },
  variant: {
    type: String as () => 'full' | 'icon' | 'compact',
    default: 'full'
  }
})
</script>