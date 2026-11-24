<script setup>
import { computed, onMounted, ref } from 'vue'
import { api } from './api'

const token = ref(localStorage.getItem('biblioteca_access'))
const refreshToken = ref(localStorage.getItem('biblioteca_refresh'))
const user = ref(null)
const view = ref('login')
const notice = ref({ type: '', text: '' })
const busy = ref(false)
const authMode = ref('login')
const auth = ref({ email: '', password: '', nombre: '', telefono: '', confirmar_password: '' })
const bookId = ref('')
const book = ref(null)
const bookForm = ref({ titulo: '', autor: '', isbn: '' })
const cover = ref(null)

const isStaff = computed(() => ['admin', 'bibliotecario'].includes(user.value?.rol))
const initials = computed(() => user.value?.nombre?.split(' ').map((part) => part[0]).slice(0, 2).join('').toUpperCase() || 'B')

function show(type, text) { notice.value = { type, text }; setTimeout(() => { notice.value = { type: '', text: '' } }, 4500) }
function clearNotice() { notice.value = { type: '', text: '' } }

async function enter() {
  busy.value = true; clearNotice()
  try {
    if (authMode.value === 'login') {
      const result = await api.login(auth.value.email, auth.value.password)
      token.value = result.access_token; refreshToken.value = result.refresh_token
      localStorage.setItem('biblioteca_access', token.value); localStorage.setItem('biblioteca_refresh', refreshToken.value)
      await loadUser(); view.value = 'dashboard'
    } else {
      await api.register(auth.value); show('success', 'Cuenta creada. Ya puedes iniciar sesión.'); authMode.value = 'login'
    }
  } catch (error) { show('error', error.message) } finally { busy.value = false }
}

async function loadUser() {
  try { user.value = await api.me(token.value) } catch { signOut() }
}

async function findBook() {
  if (!bookId.value) return show('error', 'Escribe el ID del libro que quieres consultar')
  busy.value = true; clearNotice()
  try { book.value = await api.getBook(token.value, bookId.value) } catch (error) { book.value = null; show('error', error.message) } finally { busy.value = false }
}

async function createBook() {
  busy.value = true; clearNotice()
  try { book.value = await api.createBook(token.value, bookForm.value); bookForm.value = { titulo: '', autor: '', isbn: '' }; show('success', 'Libro agregado al catálogo') } catch (error) { show('error', error.message) } finally { busy.value = false }
}

async function uploadCover() {
  if (!cover.value || !book.value) return
  busy.value = true
  try { book.value = await api.uploadCover(token.value, book.value.id, cover.value); cover.value = null; show('success', 'Portada actualizada') } catch (error) { show('error', error.message) } finally { busy.value = false }
}

function signOut() { token.value = null; user.value = null; book.value = null; localStorage.removeItem('biblioteca_access'); localStorage.removeItem('biblioteca_refresh'); view.value = 'login' }

onMounted(async () => { if (token.value) { await loadUser(); if (user.value) view.value = 'dashboard' } })
</script>

<template>
  <main class="app-shell">
    <section v-if="view === 'login'" class="auth-layout">
      <div class="auth-art">
        <div class="brand"><span class="brand-mark">B</span><span>Biblioteca</span></div>
        <div class="art-copy"><p class="eyebrow">TU ESPACIO DE LECTURA</p><h1>Las historias<br /><em>también</em> construyen hogar.</h1><p>Un catálogo sencillo para volver siempre a los libros que importan.</p></div>
        <div class="quote">“Un libro es un sueño que tienes en la mano.”<small>— Neil Gaiman</small></div>
      </div>
      <div class="auth-panel">
        <div class="mobile-brand brand"><span class="brand-mark">B</span><span>Biblioteca</span></div>
        <div class="auth-card">
          <p class="eyebrow">{{ authMode === 'login' ? 'BIENVENIDO DE VUELTA' : 'ÚNETE A LA COMUNIDAD' }}</p>
          <h2>{{ authMode === 'login' ? 'Entra a tu biblioteca' : 'Crea tu cuenta' }}</h2>
          <p class="muted">{{ authMode === 'login' ? 'Gestiona tus libros desde un solo lugar.' : 'Empieza a descubrir nuevas historias.' }}</p>
          <form @submit.prevent="enter">
            <template v-if="authMode === 'register'"><label>Nombre completo<input v-model="auth.nombre" required minlength="3" placeholder="Tu nombre" /></label><label>Teléfono <span>(opcional)</span><input v-model="auth.telefono" placeholder="300 000 0000" /></label></template>
            <label>Correo electrónico<input v-model="auth.email" required type="email" placeholder="nombre@correo.com" /></label>
            <label>Contraseña<input v-model="auth.password" required type="password" minlength="8" placeholder="Mínimo 8 caracteres" /></label>
            <label v-if="authMode === 'register'">Confirma tu contraseña<input v-model="auth.confirmar_password" required type="password" minlength="8" /></label>
            <button class="button primary full" :disabled="busy">{{ busy ? 'Procesando…' : (authMode === 'login' ? 'Ingresar a mi cuenta' : 'Crear cuenta') }} <span>→</span></button>
          </form>
          <p class="switch">{{ authMode === 'login' ? '¿Aún no tienes cuenta?' : '¿Ya tienes una cuenta?' }} <button @click="authMode = authMode === 'login' ? 'register' : 'login'">{{ authMode === 'login' ? 'Regístrate' : 'Inicia sesión' }}</button></p>
        </div>
      </div>
    </section>

    <section v-else class="dashboard">
      <header class="topbar"><div class="brand"><span class="brand-mark">B</span><span>Biblioteca</span></div><div class="top-actions"><div class="user-chip"><div class="avatar">{{ initials }}</div><div><strong>{{ user?.nombre }}</strong><small>{{ user?.rol }}</small></div></div><button class="icon-button" title="Cerrar sesión" @click="signOut">↪</button></div></header>
      <div class="dashboard-content"><div class="welcome"><div><p class="eyebrow">PANEL DE CONTROL</p><h1>Hola, {{ user?.nombre?.split(' ')[0] }} <span>✦</span></h1><p class="muted">Todo lo que necesitas para cuidar tu biblioteca.</p></div><div class="date-card"><span>HOY</span><strong>{{ new Date().toLocaleDateString('es-CO', { day: '2-digit', month: 'short' }) }}</strong></div></div>
        <div v-if="notice.text" class="notice" :class="notice.type">{{ notice.text }}</div>
        <div class="stats"><div><span class="stat-icon green">⌕</span><div><strong>Catálogo</strong><small>Consulta libros por ID</small></div></div><div><span class="stat-icon sand">✎</span><div><strong>{{ isStaff ? 'Gestión activa' : 'Cuenta activa' }}</strong><small>{{ isStaff ? 'Permisos de biblioteca' : 'Socio registrado' }}</small></div></div></div>
        <div class="content-grid"><section class="card catalog-card"><div class="card-heading"><div><p class="eyebrow">EXPLORAR</p><h2>Consultar un libro</h2></div><span class="round-icon">⌕</span></div><p class="muted">Consulta los detalles de cualquier libro usando su identificador.</p><form class="search-form" @submit.prevent="findBook"><input v-model="bookId" type="number" min="1" placeholder="Ej. 1" /><button class="button primary" :disabled="busy">Buscar libro <span>→</span></button></form><article v-if="book" class="book-result"><div class="book-cover" :style="book.portada_url ? { backgroundImage: `url(${book.portada_url})` } : {}"><span v-if="!book.portada_url">LIBRO</span></div><div class="book-info"><span class="tag">DISPONIBLE</span><h3>{{ book.titulo }}</h3><p>{{ book.autor }}</p><dl><div><dt>ISBN</dt><dd>{{ book.isbn || 'No registrado' }}</dd></div><div><dt>AÑADIDO</dt><dd>{{ new Date(book.creado_en).toLocaleDateString('es-CO') }}</dd></div></dl></div></article><div v-else class="empty-state"><span>✧</span><p>Tu próximo descubrimiento<br /><small>aparecerá aquí</small></p></div></section>
          <section v-if="isStaff" class="card add-card"><div class="card-heading"><div><p class="eyebrow">ADMINISTRACIÓN</p><h2>Agregar libro</h2></div><span class="round-icon">＋</span></div><p class="muted">Incorpora una nueva historia al catálogo.</p><form @submit.prevent="createBook"><label>Título<input v-model="bookForm.titulo" required placeholder="El nombre del libro" /></label><label>Autor<input v-model="bookForm.autor" required placeholder="Nombre del autor" /></label><label>ISBN <span>(opcional)</span><input v-model="bookForm.isbn" placeholder="978-..." /></label><button class="button dark full" :disabled="busy">Guardar en catálogo <span>→</span></button></form><div v-if="book" class="upload"><label class="file-label">{{ cover ? cover.name : 'Añadir portada (JPG, PNG o WEBP)' }}<input type="file" accept="image/jpeg,image/png,image/webp" @change="cover = $event.target.files[0]" /></label><button v-if="cover" class="button outline full" @click="uploadCover">Subir portada</button></div></section>
          <section v-else class="card read-card"><span class="round-icon">♡</span><p class="eyebrow">TU EXPERIENCIA</p><h2>Lee a tu ritmo.</h2><p class="muted">Explora el catálogo y encuentra tu próxima historia favorita.</p></section>
        </div>
      </div>
    </section>
  </main>
</template>
