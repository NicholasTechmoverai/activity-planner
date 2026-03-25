<template>
  <div class="min-h-screen font-body overflow-x-hidden bg-gray-50 dark:bg-gray-900">

    <main class="max-w-7xl mx-auto px-6 py-10 grid grid-cols-1 lg:grid-cols-5 gap-10">

      <!-- LEFT PANEL -->
      <aside class="lg:col-span-2 flex flex-col gap-8">

        <!-- Decision Inputs Card -->
        <UCard :ui="{ base: 'overflow-visible shadow-sm rounded-2xl', body: { padding: 'p-6' } }">
          <div class="flex items-center gap-2 mb-6">
            <UIcon name="i-lucide-cpu" class="size-4 text-primary" />
            <span class="text-[11px] font-semibold uppercase tracking-widest text-primary">Decision Inputs</span>
          </div>

          <!-- Location Mode -->
          <div class="mb-6">
            <p class="text-[11px] font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400 mb-3">Location Input Method</p>
            <div class="grid grid-cols-3 gap-2.5">
              <button
                v-for="mode in locationModes"
                :key="mode.value"
                @click="locationMode = mode.value"
                :class="[
                  'flex items-center justify-center gap-1.5 px-3 py-2.5 rounded-xl text-xs font-medium border transition-all duration-200 select-none',
                  locationMode === mode.value
                    ? 'border-primary bg-primary/10 text-primary shadow-sm'
                    : 'border-gray-200 dark:border-gray-700 text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
                ]"
              >
                <UIcon :name="mode.icon" class="size-4" />
                {{ mode.label }}
              </button>
            </div>
          </div>

          <!-- Manual Input -->
          <div v-if="locationMode === 'manual'" class="mb-6">
            <p class="text-[11px] font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400 mb-3">City or Address</p>
            <div class="flex gap-2">
              <UInput
                v-model="locationQuery"
                placeholder="e.g. Nairobi, Kenya"
                icon="i-lucide-map-pin"
                size="md"
                class="flex-1"
                @keyup.enter="geocodeLocation"
              />
              <UButton @click="geocodeLocation" :loading="geocoding" color="primary" icon="i-lucide-search" size="md" class="rounded-xl" />
            </div>

            <div
              v-if="locationSuggestions.length"
              class="mt-3 border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden bg-white dark:bg-gray-900 shadow-xl z-50"
            >
              <button
                v-for="s in locationSuggestions"
                :key="s.place_id"
                @click="selectSuggestion(s)"
                class="flex items-start gap-2 w-full text-left px-3 py-2.5 text-xs text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition"
              >
                <UIcon name="i-lucide-map-pin" class="size-4 text-primary mt-0.5" />
                <span class="line-clamp-1">{{ s.display_name }}</span>
              </button>
            </div>
          </div>

          <!-- Map Mode -->
          <div v-if="locationMode === 'map'" class="mb-6">
            <p class="text-[11px] uppercase font-semibold tracking-wide text-gray-500 dark:text-gray-400 mb-3">Click to pin your location</p>
            <div
              ref="mapContainer"
              class="w-full h-48 rounded-2xl overflow-hidden border border-gray-200 dark:border-gray-700 bg-gray-100 dark:bg-gray-800 relative"
            >
              <div v-if="!mapReady" class="absolute inset-0 flex items-center justify-center gap-2 text-xs text-gray-400">
                <UIcon name="i-lucide-map" class="size-4 animate-spin" />
                Loading map...
              </div>
            </div>
            <p v-if="selectedLocation" class="text-[11px] text-gray-500 dark:text-gray-400 mt-2 flex items-center gap-1 truncate">
              <UIcon name="i-lucide-map-pin-check" class="size-4 text-primary" />
              {{ selectedLocation.name }}
            </p>
          </div>

          <!-- GPS -->
          <div v-if="locationMode === 'gps'" class="mb-6">
            <UButton @click="getGPSLocation" :loading="gpsLoading" block color="primary" variant="outline" icon="i-lucide-navigation" class="rounded-xl py-3">
              Detect My Location
            </UButton>
            <p v-if="selectedLocation" class="text-[11px] text-primary mt-2 text-center flex items-center justify-center gap-1">
              <UIcon name="i-lucide-circle-check" class="size-4" />
              {{ selectedLocation.name }}
            </p>
          </div>

          <!-- Date & Time -->
          <div class="mb-6 grid grid-cols-2 gap-4">
            <div>
              <p class="text-[11px] uppercase font-semibold tracking-wide text-gray-500 dark:text-gray-400 mb-2">Date</p>
              <UInput v-model="selectedDate" type="date" :min="todayDate" icon="i-lucide-calendar" size="md" class="rounded-xl" />
            </div>
            <div>
              <p class="text-[11px] uppercase font-semibold tracking-wide text-gray-500 dark:text-gray-400 mb-2">Time</p>
              <UInput v-model="selectedTime" type="time" icon="i-lucide-clock" size="md" class="rounded-xl" />
            </div>
          </div>

          <!-- Activity Preferences -->
          <div class="mb-6">
            <p class="text-[11px] uppercase font-semibold tracking-wide text-gray-500 dark:text-gray-400 mb-3">Activity Preferences</p>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="pref in activityPrefs"
                :key="pref.value"
                @click="togglePref(pref.value)"
                :class="[
                  'flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium border transition select-none',
                  selectedPrefs.includes(pref.value)
                    ? 'border-primary bg-primary/10 text-primary shadow-sm'
                    : 'border-gray-200 dark:border-gray-700 text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
                ]"
              >
                <UIcon :name="pref.icon" class="size-3.5" />
                {{ pref.label }}
              </button>
            </div>
          </div>

          <!-- Group Size -->
          <div class="mb-8">
            <p class="text-[11px] uppercase font-semibold tracking-wide text-gray-500 dark:text-gray-400 mb-2">Group Size</p>
            <div class="flex items-center gap-3 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-3">
              <UButton @click="groupSize = Math.max(1, groupSize - 1)" icon="i-lucide-minus" color="neutral" variant="ghost" size="xs" />
              <div class="flex-1 text-center">
                <span class="text-2xl font-bold text-gray-900 dark:text-white tabular-nums">{{ groupSize }}</span>
                <span class="text-[11px] text-gray-400 ml-1">{{ groupSize === 1 ? 'person' : 'people' }}</span>
              </div>
              <UButton @click="groupSize = Math.min(50, groupSize + 1)" icon="i-lucide-plus" color="neutral" variant="ghost" size="xs" />
            </div>
          </div>

          <!-- CTA -->
          <UButton
            @click="runAdvisor"
            :loading="analyzing"
            :disabled="!selectedLocation"
            block size="lg" color="primary"
            class="rounded-xl py-3 shadow-sm"
            icon="i-lucide-sparkles"
          >
            {{ analyzing ? 'Analyzing...' : 'Get AI Recommendations' }}
          </UButton>
          <p v-if="!selectedLocation" class="text-[11px] text-center text-gray-400 mt-2">Select a location to continue</p>
        </UCard>

        <!-- AI Model Badge -->
        <div class="flex items-center gap-2 px-3 py-2 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
          <div class="w-2 h-2 rounded-full" :class="aiStatus === 'ready' ? 'bg-green-400' : aiStatus === 'error' ? 'bg-red-400' : 'bg-amber-400 animate-pulse'"></div>
          <span class="text-[11px] text-gray-500 dark:text-gray-400 flex-1">
            <span v-if="aiStatus === 'ready'">Local AI Backend — Ready</span>
            <span v-else-if="aiStatus === 'error'">AI unavailable — using smart fallback</span>
            <span v-else>Initialising model...</span>
          </span>
          <UIcon name="i-lucide-brain-circuit" class="size-4 text-primary" />
        </div>

        <!-- Reasoning Log -->
        <UCard v-if="dssLog.length" :ui="{ base: 'rounded-2xl shadow-sm', body: { padding: 'p-4' } }">
          <button @click="showLog = !showLog" class="flex items-center justify-between w-full group">
            <div class="flex items-center gap-2">
              <UIcon name="i-lucide-file-search" class="size-4 text-amber-500" />
              <span class="text-[11px] uppercase font-semibold tracking-widest text-amber-500">Reasoning Log</span>
              <UBadge color="success" variant="soft" size="xs">{{ dssLog.length }}</UBadge>
            </div>
            <UIcon :name="showLog ? 'i-lucide-chevron-up' : 'i-lucide-chevron-down'" class="size-4 text-gray-400 group-hover:text-gray-600 transition" />
          </button>
          <Transition name="log-expand">
            <div v-if="showLog" class="mt-3 space-y-1.5 max-h-52 overflow-y-auto pr-1 custom-scroll">
              <div v-for="(log, i) in dssLog" :key="i" class="flex items-start gap-2 text-[11px]">
                <span class="text-gray-300 dark:text-gray-600 font-mono flex-shrink-0 tabular-nums mt-0.5">{{ String(i + 1).padStart(2, '0') }}</span>
                <UIcon
                  :name="log.type === 'decision' ? 'i-lucide-zap' : log.type === 'warning' ? 'i-lucide-triangle-alert' : 'i-lucide-dot'"
                  :class="['size-3 mt-0.5 flex-shrink-0', log.type === 'decision' ? 'text-primary' : log.type === 'warning' ? 'text-amber-500' : 'text-gray-400']"
                />
                <span :class="['leading-relaxed', log.type === 'decision' ? 'text-primary' : log.type === 'warning' ? 'text-amber-500' : 'text-gray-500 dark:text-gray-400']">{{ log.msg }}</span>
              </div>
            </div>
          </Transition>
        </UCard>
      </aside>

      <!-- RIGHT PANEL -->
      <section class="lg:col-span-3 flex flex-col gap-8">

        <!-- WELCOME SCREEN -->
        <UCard v-if="!results && !analyzing" :ui="{ base: 'rounded-2xl shadow-sm', body: { padding: 'py-20 px-8' } }">
          <div class="flex flex-col items-center text-center">
            <div class="w-20 h-20 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center mb-6">
              <UIcon name="i-lucide-map" class="size-9 text-primary" />
            </div>
            <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-1">Where are you headed?</h2>
            <p class="text-sm text-gray-500 dark:text-gray-400 max-w-xs">
              Select your location, pick a date and time, then let our AI Decision Support System find the perfect activity.
            </p>
            <div class="mt-10 grid grid-cols-3 gap-4 w-full max-w-xs">
              <div v-for="f in featureHighlights" :key="f.label" class="flex flex-col items-center gap-2 p-3 rounded-xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-gray-800/50 shadow-sm">
                <UIcon :name="f.icon" class="size-5 text-primary" />
                <span class="text-[11px] text-gray-500 dark:text-gray-400">{{ f.label }}</span>
              </div>
            </div>
          </div>
        </UCard>

        <!-- LOADING -->
        <UCard v-if="analyzing" :ui="{ base: 'rounded-2xl shadow-sm', body: { padding: 'py-20 px-8' } }">
          <div class="flex flex-col items-center text-center">
            <div class="loader-ring mb-6"></div>
            <p class="text-lg font-semibold text-gray-900 dark:text-white">{{ loadingMsg }}</p>
            <p class="text-[11px] text-gray-400 mt-1">Powered by real-time weather & local AI backend</p>
            <div class="mt-8 w-full max-w-xs space-y-3">
              <div v-for="(step, i) in loadingSteps" :key="i" :class="['flex items-center gap-3 text-[11px] transition-opacity', i <= loadingStep ? 'opacity-100' : 'opacity-30']">
                <div :class="['w-1.5 h-1.5 rounded-full transition', i <= loadingStep ? 'bg-primary' : 'bg-gray-300 dark:bg-gray-700']" />
                <span :class="i <= loadingStep ? 'text-gray-700 dark:text-gray-200' : 'text-gray-400'">{{ step }}</span>
                <UIcon v-if="i === loadingStep" name="i-lucide-loader-circle" class="size-3 text-primary animate-spin ml-auto" />
                <UIcon v-else-if="i < loadingStep" name="i-lucide-check" class="size-3 text-green-500 ml-auto" />
              </div>
            </div>
          </div>
        </UCard>

        <!-- RESULTS -->
        <template v-if="results && !analyzing">

          <!-- WEATHER -->
          <UCard :ui="{ base: 'rounded-2xl shadow-sm', body: { padding: 'p-6' } }">
            <div class="flex items-start justify-between mb-6">
              <div>
                <div class="flex items-center gap-2 mb-1">
                  <UIcon name="i-lucide-cloud-sun" class="size-4 text-primary" />
                  <span class="text-[11px] uppercase font-semibold tracking-widest text-primary">Current Conditions</span>
                </div>
                <h3 class="text-xl font-bold text-gray-900 dark:text-white">{{ results.location.name }}</h3>
                <p class="text-[11px] text-gray-400 mt-0.5">{{ formatDateTime(selectedDate, selectedTime) }}</p>
              </div>
              <div class="text-right">
                <UIcon :name="results.weather.iconName" class="size-12 text-amber-400" />
                <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ results.weather.temp }}°C</p>
                <p class="text-[11px] text-gray-400">{{ results.weather.description }}</p>
              </div>
            </div>
            <div class="grid grid-cols-4 gap-3 mb-6">
              <div v-for="stat in results.weather.stats" :key="stat.label" class="flex flex-col items-center gap-1.5 p-3 rounded-xl bg-white dark:bg-gray-800/50 border border-gray-100 dark:border-gray-700 shadow-sm">
                <UIcon :name="stat.icon" class="size-4 text-primary" />
                <span class="text-sm font-semibold text-gray-900 dark:text-white">{{ stat.value }}</span>
                <span class="text-[10px] text-gray-400 uppercase tracking-wide">{{ stat.label }}</span>
              </div>
            </div>
            <div class="pt-4 border-t border-gray-100 dark:border-gray-800">
              <div class="flex items-center gap-2 mb-2">
                <UIcon name="i-lucide-flask-conical" class="size-4 text-primary" />
                <span class="text-[11px] uppercase font-semibold tracking-wider text-primary">Weather Assessment</span>
              </div>
              <div class="flex flex-wrap gap-1.5">
                <UBadge v-for="badge in results.weather.dssFlags" :key="badge.label" :color="badge.color" variant="soft" size="sm">
                  <UIcon :name="badge.icon" class="size-3 mr-1" />
                  {{ badge.label }}
                </UBadge>
              </div>
            </div>
          </UCard>

          <!-- AI SOURCE INDICATOR -->
          <div class="flex items-center gap-2 px-4 py-2.5 rounded-xl border text-[11px]"
            :class="results.aiPowered ? 'border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400' : 'border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-400'"
          >
            <UIcon :name="results.aiPowered ? 'i-lucide-brain-circuit' : 'i-lucide-cpu'" class="size-4" />
            <span v-if="results.aiPowered">
              Activities generated by <strong>local AI backend</strong> — uniquely tailored to real-time weather & your preferences
            </span>
            <span v-else>
              Activities generated by <strong>rule-based fallback</strong> — AI model was unavailable
            </span>
          </div>

          <!-- ACTIVITIES -->
          <div>
            <div class="flex items-center gap-2 mb-4">
              <UIcon name="i-lucide-sparkles" class="size-4 text-primary" />
              <span class="text-[11px] uppercase font-semibold tracking-widest text-primary">Recommendations</span>
              <UBadge color="primary" variant="soft" size="xs" class="ml-auto">{{ results.activities.length }} Options</UBadge>
            </div>
            <div class="space-y-4">
              <UCard
                v-for="(activity, idx) in results.activities"
                :key="activity.id"
                @click="selectedActivity = selectedActivity?.id === activity.id ? null : activity"
                :ui="{ base: 'cursor-pointer rounded-2xl transition-all bg-white dark:bg-gray-800 shadow-sm', body: { padding: 'p-5' } }"
                :class="[
                  selectedActivity?.id === activity.id ? 'ring-1 ring-primary' : 'hover:ring-1 hover:ring-primary/30',
                  activity.id === 'weather-dressing-packing' ? 'bg-gradient-to-br from-emerald-50 to-cyan-50 dark:from-emerald-900/20 dark:to-cyan-900/10 border-emerald-200 dark:border-emerald-800' : ''
                ]"
              >
                <div :class="['absolute -top-2 right-4 px-2 py-0.5 rounded-full text-[10px] font-semibold border backdrop-blur-sm', idx === 0 ? 'bg-amber-50 border-amber-200 text-amber-600' : idx === 1 ? 'bg-gray-50 border-gray-200 text-gray-500' : 'bg-orange-50 border-orange-200 text-orange-500']">
                  {{ idx === 0 ? '#1 Start Here' : idx === 1 ? '#2' : `#${idx + 1}` }}
                </div>
                <div class="flex items-start gap-4">
                  <div class="w-12 h-12 rounded-2xl bg-gray-100 dark:bg-gray-700 border border-gray-200 dark:border-gray-700 flex items-center justify-center">
                    <UIcon :name="activity.iconName || 'i-lucide-star'" class="size-6 text-primary" />
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center gap-2 flex-wrap mb-1">
                      <h4 class="font-semibold text-gray-900 dark:text-white">{{ activity.name }}</h4>
                      <UBadge :color="activity.intensityColor || 'blue'" variant="soft" size="xs">{{ activity.intensity }}</UBadge>
                      <UBadge v-if="idx === 0" color="success" variant="soft" size="xs">
                        <UIcon name="i-lucide-star" class="size-3 mr-1" />
                        {{ activity.id === 'weather-dressing-packing' ? 'Weather Guide' : 'Best Match' }}
                      </UBadge>
                    </div>
                    <p class="text-xs leading-relaxed text-gray-500 dark:text-gray-400">{{ activity.description }}</p>
                    <div class="flex flex-wrap gap-1.5 mt-3">
                      <span v-for="tag in activity.tags" :key="tag" class="text-[10px] px-2 py-0.5 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-300 border border-gray-200 dark:border-gray-600">{{ tag }}</span>
                    </div>
                    <Transition name="expand">
                      <div v-if="selectedActivity?.id === activity.id" class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                        <div class="flex items-center gap-2 mb-3">
                          <UIcon name="i-lucide-lightbulb" class="size-4 text-primary" />
                          <span class="text-[11px] font-semibold uppercase tracking-wide text-primary">Why this fits</span>
                        </div>
                        <ul class="space-y-1.5">
                          <li v-for="r in activity.reasoning" :key="r" class="flex items-start gap-2 text-xs text-gray-500 dark:text-gray-400">
                            <UIcon name="i-lucide-arrow-right" class="size-3 text-green-500 mt-1" />
                            {{ r }}
                          </li>
                        </ul>
                        <div v-if="activity.bestTime" class="mt-3 flex items-center gap-2 text-xs text-amber-600 dark:text-amber-400">
                          <UIcon name="i-lucide-clock" class="size-3" />
                          Best time: {{ activity.bestTime }}
                        </div>
                        <div v-if="activity.whatToBring?.length" class="mt-3">
                          <p class="text-[10px] uppercase font-semibold text-gray-400 mb-1.5">What to bring</p>
                          <div class="flex flex-wrap gap-1">
                            <span v-for="item in activity.whatToBring" :key="item" class="text-[10px] px-2 py-0.5 rounded-full bg-primary/10 text-primary border border-primary/20">{{ item }}</span>
                          </div>
                        </div>
                        <div class="flex gap-2 mt-4">
                          <UButton size="xs" color="primary" icon="i-lucide-check-circle" class="rounded-lg">Accept</UButton>
                          <UButton size="xs" color="neutral" variant="ghost" icon="i-lucide-refresh-cw" @click.stop="runAdvisor" class="rounded-lg">Regenerate</UButton>
                        </div>
                      </div>
                    </Transition>
                  </div>
                </div>
              </UCard>
            </div>
          </div>

          <!-- HOURLY FORECAST -->
          <UCard :ui="{ base: 'rounded-2xl shadow-sm', body: { padding: 'p-6' } }">
            <div class="flex items-center gap-2 mb-4">
              <UIcon name="i-lucide-clock" class="size-4 text-amber-500" />
              <span class="text-[11px] uppercase font-semibold tracking-widest text-amber-500">Hourly Forecast</span>
            </div>
            <p class="text-xs text-gray-500 dark:text-gray-400 mb-3">Tap any hour to refresh recommendations for that exact time.</p>
            <div class="flex gap-3 overflow-x-auto pb-2 custom-scroll-x">
              <div
                v-for="h in results.hourly" :key="h.time"
                @click="selectHourlyTime(h.time)"
                :class="['flex-shrink-0 flex flex-col items-center gap-1 px-4 py-3 min-w-[68px] rounded-xl border shadow-sm transition-all cursor-pointer', h.isSelected ? 'border-primary bg-primary/10 ring-1 ring-primary' : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800/50 hover:ring-1 hover:ring-primary/30']"
              >
                <span class="text-[10px] font-mono text-gray-400">{{ h.time }}</span>
                <UIcon :name="h.iconName" :class="['size-5', h.isSelected ? 'text-primary' : 'text-amber-400']" />
                <span class="text-sm font-semibold text-gray-900 dark:text-white">{{ h.temp }}°</span>
                <div class="flex items-center gap-1">
                  <UIcon name="i-lucide-droplets" class="size-3 text-blue-400" />
                  <span class="text-[10px] text-gray-400">{{ h.rain }}%</span>
                </div>
              </div>
            </div>
          </UCard>

          <!-- RESET -->
          <div class="flex justify-center py-4">
            <UButton @click="resetAll" color="neutral" variant="ghost" size="sm" class="rounded-lg" icon="i-lucide-rotate-ccw">Start New Analysis</UButton>
          </div>
        </template>
      </section>
    </main>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'

interface Location { lat: number; lon: number; name: string }
interface DSSLog { msg: string; type: 'info' | 'decision' | 'warning' }
interface Activity {
  id: string; name: string; iconName: string; description: string
  intensity: string; intensityColor: string
  tags: string[]; reasoning: string[]; bestTime?: string; whatToBring?: string[]
}
interface WeatherStat { icon: string; value: string; label: string }
interface WeatherData {
  temp: number; description: string; iconName: string
  stats: WeatherStat[]; dssFlags: { label: string; icon: string; color: string }[]
  raw: { humidity: number; wind: number; rainProb: number; uv: number; wc: number }
}
interface HourlyForecast { time: string; temp: number; iconName: string; rain: number; isSelected: boolean }
interface Results {
  location: Location; weather: WeatherData; activities: Activity[]
  hourly: HourlyForecast[]; aiPowered: boolean
}

// ── State ──────────────────────────────────────────────────────────────────
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

// ── Local backend AI config ────────────────────────────────────────────────
const API_URL = import.meta.env.VITE_BACKEND_RECOMMEND_URL || 'https://api.tera-in.top/recommendations'

// ── Constants ──────────────────────────────────────────────────────────────
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
  { icon: 'i-lucide-brain-circuit', label: 'Local AI Model' },
  { icon: 'i-lucide-target', label: 'Smart Ranking' },
]

const loadingMessages = [
  'Fetching real-time weather data...',
  'Building climate profile...',
  'Querying local backend AI model...',
  'Scoring recommendations...',
]

const loadingSteps = [
  'Geocoding location',
  'Fetching weather forecast',
  'Generating AI recommendations',
  'Ranking recommendation fit',
]

// ── Weather helpers ────────────────────────────────────────────────────────
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

// Map an activity name to a Lucide icon
function inferIcon(name: string): string {
  const n = name.toLowerCase()
  if (n.includes('hik') || n.includes('trek') || n.includes('walk')) return 'i-lucide-footprints'
  if (n.includes('cycl') || n.includes('bike')) return 'i-lucide-bike'
  if (n.includes('swim') || n.includes('pool') || n.includes('beach')) return 'i-lucide-waves'
  if (n.includes('museum') || n.includes('gallery') || n.includes('art')) return 'i-lucide-landmark'
  if (n.includes('food') || n.includes('dine') || n.includes('restaurant') || n.includes('eat') || n.includes('cuisine')) return 'i-lucide-utensils'
  if (n.includes('yoga') || n.includes('meditat') || n.includes('mindful')) return 'i-lucide-person-standing'
  if (n.includes('photo') || n.includes('camera')) return 'i-lucide-camera'
  if (n.includes('park') || n.includes('picnic') || n.includes('garden')) return 'i-lucide-tree-pine'
  if (n.includes('market') || n.includes('shop')) return 'i-lucide-shopping-bag'
  if (n.includes('run') || n.includes('jog')) return 'i-lucide-activity'
  if (n.includes('climb') || n.includes('boulder') || n.includes('mountain')) return 'i-lucide-mountain'
  if (n.includes('kayak') || n.includes('canoe') || n.includes('boat') || n.includes('sail')) return 'i-lucide-sailboat'
  if (n.includes('bird') || n.includes('wildlife') || n.includes('safari')) return 'i-lucide-bird'
  if (n.includes('indoor') || n.includes('lounge') || n.includes('home') || n.includes('stay')) return 'i-lucide-house'
  if (n.includes('social') || n.includes('community') || n.includes('meet')) return 'i-lucide-users'
  if (n.includes('spa') || n.includes('massage') || n.includes('relax')) return 'i-lucide-sparkles'
  return 'i-lucide-star'
}

// ── Logging ────────────────────────────────────────────────────────────────
function addLog(type: DSSLog['type'], msg: string) {
  dssLog.value.unshift({ type, msg })
  if (dssLog.value.length > 25) dssLog.value.pop()
}

// ── Preference helpers ─────────────────────────────────────────────────────
function togglePref(val: string) {
  const idx = selectedPrefs.value.indexOf(val)
  if (idx > -1) selectedPrefs.value.splice(idx, 1)
  else selectedPrefs.value.push(val)
}

function formatDateTime(date: string, time: string): string {
  try {
    const d = new Date(`${date}T${time}`)
    return d.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' }) + ' at ' + d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
  } catch { return `${date} ${time}` }
}

function buildWeatherPackingGuide(weather: WeatherData): Activity {
  const tips: string[] = []
  if (weather.temp <= 12) tips.push('Warm inner layer and a jacket')
  else if (weather.temp >= 31) tips.push('Light breathable clothes and sun hat')
  else tips.push('Comfortable light layers')

  if (weather.raw.rainProb >= 50 || (weather.raw.wc >= 51 && weather.raw.wc <= 82)) tips.push('Rain jacket or umbrella')
  if (weather.raw.uv >= 7) tips.push('Sunscreen and sunglasses')
  if (weather.raw.wind >= 30) tips.push('Wind-resistant outer layer')

  const whatToBring = Array.from(new Set([
    weather.raw.rainProb >= 50 ? 'Umbrella' : 'Light jacket',
    weather.raw.uv >= 7 ? 'Sunscreen' : 'Water bottle',
    weather.raw.wind >= 30 ? 'Windbreaker' : 'Comfortable shoes',
  ]))

  return {
    id: 'weather-dressing-packing',
    name: 'Dressing & Packing Guide',
    iconName: 'i-lucide-shirt',
    description: `For ${weather.temp}°C, ${weather.description.toLowerCase()}, and ${weather.raw.rainProb}% rain probability, dress for comfort first and pack weather protection.`,
    intensity: 'Low',
    intensityColor: 'blue',
    tags: ['clothing', 'packing', 'weather-ready'],
    reasoning: tips.slice(0, 4),
    bestTime: selectedTime.value,
    whatToBring,
  }
}

function isOutdoorActivity(a: Activity): boolean {
  const text = `${a.name} ${a.description} ${(a.tags || []).join(' ')}`.toLowerCase()
  return /outdoor|hiking|hike|walk|trek|trail|cycling|bike|jog|run|park|nature/.test(text)
}

function isIndoorActivity(a: Activity): boolean {
  const text = `${a.name} ${a.description} ${(a.tags || []).join(' ')}`.toLowerCase()
  return /indoor|museum|cafe|cinema|mall|restaurant|gallery|market|escape room|co-?work/.test(text)
}

function applyPreferenceFilters(activities: Activity[], prefs: string[]): Activity[] {
  const prefersIndoorOnly = prefs.includes('indoor') && !prefs.includes('outdoor')
  const prefersOutdoorOnly = prefs.includes('outdoor') && !prefs.includes('indoor')

  let filtered = activities
  if (prefersIndoorOnly) filtered = activities.filter(a => !isOutdoorActivity(a) || isIndoorActivity(a))
  if (prefersOutdoorOnly) filtered = filtered.filter(a => !isIndoorActivity(a) || isOutdoorActivity(a))

  return filtered.length ? filtered : activities
}

function ensureWeatherGuideFirst(weather: WeatherData, activities: Activity[]): Activity[] {
  const guide = buildWeatherPackingGuide(weather)
  const withoutExistingGuide = activities.filter(a => {
    const n = a.name.toLowerCase()
    return !(n.includes('dressing') || n.includes('packing') || n.includes('clothing'))
  })
  return [guide, ...withoutExistingGuide].slice(0, 5)
}

// ── Location ────────────────────────────────────────────────────────────────
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
    addLog('warning', 'Geocoding unavailable — using fallback')
    selectedLocation.value = { lat: -1.2864, lon: 36.8172, name: locationQuery.value }
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
    const L = await import('https://unpkg.com/leaflet@1.9.4/dist/leaflet-src.esm.js' as any).catch(() => null)
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

// ── Weather ────────────────────────────────────────────────────────────────
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

// ── Backend AI generation ──────────────────────────────────────────────────
/**
 * Builds a structured prompt for Mistral-7B-Instruct asking for
 * climate-specific activity recommendations in strict JSON.
 */
function buildPrompt(weather: WeatherData, prefs: string[], groupSz: number, location: Location): string {
  const hour = parseInt(selectedTime.value.split(':')[0])
  const timeOfDay = hour < 12 ? 'morning' : hour < 17 ? 'afternoon' : hour < 20 ? 'evening' : 'night'
  const isRainy = weather.raw.rainProb > 60
  const isHot = weather.temp > 32
  const isCold = weather.temp < 12
  const isHighUV = weather.raw.uv > 7
  const isWindy = weather.raw.wind > 30

  const climateSummary = [
    `Temperature: ${weather.temp}°C (${isHot ? 'HOT' : isCold ? 'COLD' : 'comfortable'})`,
    `Conditions: ${weather.description}`,
    `Rain probability: ${weather.raw.rainProb}% (${isRainy ? 'RAIN EXPECTED' : 'dry'})`,
    `Wind: ${weather.raw.wind} km/h (${isWindy ? 'VERY WINDY' : 'manageable'})`,
    `UV Index: ${weather.raw.uv} (${isHighUV ? 'HIGH - sun protection required' : 'moderate'})`,
    `Humidity: ${weather.raw.humidity}%`,
  ].join('\n')

  const prefersIndoorOnly = prefs.includes('indoor') && !prefs.includes('outdoor')
  const prefersOutdoorOnly = prefs.includes('outdoor') && !prefs.includes('indoor')

  return `<s>[INST] You are an expert outdoor and lifestyle activity advisor. Generate activity recommendations that are SPECIFICALLY tailored to the weather conditions described. DO NOT suggest activities that are dangerous or uncomfortable given the weather.

LOCATION: ${location.name}
DATE/TIME: ${selectedDate.value} — ${timeOfDay} (${selectedTime.value})
GROUP SIZE: ${groupSz} ${groupSz === 1 ? 'person' : 'people'}
USER PREFERENCES: ${prefs.length ? prefs.join(', ') : 'none specified'}

WEATHER CONDITIONS:
${climateSummary}

IMPORTANT RULES:
- The FIRST recommendation must be "Dressing & Packing Guide" (weather-based clothing and what to carry).
- If it is RAINY (>60% rain), recommend mostly indoor activities or rain-appropriate outdoor activities (like rainy day walks with gear, indoor markets, etc.)
- If it is HOT (>32°C), recommend early morning/evening activities, water activities, or well-shaded/indoor options
- If it is COLD (<12°C), recommend warm indoor activities or activities where staying warm is possible
- If UV is HIGH (>7), avoid midday sun exposure activities; recommend indoor or shaded options
- If it is WINDY (>30 km/h), avoid activities where wind is dangerous (sailing, cycling exposed ridges, etc.)
- ALWAYS suggest what to bring/wear for the conditions
- Consider ${timeOfDay} — some activities only make sense at certain times
- If USER PREFERENCES include indoor only, avoid hiking, walking trails, jogging, cycling, or other outdoor-first activities.
- If USER PREFERENCES include outdoor only, avoid indoor-first activities.
- Preference mode: ${prefersIndoorOnly ? 'INDOOR_ONLY' : prefersOutdoorOnly ? 'OUTDOOR_ONLY' : 'MIXED'}.

Generate exactly 5 activity recommendations. Return ONLY a valid JSON array, no other text, no markdown:

[
  {
    "id": "unique-id",
    "name": "Activity Name",
    "description": "2-sentence engaging description mentioning why it suits the current ${weather.description} conditions",
    "intensity": "Low|Moderate|High",
    "intensityColor": "blue|yellow|red",
    "tags": ["tag1", "tag2", "tag3"],
    "reasoning": [
      "Specific reason tied to ${weather.temp}°C temperature",
      "Specific reason tied to ${weather.description} conditions",
      "Reason tied to group size of ${groupSz}",
      "Reason tied to ${timeOfDay} timing"
    ],
    "bestTime": "e.g. 7:00–9:00 AM before peak heat",
    "whatToBring": ["item1", "item2", "item3"]
  }
] [/INST]`
}

/**
 * Calls local backend AI endpoint.
 */
async function callBackendAI(prompt: string, retries = 1): Promise<string | null> {
  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt: prompt,
      }),
    })

    if (res.status === 503 && retries > 0) {
      addLog('info', 'AI backend is warming up — retrying in 8s...')
      await new Promise(r => setTimeout(r, 8000))
      return callBackendAI(prompt, retries - 1)
    }

    if (res.status === 429 && retries > 0) {
      addLog('warning', 'AI backend rate limit — retrying in 12s...')
      await new Promise(r => setTimeout(r, 12000))
      return callBackendAI(prompt, retries - 1)
    }

    if (!res.ok) {
      const errText = await res.text()
      console.error('Backend AI error:', res.status, errText)
      return null
    }

    const data = await res.json()

    // Backend contract: { recommendations: "..." } (string or JSON string)
    if (typeof data?.recommendations === 'string') return data.recommendations
    if (Array.isArray(data?.recommendations)) return JSON.stringify(data.recommendations)
    if (typeof data?.generated_text === 'string') return data.generated_text
    if (data && typeof data === 'object') return JSON.stringify(data)

    return null
  } catch (err) {
    console.error('Backend fetch error:', err)
    return null
  }
}

/**
 * Extracts the JSON array from the model's raw output text.
 * Handles cases where the model includes extra prose around the JSON.
 */
function extractJSONArray(raw: string): Activity[] | null {
  const parseObjectChunks = (text: string): any[] => {
    const items: any[] = []
    let inString = false
    let escape = false
    let depth = 0
    let start = -1

    for (let i = 0; i < text.length; i++) {
      const ch = text[i]

      if (escape) {
        escape = false
        continue
      }

      if (ch === '\\') {
        if (inString) escape = true
        continue
      }

      if (ch === '"') {
        inString = !inString
        continue
      }

      if (inString) continue

      if (ch === '{') {
        if (depth === 0) start = i
        depth++
      } else if (ch === '}') {
        if (depth > 0) depth--
        if (depth === 0 && start !== -1) {
          const chunk = text.slice(start, i + 1)
          try {
            items.push(JSON.parse(chunk))
          } catch {
            // Ignore broken chunk and keep scanning for valid objects.
          }
          start = -1
        }
      }
    }

    return items
  }

  const normalise = (input: any): any[] | null => {
    if (!input) return null
    if (Array.isArray(input)) return input

    if (typeof input === 'string') {
      const trimmed = input.trim().replace(/^\uFEFF/, '')
      try {
        const parsed = JSON.parse(trimmed)
        const nested = normalise(parsed)
        if (nested) return nested
      } catch {
        const start = trimmed.indexOf('[')
        const end = trimmed.lastIndexOf(']')
        if (start !== -1 && end !== -1 && end > start) {
          try {
            const parsed = JSON.parse(trimmed.slice(start, end + 1))
            return Array.isArray(parsed) ? parsed : null
          } catch {
            // Continue with lenient parsing below.
          }
        }

        const objectChunks = parseObjectChunks(start !== -1 ? trimmed.slice(start) : trimmed)
        if (objectChunks.length) return objectChunks
      }
      return null
    }

    if (typeof input === 'object') {
      if (Array.isArray((input as any).recommendations)) return (input as any).recommendations
      if (typeof (input as any).recommendations === 'string') return normalise((input as any).recommendations)
      if (Array.isArray((input as any).activities)) return (input as any).activities
      if (typeof (input as any).generated_text === 'string') return normalise((input as any).generated_text)
    }

    return null
  }

  const parsed = normalise(raw)
  if (!parsed || !parsed.length) return null

  return parsed.map((a: any, i: number) => ({
    id: a?.id || `activity-${i}`,
    name: String(a?.name || 'Activity'),
    description: String(a?.description || ''),
    intensity: ['Low', 'Moderate', 'High'].includes(a?.intensity) ? a.intensity : 'Moderate',
    intensityColor: ['blue', 'yellow', 'red', 'green', 'orange', 'violet'].includes(a?.intensityColor) ? a.intensityColor : 'blue',
    tags: Array.isArray(a?.tags) ? a.tags.map(String) : [],
    reasoning: Array.isArray(a?.reasoning) ? a.reasoning.map(String) : [],
    bestTime: a?.bestTime ? String(a.bestTime) : undefined,
    whatToBring: Array.isArray(a?.whatToBring) ? a.whatToBring.map(String) : [],
    iconName: inferIcon(String(a?.name || '')),
  }))
}

async function generateActivitiesWithHF(weather: WeatherData, prefs: string[], groupSz: number, location: Location): Promise<{ activities: Activity[]; aiPowered: boolean }> {
  addLog('info', 'Querying local backend AI model...')

  const prompt = buildPrompt(weather, prefs, groupSz, location)
  const rawText = await callBackendAI(prompt)

  if (!rawText) {
    addLog('warning', 'Local AI backend unavailable — switching to rules fallback')
    aiStatus.value = 'error'
    return { activities: generateFallbackActivities(weather, prefs, groupSz), aiPowered: false }
  }

  const activities = extractJSONArray(rawText)

  if (!activities || activities.length === 0) {
    addLog('warning', 'Could not parse AI response — using rules fallback')
    console.error('Raw backend output:', rawText)
    aiStatus.value = 'error'
    return { activities: generateFallbackActivities(weather, prefs, groupSz), aiPowered: false }
  }

  addLog('decision', `AI generated ${activities.length} climate-specific activities`)
  aiStatus.value = 'ready'
  return { activities, aiPowered: true }
}

// ── Fallback (rules-based) ─────────────────────────────────────────────────
function generateFallbackActivities(weather: WeatherData, prefs: string[], groupSz: number): Activity[] {
  const isRainy = weather.raw.rainProb > 60
  const isHot = weather.temp > 32
  const isCold = weather.temp < 12
  const isIdeal = weather.temp >= 18 && weather.temp <= 28 && !isRainy
  const isHighUV = weather.raw.uv > 7
  const isWindy = weather.raw.wind > 30
  const hour = parseInt(selectedTime.value.split(':')[0])
  const isEvening = hour >= 17
  const isMorning = hour < 11

  const all: Activity[] = []

  // Weather-aware pool
  if (isRainy) {
    all.push({
      id: 'indoor-market', name: 'Indoor Market Exploration', iconName: 'i-lucide-shopping-bag',
      description: `Rain is the perfect excuse to dive into a vibrant covered market. Browse local crafts, street food, and sheltered stalls while staying completely dry.`,
      intensity: 'Low', intensityColor: 'blue',
      tags: ['indoor', 'social', 'food', 'cultural'],
      reasoning: [`${weather.raw.rainProb}% rain probability makes outdoor activities risky`, 'Covered markets are fully weather-proof', `${groupSz} people can browse comfortably`, 'Social and cultural experience regardless of weather'],
      bestTime: 'Any time during opening hours',
      whatToBring: ['Umbrella for transit', 'Shopping bag', 'Cash/card', 'Light jacket'],
    })
    all.push({
      id: 'cafe-cowork', name: 'Café & Creative Work', iconName: 'i-lucide-coffee',
      description: `Settle into a warm, atmospheric café. Perfect for solo reflection, reading, writing, or getting work done while rain patters on the windows.`,
      intensity: 'Low', intensityColor: 'blue',
      tags: ['indoor', 'solo', 'relaxed'],
      reasoning: ['Rain makes cozy indoor settings ideal', `Solo or small groups of ${Math.min(groupSz, 4)} work best`, 'No weather dependency', 'Low energy — great after travel or errands'],
      bestTime: 'Morning or afternoon',
      whatToBring: ['Laptop or book', 'Earphones', 'Rain jacket'],
    })
  }

  if (isHot) {
    all.push({
      id: 'water-activity', name: 'Swimming / Water Activity', iconName: 'i-lucide-waves',
      description: `Beat the ${weather.temp}°C heat with a refreshing water activity. Pools, rivers, or the ocean all make the heat enjoyable rather than exhausting.`,
      intensity: 'Moderate', intensityColor: 'yellow',
      tags: ['outdoor', 'adventure', 'social', 'refreshing'],
      reasoning: [`${weather.temp}°C is hot — water activities are the most comfortable option`, 'Swimming naturally regulates body temperature', `Group of ${groupSz} can enjoy together`, `UV is ${weather.raw.uv} — water reflects UV; apply SPF`],
      bestTime: isHighUV ? 'Before 10 AM or after 4 PM' : 'Any time',
      whatToBring: ['Swimwear', 'Sunscreen SPF50+', 'Hat', 'Plenty of water', 'Towel'],
    })
    all.push({
      id: 'early-morning-walk', name: 'Sunrise Nature Walk', iconName: 'i-lucide-footprints',
      description: `Take advantage of the cooler morning hours before the heat peaks. A sunrise walk offers stunning light, fresh air, and birds before the city wakes up.`,
      intensity: 'Low', intensityColor: 'blue',
      tags: ['outdoor', 'solo', 'relaxed', 'nature'],
      reasoning: [`${weather.temp}°C — best explored before 9 AM when it's cooler`, 'Sunrise walks avoid peak UV and heat', `${groupSz <= 4 ? 'Perfect group size for a quiet walk' : 'A larger group walk can be lively'}`, 'Low intensity — accessible for all fitness levels'],
      bestTime: '6:00 AM – 9:00 AM',
      whatToBring: ['Light breathable clothing', 'Water bottle', 'Sunscreen', 'Hat'],
    })
  }

  if (isCold) {
    all.push({
      id: 'museum', name: 'Museum / Gallery Visit', iconName: 'i-lucide-landmark',
      description: `Explore local history, art, or science in a warm, fascinating environment. Cold weather is the perfect alibi to go deep into culture.`,
      intensity: 'Low', intensityColor: 'blue',
      tags: ['indoor', 'cultural', 'educational', 'social'],
      reasoning: [`${weather.temp}°C is cold — indoor cultural spaces are ideal`, 'Museums are fully heated and weather-proof', `Group of ${groupSz} can explore at their own pace`, 'Cultural enrichment regardless of outdoor conditions'],
      bestTime: 'Morning or afternoon (check opening hours)',
      whatToBring: ['Warm coat', 'Comfortable walking shoes', 'Camera'],
    })
  }

  // Universal / ideal-weather activities
  if (isIdeal || (!isRainy && !isHot && !isCold)) {
    all.push({
      id: 'hiking', name: 'Nature Hiking', iconName: 'i-lucide-footprints',
      description: `With ${weather.temp}°C and ${weather.description}, conditions are excellent for hitting the trails. Explore scenic routes and immerse yourself in the landscape.`,
      intensity: 'Moderate', intensityColor: 'yellow',
      tags: ['outdoor', 'adventure', 'fitness', 'nature'],
      reasoning: [`${weather.temp}°C is ${isIdeal ? 'ideal' : 'good'} for hiking`, `${weather.description} — comfortable trail conditions`, `Group of ${groupSz} ${groupSz <= 8 ? 'fits well on trails' : 'is large — consider splitting'}`, `${!isWindy ? 'Low wind — great for open ridges' : 'Wind at ' + weather.raw.wind + ' km/h — stick to sheltered paths'}`],
      bestTime: isHighUV ? 'Before 10 AM or after 4 PM' : 'Any time',
      whatToBring: ['Hiking shoes', 'Water', 'Snacks', isHighUV ? 'Sunscreen + hat' : 'Light jacket', 'Trail map'],
    })

    all.push({
      id: 'cycling', name: 'City or Trail Cycling', iconName: 'i-lucide-bike',
      description: `${weather.description} makes for perfect cycling weather. Explore the area on two wheels — discover hidden streets, viewpoints, and local gems.`,
      intensity: 'Moderate', intensityColor: 'yellow',
      tags: ['outdoor', 'adventure', 'fitness', 'social'],
      reasoning: [`${weather.temp}°C — ${isWindy ? 'wind at ' + weather.raw.wind + ' km/h may slow you down' : 'great cycling temperature'}`, `${weather.description} — good visibility`, `Group of ${groupSz} can cycle together or split by pace`, 'Covers more ground than walking'],
      bestTime: isHighUV ? '7:00–10:00 AM or 4:00–7:00 PM' : 'Morning or afternoon',
      whatToBring: ['Bike (rent if needed)', 'Helmet', 'Water', 'Sunscreen', 'Repair kit'],
    })
  }

  // Always include food & evening option
  all.push({
    id: 'local-food', name: 'Local Food & Dining Experience', iconName: 'i-lucide-utensils',
    description: `Dive into the local food scene — from street markets to sit-down restaurants. A perfect activity for any weather that brings people together over great flavours.`,
    intensity: 'Low', intensityColor: 'blue',
    tags: ['indoor', 'social', 'food', 'cultural'],
    reasoning: ['Weather-independent — works in any conditions', `Food pref ${prefs.includes('food') ? 'matched ✓' : 'not prioritized but universally enjoyable'}`, `${groupSz} people — dining out is perfect for groups`, isEvening ? 'Evening timing is ideal for dinner' : 'Great for lunch or a food tour'],
    bestTime: isEvening ? '7:00–10:00 PM' : '12:00–2:00 PM',
    whatToBring: ['Appetite', 'Cash/card', 'Open mind for local cuisine'],
  })

  if (isEvening || !isRainy) {
    all.push({
      id: 'photography', name: 'Photography Walk', iconName: 'i-lucide-camera',
      description: `${isEvening ? 'Golden hour and city lights create magical photography conditions.' : `${weather.description} light offers unique photographic opportunities.`} Wander and capture the essence of ${selectedLocation.value?.name?.split(',')[0] || 'the location'}.`,
      intensity: 'Low', intensityColor: 'blue',
      tags: ['outdoor', 'solo', 'cultural', 'creative'],
      reasoning: [isEvening ? 'Evening golden hour — best photography light of the day' : `${weather.description} creates unique, dramatic lighting`, 'Solo or small groups move at a flexible pace', 'Low intensity — walkable at your own speed', `${!isRainy ? 'Dry conditions protect your camera' : 'Light rain can add atmosphere — use a camera cover'}`],
      bestTime: isEvening ? 'Sunset ± 1 hour' : 'Morning for soft light',
      whatToBring: ['Camera or phone', 'Spare battery', isHighUV ? 'Sun hat' : 'Comfortable shoes', isRainy ? 'Camera rain cover' : 'Tripod (optional)'],
    })
  }

  // Fill to 5 if needed
  if (all.length < 5) {
    all.push({
      id: 'yoga-wellness', name: 'Outdoor Yoga & Meditation', iconName: 'i-lucide-person-standing',
      description: `Find a quiet park or rooftop for a grounding yoga session. Breathe in the ${weather.temp}°C air and reconnect with your body and mind.`,
      intensity: 'Low', intensityColor: 'blue',
      tags: ['outdoor', 'solo', 'relaxed', 'wellness'],
      reasoning: [`${isIdeal ? 'Perfect conditions' : weather.description + ' — check for a sheltered spot'}`, 'Wellness activities suit any group size', `Solo or small groups of up to ${Math.min(groupSz, 6)} work best`, `${isMorning ? 'Morning is ideal for yoga' : 'Afternoon — find shade if hot'}`],
      bestTime: '6:00–9:00 AM or 5:00–7:00 PM',
      whatToBring: ['Yoga mat', 'Water', 'Comfortable clothes', isHighUV ? 'Sunscreen' : 'Light layer'],
    })
  }

  return all.slice(0, 5)
}

async function selectHourlyTime(time: string) {
  if (!selectedLocation.value || analyzing.value) return
  selectedTime.value = time
  await runAdvisor()
}

// ── Main advisor ────────────────────────────────────────────────────────────
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
    await new Promise(r => setTimeout(r, i === 2 ? 500 : 700)) // Slightly faster for first steps
  }

  // Fetch weather data
  addLog('decision', 'Fetching weather via Open-Meteo...')
  const [weather, hourly] = await Promise.all([fetchWeather(loc.lat, loc.lon), fetchHourly(loc.lat, loc.lon)])
  addLog('decision', `Weather: ${weather.temp}°C — ${weather.description} | Rain: ${weather.raw.rainProb}% | UV: ${weather.raw.uv}`)

  // Generate activities via backend AI
  const { activities: generatedActivities, aiPowered } = await generateActivitiesWithHF(weather, selectedPrefs.value, groupSize.value, loc)
  const filteredActivities = applyPreferenceFilters(generatedActivities, selectedPrefs.value)
  const activities = ensureWeatherGuideFirst(weather, filteredActivities)

  addLog('decision', `Top recommendation: "${activities[0]?.name}"`)
  addLog('decision', `Analysis complete — ${activities.length} activities ranked`)

  results.value = { location: loc, weather, activities, hourly, aiPowered }
  analyzing.value = false
  selectedActivity.value = activities[0] ?? null
  showLog.value = true
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

<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&display=swap');
.font-body { font-family: 'DM Sans', sans-serif; }

.loader-ring {
  width: 52px; height: 52px; border-radius: 50%;
  border: 3px solid rgb(var(--color-primary-500) / 0.15);
  border-top-color: rgb(var(--color-primary-500));
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.custom-scroll::-webkit-scrollbar { width: 3px; }
.custom-scroll::-webkit-scrollbar-track { background: transparent; }
.custom-scroll::-webkit-scrollbar-thumb { background: rgb(209 213 219); border-radius: 2px; }
.dark .custom-scroll::-webkit-scrollbar-thumb { background: rgb(75 85 99); }

.custom-scroll-x::-webkit-scrollbar { height: 3px; }
.custom-scroll-x::-webkit-scrollbar-track { background: transparent; }
.custom-scroll-x::-webkit-scrollbar-thumb { background: rgb(209 213 219); border-radius: 2px; }
.dark .custom-scroll-x::-webkit-scrollbar-thumb { background: rgb(75 85 99); }

.expand-enter-active, .expand-leave-active { transition: all 0.25s ease; }
.expand-enter-from, .expand-leave-to { opacity: 0; transform: translateY(-6px); }
.expand-enter-to, .expand-leave-from { opacity: 1; transform: translateY(0); }

.log-expand-enter-active, .log-expand-leave-active { transition: all 0.3s ease; overflow: hidden; }
.log-expand-enter-from, .log-expand-leave-to { opacity: 0; max-height: 0; }
.log-expand-enter-to, .log-expand-leave-from { opacity: 1; max-height: 260px; }
</style>
