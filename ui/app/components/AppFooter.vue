<template>
  <footer class="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <!-- Brand Column -->
        <div class="col-span-1 md:col-span-1">
          <AppLogo to="/v1" />
          <p class="mt-4 text-sm text-gray-600 dark:text-gray-400">
            Making activity planning smarter with AI and real-time weather data.
          </p>
          <div class="flex gap-4 mt-4">
            <a href="#" class="text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition">
              <UIcon name="i-heroicons-globe-alt" class="w-5 h-5" />
            </a>
            <a href="#" class="text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition">
              <UIcon name="i-heroicons-chat-bubble-left-right" class="w-5 h-5" />
            </a>
            <a href="#" class="text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition">
              <UIcon name="i-heroicons-envelope" class="w-5 h-5" />
            </a>
          </div>
        </div>

        <!-- Product Links -->
        <div>
          <h3 class="font-semibold text-gray-900 dark:text-white mb-3">Product</h3>
          <ul class="space-y-2">
            <li>
              <NuxtLink to="/v1" class="text-sm text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition">
                Version 1 (Classic)
              </NuxtLink>
            </li>
            <li>
              <NuxtLink to="/v2" class="text-sm text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition">
                Version 2 (Enhanced)
              </NuxtLink>
            </li>
            <li>
              <a href="#features" class="text-sm text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition">
                Features
              </a>
            </li>
            <li>
              <a href="#dss" class="text-sm text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition">
                DSS Technology
              </a>
            </li>
          </ul>
        </div>

        <!-- Resources Links -->
        <div>
          <h3 class="font-semibold text-gray-900 dark:text-white mb-3">Resources</h3>
          <ul class="space-y-2">
            <li>
              <a href="#" class="text-sm text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition">
                Documentation
              </a>
            </li>
            <li>
              <a href="#" class="text-sm text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition">
                API Reference
              </a>
            </li>
            <li>
              <a href="#" class="text-sm text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition">
                GitHub
              </a>
            </li>
            <li>
              <a href="#" class="text-sm text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition">
                Support
              </a>
            </li>
          </ul>
        </div>

        <!-- Legal Links -->
        <div>
          <h3 class="font-semibold text-gray-900 dark:text-white mb-3">Legal</h3>
          <ul class="space-y-2">
            <li>
              <a href="#" class="text-sm text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition">
                Privacy Policy
              </a>
            </li>
            <li>
              <a href="#" class="text-sm text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition">
                Terms of Service
              </a>
            </li>
            <li>
              <a href="#" class="text-sm text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition">
                Cookie Policy
              </a>
            </li>
          </ul>
        </div>
      </div>

      <!-- Bottom Bar -->
      <div class="mt-8 pt-8 border-t border-gray-200 dark:border-gray-800">
        <div class="flex flex-col md:flex-row justify-between items-center gap-4">
          <p class="text-sm text-gray-500 dark:text-gray-400">
            &copy; {{ currentYear }} AI Activity Planner. All rights reserved.
          </p>
          <div class="flex gap-6">
            <span class="text-xs text-gray-400 dark:text-gray-500">
              Powered by Open-Meteo & OpenStreetMap
            </span>
            <div class="flex gap-2">
              <UBadge color="primary" variant="soft" size="sm">
                <UIcon name="i-heroicons-sparkles" class="w-3 h-3 mr-1" />
                AI Engine v2.0
              </UBadge>
            </div>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script lang="ts" setup>
const currentYear = computed(() => new Date().getFullYear())
</script>