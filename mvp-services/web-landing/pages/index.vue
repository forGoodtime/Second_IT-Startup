<template>
  <div>
    <!-- Hero Section -->
    <section class="bg-gradient-to-r from-green-400 to-blue-500 text-white">
      <div class="container mx-auto px-4 py-20">
        <div class="max-w-4xl mx-auto text-center">
          <h1 class="text-5xl md:text-6xl font-bold mb-6">
            Превратите старую одежду в уникальные вещи
          </h1>
          <p class="text-xl md:text-2xl mb-8 opacity-90">
            BvckZ — сервис апсайкла одежды с 3D визуализацией и национальными орнаментами
          </p>
          <button 
            @click="scrollToDemo" 
            class="bg-white text-blue-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-100 transition duration-300"
          >
            Попробовать бесплатно
          </button>
        </div>
      </div>
    </section>

    <!-- How it works -->
    <section class="py-20 bg-white">
      <div class="container mx-auto px-4">
        <h2 class="text-4xl font-bold text-center mb-16">Как это работает</h2>
        <div class="grid md:grid-cols-3 gap-8">
          <div class="text-center">
            <div class="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"/>
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">1. Сдайте старые вещи</h3>
            <p class="text-gray-600">Принесите 4-5 футболок в пункт приёма или закажите курьера</p>
          </div>
          <div class="text-center">
            <div class="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3z"/>
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">2. Выберите дизайн</h3>
            <p class="text-gray-600">Создайте уникальный дизайн с орнаментами в 3D редакторе</p>
          </div>
          <div class="text-center">
            <div class="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">3. Получите готовое изделие</h3>
            <p class="text-gray-600">Мы создадим уникальную вещь и доставим её вам</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Demo Section -->
    <section ref="demoSection" class="py-20 bg-gray-50">
      <div class="container mx-auto px-4">
        <h2 class="text-4xl font-bold text-center mb-16">Попробуйте прямо сейчас</h2>
        <div class="max-w-4xl mx-auto">
          <!-- Demo WebApp Preview -->
          <div class="bg-white rounded-lg shadow-xl p-8 mb-8">
            <h3 class="text-2xl font-semibold mb-6 text-center">3D Превью вашей будущей футболки</h3>
            <div class="grid md:grid-cols-3 gap-6">
              <div class="text-center">
                <div class="bg-gray-200 h-48 rounded-lg flex items-center justify-center mb-4">
                  <span class="text-gray-500">Левая сторона</span>
                </div>
                <p class="text-sm text-gray-600">Дополнительный дизайн</p>
              </div>
              <div class="text-center">
                <div class="bg-gradient-to-b from-blue-400 to-blue-600 h-48 rounded-lg flex items-center justify-center mb-4">
                  <span class="text-white font-bold">Основной дизайн</span>
                </div>
                <p class="text-sm text-gray-600">Главная футболка</p>
              </div>
              <div class="text-center">
                <div class="bg-gray-200 h-48 rounded-lg flex items-center justify-center mb-4">
                  <span class="text-gray-500">Правая сторона</span>
                </div>
                <p class="text-sm text-gray-600">Национальный орнамент</p>
              </div>
            </div>
          </div>

          <!-- Order Form -->
          <div class="bg-white rounded-lg shadow-xl p-8">
            <h3 class="text-2xl font-semibold mb-6">Оставьте заявку</h3>
            <form @submit.prevent="submitOrder" class="space-y-6">
              <div class="grid md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Имя
                  </label>
                  <input
                    v-model="form.name"
                    type="text"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Email
                  </label>
                  <input
                    v-model="form.email"
                    type="email"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Количество вещей для сдачи
                </label>
                <select
                  v-model="form.itemsCount"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="3">3-4 футболки</option>
                  <option value="5">5-6 футболок</option>
                  <option value="7">7+ футболок</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Способ передачи вещей
                </label>
                <div class="space-y-2">
                  <label class="flex items-center">
                    <input v-model="form.pickupMethod" type="radio" value="courier" class="mr-2" />
                    Курьер (бесплатно по Алматы)
                  </label>
                  <label class="flex items-center">
                    <input v-model="form.pickupMethod" type="radio" value="drop_point" class="mr-2" />
                    Пункт приёма
                  </label>
                </div>
              </div>
              <div v-if="form.pickupMethod === 'courier'">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Адрес для курьера
                </label>
                <textarea
                  v-model="form.address"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  rows="3"
                  placeholder="Укажите точный адрес и удобное время"
                ></textarea>
              </div>
              <button
                type="submit"
                :disabled="isSubmitting"
                class="w-full bg-blue-600 text-white py-3 px-6 rounded-md hover:bg-blue-700 transition duration-300 disabled:opacity-50"
              >
                {{ isSubmitting ? 'Отправляем...' : 'Оставить заявку' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </section>

    <!-- Success Modal -->
    <div v-if="showSuccess" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-8 rounded-lg max-w-md mx-4">
        <div class="text-center">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-green-600" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h3 class="text-xl font-semibold mb-2">Заявка отправлена!</h3>
          <p class="text-gray-600 mb-6">Мы свяжемся с вами в течение 24 часов</p>
          <button
            @click="showSuccess = false"
            class="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition duration-300"
          >
            Закрыть
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const form = ref({
  name: '',
  email: '',
  itemsCount: '5',
  pickupMethod: 'courier',
  address: ''
})

const isSubmitting = ref(false)
const showSuccess = ref(false)
const demoSection = ref(null)

const scrollToDemo = () => {
  demoSection.value?.scrollIntoView({ behavior: 'smooth' })
}

const submitOrder = async () => {
  isSubmitting.value = true
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Here would be actual API call to create order
    console.log('Form submitted:', form.value)
    
    showSuccess.value = true
    
    // Reset form
    form.value = {
      name: '',
      email: '',
      itemsCount: '5',
      pickupMethod: 'courier',
      address: ''
    }
  } catch (error) {
    console.error('Error submitting form:', error)
    alert('Ошибка при отправке заявки. Попробуйте ещё раз.')
  } finally {
    isSubmitting.value = false
  }
}

// SEO Meta
useSeoMeta({
  title: 'BvckZ - Превратите старую одежду в уникальные вещи',
  ogTitle: 'BvckZ - Сервис апсайкла одежды',
  description: 'Из 4-5 старых футболок создаём 1-2 новые уникальные вещи с кастомным дизайном и национальными орнаментами',
  ogDescription: 'Сервис апсайкла одежды с 3D визуализацией. Эко-логистика, качественное производство, прозрачность процесса.',
  ogImage: '/og-image.jpg'
})
</script>

<style scoped>
/* Additional styles if needed */
</style>
