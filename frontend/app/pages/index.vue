<template>
    <div class="min-h-screen bg-gradient-to-br from-slate-50 to-white overflow-hidden relative">
      <!-- Animated Background Elements -->
      <div class="absolute inset-0 overflow-hidden">
        <!-- Floating Clouds -->
        <div class="cloud cloud-1 absolute w-32 h-16 bg-white/30 rounded-full blur-md"></div>
        <div class="cloud cloud-2 absolute w-24 h-12 bg-white/20 rounded-full blur-sm"></div>
        <div class="cloud cloud-3 absolute w-40 h-20 bg-white/15 rounded-full blur-md"></div>
        
        <!-- Animated Rain Drops -->
        <div class="raindrop raindrop-1 absolute w-1 h-6 bg-blue-400 rounded-full opacity-50"></div>
        <div class="raindrop raindrop-2 absolute w-1 h-4 bg-blue-300 rounded-full opacity-40"></div>
        <div class="raindrop raindrop-3 absolute w-1 h-5 bg-blue-300 rounded-full opacity-45"></div>
        <div class="raindrop raindrop-4 absolute w-1 h-7 bg-blue-400 rounded-full opacity-55"></div>
        <div class="raindrop raindrop-5 absolute w-1 h-4 bg-blue-300 rounded-full opacity-35"></div>
      </div>
  
      <!-- Hero Section -->
      <main class="relative z-10 flex items-center justify-center min-h-screen px-6">
        <div class="text-center max-w-6xl mx-auto">
          <!-- Main Title with Animation -->
          <h1 class="text-6xl md:text-8xl font-bold text-gray-900 drop-shadow-sm mb-6 animate-fade-in-up">
            Will It Rain On 
            <span class="text-blue-300">
              My Parade?
            </span>
          </h1>
  
          <!-- Subtitle -->
          <p class="text-xl md:text-2xl text-gray-700 mb-8 animate-fade-in-up animation-delay-300 leading-relaxed">
            Leverage NASA Earth observation data to predict weather patterns<br/>
            and never let unpredictable weather ruin your outdoor events again.
          </p>
  
          <!-- Feature Icons -->
          <div class="flex justify-center space-x-8 mb-12 animate-fade-in-up animation-delay-600">
            <div class="text-center transform hover:scale-110 transition-all duration-300 hover:text-blue-500">
              <div class="text-4xl mb-2">🌧️</div>
              <div class="text-sm text-gray-700">Rain Prediction</div>
            </div>
            <div class="text-center transform hover:scale-110 transition-all duration-300 hover:text-blue-500">
              <div class="text-4xl mb-2">❄️</div>
              <div class="text-sm text-gray-700">Snow Forecast</div>
            </div>
            <div class="text-center transform hover:scale-110 transition-all duration-300 hover:text-blue-500">
              <div class="text-4xl mb-2">☀️</div>
              <div class="text-sm text-gray-700">Temperature</div>
            </div>
            <div class="text-center transform hover:scale-110 transition-all duration-300 hover:text-blue-500">
              <div class="text-4xl mb-2">💨</div>
              <div class="text-sm text-gray-700">Wind Speed</div>
            </div>
            <div class="text-center transform hover:scale-110 transition-all duration-300 hover:text-blue-500">
              <div class="text-4xl mb-2">☁️</div>
              <div class="text-sm text-gray-700">Cloud Cover</div>
            </div>
          </div>
  
          <!-- CTA Buttons -->
          <div class="flex flex-col sm:flex-row gap-4 justify-center animate-fade-in-up animation-delay-900">
            <NuxtLink 
              to="/dashboard"
              class="px-8 py-4 bg-blue-600 text-white font-semibold rounded-lg text-lg transition-colors duration-300 hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-300"
            >
              Go to Dashboard
            </NuxtLink>
          </div>
  
          <!-- NASA Attribution -->
          <div class="mt-12 animate-fade-in-up animation-delay-1200">
            <p class="text-gray-700 text-sm">
              Powered by 🛰️ <span class="font-semibold text-gray-900">NASA Earth Science Data</span>
            </p>
            <div class="flex justify-center mt-4 space-x-6 text-gray-700">
              <div class="flex items-center">
                <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse mr-2"></div>
                Real-time Satellite Data
              </div>
              <div class="flex items-center">
                <div class="w-2 h-2 bg-blue-400 rounded-full animate-pulse mr-2"></div>
                Historical Pattern Analysis
              </div>
              <div class="flex items-center">
                <div class="w-2 h-2 bg-purple-400 rounded-full animate-pulse mr-2"></div>
                Location-Specific Predictions
              </div>
            </div>
          </div>
        </div>
      </main>
  
      <!-- Challenge Info Section -->
      <section id="challenge" class="relative z-10 py-20 px-6 bg-white/80 backdrop-blur-sm border-t border-gray-200">
        <div class="max-w-4xl mx-auto text-center">
          <h2 class="text-4xl font-bold text-gray-900 mb-8">NASA Space Apps Challenge 2025</h2>
          <p class="text-xl text-gray-700 leading-relaxed">
            This application was developed as part of the NASA Space Apps Challenge, 
            utilizing open Earth observation datasets to solve real-world problems. 
            Our mission: help you plan outdoor events with confidence, knowing the weather won't surprise you.
          </p>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12">
            <div class="bg-white rounded-lg p-6 border border-gray-200 shadow-sm transform hover:scale-[1.02] transition-all duration-300">
              <h3 class="text-xl font-semibold text-gray-900 mb-3">📊 Data-Driven</h3>
              <p class="text-gray-700">Historical weather patterns analyzed through NASA's comprehensive datasets</p>
            </div>
            <div class="bg-white rounded-lg p-6 border border-gray-200 shadow-sm transform hover:scale-[1.02] transition-all duration-300">
              <h3 class="text-xl font-semibold text-gray-900 mb-3">🎯 Location-Specific</h3>
              <p class="text-gray-700">Precise predictions tailored to your exact event location and date</p>
            </div>
            <div class="bg-white rounded-lg p-6 border border-gray-200 shadow-sm transform hover:scale-[1.02] transition-all duration-300">
              <h3 class="text-xl font-semibold text-gray-900 mb-3">🔮 Probabilistic</h3>
              <p class="text-gray-700">Statistical probability models for informed decision making</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  </template>
  
  <style>
  /* Custom Animations */
  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(30px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  @keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
  }
  
  @keyframes drift {
    0% { transform: translateX(-100px); }
    100% { transform: translateX(calc(100vw + 100px)); }
  }
  
  @keyframes rain {
    0% { transform: translateY(-100px); opacity: 0; }
    10% { opacity: 1; }
    90% { opacity: 1; }
    100% { transform: translateY(calc(100vh + 100px)); opacity: 0; }
  }
  
  .animate-fade-in-up {
    animation: fadeInUp 0.8s ease-out forwards;
  }
  
  .animation-delay-300 {
    animation-delay: 0.3s;
    opacity: 0;
  }
  
  .animation-delay-600 {
    animation-delay: 0.6s;
    opacity: 0;
  }
  
  .animation-delay-900 {
    animation-delay: 0.9s;
    opacity: 0;
  }
  
  .animation-delay-1200 {
    animation-delay: 1.2s;
    opacity: 0;
  }
  
  /* Cloud Animations */
  .cloud {
    animation: drift 20s linear infinite;
  }
  
  .cloud-1 {
    top: 15%;
    animation-duration: 25s;
    animation-delay: 0s;
  }
  
  .cloud-2 {
    top: 25%;
    animation-duration: 30s;
    animation-delay: -10s;
  }
  
  .cloud-3 {
    top: 35%;
    animation-duration: 22s;
    animation-delay: -15s;
  }
  
  /* Raindrop Animations */
  .raindrop {
    animation: rain 3s linear infinite;
  }
  
  .raindrop-1 {
    left: 10%;
    animation-delay: 0s;
    animation-duration: 2.5s;
  }
  
  .raindrop-2 {
    left: 25%;
    animation-delay: 0.5s;
    animation-duration: 3s;
  }
  
  .raindrop-3 {
    left: 45%;
    animation-delay: 1s;
    animation-duration: 2.8s;
  }
  
  .raindrop-4 {
    left: 65%;
    animation-delay: 1.5s;
    animation-duration: 3.2s;
  }
  
  .raindrop-5 {
    left: 85%;
    animation-delay: 2s;
    animation-duration: 2.7s;
  }
  
  /* Responsive Adjustments */
  @media (max-width: 768px) {
    .cloud {
      display: none;
    }
    
    .raindrop {
      display: none;
    }
  }
  </style>
