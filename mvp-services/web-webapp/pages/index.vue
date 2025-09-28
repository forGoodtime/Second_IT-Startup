<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Header -->
    <header class="bg-white shadow-sm">
      <div class="container mx-auto px-4 py-4">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-bold text-gray-800">BvckZ Designer</h1>
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-600">3D Превью</span>
            <button
              v-if="!isAuthenticated"
              @click="showAuthModal = true"
              class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition duration-300"
            >
              Войти
            </button>
            <div v-else class="flex items-center space-x-2">
              <span class="text-sm text-gray-600">{{ user?.email }}</span>
              <button
                @click="logout"
                class="text-sm text-gray-500 hover:text-gray-700"
              >
                Выйти
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto px-4 py-8">
      <!-- 3D Viewer Section -->
      <div class="bg-white rounded-lg shadow-lg p-6 mb-8">
        <h2 class="text-xl font-semibold mb-4">Ваша будущая футболка</h2>
        
        <!-- 3D Cards Layout -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <!-- Left Card -->
          <div class="bg-gray-50 rounded-lg p-6">
            <h3 class="font-medium text-gray-700 mb-4">Левая сторона</h3>
            <div 
              ref="leftCanvas" 
              class="w-full h-48 bg-gradient-to-b from-gray-200 to-gray-300 rounded-lg flex items-center justify-center cursor-pointer"
              @click="selectCard('left')"
            >
              <div class="text-center">
                <div class="w-16 h-16 bg-white rounded-full flex items-center justify-center mx-auto mb-2">
                  <svg class="w-8 h-8 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z"/>
                  </svg>
                </div>
                <p class="text-xs text-gray-500">Дополнительный патч</p>
              </div>
            </div>
            <div class="mt-4">
              <label class="block text-xs font-medium text-gray-700 mb-1">Дизайн</label>
              <select 
                v-model="leftDesign" 
                class="w-full text-sm px-2 py-1 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Без дизайна</option>
                <option value="logo">Логотип</option>
                <option value="pattern">Узор</option>
              </select>
            </div>
          </div>

          <!-- Center Card (Main) -->
          <div class="bg-blue-50 rounded-lg p-6 border-2 border-blue-200">
            <h3 class="font-medium text-blue-700 mb-4">Основная футболка</h3>
            <div 
              ref="centerCanvas" 
              class="w-full h-48 bg-gradient-to-b from-blue-400 to-blue-600 rounded-lg flex items-center justify-center cursor-pointer"
              @click="selectCard('center')"
            >
              <div class="text-center">
                <div class="w-20 h-20 bg-white bg-opacity-20 rounded-full flex items-center justify-center mx-auto mb-2">
                  <svg class="w-10 h-10 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"/>
                  </svg>
                </div>
                <p class="text-xs text-white">Основной дизайн</p>
              </div>
            </div>
            <div class="mt-4">
              <label class="block text-xs font-medium text-gray-700 mb-1">Основной цвет</label>
              <select 
                v-model="centerColor" 
                class="w-full text-sm px-2 py-1 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
              >
                <option value="blue">Синий</option>
                <option value="green">Зелёный</option>
                <option value="red">Красный</option>
                <option value="black">Чёрный</option>
              </select>
            </div>
          </div>

          <!-- Right Card -->
          <div class="bg-gray-50 rounded-lg p-6">
            <h3 class="font-medium text-gray-700 mb-4">Правая сторона</h3>
            <div 
              ref="rightCanvas" 
              class="w-full h-48 bg-gradient-to-b from-amber-200 to-amber-400 rounded-lg flex items-center justify-center cursor-pointer"
              @click="selectCard('right')"
            >
              <div class="text-center">
                <div class="w-16 h-16 bg-white bg-opacity-50 rounded-full flex items-center justify-center mx-auto mb-2">
                  <svg class="w-8 h-8 text-amber-700" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"/>
                  </svg>
                </div>
                <p class="text-xs text-amber-700">Национальный орнамент</p>
              </div>
            </div>
            <div class="mt-4">
              <label class="block text-xs font-medium text-gray-700 mb-1">Орнамент</label>
              <select 
                v-model="rightPattern" 
                class="w-full text-sm px-2 py-1 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Без орнамента</option>
                <option value="kazakh">Казахский</option>
                <option value="uzbek">Узбекский</option>
                <option value="kyrgyz">Киргизский</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Controls -->
        <div class="flex flex-wrap justify-between items-center gap-4">
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-600">Выбрано: {{ selectedCard || 'Нет' }}</span>
            <button
              @click="rotateView"
              class="text-sm bg-gray-200 text-gray-700 px-3 py-1 rounded hover:bg-gray-300 transition duration-300"
            >
              Повернуть
            </button>
          </div>
          <div class="flex items-center space-x-2">
            <button
              @click="resetDesign"
              class="text-sm bg-gray-200 text-gray-700 px-3 py-1 rounded hover:bg-gray-300 transition duration-300"
            >
              Сбросить
            </button>
            <button
              @click="saveDesign"
              :disabled="!isAuthenticated"
              class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition duration-300"
            >
              Сохранить дизайн
            </button>
          </div>
        </div>
      </div>

      <!-- Order Form -->
      <div v-if="isAuthenticated" class="bg-white rounded-lg shadow-lg p-6">
        <h2 class="text-xl font-semibold mb-4">Создать заказ</h2>
        <form @submit.prevent="createOrder" class="space-y-4">
          <div class="grid md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Количество вещей для сдачи
              </label>
              <select 
                v-model="orderForm.itemsCount"
                class="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
              >
                <option value="3">3-4 футболки</option>
                <option value="5">5-6 футболок</option>
                <option value="7">7+ футболок</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Способ передачи
              </label>
              <select 
                v-model="orderForm.pickupMethod"
                class="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
              >
                <option value="courier">Курьер</option>
                <option value="drop_point">Пункт приёма</option>
              </select>
            </div>
          </div>
          <div v-if="orderForm.pickupMethod === 'courier'">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Адрес для курьера
            </label>
            <textarea
              v-model="orderForm.address"
              class="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
              rows="3"
              placeholder="Укажите точный адрес и удобное время"
            ></textarea>
          </div>
          <button
            type="submit"
            :disabled="isSubmittingOrder"
            class="w-full bg-green-600 text-white py-2 px-4 rounded hover:bg-green-700 disabled:opacity-50 transition duration-300"
          >
            {{ isSubmittingOrder ? 'Создаём заказ...' : 'Создать заказ' }}
          </button>
        </form>
      </div>
    </main>

    <!-- Auth Modal -->
    <div v-if="showAuthModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg max-w-md w-full mx-4">
        <h3 class="text-lg font-semibold mb-4">{{ authMode === 'login' ? 'Войти' : 'Регистрация' }}</h3>
        <form @submit.prevent="handleAuth" class="space-y-4">
          <div v-if="authMode === 'register'">
            <label class="block text-sm font-medium text-gray-700 mb-1">Имя</label>
            <input
              v-model="authForm.fullName"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              v-model="authForm.email"
              type="email"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Пароль</label>
            <input
              v-model="authForm.password"
              type="password"
              required
              minlength="6"
              class="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div class="flex justify-between items-center">
            <button
              type="button"
              @click="authMode = authMode === 'login' ? 'register' : 'login'"
              class="text-sm text-blue-600 hover:text-blue-800"
            >
              {{ authMode === 'login' ? 'Нет аккаунта? Регистрация' : 'Уже есть аккаунт? Войти' }}
            </button>
          </div>
          <div class="flex space-x-3">
            <button
              type="button"
              @click="showAuthModal = false"
              class="flex-1 bg-gray-200 text-gray-800 py-2 px-4 rounded hover:bg-gray-300 transition duration-300"
            >
              Отмена
            </button>
            <button
              type="submit"
              :disabled="isAuthenticating"
              class="flex-1 bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 disabled:opacity-50 transition duration-300"
            >
              {{ isAuthenticating ? 'Загрузка...' : (authMode === 'login' ? 'Войти' : 'Регистрация') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
// Reactive data
const selectedCard = ref('')
const leftDesign = ref('')
const centerColor = ref('blue')
const rightPattern = ref('')

const showAuthModal = ref(false)
const authMode = ref('login')
const isAuthenticating = ref(false)
const isSubmittingOrder = ref(false)

const authForm = ref({
  email: '',
  password: '',
  fullName: ''
})

const orderForm = ref({
  itemsCount: '5',
  pickupMethod: 'courier',
  address: ''
})

const user = ref(null)
const isAuthenticated = computed(() => !!user.value)

// Canvas refs
const leftCanvas = ref(null)
const centerCanvas = ref(null)
const rightCanvas = ref(null)

// Methods
const selectCard = (card) => {
  selectedCard.value = card
  console.log(`Selected card: ${card}`)
}

const rotateView = () => {
  console.log('Rotating view')
  // Here would be 3D rotation logic
}

const resetDesign = () => {
  leftDesign.value = ''
  centerColor.value = 'blue'
  rightPattern.value = ''
  selectedCard.value = ''
}

const saveDesign = () => {
  if (!isAuthenticated.value) {
    showAuthModal.value = true
    return
  }
  
  const design = {
    left: leftDesign.value,
    center: { color: centerColor.value },
    right: rightPattern.value
  }
  
  console.log('Saving design:', design)
  alert('Дизайн сохранён!')
}

const handleAuth = async () => {
  isAuthenticating.value = true
  
  try {
    const config = useRuntimeConfig()
    const endpoint = authMode.value === 'login' ? '/auth/login' : '/auth/register'
    
    const response = await $fetch(`${config.public.apiBase}${endpoint}`, {
      method: 'POST',
      body: authMode.value === 'login' 
        ? { email: authForm.value.email, password: authForm.value.password }
        : { 
            email: authForm.value.email, 
            password: authForm.value.password, 
            full_name: authForm.value.fullName 
          }
    })
    
    // Store token
    localStorage.setItem('token', response.access_token)
    
    // Get user info
    const userResponse = await $fetch(`${config.public.apiBase}/users/me`, {
      headers: {
        'Authorization': `Bearer ${response.access_token}`
      }
    })
    
    user.value = userResponse
    showAuthModal.value = false
    
    // Reset form
    authForm.value = { email: '', password: '', fullName: '' }
    
  } catch (error) {
    console.error('Auth error:', error)
    alert('Ошибка авторизации. Проверьте данные.')
  } finally {
    isAuthenticating.value = false
  }
}

const logout = () => {
  localStorage.removeItem('token')
  user.value = null
}

const createOrder = async () => {
  isSubmittingOrder.value = true
  
  try {
    const config = useRuntimeConfig()
    const token = localStorage.getItem('token')
    
    // Create donation batch first
    const donationResponse = await $fetch(`${config.public.apiBase}/donations`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: {
        items_count: parseInt(orderForm.value.itemsCount),
        pickup_method: orderForm.value.pickupMethod,
        pickup_address: orderForm.value.address
      }
    })
    
    // Create order with design
    const design = {
      left: leftDesign.value,
      center: { color: centerColor.value },
      right: rightPattern.value
    }
    
    const orderResponse = await $fetch(`${config.public.apiBase}/orders`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: {
        donation_batch_id: donationResponse.id,
        design_metadata: JSON.stringify(design)
      }
    })
    
    alert(`Заказ создан! ID: ${orderResponse.id}`)
    
    // Reset form
    orderForm.value = {
      itemsCount: '5',
      pickupMethod: 'courier',
      address: ''
    }
    
  } catch (error) {
    console.error('Order creation error:', error)
    alert('Ошибка при создании заказа. Попробуйте ещё раз.')
  } finally {
    isSubmittingOrder.value = false
  }
}

// Check for existing token on mount
onMounted(async () => {
  const token = localStorage.getItem('token')
  if (token) {
    try {
      const config = useRuntimeConfig()
      const userResponse = await $fetch(`${config.public.apiBase}/users/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      user.value = userResponse
    } catch (error) {
      console.error('Token validation error:', error)
      localStorage.removeItem('token')
    }
  }
})

// SEO Meta
useSeoMeta({
  title: 'BvckZ Designer - 3D Превью одежды',
  description: 'Создайте уникальный дизайн вашей будущей футболки с 3D превью и национальными орнаментами'
})
</script>
