<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-3xl mx-auto p-6">
      <header class="mb-8">
        <h1 class="text-3xl font-bold text-gray-800">Start New Workout</h1>
        <p class="text-gray-500 mt-2">Select a plan and track your progress</p>
      </header>

      <div class="bg-white rounded-xl shadow-md p-6 mb-6">
        <label class="block text-sm font-medium text-gray-700 mb-2">Select Workout Plan</label>
        <div class="relative">
          <select
            v-model="selectedPlanId"
            @change="loadPlan"
            class="w-full p-3 bg-gray-50 border border-gray-300 rounded-lg appearance-none focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent pr-10"
          >
            <option disabled value="">Choose a workout plan</option>
            <option v-for="plan in workoutPlans" :key="plan.id" :value="plan.id">
              {{ plan.title }}
            </option>
          </select>
          <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-gray-700">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
          </div>
        </div>
      </div>

      <div v-if="sessionExercises.length > 0" class="mb-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold text-gray-800">Exercises</h2>
          <span class="bg-emerald-100 text-emerald-800 text-xs font-medium px-2.5 py-1 rounded-full">
            {{ sessionExercises.length }} exercises
          </span>
        </div>

        <div v-for="(exercise, index) in sessionExercises" :key="index"
          class="bg-white rounded-xl shadow-sm p-5 mb-4 border-l-4 border-emerald-500 transition-all hover:shadow-md">
          <div class="flex justify-between items-center mb-3">
            <h3 class="font-bold text-gray-800">{{ exercise.name }}</h3>
            <span class="text-xs bg-gray-100 px-2 py-1 rounded-full text-gray-600">Exercise {{ index + 1 }}</span>
          </div>

          <div class="grid grid-cols-3 gap-3">
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
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Weight (kg)</label>
              <input
                v-model.number="exercise.weight"
                type="number"
                min="0"
                step="0.5"
                placeholder="Weight"
                class="w-full p-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>
      </div>

      <div v-if="sessionExercises.length === 0 && selectedPlanId" class="flex flex-col items-center justify-center py-10 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
        <svg class="w-12 h-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
        </svg>
        <p class="text-gray-500">No exercises found in this plan</p>
      </div>

      <div class="flex justify-end mt-6">
        <button
          @click="submitWorkout"
          :disabled="sessionExercises.length === 0"
          class="px-6 py-3 bg-emerald-600 text-white font-medium rounded-lg shadow-sm hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          Save Workout
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

interface Plan {
  id: number
  title: string
  exercises: { name: string; sets: number; repetitions: number }[]
}

const workoutPlans = ref<Plan[]>([])
const selectedPlanId = ref<number | ''>('')
const sessionExercises = ref<any[]>([])

const loadPlans = async () => {
  try {
    const { data } = await axios.get('/api/plans/')
    workoutPlans.value = data
  } catch (error) {
    console.error('Failed to load workout plans:', error)
  }
}

const loadPlan = () => {
  const plan = workoutPlans.value.find(p => p.id === selectedPlanId.value)
  if (plan) {
    sessionExercises.value = plan.exercises.map(ex => ({
      name: ex.name,
      sets: ex.sets,
      repetitions: ex.repetitions,
      weight: null
    }))
  } else {
    sessionExercises.value = []
  }
}

const submitWorkout = async () => {
  try {
    await axios.post('/api/sessions/', {
      workout_plan: selectedPlanId.value,
      exercises: sessionExercises.value,
    })

    // Show success notification
    const notification = document.createElement('div')
    notification.className = 'fixed bottom-4 right-4 bg-emerald-500 text-white px-6 py-3 rounded-lg shadow-lg'
    notification.textContent = 'Workout saved successfully!'
    document.body.appendChild(notification)

    setTimeout(() => {
      document.body.removeChild(notification)
    }, 3000)

    // Reset form
    selectedPlanId.value = ''
    sessionExercises.value = []
  } catch (err) {
    console.error(err)
    alert('Error saving workout.')
  }
}

onMounted(loadPlans)
</script>