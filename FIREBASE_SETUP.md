# Configuración de Firebase - Tekams Jump

## ✅ Cambios implementados

### 1. **Scripts de Firebase agregados**
- `firebase-app-compat.js`
- `firebase-database-compat.js`

### 2. **Funciones de sincronización**
- `normalizeProjs()` - Convierte objetos Firebase a arrays
- `setupRealtimeListeners()` - Escucha cambios en tiempo real
- `load()` - Carga datos desde Firebase
- `save()` - Guarda datos en Firebase

### 3. **UI Mejorada**
- ✅ Flecha (chevron) para expandir/contraer proyectos en el dashboard
- ✅ Detalles del proyecto se pueden ocultar/mostrar

---

## 🔧 FALTA: Actualizar credenciales de Firebase

El archivo está en: `tekams_firebase.html` líneas **784-791**

### Busca esto en tu código:
```javascript
var firebaseConfig = {
  apiKey: "AIzaSyDMKVZ94PczVzXLfX-N3o7gK7G3q-5YJmQ",
  authDomain: "tekams-jump-22a0a.firebaseapp.com",
  databaseURL: "https://tekams-jump-22a0a-default-rtdb.europe-west1.firebasedatabase.app",
  projectId: "tekams-jump-22a0a",
  storageBucket: "tekams-jump-22a0a.appspot.com",
  messagingSenderId: "959619851851",
  appId: "1:959619851851:web:e4c5dfe1bde3be73985d13"
};
```

### Debes reemplazarlo con tus credenciales reales

**¿Dónde obtenerlas?**
1. Ve a [console.firebase.google.com](https://console.firebase.google.com)
2. Selecciona tu proyecto
3. Ve a **Configuración del proyecto** (rueda de engranaje)
4. Copia las credenciales de **Configuración de tu aplicación web**

---

## 🧪 Cómo probar

1. **Actualiza las credenciales** en el archivo
2. **Abre en navegador**: `tekams_firebase.html`
3. **Crea un proyecto** nuevo
4. **Abre en incógnito** y verifica que aparezca el proyecto (sincronización real-time)

---

## 📝 Resumen de cambios

| Función | Antes | Después |
|---------|-------|---------|
| `load()` | Solo localStorage | Firebase + localStorage |
| `save()` | Solo localStorage | Firebase + localStorage |
| Dashboard | Sin toggle | Con flecha expandir/contraer |
| Sincronización | NO | SÍ (real-time) |

