# 🔥 Tekams con Firebase - Instrucciones

## ✅ Lo que hemos hecho

Tu Tekams ahora está integrado con **Firebase Realtime Database**. Esto significa:

- 📱 **Sincronización en tiempo real** - cuando alguien edita una tarea, todos lo ven al instante
- 👥 **Trabajo colaborativo** - tus 7 compañeros pueden editar simultáneamente
- ☁️ **Datos en la nube** - los datos se guardan en Firebase (y respaldados en localStorage)
- 🔄 **Automático** - no necesitas hacer nada especial, los cambios se sincronizan solos

---

## 🚀 Cómo usar

### **Paso 1: Abre el archivo**
```
tekams_firebase.html
```

**IMPORTANTE:** Abre esto DIRECTAMENTE en el navegador (no desde un servidor):
- ✅ Correcto: `file:///C:/Users/Jose J. Gómez/Desktop/Seguimiento tareas/tekams_firebase.html`
- ✅ También funciona: Arrastra el archivo al navegador

### **Paso 2: Espera la conexión**
Verás en la consola del navegador (F12):
```
🔥 Firebase conectado para usuario: Usuario123456
✅ Sincronización Firebase activada
📤 Primera sincronización - subiendo datos...
```

La primera vez, subirá tus datos actuales a Firebase.

### **Paso 3: Comparte con tu equipo**
Todos deben abrir el mismo archivo `tekams_firebase.html` desde sus PCs.

Cada persona verá automáticamente:
- ✅ Los cambios que hace su compañero en tiempo real
- ✅ Las nuevas tareas
- ✅ Las actualizaciones de estado

---

## 🔧 Configuración

### Cambiar tu nombre de usuario
Por defecto usas un ID aleatorio. Para tener un nombre real:

En el archivo `tekams_firebase.html`, busca esta línea (línea ~25):
```javascript
const ME = localStorage.getItem('me') || 'Usuario' + Math.random().toString(36).substr(2, 9);
```

Cámbiala a:
```javascript
const ME = 'Jose'; // Tu nombre
```

Cada persona hace lo mismo con su nombre.

---

## 🔐 Seguridad (IMPORTANTE - Hazlo después de probar)

**Ahora:** El proyecto está en "modo prueba" - cualquiera puede leer/escribir
**Después:** Necesitamos protegerlo para que solo tu equipo acceda

**Pasos en Firebase Console:**
1. Ve a **Realtime Database** → **Reglas**
2. Reemplaza con esto:
```json
{
  "rules": {
    "datos": {
      ".read": true,
      ".write": true,
      ".indexOn": ["lastUpdate"]
    }
  }
}
```
3. Haz clic en "Publicar"

---

## ✨ Lo que ya sincroniza

- ✅ Todos los proyectos
- ✅ Todas las tareas y subtareas
- ✅ Estado (Pendiente/En curso/Completada)
- ✅ Personas asignadas
- ✅ Fechas y recurrencias
- ✅ Notas
- ✅ Prioridades
- ✅ Enlaces

---

## 🐛 Si algo va mal

### Reinicia la sincronización
Recarga la página (F5) - se sincronizará automáticamente

### Ver logs
Abre la consola (F12) y verás los mensajes:
- 🔥 Firebase conectado
- 📨 Cambios recibidos de [usuario]
- ❌ Errores (si los hay)

### Respaldo
Tus datos siguen guardados en `localStorage` también, así que nunca se pierden

---

## 📈 Próximos pasos

Después de probar, podemos:
1. ✅ Agregar control de tiempo (que también se sincronice)
2. ✅ Agregar notificaciones cuando alguien hace cambios
3. ✅ Historial de cambios
4. ✅ Permisos de usuario (quién puede ver qué)

---

## 🎯 Próxima tarea

1. **Cambia tu nombre** en el archivo (la línea `const ME = ...`)
2. **Abre el archivo** y verifica que ves "Firebase conectado"
3. **Comparte con uno de tu equipo** y haced cambios simultáneos
4. Dime si funciona ✅

---

¿Preguntas? Aquí estoy 👍
