<template>
    <div class="relative size-full">
        <ClientOnly>
            <LMap
                class="size-full"
                :zoom="zoom"
                :center="center"
                :use-global-leaflet="true"
                :options="{ zoomControl: false }"
                @ready="onMapReady"
            >
                <LTileLayer
                    url="https://tiles.stadiamaps.com/tiles/alidade_satellite/{z}/{x}/{y}{r}.jpg"
                    attribution='&copy; CNES, Distribution Airbus DS, © Airbus DS, © PlanetObserver (Contains Copernicus Data) | &copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                />

                <LMarker
                    ref="marker"
                    :lat-lng="center"
                    draggable
                    @dragend="onPinDrop"
                />
            </LMap>
        </ClientOnly>
        
        <div class="absolute top-4 right-4 z-[1000] flex flex-col gap-2">
            <button
                @click="zoomIn"
                class="bg-white/90 backdrop-blur-sm hover:bg-white text-gray-700 hover:text-gray-900 border border-gray-200 rounded-md size-9 flex items-center justify-center shadow-lg hover:shadow-md transition-all duration-200 ease-in-out cursor-pointer"
                title="Zoom In"
            >
                <svg class="size-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                </svg>
            </button>
            <button
                @click="zoomOut"
                class="bg-white/90 backdrop-blur-sm hover:bg-white text-gray-700 hover:text-gray-900 border border-gray-200 rounded-md size-9 flex items-center justify-center shadow-lg hover:shadow-md transition-all duration-200 ease-in-out cursor-pointer"
                title="Zoom Out"
            >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 12H6"></path>
                </svg>
            </button>
        </div>
    </div>
</template>

<script setup>
    import 'leaflet-geosearch/dist/geosearch.css'
    import { OpenStreetMapProvider, GeoSearchControl } from 'leaflet-geosearch'
    import { ref } from 'vue'


    const emit = defineEmits(['location-change'])
    const marker = ref(null)
    const map = ref(null)
    const zoom = ref(16)
    const center = ref([32.218726, -7.940312])

    const reverseGeocode = async (lat, lng) => {
        try {
            const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lng}` , {
                headers: { 'Accept': 'application/json' }
            })
            const data = await res.json()
            return data?.display_name || `${lat.toFixed(5)}, ${lng.toFixed(5)}`
        } catch {
            return `${lat.toFixed(5)}, ${lng.toFixed(5)}`
        }
    }

    const onMapReady = (leafletMap) => {
        map.value = leafletMap
        
        leafletMap.addControl(
            new GeoSearchControl({
                provider: new OpenStreetMapProvider(),
                showMarker: true,
            })
        )

        leafletMap.on('geosearch/showlocation', async ({ location }) => {
            center.value = [location.y, location.x]
            const address = await reverseGeocode(location.y, location.x)
            emit('location-change', { lat: location.y, lng: location.x, address })
        })
    }

    const onPinDrop = (e) => {
        const { lat, lng } = e.target.getLatLng()
        center.value = [lat, lng]
        reverseGeocode(lat, lng).then((address) => {
            emit('location-change', { lat, lng, address })
        })
    }

    const zoomIn = () => {
        if (map.value) {
            map.value.zoomIn()
        }
    }

    const zoomOut = () => {
        if (map.value) {
            map.value.zoomOut()
        }
    }
</script>
