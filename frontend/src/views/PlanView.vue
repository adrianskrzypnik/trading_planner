<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-3xl mx-auto p-6">
      <header class="mb-8">
        <h1 class="text-3xl font-bold text-gray-800">Create Workout Plan</h1>
        <p class="text-gray-500 mt-2">Design your custom training routine</p>
      </header>

      <div class="bg-white rounded-xl shadow-md p-6 mb-6">
        <label for="plan-title" class="block text-sm font-medium text-gray-700 mb-2">Plan Title</label>
        <input
          id="plan-title"
          v-model="planTitle"
          type="text"
          placeholder="e.g., Upper Body Strength, Leg Day, Full Body Workout"
          class="w-full p-3 bg-gray-50 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
        />
      </div>

      <div class="mb-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold text-gray-800">Exercises</h2>
          <span class="bg-emerald-100 text-emerald-800 text-xs font-medium px-2.5 py-1 rounded-full">
            {{ exercises.length }} exercises
          </span>
        </div>

        <div v-for="(exercise, index) in exercises" :key="index"
          class="bg-white rounded-xl shadow-sm p-5 mb-4 border-l-4 border-emerald-500 transition-all hover:shadow-md">
          <div class="flex justify-between items-center mb-4">
            <h3 class="font-bold text-gray-800">Exercise {{ index + 1 }}</h3>
            <button
              @click="removeExercise(index)"
              class="text-red-500 hover:text-red-700 focus:outline-none transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
              </svg>
            </button>
          </div>

          <div class="mb-4">
            <label class="block text-xs font-medium text-gray-500 mb-1">Exercise Name</label>
            <input
              v-model="exercise.name"
              type="text"
              placeholder="e.g., Bench Press, Squats, Pull-ups"
              class="w-full p-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Sets</label>
              <input
                v-model.number="exercise.sets"
                type="number"
                min="1"
                placeholder="Sets"
                class="w-full p-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Reps</label>
              <input
                v-model.number="exercise.repetitions"
                type="number"
                min="1"
                placeholder="Reps"
                class="w-full p-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>
      </div>

      <div class="flex flex-wrap gap-4 mt-6">
        <button
          @click="addExercise"
          class="px-5 py-2.5 bg-gray-200 text-gray-800 font-medium rounded-lg hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-300 focus:ring-offset-2 transition-colors flex items-center"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
          </svg>
          Add Exercise
        </button>

        <button
          @click="submitPlan"
          :disabled="!planTitle || exercises.some(e => !e.name) || exercises.length === 0"
          class="px-5 py-2.5 bg-emerald-600 text-white font-medium rounded-lg shadow-sm hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"></path>
          </svg>
          Save Plan
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import axios from 'axios'

const planTitle = ref('')
const exercises = ref([
  { name: '', sets: 3, repetitions: 10 },
])

const addExercise = () => {
  exercises.value.push({ name: '', sets: 3, repetitions: 10 })
}

const removeExercise = (index: number) => {
  exercises.value.splice(index, 1)
}

const submitPlan = async () => {
  try {
    await axios.post('/api/plans/', {
      title: planTitle.value,
      exercises: exercises.value,
    })

    // Show success notification
    const notification = document.createElement('div')
    notification.className = 'fixed bottom-4 right-4 bg-emerald-500 text-white px-6 py-3 rounded-lg shadow-lg'
    notification.textContent = 'Workout plan saved successfully!'
    document.body.appendChild(notification)

    setTimeout(() => {
      document.body.removeChild(notification)
    }, 3000)

    // Reset form
    planTitle.value = ''
    exercises.value = [{ name: '', sets: 3, repetitions: 10 }]
  } catch (err) {
    console.error(err)
    alert('Error saving plan.')
  }
}
</script>