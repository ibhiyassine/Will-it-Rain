<template>
    <div class="flex flex-col h-screen w-screen bg-gradient-to-br from-slate-50 to-white overflow-hidden">
        <!-- Header -->
        <header class="flex w-full h-16 justify-between items-center px-6 bg-white/80 backdrop-blur-sm border-b border-gray-200">
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"></path>
                    </svg>
                </div>
                <h1 class="text-xl font-semibold text-gray-900">Will It Rain?</h1>
                <span class="text-sm text-gray-500">NASA Space Apps Challenge</span>
            </div>

            <nav class="flex items-center gap-2">
                <NuxtLink href="/" class="inline-flex items-center gap-2 text-sm text-gray-700 hover:text-gray-900 px-3 py-2 rounded-lg border border-gray-200 bg-white hover:shadow-md transition-all">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0h6"></path></svg>
                    Home
                </NuxtLink>
            </nav>
        </header>

        <!-- Main Content -->
        <section class="flex flex-1 w-full p-4 md:p-6 gap-4 md:gap-6 overflow-hidden">
            <!-- Controls Panel -->
            <section class="flex flex-col h-full w-80 bg-white/80 backdrop-blur-sm rounded-2xl border border-gray-200 shadow-xl overflow-hidden text-gray-800">
                <div class="flex-1 min-h-0 overflow-auto p-6 space-y-5">
                    <!-- Location Input (bound to map) -->
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Selected Location</label>
                        <div class="relative">
                            <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M11 18a7 7 0 100-14 7 7 0 000 14z"/></svg>
                            </span>
                            <input
                                v-model="locationText"
                                type="text"
                                readonly
                                class="w-full bg-white rounded-lg pl-9 pr-3 py-2 border border-gray-200 text-gray-700 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-500 transition pointer-events-none"
                            />
                        </div>
                    </div>

                    <!-- Activities Dropdown (now above calendar) -->
                    <div>
                        <h3 class="text-sm font-medium text-gray-700 mb-2">Planned Activity</h3>
                        <div class="relative">
                            <button type="button" @click="activitiesOpen = !activitiesOpen" class="w-full bg-white/60 border border-gray-200 rounded-lg px-3 py-2 flex items-center justify-between text-left">
                                <span class="text-sm text-gray-700 truncate">{{ selectedActivityLabel }}</span>
                                <span class="text-gray-500 transition-transform" :class="{ 'rotate-180': activitiesOpen }">▾</span>
                            </button>
                            <!-- Dropdown opens downward -->
                            <div v-if="activitiesOpen" class="absolute z-30 left-0 right-0 mt-2 bg-white border border-gray-200 rounded-xl shadow-xl p-1 max-h-56 overflow-auto">
                                <ul class="py-1">
                                    <li v-for="a in activities" :key="a.value">
                                        <button type="button" @click="selectActivity(a.value)" class="w-full text-left px-3 py-2 text-sm hover:bg-gray-50 text-gray-800 rounded">
                                            {{ a.label }}
                                        </button>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>

                    <!-- Calendar Section -->
                    <div class="min-h-0">
                        <h3 class="text-sm font-medium text-gray-700 mb-2">Select Date Range</h3>
                        <div class="bg-white rounded-xl p-4 border border-gray-200 shadow-sm">
                            <RangeCalendar 
                                v-model="dateRange"
                                :min-value="minDate"
                                :max-value="maxDate"
                                class="w-full"
                            />
                        </div>
                    </div>
                </div>
            </section>

            <!-- Map Section -->
            <section class="flex flex-1 h-full overflow-hidden">
                <div class="w-full h-full rounded-2xl overflow-hidden shadow-2xl border border-gray-200 bg-white/50 backdrop-blur-sm">
                    <ClientOnly>
                        <Map @location-change="onLocationChange" />
                    </ClientOnly>
                </div>
            </section>
        </section>

        <!-- Chatbot Verdict Panel -->
        <footer class="flex w-full bg-white/90 backdrop-blur-sm border-t border-gray-200">
            <div class="flex items-center gap-5 w-full px-6 py-5 min-h-28">
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center shadow-md">
                    <svg class="w-6 h-6 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M21 15a4 4 0 01-4 4H8l-5 3V8a4 4 0 014-4h10a4 4 0 014 4v7z" />
                    </svg>
                </div>
                <div class="flex-1 min-w-0">
                    <div class="flex items-center gap-3 mb-1">
                        <span class="text-base font-semibold text-gray-900 tracking-tight">Assistant Verdict</span>
                        <span class="text-xs text-gray-500">Live updates from your selections</span>
                    </div>
                    <div class="text-base text-gray-800 leading-relaxed flex items-center min-h-[1.75rem]">
                        <template v-if="isPreparing">
                            <div class="verdict-loader">
                                <span class="verdict-dot verdict-dot--lg" style="animation-delay:-0.24s"></span>
                                <span class="verdict-dot verdict-dot--lg" style="animation-delay:-0.12s"></span>
                                <span class="verdict-dot verdict-dot--lg"></span>
                            </div>
                        </template>
                        <template v-else>
                            {{ verdictText }}
                        </template>
                    </div>
                </div>
            </div>
        </footer>
    </div>
</template>

<script setup>
    import { ref, computed } from 'vue'
    import RangeCalendar from '~/components/ui/range-calendar/RangeCalendar.vue'
    import Map from '~/components/Map.vue'
    import { today, getLocalTimeZone, fromDate } from '@internationalized/date'

    definePageMeta({
        middleware: 'auth',
    })

    // Reactive data
    const tz = getLocalTimeZone()
    const start = today(tz)
    const jsEnd = new Date()
    jsEnd.setDate(jsEnd.getDate() + 7)
    const dateRange = ref({
        start,
        end: fromDate(jsEnd, tz),
    })

    const minDate = ref(start)
    const jsMax = new Date()
    jsMax.setMonth(jsMax.getMonth() + 6)
    const maxDate = ref(fromDate(jsMax, tz))

    const locationText = ref('Select a location on the map')
    const selectedCoords = ref({ lat: null, lng: null })

    const activities = ref([
        { label: 'Outdoor Concert', value: 'concert' },
        { label: 'Hiking', value: 'hiking' },
        { label: 'Picnic', value: 'picnic' },
        { label: 'Marathon', value: 'marathon' },
        { label: 'Soccer Match', value: 'soccer' },
        { label: 'Photography', value: 'photography' },
    ])
    const selectedActivity = ref('')
    const activitiesOpen = ref(false)
    const selectedActivityLabel = computed(() => {
        if (!selectedActivity.value) return 'Select activity'
        return activities.value.find(a => a.value === selectedActivity.value)?.label || selectedActivity.value
    })

    const selectActivity = (value) => {
        selectedActivity.value = value
        activitiesOpen.value = false
    }

    const verdictText = computed(() => {
        const hasLocation = !!locationText.value && locationText.value !== 'Select a location on the map'
        const hasDates = !!dateRange.value?.start && !!dateRange.value?.end
        const hasActivities = !!selectedActivity.value

        if (!hasLocation) return 'Drop the pin or search for a location to begin.'
        if (!hasDates) return 'Select a date range within the next 6 months.'
        if (!hasActivities) return 'Select at least one activity to tailor the recommendation.'

        const fromStr = dateRange.value.start.toDate(tz).toLocaleDateString()
        const toStr = dateRange.value.end.toDate(tz).toLocaleDateString()
        const actLabel = activities.value.find(a => a.value === selectedActivity.value)?.label || selectedActivity.value
        return `Preparing a verdict for ${actLabel} at ${locationText.value} between ${fromStr} and ${toStr}…`
    })

    const isPreparing = computed(() => {
        const hasLocation = !!locationText.value && locationText.value !== 'Select a location on the map'
        const hasDates = !!dateRange.value?.start && !!dateRange.value?.end
        const hasActivities = !!selectedActivity.value
        return hasLocation && hasDates && hasActivities
    })

    const onLocationChange = ({ lat, lng, address }) => {
        selectedCoords.value = { lat, lng }
        locationText.value = address
    }
</script>
