<template>
  <div class="min-h-screen font-body overflow-x-hidden bg-gradient-to-br from-gray-50 via-white to-gray-100 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800">
    
    <!-- Animated Background Pattern -->
    <div class="fixed inset-0 pointer-events-none opacity-5 dark:opacity-10">
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(0,0,0,0.1)_1px,transparent_1px)] bg-[length:24px_24px]"></div>
    </div>

    <main class="relative max-w-7xl mx-auto px-4 sm:px-6 py-8 sm:py-10">
      
    
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-7">
        
        <!-- LEFT PANEL -->
        <aside class="lg:col-span-4 space-y-5">
          
          <!-- Decision Inputs Card -->
          <div class="backdrop-blur-xl bg-white/80 dark:bg-gray-900/80 rounded-2xl shadow-xl border border-gray-200/50 dark:border-gray-700/50 overflow-hidden transition-all duration-300 hover:shadow-2xl">
            <div class="p-5 sm:p-6">
              <div class="flex items-center gap-3 mb-6 pb-3 border-b border-gray-200/50 dark:border-gray-700/50">
                <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-primary-500 to-primary-600 flex items-center justify-center shadow-lg">
                  <UIcon name="i-lucide-cpu" class="size-4 text-white" />
                </div>
                <div>
                  <span class="text-xs font-semibold uppercase tracking-wider text-primary">Decision Engine</span>
                  <p class="text-xs text-gray-500 dark:text-gray-400">Configure your preferences</p>
                </div>
              </div>

              <!-- Location Mode -->
              <div class="mb-5">
                <label class="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400 block mb-2">Location Method</label>
                <div class="grid grid-cols-3 gap-2">
                  <button
                    v-for="mode in locationModes"
                    :key="mode.value"
                    @click="locationMode = mode.value"
                    class="group relative px-3 py-2.5 rounded-xl text-xs font-medium transition-all duration-200"
                    :class="locationMode === mode.value 
                      ? 'bg-gradient-to-r from-primary-500 to-primary-600 text-white shadow-md scale-[1.02]' 
                      : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700'"
                  >
                    <UIcon :name="mode.icon" class="size-4 mx-auto mb-1" />
                    {{ mode.label }}
                  </button>
                </div>
              </div>

              <!-- Manual Input -->
              <div v-if="locationMode === 'manual'" class="mb-5 animate-slide-down">
                <label class="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400 block mb-2">Search Location</label>
                <div class="relative">
                  <UInput
                    v-model="locationQuery"
                    placeholder="e.g., Tokyo, Japan"
                    icon="i-lucide-map-pin"
                    size="md"
                    class="w-full rounded-xl"
                    @keyup.enter="geocodeLocation"
                  >
                    <template #trailing>
                      <UButton @click="geocodeLocation" :loading="geocoding" color="primary" variant="ghost" size="xs" icon="i-lucide-search" class="rounded-lg" />
                    </template>
                  </UInput>
                  
                  <!-- Suggestions -->
                  <div v-if="locationSuggestions.length" class="absolute z-50 w-full mt-2 bg-white dark:bg-gray-800 rounded-xl shadow-2xl border border-gray-200 dark:border-gray-700 overflow-hidden">
                    <button
                      v-for="s in locationSuggestions"
                      :key="s.place_id"
                      @click="selectSuggestion(s)"
                      class="flex items-center gap-3 w-full text-left px-4 py-3 text-sm hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors group"
                    >
                      <UIcon name="i-lucide-map-pin" class="size-4 text-primary group-hover:scale-110 transition-transform" />
                      <span class="flex-1 line-clamp-1">{{ s.display_name }}</span>
                      <UIcon name="i-lucide-arrow-right" class="size-3 text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity" />
                    </button>
                  </div>
                </div>
              </div>

              <!-- Map Mode -->
              <div v-if="locationMode === 'map'" class="mb-5 animate-slide-down">
                <label class="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400 block mb-2">Interactive Map</label>
                <div ref="mapContainer" class="w-full h-56 rounded-xl overflow-hidden border-2 border-gray-200 dark:border-gray-700 relative shadow-inner">
                  <div v-if="!mapReady" class="absolute inset-0 flex items-center justify-center bg-gray-100 dark:bg-gray-800">
                    <div class="loader-ring"></div>
                  </div>
                </div>
                <div v-if="selectedLocation" class="mt-2 text-xs text-primary flex items-center gap-1 animate-fade-in">
                  <UIcon name="i-lucide-check-circle-2" class="size-3" />
                  {{ selectedLocation.name }}
                </div>
              </div>

              <!-- GPS Mode -->
              <div v-if="locationMode === 'gps'" class="mb-5 animate-slide-down">
                <UButton @click="getGPSLocation" :loading="gpsLoading" block class="rounded-xl py-3 bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 shadow-lg transition-all">
                  <UIcon name="i-lucide-navigation" class="size-4 mr-2" />
                  Detect My Current Location
                </UButton>
                <div v-if="selectedLocation" class="mt-2 text-center animate-fade-in">
                  <span class="text-xs text-primary flex items-center justify-center gap-1">
                    <UIcon name="i-lucide-circle-check" class="size-3" />
                    {{ selectedLocation.name }}
                  </span>
                </div>
              </div>

              <!-- Date & Time -->
              <div class="mb-5 grid grid-cols-2 gap-3">
                <div>
                  <label class="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400 block mb-2">Date</label>
                  <UInput v-model="selectedDate" type="date" :min="todayDate" icon="i-lucide-calendar" class="rounded-xl" />
                </div>
                <div>
                  <label class="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400 block mb-2">Time</label>
                  <UInput v-model="selectedTime" type="time" icon="i-lucide-clock" class="rounded-xl" />
                </div>
              </div>

              <!-- Activity Preferences -->
              <div class="mb-5">
                <label class="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400 block mb-2">Interests</label>
                <div class="flex flex-wrap gap-2">
                  <button
                    v-for="pref in activityPrefs"
                    :key="pref.value"
                    @click="togglePref(pref.value)"
                    class="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium transition-all duration-200"
                    :class="selectedPrefs.includes(pref.value)
                      ? 'bg-gradient-to-r from-primary-500 to-primary-600 text-white shadow-md scale-105'
                      : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700'"
                  >
                    <UIcon :name="pref.icon" class="size-3" />
                    {{ pref.label }}
                  </button>
                </div>
              </div>

              <!-- Group Size -->
              <div class="mb-6">
                <label class="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400 block mb-2">Group Size</label>
                <div class="flex items-center gap-3 bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-800/50 rounded-xl p-2 border border-gray-200 dark:border-gray-700">
                  <button @click="groupSize = Math.max(1, groupSize - 1)" class="w-8 h-8 rounded-lg bg-white dark:bg-gray-700 shadow hover:shadow-md transition-all flex items-center justify-center">
                    <UIcon name="i-lucide-minus" class="size-4" />
                  </button>
                  <div class="flex-1 text-center">
                    <span class="text-3xl font-bold bg-gradient-to-r from-primary-500 to-primary-600 bg-clip-text text-transparent tabular-nums">{{ groupSize }}</span>
                    <span class="text-xs text-gray-400 ml-1">{{ groupSize === 1 ? 'person' : 'people' }}</span>
                  </div>
                  <button @click="groupSize = Math.min(50, groupSize + 1)" class="w-8 h-8 rounded-lg bg-white dark:bg-gray-700 shadow hover:shadow-md transition-all flex items-center justify-center">
                    <UIcon name="i-lucide-plus" class="size-4" />
                  </button>
                </div>
              </div>

              <!-- CTA Button -->
              <UButton
                @click="runAdvisor"
                :loading="analyzing"
                :disabled="!selectedLocation"
                block size="lg"
                class="relative rounded-xl py-3 bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 shadow-lg hover:shadow-xl transition-all duration-300 group overflow-hidden"
              >
                <div class="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
                <UIcon name="i-lucide-sparkles" class="size-5 mr-2" />
                {{ analyzing ? 'Analyzing Conditions...' : 'Generate Smart Recommendations' }}
              </UButton>
              <p v-if="!selectedLocation" class="text-xs text-center text-gray-400 mt-2 animate-pulse">Select a location to begin</p>
            </div>
          </div>

          <!-- AI Status Card -->
          <div class="backdrop-blur-sm bg-white/50 dark:bg-gray-900/50 rounded-xl p-3 border border-gray-200/50 dark:border-gray-700/50">
            <div class="flex items-center gap-2">
              <div class="w-2 h-2 rounded-full" :class="aiStatus === 'ready' ? 'bg-green-500 animate-pulse' : aiStatus === 'error' ? 'bg-red-500' : 'bg-amber-500 animate-pulse'"></div>
              <span class="text-xs text-gray-500 dark:text-gray-400 flex-1">
                <span v-if="aiStatus === 'ready'">✨ AI Model Active</span>
                <span v-else-if="aiStatus === 'error'">⚡ Fallback Mode Active</span>
                <span v-else>🔄 Initializing AI...</span>
              </span>
              <UIcon name="i-lucide-brain-circuit" class="size-4 text-primary" />
            </div>
          </div>

          <!-- Reasoning Log -->
          <div v-if="dssLog.length" class="backdrop-blur-sm bg-white/50 dark:bg-gray-900/50 rounded-xl border border-gray-200/50 dark:border-gray-700/50 overflow-hidden transition-all">
            <button @click="showLog = !showLog" class="flex items-center justify-between w-full p-3 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors group">
              <div class="flex items-center gap-2">
                <UIcon name="i-lucide-file-search" class="size-4 text-amber-500" />
                <span class="text-xs font-semibold uppercase tracking-wider text-amber-600 dark:text-amber-400">Decision Log</span>
                <UBadge color="primary" variant="soft" size="xs" class="ml-1">{{ dssLog.length }}</UBadge>
              </div>
              <UIcon :name="showLog ? 'i-lucide-chevron-up' : 'i-lucide-chevron-down'" class="size-4 text-gray-400 transition-transform group-hover:scale-110" />
            </button>
            <Transition name="log-expand">
              <div v-if="showLog" class="p-3 pt-0 space-y-1.5 max-h-64 overflow-y-auto custom-scroll border-t border-gray-200/50 dark:border-gray-700/50">
                <div v-for="(log, i) in dssLog" :key="i" class="flex items-start gap-2 text-xs animate-slide-in">
                  <span class="text-gray-400 font-mono flex-shrink-0 w-8">{{ String(i + 1).padStart(2, '0') }}</span>
                  <UIcon :name="log.type === 'decision' ? 'i-lucide-zap' : log.type === 'warning' ? 'i-lucide-alert-triangle' : 'i-lucide-info'" class="size-3 mt-0.5" :class="log.type === 'decision' ? 'text-primary' : log.type === 'warning' ? 'text-amber-500' : 'text-blue-500'" />
                  <span class="flex-1 leading-relaxed">{{ log.msg }}</span>
                </div>
              </div>
            </Transition>
          </div>
        </aside>

        <!-- RIGHT PANEL -->
        <section class="lg:col-span-8 space-y-6">
          
          <Transition name="fade" mode="out-in">
            <div class="flex flex-col gap-3">
              <!-- Welcome Screen -->
              <div v-if="!results && !analyzing" class="backdrop-blur-xl bg-white/60 dark:bg-gray-900/60 rounded-2xl shadow-xl border border-gray-200/50 dark:border-gray-700/50 p-12 text-center animate-fade-in">
                <div class="relative inline-block mb-6">
                  <div class="absolute inset-0 bg-gradient-to-r from-primary-500 to-primary-600 rounded-full blur-xl opacity-30 animate-pulse"></div>
                  <div class="relative w-24 h-24 rounded-full bg-gradient-to-r from-primary-500 to-primary-600 flex items-center justify-center shadow-2xl">
                    <UIcon name="i-lucide-map" class="size-12 text-white" />
                  </div>
                </div>
                <h2 class="text-3xl font-bold bg-gradient-to-r from-gray-900 to-primary-600 dark:from-white dark:to-primary-400 bg-clip-text text-transparent mb-2">Ready for Adventure?</h2>
                <p class="text-gray-500 dark:text-gray-400 max-w-md mx-auto">
                  Tell us where you're going and what you like. Our AI will handle the rest.
                </p>
                <div class="mt-8 grid grid-cols-3 gap-3 max-w-sm mx-auto">
                  <div v-for="f in featureHighlights" :key="f.label" class="flex flex-col items-center gap-2 p-3 rounded-xl bg-white/50 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 backdrop-blur-sm">
                    <UIcon :name="f.icon" class="size-5 text-primary" />
                    <span class="text-xs text-gray-600 dark:text-gray-400">{{ f.label }}</span>
                  </div>
                </div>
              </div>

              <!-- Loading State -->
              <div v-else-if="analyzing" class="backdrop-blur-xl bg-white/60 dark:bg-gray-900/60 rounded-2xl shadow-xl border border-gray-200/50 dark:border-gray-700/50 p-12 text-center">
                <div class="loader-ring mx-auto mb-6"></div>
                <p class="text-lg font-semibold text-gray-900 dark:text-white">{{ loadingMsg }}</p>
                <div class="mt-6 space-y-2 max-w-xs mx-auto">
                  <div v-for="(step, i) in loadingSteps" :key="i" class="flex items-center gap-3 text-sm">
                    <div class="w-2 h-2 rounded-full transition-all" :class="i <= loadingStep ? 'bg-primary' : 'bg-gray-300 dark:bg-gray-600'"></div>
                    <span :class="i <= loadingStep ? 'text-gray-700 dark:text-gray-300' : 'text-gray-400'">{{ step }}</span>
                    <UIcon v-if="i === loadingStep" name="i-lucide-loader-2" class="size-3 text-primary animate-spin ml-auto" />
                    <UIcon v-else-if="i < loadingStep" name="i-lucide-check" class="size-3 text-green-500 ml-auto" />
                  </div>
                </div>
              </div>

              <!-- Results -->
              <template v-else-if="results && !analyzing">
                <!-- Weather Overview -->
              <div class="backdrop-blur-xl bg-gradient-to-br from-white to-gray-50 dark:from-gray-900 dark:to-gray-800 rounded-2xl shadow-xl border border-gray-200/50 dark:border-gray-700/50 p-5 sm:p-6 animate-slide-up">
                  <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                    <div>
                      <div class="flex items-center gap-2 mb-1">
                        <UIcon name="i-lucide-map-pin" class="size-4 text-primary" />
                        <span class="text-xs font-semibold uppercase tracking-wider text-primary">{{ results.location.name }}</span>
                      </div>
                      <h3 class="text-2xl font-bold text-gray-900 dark:text-white">{{ formatDateTime(selectedDate, selectedTime) }}</h3>
                      <p class="text-xs text-gray-500 mt-1">Local time at destination</p>
                    </div>
                    <div class="flex items-center gap-4">
                      <div class="text-right">
                        <UIcon :name="results.weather.iconName" class="size-12 text-amber-400" />
                        <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ results.weather.temp }}°C</p>
                        <p class="text-xs text-gray-500">{{ results.weather.description }}</p>
                      </div>
                    </div>
                  </div>
                  
                  <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6">
                    <div v-for="stat in results.weather.stats" :key="stat.label" class="flex flex-col items-center gap-1 p-3 rounded-xl bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
                      <UIcon :name="stat.icon" class="size-4 text-primary" />
                      <span class="text-lg font-bold text-gray-900 dark:text-white">{{ stat.value }}</span>
                      <span class="text-[10px] text-gray-500 uppercase">{{ stat.label }}</span>
                    </div>
                  </div>
                  
                  <div class="flex flex-wrap gap-2 mt-4 pt-4 border-t border-gray-200/50 dark:border-gray-700/50">
                    <UBadge v-for="badge in results.weather.dssFlags" :key="badge.label" :color="badge.color" variant="soft" size="sm" class="gap-1">
                      <UIcon :name="badge.icon" class="size-3" />
                      {{ badge.label }}
                    </UBadge>
                  </div>
                </div>

                <!-- Dressing & Packing Guide (First Recommendation) -->
                <div class="backdrop-blur-xl bg-gradient-to-r from-emerald-50/80 to-cyan-50/80 dark:from-emerald-900/20 dark:to-cyan-900/20 rounded-xl border border-emerald-200 dark:border-emerald-800 p-4 sm:p-5 animate-slide-up">
                  <div class="flex items-start gap-4">
                    <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-emerald-500 to-cyan-500 flex items-center justify-center shadow-lg">
                      <UIcon name="i-lucide-shirt" class="size-6 text-white" />
                    </div>
                    <div class="flex-1">
                      <div class="flex items-center gap-2 mb-2">
                        <span class="text-sm font-bold text-gray-900 dark:text-white">What to Wear & Pack</span>
                        <UBadge color="success" variant="soft" size="xs">Weather Guide</UBadge>
                      </div>
                      <p class="text-sm text-gray-600 dark:text-gray-300 mb-3">
                        {{ primaryWearReasons.length ? 'AI-personalized clothing advice for your selected conditions.' : results.packingAdvice.summary }}
                      </p>
                      <div class="flex flex-wrap gap-2">
                        <span v-for="item in primaryWearItems" :key="item" class="text-xs px-2.5 py-1 rounded-full bg-white/70 dark:bg-gray-800/70 text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-700">
                          <UIcon name="i-lucide-check-circle-2" class="size-3 inline mr-1 text-green-500" />
                          {{ item }}
                        </span>
                      </div>
                      <ul v-if="primaryWearReasons.length" class="mt-3 space-y-1.5">
                        <li v-for="reason in primaryWearReasons" :key="reason" class="flex items-start gap-2 text-xs text-gray-600 dark:text-gray-300">
                          <UIcon name="i-lucide-arrow-right" class="size-3 mt-0.5 text-emerald-500 flex-shrink-0" />
                          {{ reason }}
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>

                <!-- Recommendations Section -->
                <div class="space-y-3.5">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center gap-2">
                      <div class="w-1 h-6 bg-gradient-to-b from-primary-500 to-primary-600 rounded-full"></div>
                      <span class="text-sm font-semibold uppercase tracking-wider text-primary">AI Recommendations</span>
                      <UBadge color="primary" variant="soft" size="xs">{{ results.activities?.length }} Options</UBadge>
                    </div>
                    <div class="flex items-center gap-1 text-xs text-gray-500">
                      <UIcon name="i-lucide-brain" class="size-3" />
                      <span>{{ results.aiPowered ? 'AI Generated' : 'Rule-Based' }}</span>
                    </div>
                  </div>

                  <div class="space-y-3">
                    <div
                      v-for="(activity, idx) in results.activities"
                      :key="activity.id"
                      class="group relative backdrop-blur-sm bg-white/70 dark:bg-gray-900/70 rounded-xl border transition-all duration-300 cursor-pointer overflow-hidden"
                      :class="[
                        selectedActivity?.id === activity.id 
                          ? 'border-primary shadow-xl scale-[1.01]' 
                          : 'border-gray-200/50 dark:border-gray-700/50 hover:shadow-lg hover:scale-[1.01]'
                      ]"
                      @click="selectedActivity = selectedActivity?.id === activity.id ? null : activity"
                    >
                      <div class="p-5">
                        <div class="flex items-start gap-4">
                          <div class="relative flex-shrink-0">
                            <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-primary-100 to-primary-200 dark:from-primary-900/30 dark:to-primary-800/30 flex items-center justify-center border border-primary/20 group-hover:scale-110 transition-transform">
                              <UIcon :name="activity.iconName" class="size-7 text-primary" />
                            </div>
                            <div v-if="idx === 0" class="absolute -top-2 -right-2 w-6 h-6 rounded-full bg-gradient-to-r from-amber-400 to-orange-500 flex items-center justify-center shadow-lg animate-bounce">
                              <span class="text-[10px] font-bold text-white">1</span>
                            </div>
                          </div>
                          
                          <div class="flex-1">
                            <div class="flex items-center gap-2 flex-wrap mb-2">
                              <h4 class="font-bold text-gray-900 dark:text-white">{{ activity.name }}</h4>
                              <UBadge :color="activity.intensityColor" variant="soft" size="xs" class="gap-1">
                                <UIcon name="i-lucide-activity" class="size-3" />
                                {{ activity.intensity }}
                              </UBadge>
                            </div>
                            <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">{{ activity.description }}</p>
                            <div class="flex flex-wrap gap-1.5 mt-3">
                              <span v-for="tag in activity.tags" :key="tag" class="text-[10px] px-2 py-0.5 rounded-full bg-gray-200/70 dark:bg-gray-700/70 text-gray-600 dark:text-gray-400">
                                #{{ tag }}
                              </span>
                            </div>
                            
                            <Transition name="expand">
                              <div v-if="selectedActivity?.id === activity.id" class="mt-4 pt-4 border-t border-gray-200/50 dark:border-gray-700/50 space-y-3">
                                <div>
                                  <div class="flex items-center gap-2 mb-2">
                                    <UIcon name="i-lucide-lightbulb" class="size-4 text-amber-500" />
                                    <span class="text-xs font-semibold uppercase text-primary">Why This Works</span>
                                  </div>
                                  <ul class="space-y-1.5">
                                    <li v-for="r in activity.reasoning" :key="r" class="flex items-start gap-2 text-xs text-gray-600 dark:text-gray-400">
                                      <UIcon name="i-lucide-check-circle-2" class="size-3 text-green-500 mt-0.5 flex-shrink-0" />
                                      {{ r }}
                                    </li>
                                  </ul>
                                </div>
                                
                                <div v-if="activity.bestTime" class="flex items-center gap-2 text-xs bg-amber-50 dark:bg-amber-900/20 p-2 rounded-lg">
                                  <UIcon name="i-lucide-clock" class="size-3 text-amber-600" />
                                  <span class="text-amber-700 dark:text-amber-400">Best time: {{ activity.bestTime }}</span>
                                </div>

                                <div v-if="activity.whatToWear?.length">
                                  <div class="flex items-center gap-2 mb-2">
                                    <UIcon name="i-lucide-shirt" class="size-4 text-emerald-600" />
                                    <span class="text-xs font-semibold uppercase text-emerald-600 dark:text-emerald-400">What to Wear</span>
                                  </div>
                                  <div class="flex flex-wrap gap-1.5">
                                    <span v-for="item in activity.whatToWear" :key="item" class="text-xs px-2 py-1 rounded-full bg-emerald-100/70 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800">
                                      {{ item }}
                                    </span>
                                  </div>
                                </div>

                                <div v-if="activity.wearReasoning?.length">
                                  <div class="flex items-center gap-2 mb-2">
                                    <UIcon name="i-lucide-list-checks" class="size-4 text-emerald-600" />
                                    <span class="text-xs font-semibold uppercase text-emerald-600 dark:text-emerald-400">Why This Clothing Works</span>
                                  </div>
                                  <ul class="space-y-1.5">
                                    <li v-for="reason in activity.wearReasoning" :key="reason" class="flex items-start gap-2 text-xs text-gray-600 dark:text-gray-400">
                                      <UIcon name="i-lucide-check-circle-2" class="size-3 text-emerald-500 mt-0.5 flex-shrink-0" />
                                      {{ reason }}
                                    </li>
                                  </ul>
                                </div>
                                
                                <div v-if="activity.whatToBring?.length">
                                  <div class="flex items-center gap-2 mb-2">
                                    <UIcon name="i-lucide-package" class="size-4 text-primary" />
                                    <span class="text-xs font-semibold uppercase text-primary">What to Bring</span>
                                  </div>
                                  <div class="flex flex-wrap gap-1.5">
                                    <span v-for="item in activity.whatToBring" :key="item" class="text-xs px-2 py-1 rounded-full bg-primary/10 text-primary border border-primary/20">
                                      {{ item }}
                                    </span>
                                  </div>
                                </div>
                                
                                <div class="flex gap-2 pt-2">
                                  <UButton size="xs" color="primary" icon="i-lucide-thumbs-up" class="rounded-lg">Save</UButton>
                                  <UButton size="xs" color="neutral" variant="ghost" icon="i-lucide-refresh-cw" @click.stop="runAdvisor" class="rounded-lg">Refresh</UButton>
                                </div>
                              </div>
                            </Transition>
                          </div>
                          
                          <div class="flex flex-col items-end gap-1">
                            <div class="text-right">
                              <div class="text-2xl font-bold bg-gradient-to-r from-primary-500 to-primary-600 bg-clip-text text-transparent">{{ activity.dssScore }}</div>
                              <div class="text-[10px] text-gray-400 uppercase">match</div>
                            </div>
                            <UIcon :name="selectedActivity?.id === activity.id ? 'i-lucide-chevron-up' : 'i-lucide-chevron-down'" class="size-4 text-gray-400 group-hover:text-primary transition-colors" />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

        

                <!-- Hourly Forecast -->
                <div class="backdrop-blur-xl bg-white/70 dark:bg-gray-900/70 rounded-xl border border-gray-200/50 dark:border-gray-700/50 p-4 sm:p-5">
                  <div class="flex items-center justify-between mb-4">
                    <div class="flex items-center gap-2">
                      <UIcon name="i-lucide-calendar-clock" class="size-5 text-amber-500" />
                      <span class="text-sm font-semibold uppercase tracking-wider text-amber-600 dark:text-amber-400">Hourly Outlook</span>
                    </div>
                    <span class="text-xs text-gray-500">Click any hour to update recommendations</span>
                  </div>
                  <div class="flex gap-3 overflow-x-auto pb-3 custom-scroll-x">
                    <button
                      v-for="h in results.hourly" 
                      :key="h.time"
                      @click="selectHourlyTime(h.time)"
                      class="flex-shrink-0 flex flex-col items-center gap-1.5 px-4 py-3 min-w-[70px] rounded-xl transition-all duration-200 hover:scale-105"
                      :class="h.isSelected 
                        ? 'bg-gradient-to-r from-primary-500 to-primary-600 text-white shadow-lg' 
                        : 'bg-white/50 dark:bg-gray-800/50 border border-gray-200/50 dark:border-gray-700/50 hover:border-primary/50'"
                    >
                      <span class="text-xs font-mono">{{ h.time }}</span>
                      <UIcon :name="h.iconName" class="size-6" :class="h.isSelected ? 'text-white' : 'text-amber-400'" />
                      <span class="text-sm font-bold">{{ h.temp }}°</span>
                      <div class="flex items-center gap-0.5">
                        <UIcon name="i-lucide-droplets" class="size-2.5" />
                        <span class="text-[10px]">{{ h.rain }}%</span>
                      </div>
                    </button>
                  </div>
                </div>

                   <!-- Multi-Criteria Scoring (Last) -->
                <div class="backdrop-blur-xl bg-white/70 dark:bg-gray-900/70 rounded-xl border border-gray-200/50 dark:border-gray-700/50 p-4 sm:p-5">
                  <div class="flex items-center gap-2 mb-4">
                    <UIcon name="i-lucide-bar-chart-3" class="size-5 text-violet-500" />
                    <span class="text-sm font-semibold uppercase tracking-wider text-violet-500">Multi-Criteria Scoring</span>
                  </div>
                  <div class="space-y-4">
                    <div v-for="c in results.dssScores" :key="c.name">
                      <div class="flex justify-between text-xs mb-1">
                        <span class="text-gray-600 dark:text-gray-400 flex items-center gap-1.5">
                          <UIcon :name="c.icon" class="size-3.5" />
                          {{ c.name }}
                        </span>
                        <span class="font-mono font-semibold" :class="c.score >= 70 ? 'text-green-500' : c.score >= 40 ? 'text-amber-500' : 'text-red-500'">{{ c.score }}/100</span>
                      </div>
                      <div class="h-2 bg-gray-200 dark:bg-gray-800 rounded-full overflow-hidden">
                        <div class="h-full rounded-full transition-all duration-700 ease-out" :style="{ width: c.score + '%', background: c.color }" />
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Reset Button -->
                <div class="flex justify-center">
                  <UButton @click="resetAll" color="neutral" variant="soft" size="sm" class="rounded-lg opacity-60 hover:opacity-100 transition-opacity" icon="i-lucide-rotate-ccw">
                    Start New Analysis
                  </UButton>
                </div>
              </template>
            </div>
          </Transition>
        </section>
      </div>
    </main>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'

// Interfaces
interface Location { lat: number; lon: number; name: string }
interface DSSLog { msg: string; type: 'info' | 'decision' | 'warning' }
interface Activity {
  id: string; name: string; iconName: string; description: string
  intensity: string; intensityColor: string; dssScore: number
  tags: string[]; reasoning: string[]; bestTime?: string; whatToBring?: string[]
  whatToWear?: string[]; wearReasoning?: string[]
}
interface WeatherStat { icon: string; value: string; label: string }
interface WeatherData {
  temp: number; description: string; iconName: string
  stats: WeatherStat[]; dssFlags: { label: string; icon: string; color: string }[]
  raw: { humidity: number; wind: number; rainProb: number; uv: number; wc: number }
}
interface HourlyForecast { time: string; temp: number; iconName: string; rain: number; isSelected: boolean }
interface DSSCriteria { name: string; icon: string; score: number; color: string }
interface PackingAdvice { summary: string; items: string[] }
interface Results {
  location: Location; weather: WeatherData; activities: Activity[]
  dssScores: DSSCriteria[]; hourly: HourlyForecast[]; aiPowered: boolean
  packingAdvice: PackingAdvice
}

// State
const locationMode = ref<'manual' | 'map' | 'gps'>('manual')
const locationQuery = ref('')
const locationSuggestions = ref<any[]>([])
const selectedLocation = ref<Location | null>(null)
const geocoding = ref(false)
const gpsLoading = ref(false)
const mapReady = ref(false)
const mapContainer = ref<HTMLElement | null>(null)
const selectedDate = ref(new Date().toISOString().split('T')[0])
const selectedTime = ref('12:00')
const groupSize = ref(2)
const selectedPrefs = ref<string[]>(['outdoor', 'social'])
const analyzing = ref(false)
const results = ref<Results | null>(null)
const selectedActivity = ref<Activity | null>(null)
const dssLog = ref<DSSLog[]>([])
const showLog = ref(false)
const loadingStep = ref(0)
const loadingMsg = ref('Fetching real-time weather data...')
const aiStatus = ref<'ready' | 'error' | 'loading'>('loading')
let leafletMap: any = null

const primaryWearItems = computed(() => {
  const lead = results.value?.activities?.[0]
  if (lead?.whatToWear?.length) return lead.whatToWear
  return results.value?.packingAdvice.items ?? []
})

const primaryWearReasons = computed(() => {
  const lead = results.value?.activities?.[0]
  return lead?.wearReasoning?.slice(0, 3) ?? []
})

// Constants
const API_URL = 'https://api.tera-in.top/recommendations'
const todayDate = computed(() => new Date().toISOString().split('T')[0])

const locationModes = [
  { value: 'manual', label: 'Type', icon: 'i-lucide-pencil' },
  { value: 'map', label: 'Map', icon: 'i-lucide-map' },
  { value: 'gps', label: 'GPS', icon: 'i-lucide-navigation' },
]

const activityPrefs = [
  { value: 'outdoor', label: 'Outdoor', icon: 'i-lucide-tree-pine' },
  { value: 'indoor', label: 'Indoor', icon: 'i-lucide-house' },
  { value: 'social', label: 'Social', icon: 'i-lucide-users' },
  { value: 'solo', label: 'Solo', icon: 'i-lucide-user' },
  { value: 'adventure', label: 'Adventure', icon: 'i-lucide-zap' },
  { value: 'relaxed', label: 'Relaxed', icon: 'i-lucide-waves' },
  { value: 'cultural', label: 'Cultural', icon: 'i-lucide-theater' },
  { value: 'food', label: 'Food', icon: 'i-lucide-utensils' },
]

const featureHighlights = [
  { icon: 'i-lucide-cloud-sun', label: 'Live Weather' },
  { icon: 'i-lucide-brain-circuit', label: 'AI Model' },
  { icon: 'i-lucide-target', label: 'Smart Scoring' },
]

const loadingMessages = [
  'Fetching real-time weather data...',
  'Building climate profile...',
  'Querying AI model...',
  'Scoring recommendations...',
]

const loadingSteps = [
  'Geocoding location',
  'Fetching weather forecast',
  'Generating AI recommendations',
  'Ranking recommendation fit',
]

// Helper Functions
function wcToIconName(wc: number): string {
  if (wc === 0) return 'i-lucide-sun'
  if (wc <= 3) return 'i-lucide-cloud-sun'
  if (wc <= 48) return 'i-lucide-cloud-fog'
  if (wc <= 67) return 'i-lucide-cloud-rain'
  if (wc <= 77) return 'i-lucide-snowflake'
  if (wc <= 82) return 'i-lucide-cloud-drizzle'
  return 'i-lucide-cloud-lightning'
}

function wcToDesc(wc: number): string {
  if (wc === 0) return 'Clear sky'
  if (wc <= 3) return 'Partly cloudy'
  if (wc <= 48) return 'Foggy'
  if (wc <= 67) return 'Rainy'
  if (wc <= 77) return 'Snowy'
  if (wc <= 82) return 'Showers'
  return 'Thunderstorm'
}

function inferIcon(name: string): string {
  const n = name.toLowerCase()
  if (n.includes('hik') || n.includes('trek') || n.includes('walk')) return 'i-lucide-footprints'
  if (n.includes('cycl') || n.includes('bike')) return 'i-lucide-bike'
  if (n.includes('swim') || n.includes('pool') || n.includes('beach')) return 'i-lucide-waves'
  if (n.includes('museum') || n.includes('gallery') || n.includes('art')) return 'i-lucide-landmark'
  if (n.includes('food') || n.includes('dine') || n.includes('restaurant')) return 'i-lucide-utensils'
  if (n.includes('yoga') || n.includes('meditat')) return 'i-lucide-person-standing'
  if (n.includes('photo') || n.includes('camera')) return 'i-lucide-camera'
  if (n.includes('park') || n.includes('picnic')) return 'i-lucide-tree-pine'
  if (n.includes('market') || n.includes('shop')) return 'i-lucide-shopping-bag'
  if (n.includes('stargazing') || n.includes('stars')) return 'i-lucide-stars'
  if (n.includes('bird') || n.includes('wildlife')) return 'i-lucide-bird'
  if (n.includes('indoor')) return 'i-lucide-house'
  return 'i-lucide-star'
}

function addLog(type: DSSLog['type'], msg: string) {
  dssLog.value.unshift({ type, msg })
  if (dssLog.value.length > 25) dssLog.value.pop()
}

function togglePref(val: string) {
  const idx = selectedPrefs.value.indexOf(val)
  if (idx > -1) selectedPrefs.value.splice(idx, 1)
  else selectedPrefs.value.push(val)
}

function formatDateTime(date: string, time: string): string {
  try {
    const d = new Date(`${date}T${time}`)
    return d.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' }) + ' at ' + d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
  } catch { return `${date} ${time}` }
}

function normalizeStringList(value: unknown): string[] {
  if (Array.isArray(value)) {
    return value.map(v => String(v).trim()).filter(Boolean)
  }
  if (typeof value === 'string') {
    return value
      .split(/[\n,;]+/)
      .map(v => v.replace(/^[-*]\s*/, '').trim())
      .filter(Boolean)
  }
  return []
}

function generatePackingAdvice(weather: WeatherData): PackingAdvice {
  const isRainy = weather.raw.rainProb > 60
  const isHot = weather.temp > 32
  const isCold = weather.temp < 12
  const isHighUV = weather.raw.uv > 7
  const isWindy = weather.raw.wind > 30
  
  const items: string[] = []
  let summary = ''
  
  if (isHot) {
    summary = `With ${weather.temp}°C heat, prioritize lightweight, breathable fabrics and sun protection.`
    items.push('Lightweight, breathable clothing', 'Sun hat or cap', 'Sunscreen SPF 50+', 'Sunglasses', 'Reusable water bottle')
    if (isHighUV) items.push('UPF-rated clothing')
  } else if (isCold) {
    summary = `Bundle up! ${weather.temp}°C calls for layers and warm accessories.`
    items.push('Warm jacket or coat', 'Layers (thermal base layer)', 'Scarf, gloves, and beanie', 'Warm socks')
  } else {
    summary = `Comfortable ${weather.temp}°C conditions — dress for comfort and be prepared.`
    items.push('Comfortable walking shoes', 'Light jacket or sweater', 'Water bottle')
  }
  
  if (isRainy) {
    summary += ` ${weather.raw.rainProb}% chance of rain — bring waterproof gear.`
    items.push('Umbrella', 'Waterproof jacket')
  }
  
  if (isWindy) items.push('Windbreaker')
  if (isHighUV && !isHot) items.push('Sunscreen', 'Sun hat')
  
  return { summary, items }
}

// Location Functions
async function geocodeLocation() {
  if (!locationQuery.value.trim()) return
  geocoding.value = true
  locationSuggestions.value = []
  try {
    const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(locationQuery.value)}&limit=5`, { headers: { 'Accept-Language': 'en' } })
    const data = await res.json()
    locationSuggestions.value = data
    if (data.length === 1) selectSuggestion(data[0])
  } catch {
    addLog('warning', 'Geocoding unavailable')
  } finally { geocoding.value = false }
}

function selectSuggestion(s: any) {
  selectedLocation.value = { lat: parseFloat(s.lat), lon: parseFloat(s.lon), name: s.display_name.split(',').slice(0, 3).join(', ') }
  locationSuggestions.value = []
  locationQuery.value = selectedLocation.value.name
  addLog('info', `Location set: ${selectedLocation.value.name}`)
}

async function getGPSLocation() {
  gpsLoading.value = true
  try {
    const pos = await new Promise<GeolocationPosition>((res, rej) => navigator.geolocation.getCurrentPosition(res, rej, { timeout: 10000 }))
    const { latitude: lat, longitude: lon } = pos.coords
    const rev = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`)
    const data = await rev.json()
    selectedLocation.value = { lat, lon, name: data.display_name?.split(',').slice(0, 3).join(', ') || `${lat.toFixed(4)}, ${lon.toFixed(4)}` }
    addLog('info', `GPS: ${selectedLocation.value.name}`)
  } catch { addLog('warning', 'GPS unavailable') } finally { gpsLoading.value = false }
}

async function initMap() {
  await nextTick()
  if (!mapContainer.value || leafletMap) return
  try {
    if (!document.getElementById('leaflet-css')) {
      const link = document.createElement('link')
      link.id = 'leaflet-css'; link.rel = 'stylesheet'
      link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
      document.head.appendChild(link)
    }
    const L = await import('https://unpkg.com/leaflet@1.9.4/dist/leaflet-src.esm.js' as any)
    if (!L) return
    leafletMap = L.map(mapContainer.value).setView([-1.286, 36.817], 6)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', { attribution: '© CartoDB', subdomains: 'abcd', maxZoom: 19 }).addTo(leafletMap)
    leafletMap.on('click', async (e: any) => {
      const { lat, lng } = e.latlng
      try {
        const rev = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`)
        const data = await rev.json()
        selectedLocation.value = { lat, lon: lng, name: data.display_name?.split(',').slice(0, 3).join(', ') || `${lat.toFixed(4)}, ${lng.toFixed(4)}` }
      } catch { selectedLocation.value = { lat, lon: lng, name: `${lat.toFixed(4)}, ${lng.toFixed(4)}` } }
      L.marker([lat, lng]).addTo(leafletMap).bindPopup(selectedLocation.value!.name).openPopup()
      addLog('info', `Map pin: ${selectedLocation.value!.name}`)
    })
    mapReady.value = true
  } catch { mapReady.value = false }
}

watch(locationMode, async (val) => { if (val === 'map') { await nextTick(); setTimeout(initMap, 100) } })

// Weather Functions
async function fetchWeather(lat: number, lon: number): Promise<WeatherData> {
  try {
    const res = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation_probability,weathercode,uv_index&forecast_days=1`)
    const data = await res.json()
    const c = data.current
    const temp = Math.round(c.temperature_2m)
    const humidity = c.relative_humidity_2m
    const wind = Math.round(c.wind_speed_10m)
    const rainProb = c.precipitation_probability ?? 0
    const uv = c.uv_index ?? 0
    const wc = c.weathercode ?? 0

    const flags: any[] = []
    if (temp >= 20 && temp <= 30) flags.push({ label: 'Comfortable Temp', icon: 'i-lucide-circle-check', color: 'green' })
    else if (temp > 35) flags.push({ label: 'Heat Alert', icon: 'i-lucide-flame', color: 'red' })
    else if (temp < 10) flags.push({ label: 'Cold Advisory', icon: 'i-lucide-snowflake', color: 'blue' })
    if (rainProb > 60) flags.push({ label: 'Rain Likely', icon: 'i-lucide-cloud-rain', color: 'yellow' })
    if (uv > 7) flags.push({ label: 'High UV', icon: 'i-lucide-sun', color: 'orange' })
    if (wind > 30) flags.push({ label: 'Windy', icon: 'i-lucide-wind', color: 'sky' })
    if (!flags.length) flags.push({ label: 'Ideal Conditions', icon: 'i-lucide-star', color: 'green' })

    return {
      temp, description: wcToDesc(wc), iconName: wcToIconName(wc),
      stats: [
        { icon: 'i-lucide-droplets', value: `${humidity}%`, label: 'Humidity' },
        { icon: 'i-lucide-wind', value: `${wind} km/h`, label: 'Wind' },
        { icon: 'i-lucide-cloud-rain', value: `${rainProb}%`, label: 'Rain' },
        { icon: 'i-lucide-sun', value: String(uv), label: 'UV Index' },
      ],
      dssFlags: flags,
      raw: { humidity, wind, rainProb, uv, wc },
    }
  } catch {
    return {
      temp: 24, description: 'Partly cloudy', iconName: 'i-lucide-cloud-sun',
      stats: [
        { icon: 'i-lucide-droplets', value: '60%', label: 'Humidity' },
        { icon: 'i-lucide-wind', value: '15 km/h', label: 'Wind' },
        { icon: 'i-lucide-cloud-rain', value: '20%', label: 'Rain' },
        { icon: 'i-lucide-sun', value: '5', label: 'UV Index' },
      ],
      dssFlags: [{ label: 'Estimated Data', icon: 'i-lucide-triangle-alert', color: 'yellow' }],
      raw: { humidity: 60, wind: 15, rainProb: 20, uv: 5, wc: 2 },
    }
  }
}

async function fetchHourly(lat: number, lon: number): Promise<HourlyForecast[]> {
  try {
    const res = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&hourly=temperature_2m,weathercode,precipitation_probability&forecast_days=1`)
    const data = await res.json()
    const h = data.hourly
    const selectedHour = parseInt(selectedTime.value.split(':')[0])
    return Array.from({ length: 8 }, (_, i) => {
      const hourIdx = Math.max(0, Math.min(23, selectedHour - 2 + i))
      const wc = h.weathercode?.[hourIdx] ?? 0
      return { time: `${String(hourIdx).padStart(2, '0')}:00`, temp: Math.round(h.temperature_2m?.[hourIdx] ?? 20), iconName: wcToIconName(wc), rain: h.precipitation_probability?.[hourIdx] ?? 0, isSelected: hourIdx === selectedHour }
    })
  } catch { return [] }
}

// Build AI Prompt
function buildAIPrompt(weather: WeatherData, prefs: string[], groupSz: number, location: Location): string {
  const hour = parseInt(selectedTime.value.split(':')[0])
  const timeOfDay = hour < 12 ? 'morning' : hour < 17 ? 'afternoon' : hour < 20 ? 'evening' : 'night'
  const comfortBand = weather.temp < 12 ? 'cold' : weather.temp <= 26 ? 'mild' : weather.temp <= 32 ? 'warm' : 'hot'
  const rainBand = weather.raw.rainProb >= 70 ? 'high' : weather.raw.rainProb >= 40 ? 'moderate' : 'low'
  const uvBand = weather.raw.uv >= 8 ? 'very high' : weather.raw.uv >= 6 ? 'high' : weather.raw.uv >= 3 ? 'moderate' : 'low'
  
  const prefersIndoorOnly = prefs.includes('indoor') && !prefs.includes('outdoor')
  const prefersOutdoorOnly = prefs.includes('outdoor') && !prefs.includes('indoor')
  
  let preferenceGuidance = ''
  if (prefersIndoorOnly) {
    preferenceGuidance = 'IMPORTANT: User prefers INDOOR activities only. DO NOT recommend hiking, walking, outdoor sports, or any outdoor physical activities. Focus on museums, cafes, galleries, indoor markets, cinemas, etc.'
  } else if (prefersOutdoorOnly) {
    preferenceGuidance = 'IMPORTANT: User prefers OUTDOOR activities only. DO NOT recommend indoor museums, cinemas, or indoor venues. Focus on parks, hiking, cycling, outdoor sports, etc.'
  }
  
  return `You are a weather-aware local activity planner.
Generate exactly 5 personalized recommendations for ${location.name} on ${selectedDate.value} at ${selectedTime.value} (${timeOfDay}).

Weather context:
- temperature_c: ${weather.temp}
- apparent_comfort_band: ${comfortBand}
- condition_text: ${weather.description}
- weather_code: ${weather.raw.wc}
- rain_probability_percent: ${weather.raw.rainProb} (${rainBand})
- humidity_percent: ${weather.raw.humidity}
- wind_kmh: ${weather.raw.wind}
- uv_index: ${weather.raw.uv} (${uvBand})

User context:
- group_size: ${groupSz}
- preferences: ${prefs.join(', ') || 'none'}
${preferenceGuidance}

Rules:
1) First item should be "Dressing & Packing Guide".
2) For every item, include specific clothing choices based on the weather (examples: "light waterproof jacket", "breathable long-sleeve layer", "non-slip shoes").
3) Include short reasons explaining why each clothing choice works for this exact weather.
4) If indoor-only preference is selected, do not include hiking/walk/trail/outdoor-only activities.
5) Avoid percentages and avoid saying what not to do.

Return ONLY valid JSON array (no markdown) with this exact schema per item:
{
  "id": "string",
  "name": "string",
  "description": "string",
  "intensity": "Low|Moderate|High",
  "intensityColor": "blue|yellow|red",
  "tags": ["string"],
  "reasoning": ["string"],
  "bestTime": "string",
  "whatToWear": ["string"],
  "wearReasoning": ["string"],
  "whatToBring": ["string"]
}`
}

function extractAIActivities(input: any): any[] {
  const parseObjectChunks = (text: string): any[] => {
    const out: any[] = []
    let inString = false
    let escape = false
    let depth = 0
    let start = -1

    for (let i = 0; i < text.length; i++) {
      const ch = text[i]
      if (escape) { escape = false; continue }
      if (ch === '\\') { if (inString) escape = true; continue }
      if (ch === '"') { inString = !inString; continue }
      if (inString) continue
      if (ch === '{') { if (depth === 0) start = i; depth++ }
      else if (ch === '}') {
        if (depth > 0) depth--
        if (depth === 0 && start !== -1) {
          try { out.push(JSON.parse(text.slice(start, i + 1))) } catch {}
          start = -1
        }
      }
    }
    return out
  }

  const normalise = (value: any): any[] => {
    if (!value) return []
    if (Array.isArray(value)) return value

    if (typeof value === 'object') {
      if (Array.isArray(value.recommendations)) return value.recommendations
      if (typeof value.recommendations === 'string') return normalise(value.recommendations)
      if (Array.isArray(value.activities)) return value.activities
      if (typeof value.generated_text === 'string') return normalise(value.generated_text)
      return []
    }

    if (typeof value === 'string') {
      const cleaned = value
        .replace(/```json\s*/g, '')
        .replace(/```\s*/g, '')
        .trim()

      try {
        const parsed = JSON.parse(cleaned)
        return normalise(parsed)
      } catch {
        const start = cleaned.indexOf('[')
        const end = cleaned.lastIndexOf(']')
        if (start !== -1 && end > start) {
          try {
            const parsed = JSON.parse(cleaned.slice(start, end + 1))
            return Array.isArray(parsed) ? parsed : []
          } catch {
            // Try chunk mode below.
          }
        }
        return parseObjectChunks(start !== -1 ? cleaned.slice(start) : cleaned)
      }
    }

    return []
  }

  return normalise(input)
}

// Call AI API
async function callAIApi(prompt: string): Promise<any[]> {
  try {
    addLog('info', 'Calling AI recommendation API...')
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt }),
    })
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`)
    }
    
    const data = await response.json()
    
    return extractAIActivities(data)
  } catch (error) {
    console.error('AI API error:', error)
    addLog('warning', 'AI API failed, using fallback')
    return []
  }
}

// Parse AI response into Activity objects
function parseAIResponse(aiActivities: any[]): Activity[] {
  return aiActivities.map((a, idx) => {
    const tags = normalizeStringList(a.tags)
    const reasoning = normalizeStringList(a.reasoning)
    const whatToBring = normalizeStringList(a.whatToBring)
    const whatToWear = normalizeStringList(a.whatToWear ?? a.clothing ?? a.wear ?? a.outfit)
    const wearReasoning = normalizeStringList(a.wearReasoning ?? a.clothingReasoning ?? a.clothingReasons ?? a.whyWear)

    return {
      id: a.id || `ai-activity-${idx}`,
      name: a.name || 'Activity',
      description: a.description || 'No description available',
      intensity: ['Low', 'Moderate', 'High'].includes(a.intensity) ? a.intensity : 'Moderate',
      intensityColor: ['blue', 'yellow', 'red'].includes(a.intensityColor) ? a.intensityColor : 'blue',
      dssScore: typeof a.dssScore === 'number' ? a.dssScore : 75,
      tags,
      reasoning: reasoning.length ? reasoning : ['AI-generated recommendation based on weather and preferences'],
      bestTime: a.bestTime,
      whatToBring,
      whatToWear,
      wearReasoning,
      iconName: inferIcon(a.name || ''),
    }
  })
}

// Generate fallback activities (in case AI fails)
function generateFallbackActivities(weather: WeatherData, prefs: string[], groupSz: number): Activity[] {
  const isRainy = weather.raw.rainProb > 60
  const isHot = weather.temp > 32
  const isCold = weather.temp < 12
  const hour = parseInt(selectedTime.value.split(':')[0])
  const isEvening = hour >= 17
  
  const activities: Activity[] = []
  
  if (isRainy) {
    activities.push({
      id: 'indoor-market', name: 'Indoor Market Exploration', iconName: 'i-lucide-shopping-bag',
      description: `Rain is the perfect excuse to dive into a vibrant covered market. Browse local crafts, street food, and sheltered stalls while staying completely dry.`,
      intensity: 'Low', intensityColor: 'blue', dssScore: 85,
      tags: ['indoor', 'social', 'food', 'cultural'],
      reasoning: [`${weather.raw.rainProb}% rain probability makes outdoor activities risky`, 'Covered markets are fully weather-proof', `${groupSz} people can browse comfortably`, 'Social and cultural experience regardless of weather'],
      bestTime: 'Any time during opening hours',
      whatToBring: ['Umbrella', 'Shopping bag', 'Cash/card'],
      whatToWear: ['Light waterproof jacket', 'Breathable t-shirt', 'Non-slip sneakers'],
      wearReasoning: ['A waterproof top keeps you dry between indoor sections.', 'Breathable base layer avoids overheating indoors.', 'Non-slip soles help on wet market floors.'],
    })
  }
  
  if (isHot && !prefs.includes('indoor')) {
    activities.push({
      id: 'water-activity', name: 'Swimming / Water Activity', iconName: 'i-lucide-waves',
      description: `Beat the ${weather.temp}°C heat with a refreshing water activity.`,
      intensity: 'Moderate', intensityColor: 'yellow', dssScore: 88,
      tags: ['outdoor', 'adventure', 'social'],
      reasoning: [`${weather.temp}°C is hot — water activities are the most comfortable`, 'Swimming naturally regulates body temperature', `Group of ${groupSz} can enjoy together`, 'Water reflects UV; apply SPF'],
      bestTime: 'Before 10 AM or after 4 PM',
      whatToBring: ['Swimwear', 'Sunscreen SPF50+', 'Hat', 'Water bottle'],
      whatToWear: ['Quick-dry top', 'Swimwear', 'Slip-resistant sandals', 'UV-protective hat'],
      wearReasoning: ['Quick-dry fabric prevents discomfort after splashes.', 'Lightwear helps your body cool in heat.', 'Grip footwear helps around wet surfaces.', 'A hat reduces direct sun exposure.'],
    })
  }
  
  if (isCold || prefs.includes('indoor')) {
    activities.push({
      id: 'museum', name: 'Museum / Gallery Visit', iconName: 'i-lucide-landmark',
      description: `Explore local history, art, or science in a warm, fascinating environment.`,
      intensity: 'Low', intensityColor: 'blue', dssScore: 82,
      tags: ['indoor', 'cultural', 'educational'],
      reasoning: [`${weather.temp}°C is ${isCold ? 'cold' : 'ideal'} — indoor spaces are perfect`, 'Museums are fully heated and weather-proof', `Group of ${groupSz} can explore at their own pace`, 'Cultural enrichment regardless of conditions'],
      bestTime: 'Morning or afternoon',
      whatToBring: ['Warm coat', 'Comfortable shoes', 'Camera'],
      whatToWear: ['Light jacket', 'Comfortable jeans or chinos', 'Walking shoes'],
      wearReasoning: ['A light jacket handles cool outdoor transitions.', 'Comfortable bottoms support longer visits.', 'Supportive shoes reduce fatigue while walking exhibits.'],
    })
  }
  
  activities.push({
    id: 'local-food', name: 'Local Food & Dining', iconName: 'i-lucide-utensils',
    description: `Dive into the local food scene — from street markets to restaurants.`,
    intensity: 'Low', intensityColor: 'blue', dssScore: 75,
    tags: ['indoor', 'social', 'food'],
    reasoning: ['Weather-independent — works in any conditions', `${groupSz} people — dining is perfect for groups`, isEvening ? 'Evening timing is ideal for dinner' : 'Great for lunch'],
    bestTime: isEvening ? '7:00–10:00 PM' : '12:00–2:00 PM',
    whatToBring: ['Appetite', 'Cash/card'],
    whatToWear: ['Smart-casual top', 'Light layer', 'Comfortable shoes'],
    wearReasoning: ['Smart-casual wear fits most dining venues.', 'A light layer helps with indoor AC or cool breeze.', 'Comfortable shoes make moving between venues easier.'],
  })
  
  return activities.slice(0, 5)
}

// DSS Scoring
function computeTimeScore(): number {
  const h = parseInt(selectedTime.value.split(':')[0])
  return h >= 8 && h <= 20 ? 90 : h >= 6 && h <= 22 ? 65 : 30
}

function computeDSSScores(weather: WeatherData, prefs: string[], groupSz: number): DSSCriteria[] {
  const tempScore = weather.temp >= 18 && weather.temp <= 28 ? 90 : weather.temp >= 10 && weather.temp <= 35 ? 60 : 30
  const isRainy = weather.dssFlags.some(f => f.label === 'Rain Likely')
  return [
    { name: 'Weather Suitability', icon: 'i-lucide-cloud-sun', score: isRainy ? 40 : 85, color: 'rgb(14,165,233)' },
    { name: 'Temperature Comfort', icon: 'i-lucide-thermometer', score: tempScore, color: 'rgb(168,85,247)' },
    { name: 'Preference Match', icon: 'i-lucide-target', score: prefs.length >= 2 ? 80 : 50, color: 'rgb(34,197,94)' },
    { name: 'Group Compatibility', icon: 'i-lucide-users', score: groupSz === 1 ? 70 : groupSz <= 5 ? 90 : groupSz <= 15 ? 75 : 55, color: 'rgb(245,158,11)' },
    { name: 'Time Appropriateness', icon: 'i-lucide-clock', score: computeTimeScore(), color: 'rgb(236,72,153)' },
  ]
}

// Filter activities based on indoor/outdoor preference
function filterActivitiesByPrefs(activities: Activity[], prefs: string[]): Activity[] {
  const prefersIndoorOnly = prefs.includes('indoor') && !prefs.includes('outdoor')
  const prefersOutdoorOnly = prefs.includes('outdoor') && !prefs.includes('indoor')
  
  if (prefersIndoorOnly) {
    const filtered = activities.filter(a => 
      a.tags.some(tag => tag === 'indoor') || 
      a.name.toLowerCase().includes('indoor') ||
      a.description.toLowerCase().includes('indoor')
    )
    return filtered.length ? filtered : activities
  }
  
  if (prefersOutdoorOnly) {
    const filtered = activities.filter(a => 
      a.tags.some(tag => tag === 'outdoor') || 
      a.name.toLowerCase().includes('outdoor') ||
      a.description.toLowerCase().includes('outdoor')
    )
    return filtered.length ? filtered : activities
  }
  
  return activities
}

// Main advisor function
async function runAdvisor() {
  if (!selectedLocation.value) return
  analyzing.value = true
  results.value = null
  selectedActivity.value = null
  dssLog.value = []
  showLog.value = false
  loadingStep.value = 0

  const loc = selectedLocation.value
  addLog('info', `Analysis started: ${loc.name}`)
  addLog('info', `${selectedDate.value} ${selectedTime.value} | Group: ${groupSize.value} | Prefs: ${selectedPrefs.value.join(', ')}`)

  for (let i = 0; i < loadingMessages.length; i++) {
    loadingMsg.value = loadingMessages[i]
    loadingStep.value = i
    await new Promise(r => setTimeout(r, 500))
  }

  addLog('decision', 'Fetching weather via Open-Meteo...')
  const [weather, hourly] = await Promise.all([fetchWeather(loc.lat, loc.lon), fetchHourly(loc.lat, loc.lon)])
  addLog('decision', `Weather: ${weather.temp}°C — ${weather.description} | Rain: ${weather.raw.rainProb}% | UV: ${weather.raw.uv}`)

  const packingAdvice = generatePackingAdvice(weather)
  const dssScores = computeDSSScores(weather, selectedPrefs.value, groupSize.value)
  
  // Try to get AI recommendations
  addLog('decision', 'Calling AI recommendation engine...')
  const prompt = buildAIPrompt(weather, selectedPrefs.value, groupSize.value, loc)
  let activities: Activity[] = []
  let aiPowered = false
  
  try {
    const aiResults = await callAIApi(prompt)
    if (aiResults.length > 0) {
      activities = parseAIResponse(aiResults)
      aiPowered = true
      aiStatus.value = 'ready'
      addLog('decision', `AI generated ${activities.length} personalized recommendations`)
    } else {
      throw new Error('No AI results')
    }
  } catch (error) {
    addLog('warning', 'AI unavailable, using fallback recommendations')
    activities = generateFallbackActivities(weather, selectedPrefs.value, groupSize.value)
    aiPowered = false
    aiStatus.value = 'error'
  }
  
  // Apply preference filtering
  const filteredActivities = filterActivitiesByPrefs(activities, selectedPrefs.value)
  
  addLog('decision', `Top pick: "${filteredActivities[0]?.name}" with score ${filteredActivities[0]?.dssScore}`)
  addLog('decision', `Analysis complete — ${filteredActivities.length} activities`)

  results.value = { location: loc, weather, activities: filteredActivities, dssScores, hourly, aiPowered, packingAdvice }
  analyzing.value = false
  selectedActivity.value = filteredActivities[0] ?? null
  showLog.value = true
  aiStatus.value = aiPowered ? 'ready' : 'error'
}

async function selectHourlyTime(time: string) {
  if (!selectedLocation.value || analyzing.value) return
  selectedTime.value = time
  await runAdvisor()
}

function resetAll() {
  results.value = null
  selectedActivity.value = null
  dssLog.value = []
  showLog.value = false
  loadingStep.value = 0
  selectedLocation.value = null
  locationQuery.value = ''
  locationSuggestions.value = []
  aiStatus.value = 'ready'
}

onMounted(() => {
  selectedDate.value = new Date().toISOString().split('T')[0]
  const now = new Date()
  selectedTime.value = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`
  aiStatus.value = 'ready'
})
</script>

<style scoped>
/* Smooth animations */
@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slide-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slide-down {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slide-in {
  from { opacity: 0; transform: translateX(-10px); }
  to { opacity: 1; transform: translateX(0); }
}

@keyframes gradient {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.animate-fade-in { animation: fade-in 0.5s ease-out; }
.animate-slide-up { animation: slide-up 0.5s ease-out; }
.animate-slide-down { animation: slide-down 0.3s ease-out; }
.animate-slide-in { animation: slide-in 0.3s ease-out; }
.animate-gradient { animation: gradient 3s ease infinite; background-size: 200% 200%; }

.bg-300\% { background-size: 300% 300%; }

.loader-ring {
  width: 48px;
  height: 48px;
  border: 3px solid rgba(var(--color-primary-500), 0.2);
  border-top-color: rgb(var(--color-primary-500));
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Custom scrollbar */
.custom-scroll::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}

.custom-scroll::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scroll::-webkit-scrollbar-thumb {
  background: rgb(203, 213, 225);
  border-radius: 4px;
}

.dark .custom-scroll::-webkit-scrollbar-thumb {
  background: rgb(51, 65, 85);
}

.custom-scroll-x::-webkit-scrollbar {
  height: 3px;
}

.custom-scroll-x::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scroll-x::-webkit-scrollbar-thumb {
  background: rgb(203, 213, 225);
  border-radius: 3px;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.suggestion-enter-active,
.suggestion-leave-active {
  transition: all 0.2s ease;
}

.suggestion-enter-from,
.suggestion-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.expand-enter-active,
.expand-leave-active {
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  max-height: 0;
  transform: translateY(-8px);
}

.expand-enter-to,
.expand-leave-from {
  opacity: 1;
  max-height: 500px;
  transform: translateY(0);
}

.log-expand-enter-active,
.log-expand-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}

.log-expand-enter-from,
.log-expand-leave-to {
  opacity: 0;
  max-height: 0;
}

.log-expand-enter-to,
.log-expand-leave-from {
  opacity: 1;
  max-height: 300px;
}
</style>
