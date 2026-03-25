<template>
  <div class="min-h-screen bg-white dark:bg-gray-900">
    <!-- Hero Section -->
    <section class="pt-24 pb-16 md:pt-32 md:pb-24">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <UBadge color="primary" variant="soft" class="mb-6">
            <template #leading>
              <UIcon name="i-heroicons-sparkles" class="w-4 h-4" />
            </template>
            AI-Powered Decision Support System
          </UBadge>
          
          <h1 class="text-4xl md:text-6xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-300 bg-clip-text text-transparent mb-6">
            Smart Activity Planner
          </h1>
          
          <p class="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto mb-8">
            Let AI help you discover the perfect activity based on your location, weather conditions, and preferred time. Smart recommendations powered by real-time data.
          </p>
          
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <UButton
              size="xl"
              color="primary"
              to="/v1"
              class="shadow-lg hover:shadow-xl transform hover:scale-105 transition-all"
            >
              <template #leading>
                <UIcon name="i-heroicons-sparkles" class="w-5 h-5" />
              </template>
              Try Version 1
            </UButton>
            
            <UButton
              size="xl"
              variant="outline"
              to="/v2"
              class="dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-800"
            >
              <template #leading>
                <UIcon name="i-heroicons-rocket-launch" class="w-5 h-5" />
              </template>
              Explore Version 2
            </UButton>
          </div>
        </div>

        <!-- Version Cards Section -->
        <div class="mt-16 grid md:grid-cols-2 gap-8">
          <!-- Version 1 Card -->
          <UCard class="group hover:shadow-xl transition-all duration-300 dark:bg-gray-800 border-2 hover:border-primary-200 dark:hover:border-primary-800">
            <div class="flex items-start justify-between mb-4">
              <div>
                <UBadge color="primary" variant="soft" class="mb-2">Stable</UBadge>
                <h3 class="text-2xl font-bold text-gray-900 dark:text-white">Version 1</h3>
                <p class="text-gray-600 dark:text-gray-300 mt-2">Classic experience with core features</p>
              </div>
              <div class="w-12 h-12 bg-primary-100 dark:bg-primary-900/50 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
                <UIcon name="i-heroicons-map-pin" class="w-6 h-6 text-primary-600 dark:text-primary-400" />
              </div>
            </div>
            
            <div class="space-y-4 mb-6">
              <div class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-300">
                <UIcon name="i-heroicons-check-circle" class="w-4 h-4 text-green-500" />
                Interactive map selection
              </div>
              <div class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-300">
                <UIcon name="i-heroicons-check-circle" class="w-4 h-4 text-green-500" />
                Real-time weather data
              </div>
              <div class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-300">
                <UIcon name="i-heroicons-check-circle" class="w-4 h-4 text-green-500" />
                Basic DSS recommendations
              </div>
              <div class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-300">
                <UIcon name="i-heroicons-check-circle" class="w-4 h-4 text-green-500" />
                Location search & map click
              </div>
            </div>
            
            <UButton color="primary" variant="outline" to="/v1" block class="mt-4">
              Launch Version 1
              <template #trailing>
                <UIcon name="i-heroicons-arrow-right" class="w-4 h-4" />
              </template>
            </UButton>
          </UCard>

          <!-- Version 2 Card -->
          <UCard class="group hover:shadow-xl transition-all duration-300 dark:bg-gray-800 border-2 border-primary-200 dark:border-primary-800 relative overflow-hidden">
            <!-- Beta Badge -->
            <div class="absolute top-4 right-4">
              <UBadge color="amber" variant="solid" class="animate-pulse">
                <UIcon name="i-heroicons-rocket-launch" class="w-3 h-3 mr-1" />
                Beta
              </UBadge>
            </div>
            
            <div class="flex items-start justify-between mb-4">
              <div>
                <UBadge color="amber" variant="soft" class="mb-2">Enhanced</UBadge>
                <h3 class="text-2xl font-bold text-gray-900 dark:text-white">Version 2</h3>
                <p class="text-gray-600 dark:text-gray-300 mt-2">Advanced AI with enhanced features</p>
              </div>
              <div class="w-12 h-12 bg-amber-100 dark:bg-amber-900/50 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
                <UIcon name="i-heroicons-rocket-launch" class="w-6 h-6 text-amber-600 dark:text-amber-400" />
              </div>
            </div>
            
            <div class="space-y-4 mb-6">
              <div class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-300">
                <UIcon name="i-heroicons-check-circle" class="w-4 h-4 text-green-500" />
                Advanced AI recommendations
              </div>
              <div class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-300">
                <UIcon name="i-heroicons-check-circle" class="w-4 h-4 text-green-500" />
                Enhanced DSS scoring system
              </div>
              <div class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-300">
                <UIcon name="i-heroicons-check-circle" class="w-4 h-4 text-green-500" />
                Activity categories & filters
              </div>
              <div class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-300">
                <UIcon name="i-heroicons-check-circle" class="w-4 h-4 text-green-500" />
                Social sharing & favorites
              </div>
              <div class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-300">
                <UIcon name="i-heroicons-sparkles" class="w-4 h-4 text-amber-500" />
                Real-time weather alerts
              </div>
            </div>
            
            <UButton color="primary" to="/v2" block class="mt-4 bg-gradient-to-r from-primary-500 to-primary-600">
              Try Version 2 Beta
              <template #trailing>
                <UIcon name="i-heroicons-arrow-right" class="w-4 h-4" />
              </template>
            </UButton>
          </UCard>
        </div>

        <!-- Demo Preview -->
        <div class="mt-16 relative">
          <div class="absolute inset-0 bg-gradient-to-r from-primary-500 to-primary-600 rounded-2xl blur-3xl opacity-20 dark:opacity-30"></div>
          <div class="relative bg-white dark:bg-gray-800 rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-700 overflow-hidden">
            <div class="bg-gray-100 dark:bg-gray-900 px-4 py-2 border-b border-gray-200 dark:border-gray-700 flex items-center gap-2">
              <div class="w-3 h-3 bg-red-500 rounded-full"></div>
              <div class="w-3 h-3 bg-yellow-500 rounded-full"></div>
              <div class="w-3 h-3 bg-green-500 rounded-full"></div>
              <span class="text-sm text-gray-500 dark:text-gray-400 ml-2">app.activity-planner.ai</span>
              <div class="flex gap-2 ml-auto">
                <UBadge color="primary" variant="soft" size="sm">v1</UBadge>
                <UBadge color="amber" variant="soft" size="sm">v2 Beta</UBadge>
              </div>
            </div>
            <div class="bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-800 dark:to-gray-900 p-8">
              <div class="grid md:grid-cols-2 gap-6">
                <!-- Mock Location Card -->
                <div class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-lg">
                  <div class="flex items-center gap-2 mb-3">
                    <UIcon name="i-heroicons-map-pin" class="w-5 h-5 text-primary-500" />
                    <h3 class="font-semibold dark:text-white">Location Selection</h3>
                  </div>
                  <div class="h-32 bg-gray-200 dark:bg-gray-700 rounded-lg mb-3 flex items-center justify-center">
                    <UIcon name="i-heroicons-map" class="w-8 h-8 text-gray-400" />
                  </div>
                  <div class="h-8 bg-gray-200 dark:bg-gray-700 rounded-lg w-3/4"></div>
                </div>
                <!-- Mock Weather Card -->
                <div class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-lg">
                  <div class="flex items-center gap-2 mb-3">
                    <UIcon name="i-heroicons-cloud" class="w-5 h-5 text-primary-500" />
                    <h3 class="font-semibold dark:text-white">Weather & AI Recommendation</h3>
                  </div>
                  <div class="flex items-center justify-between mb-3">
                    <div class="h-12 w-12 bg-gradient-to-br from-primary-500 to-primary-600 rounded-full flex items-center justify-center">
                      <UIcon name="i-heroicons-sun" class="w-6 h-6 text-white" />
                    </div>
                    <div class="h-8 bg-gray-200 dark:bg-gray-700 rounded-lg w-24"></div>
                  </div>
                  <div class="h-8 bg-gray-200 dark:bg-gray-700 rounded-lg mb-2"></div>
                  <div class="h-6 bg-gray-200 dark:bg-gray-700 rounded-lg w-2/3"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-16 bg-gray-50 dark:bg-gray-800/50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <UBadge color="primary" variant="soft" class="mb-4">Features</UBadge>
          <h2 class="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Powerful Features
          </h2>
          <p class="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Everything you need to make informed decisions about your next activity
          </p>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <UCard class="group hover:shadow-xl transition-all duration-300 dark:bg-gray-800">
            <div class="w-12 h-12 bg-primary-100 dark:bg-primary-900/50 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <UIcon name="i-heroicons-map-pin" class="w-6 h-6 text-primary-600 dark:text-primary-400" />
            </div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              Smart Location Selection
            </h3>
            <p class="text-gray-600 dark:text-gray-300">
              Choose your location manually, click on an interactive map, or use your current GPS location.
            </p>
          </UCard>

          <UCard class="group hover:shadow-xl transition-all duration-300 dark:bg-gray-800">
            <div class="w-12 h-12 bg-primary-100 dark:bg-primary-900/50 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <UIcon name="i-heroicons-cloud" class="w-6 h-6 text-primary-600 dark:text-primary-400" />
            </div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              Real-time Weather Data
            </h3>
            <p class="text-gray-600 dark:text-gray-300">
              Get accurate weather forecasts for your selected date and time using Open-Meteo API.
            </p>
          </UCard>

          <UCard class="group hover:shadow-xl transition-all duration-300 dark:bg-gray-800">
            <div class="w-12 h-12 bg-primary-100 dark:bg-primary-900/50 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <UIcon name="i-heroicons-light-bulb" class="w-6 h-6 text-primary-600 dark:text-primary-400" />
            </div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              AI-Powered Recommendations
            </h3>
            <p class="text-gray-600 dark:text-gray-300">
              Get intelligent activity suggestions based on weather, time of day, and location context.
            </p>
          </UCard>
        </div>
      </div>
    </section>

    <!-- Version Comparison Table -->
    <section class="py-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <UBadge color="primary" variant="soft" class="mb-4">Compare Versions</UBadge>
          <h2 class="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Choose Your Experience
          </h2>
          <p class="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Both versions offer powerful features, but v2 includes advanced AI capabilities
          </p>
        </div>

        <div class="grid md:grid-cols-2 gap-8">
          <UCard class="dark:bg-gray-800">
            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-4 text-center">Version 1</h3>
            <div class="space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-gray-600 dark:text-gray-300">Interactive Map</span>
                <UIcon name="i-heroicons-check-circle" class="w-5 h-5 text-green-500" />
              </div>
              <div class="flex justify-between items-center">
                <span class="text-gray-600 dark:text-gray-300">Real-time Weather</span>
                <UIcon name="i-heroicons-check-circle" class="w-5 h-5 text-green-500" />
              </div>
              <div class="flex justify-between items-center">
                <span class="text-gray-600 dark:text-gray-300">Basic DSS</span>
                <UIcon name="i-heroicons-check-circle" class="w-5 h-5 text-green-500" />
              </div>
              <div class="flex justify-between items-center">
                <span class="text-gray-600 dark:text-gray-300">AI Recommendations</span>
                <UIcon name="i-heroicons-x-mark" class="w-5 h-5 text-gray-400" />
              </div>
              <div class="flex justify-between items-center">
                <span class="text-gray-600 dark:text-gray-300">Activity Filters</span>
                <UIcon name="i-heroicons-x-mark" class="w-5 h-5 text-gray-400" />
              </div>
            </div>
          </UCard>

          <UCard class="dark:bg-gray-800 border-2 border-primary-200 dark:border-primary-800">
            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-4 text-center">
              Version 2
              <UBadge color="amber" variant="soft" size="sm" class="ml-2">Beta</UBadge>
            </h3>
            <div class="space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-gray-600 dark:text-gray-300">Interactive Map</span>
                <UIcon name="i-heroicons-check-circle" class="w-5 h-5 text-green-500" />
              </div>
              <div class="flex justify-between items-center">
                <span class="text-gray-600 dark:text-gray-300">Real-time Weather</span>
                <UIcon name="i-heroicons-check-circle" class="w-5 h-5 text-green-500" />
              </div>
              <div class="flex justify-between items-center">
                <span class="text-gray-600 dark:text-gray-300">Advanced DSS</span>
                <UIcon name="i-heroicons-check-circle" class="w-5 h-5 text-green-500" />
              </div>
              <div class="flex justify-between items-center">
                <span class="text-gray-600 dark:text-gray-300">AI Recommendations</span>
                <UIcon name="i-heroicons-check-circle" class="w-5 h-5 text-green-500" />
              </div>
              <div class="flex justify-between items-center">
                <span class="text-gray-600 dark:text-gray-300">Activity Filters</span>
                <UIcon name="i-heroicons-check-circle" class="w-5 h-5 text-green-500" />
              </div>
            </div>
          </UCard>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section id="how-it-works" class="py-16 bg-gray-50 dark:bg-gray-800/50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <UBadge color="primary" variant="soft" class="mb-4">Simple Process</UBadge>
          <h2 class="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
            How It Works
          </h2>
          <p class="text-xl text-gray-600 dark:text-gray-300">Three simple steps to your perfect activity</p>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <div class="text-center">
            <div class="w-20 h-20 bg-gradient-to-br from-primary-500 to-primary-600 rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg">
              <span class="text-2xl font-bold text-white">1</span>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">Choose Location</h3>
            <p class="text-gray-600 dark:text-gray-300">Select your desired location by searching, clicking on the map, or using your current position.</p>
          </div>

          <div class="text-center">
            <div class="w-20 h-20 bg-gradient-to-br from-primary-500 to-primary-600 rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg">
              <span class="text-2xl font-bold text-white">2</span>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">Pick Date & Time</h3>
            <p class="text-gray-600 dark:text-gray-300">Select when you want to go. Use presets for morning, afternoon, evening, or night activities.</p>
          </div>

          <div class="text-center">
            <div class="w-20 h-20 bg-gradient-to-br from-primary-500 to-primary-600 rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg">
              <span class="text-2xl font-bold text-white">3</span>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">Get Recommendations</h3>
            <p class="text-gray-600 dark:text-gray-300">Receive AI-powered suggestions with detailed decision factors and alternative options.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-16 bg-gradient-to-br from-primary-600 to-primary-700 dark:from-primary-700 dark:to-primary-900">
      <div class="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
        <h2 class="text-3xl md:text-4xl font-bold text-white mb-4">
          Ready to Find Your Perfect Activity?
        </h2>
        <p class="text-xl text-primary-100 mb-8">
          Choose your preferred version and start exploring AI-powered recommendations today.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <UButton size="xl" color="white" to="/v1" class="text-primary-600">
            <template #leading>
              <UIcon name="i-heroicons-sparkles" class="w-5 h-5" />
            </template>
            Version 1 (Stable)
          </UButton>
          <UButton size="xl" variant="outline" to="/v2" class="border-white text-white hover:bg-white/10">
            <template #leading>
              <UIcon name="i-heroicons-rocket-launch" class="w-5 h-5" />
            </template>
            Version 2 (Beta)
          </UButton>
        </div>
      </div>
    </section>
  </div>
</template>

<script lang="ts" setup>
// No additional logic needed - pure presentation component
</script>

<style scoped>
html {
  scroll-behavior: smooth;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

section {
  animation: fadeInUp 0.6s ease-out;
}
</style>