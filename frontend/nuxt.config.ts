// https://nuxt.com/docs/api/configuration/nuxt-config

import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
    compatibilityDate: '2025-07-15',
    devtools: { enabled: true },
    modules: ['@nuxt/content', 'shadcn-nuxt', '@nuxtjs/leaflet', '@nuxt-alt/markdown-it'],
    css: ['~/assets/css/main.css'],
    vite: {    
        plugins: [      
            tailwindcss(),
        ],  
    },
    shadcn: {
        /**
     * Prefix for all the imported component
     */
        prefix: '',
        /**
     * Directory that the component lives in.
     * @default "./components/ui"
     */
        componentDir: './app/components/ui',
    },
    markdownit: { runtime: true, linkify: true, breaks: true }, // options forwarded to markdown-it
})
