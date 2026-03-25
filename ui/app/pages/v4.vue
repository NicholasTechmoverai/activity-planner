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

          <!-- DSS Weights -->
          <div class="mb-6">
            <div class="flex items-center justify-between mb-3">
              <p class="text-[11px] uppercase font-semibold tracking-wide text-gray-600 dark:text-gray-400">DSS Decision Weights</p>
              <UTooltip text="Adjust how the AI balances factors when recommending activities">
                <UIcon name="i-lucide-info" class="size-4 text-gray-400 cursor-help" />
              </UTooltip>
            </div>

            <div class="space-y-4">
              <div v-for="w in dssWeights" :key="w.key">
                <div class="flex justify-between text-[11px] mb-2">
                  <span class="text-gray-600 dark:text-gray-400 flex items-center gap-1.5">
                    <UIcon :name="w.icon" class="size-3.5" />
                    {{ w.label }}
                  </span>
                  <span class="font-mono text-primary font-semibold">{{ w.value }}%</span>
                </div>

                <input
                  type="range"
                  min="0"
                  max="100"
                  step="5"
                  v-model.number="w.value"
                  class="w-full h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full accent-primary transition"
                />
              </div>
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
            block
            size="lg"
            color="primary"
            class="rounded-xl py-3 shadow-sm"
            icon="i-lucide-sparkles"
          >
            {{ analyzing ? 'Analyzing...' : 'Get AI Recommendations' }}
          </UButton>

          <p v-if="!selectedLocation" class="text-[11px] text-center text-gray-400 mt-2">Select a location to continue</p>
        </UCard>

        <!-- DSS Log -->
        <UCard v-if="dssLog.length" :ui="{ base: 'rounded-2xl shadow-sm', body: { padding: 'p-4' } }">
          <button @click="showLog = !showLog" class="flex items-center justify-between w-full group">
            <div class="flex items-center gap-2">
              <UIcon name="i-lucide-file-search" class="size-4 text-amber-500" />
              <span class="text-[11px] uppercase font-semibold tracking-widest text-amber-500">DSS Reasoning Log</span>
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
              Select your location, pick a date and time, then let our AI Decision Support System find the perfect activity.
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

        <!-- RESULTS (WEATHER + SCORING + ACTIVITIES) -->
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
                <span class="text-[11px] uppercase font-semibold tracking-wider text-primary">DSS Weather Assessment</span>
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
          </UCard>

          <!-- SCORING -->
          <UCard :ui="{ base: 'rounded-2xl shadow-sm', body: { padding: 'p-6' } }">
            <div class="flex items-center gap-2 mb-6">
              <UIcon name="i-lucide-bar-chart-3" class="size-4 text-violet-500" />
              <span class="text-[11px] uppercase tracking-widest font-semibold text-violet-500">DSS Multi-Criteria Scoring</span>
            </div>

            <div class="space-y-5">
              <div v-for="c in results.dssScores" :key="c.name">
                <div class="flex justify-between text-[11px] mb-1">
                  <span class="text-gray-600 dark:text-gray-400 flex items-center gap-1.5">
                    <UIcon :name="c.icon" class="size-4" />
                    {{ c.name }}
                  </span>

                  <span
                    class="font-mono font-semibold"
                    :class="c.score >= 70 ? 'text-green-500' : c.score >= 40 ? 'text-amber-500' : 'text-red-500'"
                  >
                    {{ c.score }}/100
                  </span>
                </div>

                <div class="h-2 bg-gray-200 dark:bg-gray-800 rounded-full overflow-hidden">
                  <div
                    class="h-full rounded-full transition-all duration-700 ease-out"
                    :style="{ width: c.score + '%', background: c.color }"
                  />
                </div>
              </div>
            </div>
          </UCard>

          <!-- ACTIVITIES -->
          <div>
            <div class="flex items-center gap-2 mb-4">
              <UIcon name="i-lucide-sparkles" class="size-4 text-primary" />
              <span class="text-[11px] uppercase font-semibold tracking-widest text-primary">AI Recommendations</span>
              <UBadge color="primary" variant="soft" size="xs" class="ml-auto">{{ results.activities.length }} Options</UBadge>
            </div>

            <div class="space-y-4">
              <UCard
                v-for="(activity, idx) in results.activities"
                :key="activity.id"
                @click="selectedActivity = selectedActivity?.id === activity.id ? null : activity"
                :ui="{ base: 'cursor-pointer rounded-2xl transition-all bg-white dark:bg-gray-800 shadow-sm', body: { padding: 'p-5' } }"
                :class="selectedActivity?.id === activity.id ? 'ring-1 ring-primary' : 'hover:ring-1 hover:ring-primary/30'"
              >
                <!-- Rank badge -->
                <div
                  :class="[
                    'absolute -top-2 right-4 px-2 py-0.5 rounded-full text-[10px] font-semibold border backdrop-blur-sm',
                    idx === 0
                      ? 'bg-amber-50 border-amber-200 text-amber-600'
                      : idx === 1
                        ? 'bg-gray-50 border-gray-200 text-gray-500'
                        : 'bg-orange-50 border-orange-200 text-orange-500'
                  ]"
                >
                  {{ idx === 0 ? '#1 Best' : idx === 1 ? '#2' : '#3' }}
                </div>

                <div class="flex items-start gap-4">
                  <!-- Icon -->
                  <div class="w-12 h-12 rounded-2xl bg-gray-100 dark:bg-gray-700 border border-gray-200 dark:border-gray-700 flex items-center justify-center">
                    <UIcon :name="activity.iconName" class="size-6 text-primary" />
                  </div>

                  <div class="flex-1 min-w-0">
                    <div class="flex items-center gap-2 flex-wrap mb-1">
                      <h4 class="font-semibold text-gray-900 dark:text-white">{{ activity.name }}</h4>

                      <UBadge :color="activity.intensityColor" variant="soft" size="xs">{{ activity.intensity }}</UBadge>

                      <UBadge v-if="idx === 0" color="success" variant="soft" size="xs">
                        <UIcon name="i-lucide-star" class="size-3 mr-1" />
                        Best Match
                      </UBadge>
                    </div>

                    <p class="text-xs leading-relaxed text-gray-500 dark:text-gray-400">{{ activity.description }}</p>

                    <!-- Score bar -->
                    <div class="flex items-center gap-2 mt-3">
                      <span class="text-[10px] uppercase tracking-wide text-gray-400">DSS Score</span>

                      <div class="flex-1 h-1.5 bg-gray-200 dark:bg-gray-800 rounded-full overflow-hidden">
                        <div
                          class="h-full rounded-full transition-all duration-700"
                          :style="{ width: activity.dssScore + '%', background: 'linear-gradient(90deg, rgb(var(--color-primary-500)), #a855f7)' }"
                        />
                      </div>

                      <span class="text-xs font-mono font-semibold text-primary">{{ activity.dssScore }}%</span>
                    </div>

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
                          <span class="text-[11px] font-semibold uppercase tracking-wide text-primary">DSS Decision Rationale</span>
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

                        <div class="flex gap-2 mt-4">
                          <UButton size="xs" color="primary" icon="i-lucide-check-circle" class="rounded-lg">
                            Accept
                          </UButton>
                          <UButton
                            size="xs"
                            color="neutral"
                            variant="ghost"
                            icon="i-lucide-refresh-cw"
                            @click.stop="runAdvisor"
                            class="rounded-lg"
                          >
                            Regenerate
                          </UButton>
                        </div>
                      </div>
                    </Transition>
                  </div>

                  <!-- Score -->
                  <div class="text-right flex-shrink-0">
                    <div
                      class="text-2xl font-bold tabular-nums"
                      :class="activity.dssScore >= 75 ? 'text-green-500' : activity.dssScore >= 50 ? 'text-amber-500' : 'text-red-500'"
                    >
                      {{ activity.dssScore }}
                    </div>
                    <div class="text-[10px] text-gray-400 uppercase tracking-wide">score</div>

                    <UIcon
                      :name="selectedActivity?.id === activity.id ? 'i-lucide-chevron-up' : 'i-lucide-chevron-down'"
                      class="size-4 text-gray-400 mt-1"
                    />
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
                Hourly Forecast — DSS Window
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

// Types (same as before)
interface Location { lat: number; lon: number; name: string }
interface DSSLog { msg: string; type: 'info' | 'decision' | 'warning' }
interface Activity {
  id: string; name: string; iconName: string; description: string
  intensity: string; intensityColor: string; dssScore: number
  tags: string[]; reasoning: string[]
}
interface WeatherStat { icon: string; value: string; label: string }
interface WeatherData {
  temp: number; description: string; iconName: string
  stats: WeatherStat[]; dssFlags: { label: string; icon: string; color: string }[]
}
interface HourlyForecast { time: string; temp: number; iconName: string; rain: number; isSelected: boolean }
interface DSSCriteria { name: string; icon: string; score: number; color: string }
interface Results {
  location: Location; weather: WeatherData
  activities: Activity[]; dssScores: DSSCriteria[]; hourly: HourlyForecast[]
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
let leafletMap: any = null

// Rate limiting helper
let lastApiCall = 0
const RATE_LIMIT_DELAY = 2000 // 2 seconds between API calls

async function waitForRateLimit() {
  const now = Date.now()
  const timeSinceLastCall = now - lastApiCall
  if (timeSinceLastCall < RATE_LIMIT_DELAY) {
    const waitTime = RATE_LIMIT_DELAY - timeSinceLastCall
    console.log(`Rate limiting: waiting ${waitTime}ms...`)
    await new Promise(resolve => setTimeout(resolve, waitTime))
  }
  lastApiCall = Date.now()
}

// OpenAI API Key
const OPENAI_API_KEY = import.meta.env.VITE_OPENAI_API_KEY || ''

console.log("API Key present:", !!OPENAI_API_KEY)

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

const dssWeights = ref([
  { key: 'weather', label: 'Weather Suitability', icon: 'i-lucide-cloud-sun', value: 40 },
  { key: 'preference', label: 'User Preferences', icon: 'i-lucide-target', value: 30 },
  { key: 'social', label: 'Group Suitability', icon: 'i-lucide-users', value: 20 },
  { key: 'time', label: 'Time Appropriateness', icon: 'i-lucide-clock', value: 10 },
])

const featureHighlights = [
  { icon: 'i-lucide-cloud-sun', label: 'Live Weather' },
  { icon: 'i-lucide-bot', label: 'AI Scoring' },
  { icon: 'i-lucide-scale', label: 'DSS Weights' },
]

const loadingMessages = [
  'Fetching real-time weather data...',
  'Running DSS multi-criteria analysis...',
  'Scoring activity options with AI...',
  'Compiling your recommendations...',
]
const loadingSteps = [
  'Geocoding location',
  'Fetching weather forecast',
  'Running DSS scoring engine',
  'Generating AI recommendations',
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

async function initMap() {
  await nextTick()
  if (!mapContainer.value || leafletMap) return
  try {
    if (!document.getElementById('leaflet-css')) {
      const link = document.createElement('link')
      link.id = 'leaflet-css'
      link.rel = 'stylesheet'
      link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
      document.head.appendChild(link)
    }
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
    const res = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation_probability,weathercode,uv_index&forecast_days=1`)
    const data = await res.json()
    const c = data.current
    const temp = Math.round(c.temperature_2m), humidity = c.relative_humidity_2m
    const wind = Math.round(c.wind_speed_10m), rainProb = c.precipitation_probability ?? 0
    const uv = c.uv_index ?? 0, wc = c.weathercode ?? 0
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
    }
  } catch {
    return {
      temp: 24, description: 'Partly cloudy', iconName: 'i-lucide-cloud-sun',
      stats: [{ icon: 'i-lucide-droplets', value: '60%', label: 'Humidity' }, { icon: 'i-lucide-wind', value: '15 km/h', label: 'Wind' }, { icon: 'i-lucide-cloud-rain', value: '20%', label: 'Rain' }, { icon: 'i-lucide-sun', value: '5', label: 'UV Index' }],
      dssFlags: [{ label: 'Estimated Data', icon: 'i-lucide-triangle-alert', color: 'yellow' }],
    }
  }
}

async function fetchHourly(lat: number, lon: number): Promise<HourlyForecast[]> {
  try {
    const res = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&hourly=temperature_2m,weathercode,precipitation_probability&forecast_days=1`)
    const data = await res.json(); const h = data.hourly
    const selectedHour = parseInt(selectedTime.value.split(':')[0])
    return Array.from({ length: 8 }, (_, i) => {
      const hourIdx = Math.max(0, Math.min(23, selectedHour - 2 + i))
      const wc = h.weathercode?.[hourIdx] ?? 0
      return { time: `${String(hourIdx).padStart(2, '0')}:00`, temp: Math.round(h.temperature_2m?.[hourIdx] ?? 20), iconName: wcToIconName(wc), rain: h.precipitation_probability?.[hourIdx] ?? 0, isSelected: hourIdx === selectedHour }
    })
  } catch { return [] }
}

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

// FIXED: AI-powered activity generation with better error handling and rate limiting
async function generateActivitiesWithAI(weather: WeatherData, prefs: string[], groupSz: number, location: Location): Promise<Activity[]> {
  // Check if API key is valid
  if (!OPENAI_API_KEY || OPENAI_API_KEY === '') {
    addLog('warning', 'No OpenAI API key found. Using fallback recommendations.')
    return generateFallbackActivities(weather, prefs, groupSz)
  }

  try {
    // Wait for rate limit before making the call
    await waitForRateLimit()
    
    const prompt = `You are a global Decision Support System for activity recommendations. Based on the following context, recommend 5-6 activities with detailed reasoning:

LOCATION: ${location.name} (${location.lat}, ${location.lon})
WEATHER: ${weather.temp}°C, ${weather.description}
PRECIPITATION: ${weather.stats[2].value}
WIND: ${weather.stats[1].value}
HUMIDITY: ${weather.stats[0].value}
UV INDEX: ${weather.stats[3].value}
TIME: ${selectedTime.value}
DATE: ${selectedDate.value}
GROUP SIZE: ${groupSz} people
USER PREFERENCES: ${prefs.join(', ')}

Return a JSON object with an "activities" array where each object has:
- id (string, unique)
- name (string)
- iconName (one of: i-lucide-footprints, i-lucide-landmark, i-lucide-bike, i-lucide-utensils, i-lucide-person-standing, i-lucide-camera, i-lucide-beach, i-lucide-mountain)
- description (string, engaging)
- intensity (Low/Moderate/High)
- intensityColor (blue/yellow/red)
- tags (array of relevant tags)
- reasoning (array of 3-5 clear, logical reasons why this activity is recommended)
- dssScore (integer 0-100, based on weather, preferences, group size, time)

Make sure activities are appropriate for the weather conditions, time of day, and group size. Consider local culture and typical activities in ${location.name}.`

    const response = await fetch('https://api-inference.huggingface.co/models/google/gemma-2b-it', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${OPENAI_API_KEY}`
      },
      body: JSON.stringify({
        inputs: [
          { role: 'system', content: 'You are an expert travel and activity recommendation system. Always respond with valid JSON only.' },
          { role: 'user', content: prompt }
        ],
        temperature: 0.7,
        max_tokens: 2000 // Limit response size
      })
    })

    if (!response.ok) {
      const errorData = await response.text()
      console.error('OpenAI API Error:', response.status, errorData)
      
      if (response.status === 429) {
        addLog('warning', 'Rate limit reached. Waiting 5 seconds before retry...')
        await new Promise(resolve => setTimeout(resolve, 5000))
        // Retry once
        return generateActivitiesWithAI(weather, prefs, groupSz, location)
      }
      
      throw new Error(`AI API error: ${response.status}`)
    }
    
    const data = await response.json()
    let parsedContent
    
    try {
      parsedContent = JSON.parse(data.choices[0].message.content)
    } catch (parseError) {
      console.error('Failed to parse AI response:', data.choices[0].message.content)
      throw new Error('Invalid JSON response from AI')
    }
    
    const activities = parsedContent.activities || parsedContent
    
    if (!Array.isArray(activities)) {
      console.error('AI response is not an array:', activities)
      throw new Error('AI returned invalid format')
    }
    
    addLog('decision', `AI generated ${activities.length} personalized recommendations`)
    return activities
  } catch (error) {
    console.error('AI generation failed:', error)
    addLog('warning', 'AI service unavailable, using fallback recommendations')
    return generateFallbackActivities(weather, prefs, groupSz)
  }
}

function generateFallbackActivities(weather: WeatherData, prefs: string[], groupSz: number): Activity[] {
  const isRainy = weather.dssFlags.some(f => f.label === 'Rain Likely')
  const isHot = weather.temp > 32
  const isCold = weather.temp < 12
  const isIdeal = weather.temp >= 18 && weather.temp <= 28 && !isRainy
  const isEvening = parseInt(selectedTime.value.split(':')[0]) >= 17
  const weights = Object.fromEntries(dssWeights.value.map(w => [w.key, w.value / 100]))
  
  const dssScores = computeDSSScores(weather, prefs, groupSz)
  const wScore = dssScores[0].score

  const all: Activity[] = [
    {
      id: 'hiking', name: 'Nature Hiking', iconName: 'i-lucide-footprints',
      description: 'Explore local trails and immerse yourself in nature. Great for fitness and mental clarity.',
      intensity: 'Moderate', intensityColor: 'yellow', tags: ['outdoor', 'adventure', 'fitness', 'nature'],
      reasoning: [`Temperature ${weather.temp}°C is ${isIdeal ? 'ideal' : 'acceptable'} for hiking`, `${weather.description} — ${isRainy ? 'moderate caution' : 'suitable conditions'}`, `Group of ${groupSz} ${groupSz <= 6 ? 'is perfect' : 'may need splitting'}`, `Weather weight: ${Math.round(weights.weather * 100)}%`],
      dssScore: Math.round((wScore * weights.weather + (prefs.includes('outdoor') ? 90 : 40) * weights.preference + (groupSz <= 8 ? 85 : 55) * weights.social) * 0.8 + (isRainy ? -20 : 0) + (isIdeal ? 15 : 0)),
    },
    {
      id: 'museum', name: 'Museum / Gallery Visit', iconName: 'i-lucide-landmark',
      description: 'Discover art, history, and culture at a local museum or gallery. Weather-proof choice.',
      intensity: 'Low', intensityColor: 'blue', tags: ['indoor', 'cultural', 'educational'],
      reasoning: [isRainy ? 'Rain makes indoor optimal' : 'Weather-independent indoor option', `Cultural pref ${prefs.includes('cultural') ? 'matched ✓' : 'not prioritized'}`, `Group of ${groupSz} fits comfortably`, 'DSS favors indoor when weather score is low'],
      dssScore: Math.round((isRainy ? 90 : 65) * weights.weather + (prefs.includes('cultural') || prefs.includes('indoor') ? 88 : 55) * weights.preference + 80 * weights.social + 75 * weights.time),
    },
    {
      id: 'cycling', name: 'City Cycling Tour', iconName: 'i-lucide-bike',
      description: 'Explore the city on two wheels with scenic routes and hidden local gems.',
      intensity: 'Moderate', intensityColor: 'green', tags: ['outdoor', 'adventure', 'social', 'fitness'],
      reasoning: [`Wind: ${weather.stats[1].value} — ${parseInt(weather.stats[1].value) < 25 ? 'manageable' : 'high wind caution'}`, `${weather.temp}°C — ${isHot ? 'warm, hydrate well' : isCold ? 'cool, dress warmly' : 'comfortable'}`, `Suits group of ${groupSz}`, `Adventure pref ${prefs.includes('adventure') ? 'matched ✓' : 'partial match'}`],
      dssScore: Math.round((isRainy ? 30 : isIdeal ? 88 : 65) * weights.weather + (prefs.includes('outdoor') || prefs.includes('adventure') ? 85 : 55) * weights.preference + (groupSz <= 10 ? 80 : 60) * weights.social + 70 * weights.time),
    },
    {
      id: 'dining', name: 'Local Food Experience', iconName: 'i-lucide-utensils',
      description: 'Sample authentic local cuisine at a food market or restaurant with great atmosphere.',
      intensity: 'Low', intensityColor: 'orange', tags: ['indoor', 'social', 'food', 'relaxed'],
      reasoning: ['Weather-independent — all-conditions activity', `Food pref ${prefs.includes('food') ? 'matched ✓' : 'neutral'}`, `Social dining ideal for ${groupSz} people`, isEvening ? 'Evening — perfect for dinner' : 'Great lunch or brunch timing'],
      dssScore: Math.round(80 * weights.weather + (prefs.includes('food') || prefs.includes('social') ? 90 : 60) * weights.preference + (groupSz <= 12 ? 88 : 70) * weights.social + (isEvening ? 90 : 70) * weights.time),
    },
    {
      id: 'yoga', name: 'Outdoor Yoga / Meditation', iconName: 'i-lucide-person-standing',
      description: 'Connect mind and body in a quiet park spot for a mindful, restorative session.',
      intensity: 'Low', intensityColor: 'violet', tags: ['outdoor', 'solo', 'relaxed', 'wellness'],
      reasoning: [`Conditions ${isIdeal ? '✓ ideal for wellness' : '— weather consideration needed'}`, `Solo/relaxed pref ${prefs.includes('solo') || prefs.includes('relaxed') ? 'matched ✓' : 'not prioritized'}`, `${groupSz <= 4 ? 'Small group — optimal' : 'May feel crowded'}`, `${!isEvening ? 'Morning timing — great ✓' : 'Evening — find a lit park'}`],
      dssScore: Math.round((isIdeal ? 85 : isRainy ? 25 : 60) * weights.weather + (prefs.includes('relaxed') || prefs.includes('solo') ? 88 : 50) * weights.preference + (groupSz <= 6 ? 82 : 50) * weights.social + (!isEvening ? 85 : 65) * weights.time),
    },
  ]

  return all.map(a => ({ ...a, dssScore: Math.max(10, Math.min(99, a.dssScore)) })).sort((a, b) => b.dssScore - a.dssScore)
}

// FIXED: Clothing recommendations with rate limiting and better error handling
async function getClothingRecommendations(weather: WeatherData, activities: Activity[], location: Location): Promise<string[]> {
  // Skip if no API key
  if (!OPENAI_API_KEY || OPENAI_API_KEY === '') {
    return generateFallbackClothing(weather)
  }

  try {
    // Wait for rate limit before making the call
    await waitForRateLimit()
    
    const prompt = `Based on ${weather.temp}°C, ${weather.description}, with ${weather.stats[1].value} wind and ${weather.stats[2].value} rain chance in ${location.name}, for activities like ${activities.slice(0, 3).map(a => a.name).join(', ')}, recommend 5 essential clothing items. Return as JSON array of strings.`
    
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${OPENAI_API_KEY}`
      },
      body: JSON.stringify({
        model: 'gpt-3.5-turbo',
        messages: [
          { role: 'system', content: 'Return only a JSON array of clothing recommendations. Example: ["item1", "item2", "item3"]' },
          { role: 'user', content: prompt }
        ],
        temperature: 0.5,
        max_tokens: 300
      })
    })
    
    if (!response.ok) {
      if (response.status === 429) {
        addLog('warning', 'Rate limit for clothing recommendations, using fallback')
        return generateFallbackClothing(weather)
      }
      throw new Error(`Clothing API error: ${response.status}`)
    }
    
    const data = await response.json()
    let clothing
    
    try {
      clothing = JSON.parse(data.choices[0].message.content)
    } catch (parseError) {
      console.error('Failed to parse clothing response:', data.choices[0].message.content)
      return generateFallbackClothing(weather)
    }
    
    if (Array.isArray(clothing) && clothing.length > 0) {
      addLog('info', `Clothing recommendations generated: ${clothing.slice(0, 3).join(', ')}...`)
      return clothing
    }
    
    return generateFallbackClothing(weather)
  } catch (error) {
    console.error('Clothing AI failed:', error)
    return generateFallbackClothing(weather)
  }
}

function generateFallbackClothing(weather: WeatherData): string[] {
  const clothing = []
  if (weather.temp < 10) clothing.push('Warm jacket', 'Thermal layers', 'Scarf and gloves')
  else if (weather.temp < 20) clothing.push('Light jacket', 'Long sleeves', 'Comfortable pants')
  else if (weather.temp < 30) clothing.push('Breathable t-shirt', 'Shorts or light pants', 'Sun hat')
  else clothing.push('Light and breathable clothing', 'Sun protection', 'Hydration pack')
  
  if (weather.dssFlags.some(f => f.label === 'Rain Likely')) clothing.push('Waterproof jacket', 'Umbrella')
  if (parseInt(weather.stats[1].value) > 20) clothing.push('Windbreaker')
  if (parseInt(weather.stats[3].value) > 5) clothing.push('Sunscreen', 'Sunglasses')
  
  return clothing.slice(0, 5) // Return max 5 items
}

async function runAdvisor() {
  if (!selectedLocation.value) return
  analyzing.value = true
  results.value = null
  selectedActivity.value = null
  dssLog.value = []
  showLog.value = false
  loadingStep.value = 0
  
  const loc = selectedLocation.value
  addLog('info', `DSS analysis: ${loc.name}`)
  addLog('info', `${selectedDate.value} ${selectedTime.value} | Group: ${groupSize.value} | Prefs: ${selectedPrefs.value.join(', ')}`)

  for (let i = 0; i < loadingMessages.length; i++) {
    loadingMsg.value = loadingMessages[i]
    loadingStep.value = i
    if (i === 0) addLog('decision', 'Fetching weather via Open-Meteo...')
    if (i === 1) addLog('decision', 'Running multi-criteria scoring...')
    if (i === 2) addLog('decision', 'Applying decision weights...')
    if (i === 3) addLog('info', 'Compiling ranked results...')
    await new Promise(r => setTimeout(r, 650))
  }

  const [weather, hourly] = await Promise.all([fetchWeather(loc.lat, loc.lon), fetchHourly(loc.lat, loc.lon)])
  addLog('decision', `Weather: ${weather.temp}°C — ${weather.description}`)
  
  const dssScores = computeDSSScores(weather, selectedPrefs.value, groupSize.value)
  
  // Reset rate limit counter for fresh start
  lastApiCall = 0
  
  // Generate activities (with fallback if AI fails)
  let activities: Activity[]
  if (OPENAI_API_KEY && OPENAI_API_KEY !== '') {
    addLog('info', 'Attempting to generate AI recommendations...')
    activities = await generateActivitiesWithAI(weather, selectedPrefs.value, groupSize.value, loc)
    activities = activities.map(a => ({ ...a, dssScore: Math.max(10, Math.min(99, a.dssScore || 50)) }))
  } else {
    addLog('warning', 'No API key, using rule-based recommendations')
    activities = generateFallbackActivities(weather, selectedPrefs.value, groupSize.value)
  }
  
  // Get clothing recommendations (will auto-fallback if rate limited)
  const clothingRecs = await getClothingRecommendations(weather, activities, loc)
  
  // Add clothing recommendations to the top activity's reasoning
  if (activities[0] && clothingRecs.length > 0) {
    activities[0].reasoning.push(`Clothing recommendation: ${clothingRecs.join(', ')}`)
  }
  
  dssWeights.value.forEach(w => addLog('info', `Weight — ${w.label}: ${w.value}%`))
  addLog('decision', `Top pick: ${activities[0].name} (${activities[0].dssScore})`)
  addLog('decision', `Complete — ${activities.length} activities ranked`)

  results.value = { location: loc, weather, activities, dssScores, hourly }
  analyzing.value = false
  selectedActivity.value = activities[0]
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
  lastApiCall = 0 // Reset rate limit timer
}

onMounted(() => {
  selectedDate.value = new Date().toISOString().split('T')[0]
  const now = new Date()
  selectedTime.value = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`
  
  // Check API key status
  if (!OPENAI_API_KEY || OPENAI_API_KEY === '') {
    console.warn('OpenAI API key not found. The app will use fallback recommendations.')
    addLog('warning', 'OpenAI API key not configured. Using fallback recommendations.')
  } else {
    console.log('OpenAI API key configured successfully')
  }
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