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

            <!-- Suggestions -->
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

            <p
              v-if="selectedLocation"
              class="text-[11px] text-gray-500 dark:text-gray-400 mt-2 flex items-center gap-1 truncate"
            >
              <UIcon name="i-lucide-map-pin-check" class="size-4 text-primary" />
              {{ selectedLocation.name }}
            </p>
          </div>

          <!-- GPS -->
          <div v-if="locationMode === 'gps'" class="mb-6">
            <UButton
              @click="getGPSLocation"
              :loading="gpsLoading"
              block
              color="primary"
              variant="outline"
              icon="i-lucide-navigation"
              class="rounded-xl py-3"
            >
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
              <UInput v-model="selectedDate" type="date" :min="todayDate" :max="maxForecastDate" icon="i-lucide-calendar" size="md" class="rounded-xl" />
            </div>
            <div>
              <p class="text-[11px] uppercase font-semibold tracking-wide text-gray-500 dark:text-gray-400 mb-2">Time</p>
              <UInput v-model="selectedTime" type="time" icon="i-lucide-clock" size="md" class="rounded-xl" />
            </div>
          </div>

          <!-- CTA -->
          <UButton
            @click="runAdvisor"
            :loading="analyzing"
            :disabled="!selectedLocation"
            block
            size="lg"
            color="primary"
            class="rounded-xl py-3 shadow-sm"
            icon="i-lucide-sparkles"
          >
            {{ analyzing ? 'Analyzing...' : 'Get Climate Advice' }}
          </UButton>

          <p v-if="!selectedLocation" class="text-[11px] text-center text-gray-400 mt-2">Select a location to continue</p>
        </UCard>

        <!-- Climate Log -->
        <UCard v-if="dssLog.length" :ui="{ base: 'rounded-2xl shadow-sm', body: { padding: 'p-4' } }">
          <button @click="showLog = !showLog" class="flex items-center justify-between w-full group">
            <div class="flex items-center gap-2">
              <UIcon name="i-lucide-file-search" class="size-4 text-amber-500" />
              <span class="text-[11px] uppercase font-semibold tracking-widest text-amber-500">Climate Reasoning Log</span>
              <UBadge color="success" variant="soft" size="xs">{{ dssLog.length }}</UBadge>
            </div>

            <UIcon
              :name="showLog ? 'i-lucide-chevron-up' : 'i-lucide-chevron-down'"
              class="size-4 text-gray-400 group-hover:text-gray-600 transition"
            />
          </button>

          <Transition name="log-expand">
            <div v-if="showLog" class="mt-3 space-y-1.5 max-h-52 overflow-y-auto pr-1 custom-scroll">
              <div
                v-for="(log, i) in dssLog"
                :key="i"
                class="flex items-start gap-2 text-[11px]"
              >
                <span class="text-gray-300 dark:text-gray-600 font-mono flex-shrink-0 tabular-nums mt-0.5">
                  {{ String(i + 1).padStart(2, '0') }}
                </span>

                <UIcon
                  :name="log.type === 'decision' ? 'i-lucide-zap' : log.type === 'warning' ? 'i-lucide-triangle-alert' : 'i-lucide-dot'"
                  :class="[
                    'size-3 mt-0.5 flex-shrink-0',
                    log.type === 'decision' ? 'text-primary' : log.type === 'warning' ? 'text-amber-500' : 'text-gray-400'
                  ]"
                />

                <span
                  :class="[
                    'leading-relaxed',
                    log.type === 'decision'
                      ? 'text-primary'
                      : log.type === 'warning'
                        ? 'text-amber-500'
                        : 'text-gray-500 dark:text-gray-400'
                  ]"
                >
                  {{ log.msg }}
                </span>
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
              Select your location, date, and time to get climate-based guidance on what to do and what to wear.
            </p>

            <div class="mt-10 grid grid-cols-3 gap-4 w-full max-w-xs">
              <div
                v-for="f in featureHighlights"
                :key="f.label"
                class="flex flex-col items-center gap-2 p-3 rounded-xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-gray-800/50 shadow-sm"
              >
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
            <p class="text-[11px] text-gray-400 mt-1">Powered by real-time weather & AI</p>

            <div class="mt-8 w-full max-w-xs space-y-3">
              <div
                v-for="(step, i) in loadingSteps"
                :key="i"
                :class="[
                  'flex items-center gap-3 text-[11px] transition-opacity',
                  i <= loadingStep ? 'opacity-100' : 'opacity-30'
                ]"
              >
                <div
                  :class="[
                    'w-1.5 h-1.5 rounded-full transition',
                    i <= loadingStep ? 'bg-primary' : 'bg-gray-300 dark:bg-gray-700'
                  ]"
                />

                <span :class="i <= loadingStep ? 'text-gray-700 dark:text-gray-200' : 'text-gray-400'">{{ step }}</span>

                <UIcon
                  v-if="i === loadingStep"
                  name="i-lucide-loader-circle"
                  class="size-3 text-primary animate-spin ml-auto"
                />

                <UIcon
                  v-else-if="i < loadingStep"
                  name="i-lucide-check"
                  class="size-3 text-green-500 ml-auto"
                />
              </div>
            </div>
          </div>
        </UCard>

        <!-- RESULTS (WEATHER + CLIMATE SUGGESTIONS) -->
        <template v-if="results && !analyzing">

          <!-- WEATHER -->
          <UCard :ui="{ base: 'rounded-2xl shadow-sm', body: { padding: 'p-6' } }">
            <div class="flex items-start justify-between mb-6">
              <div>
                <div class="flex items-center gap-2 mb-1">
                  <UIcon name="i-lucide-cloud-sun" class="size-4 text-primary" />
                  <span class="text-[11px] uppercase font-semibold tracking-widest text-primary">Selected Conditions</span>
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
              <div
                v-for="stat in results.weather.stats"
                :key="stat.label"
                class="flex flex-col items-center gap-1.5 p-3 rounded-xl bg-white dark:bg-gray-800/50 border border-gray-100 dark:border-gray-700 shadow-sm"
              >
                <UIcon :name="stat.icon" class="size-4 text-primary" />
                <span class="text-sm font-semibold text-gray-900 dark:text-white">{{ stat.value }}</span>
                <span class="text-[10px] text-gray-400 uppercase tracking-wide">{{ stat.label }}</span>
              </div>
            </div>

            <div class="pt-4 border-t border-gray-100 dark:border-gray-800">
              <div class="flex items-center gap-2 mb-2">
                <UIcon name="i-lucide-flask-conical" class="size-4 text-primary" />
                <span class="text-[11px] uppercase font-semibold tracking-wider text-primary">Climate Assessment</span>
              </div>

              <div class="flex flex-wrap gap-1.5">
                <UBadge
                  v-for="badge in results.weather.dssFlags"
                  :key="badge.label"
                  :color="badge.color"
                  variant="soft"
                  size="sm"
                >
                  <UIcon :name="badge.icon" class="size-3 mr-1" />
                  {{ badge.label }}
                </UBadge>
              </div>
            </div>

            <div class="mt-4 pt-4 border-t border-gray-100 dark:border-gray-800">
              <div class="flex items-center gap-2 mb-2">
                <UIcon name="i-lucide-shirt" class="size-4 text-emerald-500" />
                <span class="text-[11px] uppercase font-semibold tracking-wider text-emerald-500">Dressing & Packing Guide</span>
              </div>

              <p class="text-xs text-gray-500 dark:text-gray-400 mb-3 leading-relaxed">{{ results.weather.advisory }}</p>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div class="rounded-xl border border-gray-200 dark:border-gray-700 p-3 bg-white dark:bg-gray-800/40">
                  <div class="flex items-center gap-1.5 mb-2 text-[11px] uppercase tracking-wide font-semibold text-gray-600 dark:text-gray-300">
                    <UIcon name="i-lucide-shirt" class="size-3.5 text-primary" />
                    Dressing
                  </div>
                  <ul class="space-y-1.5">
                    <li v-for="tip in results.weather.dressingTips" :key="tip" class="text-xs text-gray-500 dark:text-gray-400 flex items-start gap-1.5">
                      <UIcon name="i-lucide-check" class="size-3 text-green-500 mt-0.5" />
                      <span>{{ tip }}</span>
                    </li>
                  </ul>
                </div>

                <div class="rounded-xl border border-gray-200 dark:border-gray-700 p-3 bg-white dark:bg-gray-800/40">
                  <div class="flex items-center gap-1.5 mb-2 text-[11px] uppercase tracking-wide font-semibold text-gray-600 dark:text-gray-300">
                    <UIcon name="i-lucide-briefcase" class="size-3.5 text-primary" />
                    Packing
                  </div>
                  <ul class="space-y-1.5">
                    <li v-for="item in results.weather.packingTips" :key="item" class="text-xs text-gray-500 dark:text-gray-400 flex items-start gap-1.5">
                      <UIcon name="i-lucide-check" class="size-3 text-green-500 mt-0.5" />
                      <span>{{ item }}</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </UCard>

          <!-- ACTIVITIES -->
          <div>
            <div class="flex items-center gap-2 mb-4">
              <UIcon name="i-lucide-sparkles" class="size-4 text-primary" />
              <span class="text-[11px] uppercase font-semibold tracking-widest text-primary">What This Weather Is Good For</span>
              <UBadge color="primary" variant="soft" size="xs" class="ml-auto">{{ results.activities.length }} Options</UBadge>
            </div>

            <div class="space-y-4">
              <UCard
                v-for="activity in results.activities"
                :key="activity.id"
                @click="selectedActivity = selectedActivity?.id === activity.id ? null : activity"
                :ui="{ base: 'cursor-pointer rounded-2xl transition-all bg-white dark:bg-gray-800 shadow-sm', body: { padding: 'p-5' } }"
                :class="selectedActivity?.id === activity.id ? 'ring-1 ring-primary' : 'hover:ring-1 hover:ring-primary/30'"
              >
                <div class="flex items-start gap-4">
                  <!-- Icon -->
                  <div class="w-12 h-12 rounded-2xl bg-gray-100 dark:bg-gray-700 border border-gray-200 dark:border-gray-700 flex items-center justify-center">
                    <UIcon :name="activity.iconName" class="size-6 text-primary" />
                  </div>

                  <div class="flex-1 min-w-0">
                    <div class="flex items-center gap-2 flex-wrap mb-1">
                      <h4 class="font-semibold text-gray-900 dark:text-white">{{ activity.name }}</h4>
                    </div>

                    <p class="text-xs leading-relaxed text-gray-500 dark:text-gray-400">{{ activity.description }}</p>
                    <p class="text-xs leading-relaxed text-emerald-600 dark:text-emerald-400 mt-2">
                      <span class="font-semibold">Clothing:</span> {{ activity.clothingRecommendation }}
                    </p>

                    <!-- Tags -->
                    <div class="flex flex-wrap gap-1.5 mt-3">
                      <span
                        v-for="tag in activity.tags"
                        :key="tag"
                        class="text-[10px] px-2 py-0.5 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-300 border border-gray-200 dark:border-gray-600"
                      >
                        {{ tag }}
                      </span>
                    </div>

                    <!-- Expanded rationale -->
                    <Transition name="expand">
                      <div
                        v-if="selectedActivity?.id === activity.id"
                        class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700"
                      >
                        <div class="flex items-center gap-2 mb-3">
                          <UIcon name="i-lucide-lightbulb" class="size-4 text-primary" />
                          <span class="text-[11px] font-semibold uppercase tracking-wide text-primary">Why It Fits This Climate</span>
                        </div>

                        <ul class="space-y-1.5">
                          <li
                            v-for="r in activity.reasoning"
                            :key="r"
                            class="flex items-start gap-2 text-xs text-gray-500 dark:text-gray-400"
                          >
                            <UIcon name="i-lucide-arrow-right" class="size-3 text-green-500 mt-1" />
                            {{ r }}
                          </li>
                        </ul>

                        <UButton
                          size="xs"
                          color="neutral"
                          variant="ghost"
                          icon="i-lucide-refresh-cw"
                          @click.stop="runAdvisor"
                          class="rounded-lg mt-2"
                        >
                          Refresh Advice
                        </UButton>
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
              <span class="text-[11px] uppercase font-semibold tracking-widest text-amber-500">
                Hourly Forecast Around Your Selected Time
              </span>
            </div>

            <div class="flex gap-3 overflow-x-auto pb-2 custom-scroll-x">
              <div
                v-for="h in results.hourly"
                :key="h.time"
                :class="[
                  'flex-shrink-0 flex flex-col items-center gap-1 px-4 py-3 min-w-[68px] rounded-xl border shadow-sm transition-all',
                  h.isSelected
                    ? 'border-primary bg-primary/10 ring-1 ring-primary'
                    : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800/50'
                ]"
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
            <UButton
              @click="resetAll"
              color="neutral"
              variant="ghost"
              size="sm"
              class="rounded-lg"
              icon="i-lucide-rotate-ccw"
            >
              Start New Analysis
            </UButton>
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
  tags: string[]; reasoning: string[]; clothingRecommendation: string
}
interface WeatherStat { icon: string; value: string; label: string }
interface WeatherData {
  temp: number; description: string; iconName: string
  rainProb: number; weatherCode: number
  stats: WeatherStat[]; dssFlags: { label: string; icon: string; color: string }[]
  dressingTips: string[]; packingTips: string[]; advisory: string
}
interface HourlyForecast { time: string; temp: number; iconName: string; rain: number; isSelected: boolean }
interface Results {
  location: Location; weather: WeatherData
  activities: Activity[]; hourly: HourlyForecast[]
}

const locationMode = ref<'manual' | 'map' | 'gps'>('manual')
const locationQuery = ref('')
const locationSuggestions = ref<any[]>([])
const selectedLocation = ref<Location | null>(null)
const geocoding = ref(false)
const gpsLoading = ref(false)
const mapReady = ref(false)
const mapContainer = ref<HTMLElement | null>(null)
const selectedDate = ref<string>(new Date().toISOString().slice(0, 10))
const selectedTime = ref('12:00')
const analyzing = ref(false)
const results = ref<Results | null>(null)
const selectedActivity = ref<Activity | null>(null)
const dssLog = ref<DSSLog[]>([])
const showLog = ref(false)
const loadingStep = ref(0)
const loadingMsg = ref('Fetching real-time weather data...')
let leafletMap: any = null

function isoDate(value: Date): string {
  return value.toISOString().slice(0, 10)
}

const todayDate = computed(() => isoDate(new Date()))
const maxForecastDate = computed(() => {
  const d = new Date()
  d.setDate(d.getDate() + 15)
  return isoDate(d)
})

const locationModes = [
  { value: 'manual', label: 'Type', icon: 'i-lucide-pencil' },
  { value: 'map', label: 'Map', icon: 'i-lucide-map' },
  { value: 'gps', label: 'GPS', icon: 'i-lucide-navigation' },
]

const featureHighlights = [
  { icon: 'i-lucide-cloud-sun', label: 'Live Weather' },
  { icon: 'i-lucide-list-checks', label: 'Climate Suggestions' },
  { icon: 'i-lucide-shirt', label: 'Clothing Tips' },
]

const loadingMessages = [
  'Fetching real-time weather data...',
  'Analyzing climate conditions...',
  'Building practical suggestions...',
  'Compiling your recommendations...',
]
const loadingSteps = [
  'Geocoding location',
  'Fetching weather forecast',
  'Analyzing climate conditions',
  'Preparing recommendations',
]

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

function addLog(type: DSSLog['type'], msg: string) {
  dssLog.value.unshift({ type, msg })
  if (dssLog.value.length > 20) dssLog.value.pop()
}

function formatDateTime(date: string, time: string): string {
  try {
    const d = new Date(`${date}T${time}`)
    return d.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' }) + ' at ' + d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
  } catch { return `${date} ${time}` }
}

function clampDateWithinForecast(date: string): string {
  if (date < todayDate.value) return todayDate.value
  if (date > maxForecastDate.value) return maxForecastDate.value
  return date
}

function pickBestHourlyIndex(times: string[], date: string, time: string): number {
  if (!times.length) return -1
  const selectedHour = Number.parseInt(time.split(':')[0] ?? '12', 10)
  const exactKey = `${date}T${String(selectedHour).padStart(2, '0')}:00`
  const exactIdx = times.findIndex((t: string) => t === exactKey)
  if (exactIdx >= 0) return exactIdx

  const dateRows = times
    .map((t: string, idx: number) => ({ t, idx }))
    .filter((row: { t: string; idx: number }) => row.t.startsWith(`${date}T`))

  if (dateRows.length) {
    let bestIdx = dateRows[0].idx
    let bestDist = Number.POSITIVE_INFINITY
    for (const row of dateRows) {
      const hour = Number.parseInt(row.t.split('T')[1]?.split(':')[0] ?? '0', 10)
      const dist = Math.abs(hour - selectedHour)
      if (dist < bestDist) {
        bestDist = dist
        bestIdx = row.idx
      }
    }
    return bestIdx
  }

  // Forecast may not include the requested day (for example, too far in future): use nearest available row.
  const target = `${date}T${String(selectedHour).padStart(2, '0')}:00`
  const targetTs = new Date(target).getTime()
  let nearest = 0
  let nearestDist = Number.POSITIVE_INFINITY
  for (let i = 0; i < times.length; i++) {
    const ts = new Date(times[i]).getTime()
    const dist = Number.isNaN(ts) || Number.isNaN(targetTs)
      ? Math.abs(times[i].localeCompare(target))
      : Math.abs(ts - targetTs)
    if (dist < nearestDist) {
      nearestDist = dist
      nearest = i
    }
  }
  return nearest
}

function buildWeatherAdvice(temp: number, rainProb: number, wind: number, uv: number, wc: number, hour: number) {
  const dressingTips: string[] = []
  const packingTips: string[] = []

  if (temp >= 32) {
    dressingTips.push('Wear light, breathable clothing and avoid dark heavy fabrics')
    packingTips.push('Carry extra water or an electrolyte drink')
  } else if (temp <= 10) {
    dressingTips.push('Layer up with a warm inner layer and insulated outerwear')
    packingTips.push('Pack gloves or a scarf for warmth')
  } else if (temp <= 18) {
    dressingTips.push('Use light layers with a long-sleeve top or light jacket')
    packingTips.push('Bring a thin extra layer for cooler periods')
  } else {
    dressingTips.push('A comfortable light outfit should work well for this weather')
  }

  if (rainProb >= 60 || (wc >= 51 && wc <= 82)) {
    dressingTips.push('Use a rainproof outer layer and water-resistant shoes')
    packingTips.push('Pack a compact umbrella or rain jacket')
  } else if (rainProb >= 30) {
    dressingTips.push('Carry a light layer in case of a brief shower')
  }

  if (wind >= 30) {
    dressingTips.push('Wear a wind-resistant outer layer')
    packingTips.push('Bring a secure hat or hair tie for windy conditions')
  }

  if (uv >= 7) {
    packingTips.push('Carry sunscreen, sunglasses, and a hat for UV protection')
  }

  if (hour < 7 || hour >= 18) {
    packingTips.push('Add a light reflective or visible layer for lower-light hours')
  }

  const advisory = rainProb >= 60
    ? 'Rain risk is elevated at your selected time, so keep plans flexible and pack rain protection.'
    : uv >= 7
      ? 'UV exposure is elevated around your selected time, so prioritize sun protection.'
      : temp >= 32
        ? 'Heat stress risk is higher around your selected time, so hydrate consistently.'
        : temp <= 10
          ? 'Cold exposure risk is higher around your selected time, so keep warm layers on hand.'
          : 'Conditions look manageable for your selected time with standard weather prep.'

  return {
    dressingTips: dressingTips.slice(0, 4),
    packingTips: packingTips.slice(0, 4),
    advisory,
  }
}

function getClothingRecommendation(temp: number, rainProb: number, wc: number): string {
  const rainy = rainProb >= 50 || (wc >= 51 && wc <= 82)
  if (temp <= 10) return rainy ? 'Warm layers + waterproof jacket and closed shoes.' : 'Warm layers, insulated outerwear, and closed shoes.'
  if (temp <= 18) return rainy ? 'Long sleeves, light jacket, and a rainproof shell.' : 'Long sleeves with a light jacket or hoodie.'
  if (temp <= 30) return rainy ? 'Breathable clothes with a waterproof light jacket.' : 'Light, breathable outfit with comfortable shoes.'
  return rainy ? 'Very light breathable clothes plus a thin rain shell.' : 'Very light breathable clothes, hat, and hydration-friendly outfit.'
}

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
  addLog('info', `Location: ${selectedLocation.value.name}`)
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

// Map integration
async function initMap() {
  await nextTick()
  if (!mapContainer.value || leafletMap) return
  try {
    // Dynamically load Leaflet CSS
    if (!document.getElementById('leaflet-css')) {
      const link = document.createElement('link')
      link.id = 'leaflet-css'
      link.rel = 'stylesheet'
      link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
      document.head.appendChild(link)
    }
    // Load Leaflet JS
    const L = await import('https://unpkg.com/leaflet@1.9.4/dist/leaflet-src.esm.js' as any).catch(() => null)
    if (!L) return
    leafletMap = L.map(mapContainer.value).setView([-1.286, 36.817], 6)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      attribution: '© CartoDB',
      subdomains: 'abcd',
      maxZoom: 19,
    }).addTo(leafletMap)
    leafletMap.on('click', async (e: any) => {
      const { lat, lng } = e.latlng
      // Reverse geocode
      try {
        const rev = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`)
        const data = await rev.json()
        selectedLocation.value = {
          lat, lon: lng,
          name: data.display_name?.split(',').slice(0, 3).join(', ') || `${lat.toFixed(4)}, ${lng.toFixed(4)}`,
        }
      } catch {
        selectedLocation.value = { lat, lon: lng, name: `${lat.toFixed(4)}, ${lng.toFixed(4)}` }
      }
      // Add marker
      L.marker([lat, lng]).addTo(leafletMap)
        .bindPopup(selectedLocation.value!.name).openPopup()
      addLog('info', `Map pin dropped at ${selectedLocation.value!.name}`)
    })
    mapReady.value = true
  } catch {
    mapReady.value = false
  }
}


watch(locationMode, async (val) => { if (val === 'map') { await nextTick(); setTimeout(initMap, 100) } })

async function fetchWeather(lat: number, lon: number): Promise<WeatherData> {
  try {
    const requestedDate = clampDateWithinForecast(selectedDate.value)
    if (requestedDate !== selectedDate.value) {
      addLog('warning', `Forecast is limited to 16 days; using ${requestedDate} weather data.`)
    }
    const res = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation_probability,weathercode,uv_index&timezone=auto&forecast_days=16`)
    const data = await res.json()
    const h = data.hourly
    const times: string[] = h?.time ?? []
    const idx = pickBestHourlyIndex(times, requestedDate, selectedTime.value)
    if (idx < 0) throw new Error('No hourly weather rows returned')

    const matched = times[idx] ?? `${requestedDate}T${selectedTime.value}`
    const matchedHour = Number.parseInt(matched.split('T')[1]?.split(':')[0] ?? '12', 10)
    const temp = Math.round(h.temperature_2m?.[idx] ?? 24)
    const humidity = Math.round(h.relative_humidity_2m?.[idx] ?? 60)
    const wind = Math.round(h.wind_speed_10m?.[idx] ?? 15)
    const rainProb = Math.round(h.precipitation_probability?.[idx] ?? 0)
    const uv = Number(h.uv_index?.[idx] ?? 0)
    const wc = Number(h.weathercode?.[idx] ?? 0)

    if (!matched.startsWith(`${requestedDate}T`)) {
      addLog('warning', `Requested time not fully available; using nearest forecast slot (${matched.replace('T', ' ')})`)
    }

    const flags: any[] = []
    if (temp >= 20 && temp <= 30) flags.push({ label: 'Comfortable Temp', icon: 'i-lucide-circle-check', color: 'green' })
    else if (temp > 35) flags.push({ label: 'Heat Alert', icon: 'i-lucide-flame', color: 'red' })
    else if (temp < 10) flags.push({ label: 'Cold Advisory', icon: 'i-lucide-snowflake', color: 'blue' })
    if (rainProb > 60) flags.push({ label: 'Rain Likely', icon: 'i-lucide-cloud-rain', color: 'yellow' })
    if (uv > 7) flags.push({ label: 'High UV', icon: 'i-lucide-sun', color: 'orange' })
    if (wind > 30) flags.push({ label: 'Windy', icon: 'i-lucide-wind', color: 'sky' })
    if (!flags.length) flags.push({ label: 'Ideal Conditions', icon: 'i-lucide-star', color: 'green' })
    const advice = buildWeatherAdvice(temp, rainProb, wind, uv, wc, matchedHour)
    return {
      temp, description: wcToDesc(wc), iconName: wcToIconName(wc), rainProb, weatherCode: wc,
      stats: [
        { icon: 'i-lucide-droplets', value: `${humidity}%`, label: 'Humidity' },
        { icon: 'i-lucide-wind', value: `${wind} km/h`, label: 'Wind' },
        { icon: 'i-lucide-cloud-rain', value: `${rainProb}%`, label: 'Rain' },
        { icon: 'i-lucide-sun', value: String(uv), label: 'UV Index' },
      ],
      dssFlags: flags,
      dressingTips: advice.dressingTips,
      packingTips: advice.packingTips,
      advisory: advice.advisory,
    }
  } catch {
    return {
      temp: 24, description: 'Partly cloudy', iconName: 'i-lucide-cloud-sun', rainProb: 20, weatherCode: 2,
      stats: [{ icon: 'i-lucide-droplets', value: '60%', label: 'Humidity' }, { icon: 'i-lucide-wind', value: '15 km/h', label: 'Wind' }, { icon: 'i-lucide-cloud-rain', value: '20%', label: 'Rain' }, { icon: 'i-lucide-sun', value: '5', label: 'UV Index' }],
      dssFlags: [{ label: 'Estimated Data', icon: 'i-lucide-triangle-alert', color: 'yellow' }],
      dressingTips: ['Wear light layers and adjust based on comfort'],
      packingTips: ['Carry water and a compact weather layer'],
      advisory: 'Live weather data was unavailable, so this guidance uses fallback estimates.',
    }
  }
}

async function fetchHourly(lat: number, lon: number): Promise<HourlyForecast[]> {
  try {
    const requestedDate = clampDateWithinForecast(selectedDate.value)
    const res = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&hourly=temperature_2m,weathercode,precipitation_probability&timezone=auto&forecast_days=16`)
    const data = await res.json(); const h = data.hourly
    const times: string[] = h?.time ?? []
    const selectedIdx = pickBestHourlyIndex(times, requestedDate, selectedTime.value)
    if (selectedIdx < 0) return []
    return Array.from({ length: 8 }, (_, i) => {
      const hourIdx = Math.max(0, Math.min(times.length - 1, selectedIdx - 2 + i))
      const wc = h.weathercode?.[hourIdx] ?? 0
      const label = (times[hourIdx]?.split('T')[1] ?? `${String(hourIdx).padStart(2, '0')}:00`).slice(0, 5)
      return { time: label, temp: Math.round(h.temperature_2m?.[hourIdx] ?? 20), iconName: wcToIconName(wc), rain: h.precipitation_probability?.[hourIdx] ?? 0, isSelected: hourIdx === selectedIdx }
    })
  } catch { return [] }
}

function generateActivities(weather: WeatherData): Activity[] {
  const isRainy = weather.rainProb >= 55 || (weather.weatherCode >= 51 && weather.weatherCode <= 82)
  const isHot = weather.temp >= 31
  const isCold = weather.temp <= 12
  const isCool = weather.temp > 12 && weather.temp <= 20
  const isEvening = parseInt(selectedTime.value.split(':')[0] ?? '12', 10) >= 17
  const clothing = getClothingRecommendation(weather.temp, weather.rainProb, weather.weatherCode)

  if (isRainy) {
    return [
      {
        id: 'indoor-cafe',
        name: 'Cafe, Reading, or Co-working Session',
        iconName: 'i-lucide-coffee',
        description: 'Comfortable for rainy conditions with minimal exposure between stops.',
        tags: ['indoor', 'rain-safe', 'casual'],
        clothingRecommendation: clothing,
        reasoning: ['Rain is likely, so an indoor plan is more reliable.', 'Easy to adapt if showers intensify.'],
      },
      {
        id: 'museum-arts',
        name: 'Museum, Gallery, or Cultural Center',
        iconName: 'i-lucide-landmark',
        description: 'A weather-safe way to spend a few hours productively and comfortably.',
        tags: ['indoor', 'cultural'],
        clothingRecommendation: clothing,
        reasoning: ['Keeps plans stable during rainy periods.', 'Good for both day and evening slots.'],
      },
      {
        id: 'mall-cinema',
        name: 'Mall Walk + Cinema or Indoor Games',
        iconName: 'i-lucide-clapperboard',
        description: 'Useful when rain makes outdoor movement inconvenient.',
        tags: ['indoor', 'social'],
        clothingRecommendation: clothing,
        reasoning: ['Indoor venues reduce disruption from rain.', 'Good option when roads/paths are wet.'],
      },
    ]
  }

  if (isHot) {
    return [
      {
        id: 'early-late-walk',
        name: 'Short Walk in Shade (Early or Late)',
        iconName: 'i-lucide-trees',
        description: 'Outdoor time is better in shaded places and cooler hours.',
        tags: ['outdoor', 'light-activity'],
        clothingRecommendation: clothing,
        reasoning: ['Heat is high, so shorter low-intensity options are safer.', 'Hydration and sun protection are important.'],
      },
      {
        id: 'pool-indoor-sport',
        name: 'Swimming or Indoor Fitness',
        iconName: 'i-lucide-dumbbell',
        description: 'Keeps activity levels up while limiting heat stress.',
        tags: ['fitness', 'heat-aware'],
        clothingRecommendation: clothing,
        reasoning: ['Lower heat exposure than long outdoor sessions.', 'Easier to control rest and hydration.'],
      },
      {
        id: 'evening-dining',
        name: 'Evening Food Spot or Rooftop Chill',
        iconName: 'i-lucide-utensils',
        description: 'Better comfort once temperatures begin to drop.',
        tags: ['social', 'evening'],
        clothingRecommendation: clothing,
        reasoning: [isEvening ? 'Your selected time already favors this option.' : 'Usually more comfortable later in the day.'],
      },
    ]
  }

  if (isCold || isCool) {
    return [
      {
        id: 'park-walk',
        name: 'Park Walk or Light Jog',
        iconName: 'i-lucide-footprints',
        description: 'Comfortable for gentle movement when layered appropriately.',
        tags: ['outdoor', 'wellness'],
        clothingRecommendation: clothing,
        reasoning: ['Cool temperatures can be pleasant with layers.', 'Good balance of movement and comfort.'],
      },
      {
        id: 'city-explore',
        name: 'City Exploring and Photography',
        iconName: 'i-lucide-camera',
        description: 'Good visibility and comfort for urban exploration.',
        tags: ['outdoor', 'casual'],
        clothingRecommendation: clothing,
        reasoning: ['Lower heat load supports longer exploration.', 'Simple to pause indoors if needed.'],
      },
      {
        id: 'community-events',
        name: 'Community Event or Local Market',
        iconName: 'i-lucide-store',
        description: 'Flexible option with both indoor and outdoor segments.',
        tags: ['social', 'flexible'],
        clothingRecommendation: clothing,
        reasoning: ['Easy to adapt to changing comfort conditions.', 'Works across daytime and evening.'],
      },
    ]
  }

  return [
    {
      id: 'general-outdoor',
      name: 'General Outdoor Activities',
      iconName: 'i-lucide-sun',
      description: 'Weather is generally favorable for walking, parks, and casual outdoor plans.',
      tags: ['outdoor', 'balanced'],
      clothingRecommendation: clothing,
      reasoning: ['Temperature and rain risk look manageable.', 'Suitable for a wide range of activities.'],
    },
    {
      id: 'sports-social',
      name: 'Social Sports or Group Meetups',
      iconName: 'i-lucide-users',
      description: 'A good climate window for active and social plans.',
      tags: ['social', 'active'],
      clothingRecommendation: clothing,
      reasoning: ['Comfort level supports moderate activity.', 'Low weather friction for movement.'],
    },
    {
      id: 'mixed-day',
      name: 'Mixed Plan (Outdoor + Indoor)',
      iconName: 'i-lucide-route',
      description: 'Combine outdoor time with an indoor backup for flexibility.',
      tags: ['flexible'],
      clothingRecommendation: clothing,
      reasoning: ['Keeps your plan robust if weather shifts.', 'Useful for longer outings.'],
    },
  ]
}

async function runAdvisor() {
  if (!selectedLocation.value) return
  analyzing.value = true; results.value = null; selectedActivity.value = null
  dssLog.value = []; showLog.value = false; loadingStep.value = 0
  const loc = selectedLocation.value
  addLog('info', `Climate analysis: ${loc.name}`)
  selectedDate.value = clampDateWithinForecast(selectedDate.value)
  addLog('info', `${selectedDate.value} ${selectedTime.value}`)

  for (let i = 0; i < loadingMessages.length; i++) {
    loadingMsg.value = loadingMessages[i]; loadingStep.value = i
    if (i === 0) addLog('decision', 'Fetching weather via Open-Meteo...')
    if (i === 1) addLog('decision', 'Analyzing temperature, rain, and timing...')
    if (i === 2) addLog('decision', 'Building practical activity suggestions...')
    if (i === 3) addLog('info', 'Compiling climate advice...')
    await new Promise(r => setTimeout(r, 650))
  }

  const [weather, hourly] = await Promise.all([fetchWeather(loc.lat, loc.lon), fetchHourly(loc.lat, loc.lon)])
  addLog('decision', `Weather: ${weather.temp}°C — ${weather.description}`)
  const activities = generateActivities(weather)
  if (activities.length) addLog('decision', `Suggested: ${activities[0].name}`)
  addLog('decision', `Complete — ${activities.length} climate-based options generated`)

  results.value = { location: loc, weather, activities, hourly }
  analyzing.value = false
  selectedActivity.value = activities[0] ?? null
  showLog.value = true
}

function resetAll() {
  results.value = null; selectedActivity.value = null; dssLog.value = []
  showLog.value = false; loadingStep.value = 0; selectedLocation.value = null
  locationQuery.value = ''; locationSuggestions.value = []
}

onMounted(() => {
  selectedDate.value = isoDate(new Date())
  const now = new Date()
  selectedTime.value = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&display=swap');
.font-body { font-family: 'DM Sans', sans-serif; }

.dss-slider {
  -webkit-appearance: none; appearance: none;
  width: 100%; height: 4px;
  background: rgb(229 231 235);
  border-radius: 2px; outline: none; cursor: pointer;
}
.dark .dss-slider { background: rgb(55 65 81); }
.dss-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 14px; height: 14px; border-radius: 50%;
  background: rgb(var(--color-primary-500));
  cursor: pointer;
  box-shadow: 0 0 6px rgb(var(--color-primary-500) / 0.5);
}

.ring-pulse { animation: pulse-ring 3s ease-in-out infinite; }
@keyframes pulse-ring {
  0%, 100% { box-shadow: 0 0 0 0 rgb(var(--color-primary-500) / 0.2); }
  50% { box-shadow: 0 0 0 12px rgb(var(--color-primary-500) / 0); }
}

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
