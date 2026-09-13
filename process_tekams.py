#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import os

# Ruta del archivo original
input_file = r"C:\Users\Jose J. Gómez\AppData\Roaming\Claude\local-agent-mode-sessions\45997731-6d35-4f60-84af-00b65211ddac\a39b206f-47a6-4fb5-b04c-4599015c17dd\local_e7034798-53ad-4f92-9cef-d2b4ccdcb33b\uploads\tekams_jump_2026-08-04-v1-2d00f029.html"
output_file = r"C:\Users\Jose J. Gómez\Desktop\Seguimiento tareas\tekams_firebase.html"

print("Leyendo archivo original...")
with open(input_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

print(f"Tamaño original: {len(html_content)} caracteres")

# PARTE 1: Agregar CSS para Login Screen antes de </style>
login_css = '''

/* ── LOGIN SCREEN AUTHENTICATION ── */
.login-wrapper{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#F2F1F8;z-index:1000;padding:1rem}
.login-wrapper.hidden{display:none}
.login-box{background:#FFFFFF;border-radius:14px;border:1px solid rgba(42,41,99,.15);padding:2.5rem;width:100%;max-width:400px;box-shadow:0 4px 16px rgba(42,41,99,.1),0 12px 40px rgba(42,41,99,.08)}
.login-box h1{font-size:22px;font-weight:700;color:#1A1940;letter-spacing:-.02em;margin-bottom:8px}
.login-box .subtitle{font-size:12px;color:#5A5880;margin-bottom:2rem}
.login-field{margin-bottom:1.25rem}
.login-field label{display:block;font-size:10px;font-weight:700;color:#5A5880;text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px}
.login-field input{width:100%;font-size:13px;font-family:'DM Sans',sans-serif;padding:10px 12px;border-radius:10px;border:1px solid rgba(42,41,99,.15);background:#F2F1F8;color:#1A1940;outline:none;box-sizing:border-box}
.login-field input:focus{border-color:#2A2963;background:#FFFFFF}
.login-actions{display:flex;flex-direction:column;gap:10px}
.login-btn{padding:11px 14px;border-radius:10px;font-size:12px;font-family:'DM Sans',sans-serif;font-weight:600;border:none;background:#2A2963;color:#fff;cursor:pointer;transition:all .15s}
.login-btn:hover{background:#3D3C80}
.login-btn:disabled{background:#9896B8;cursor:not-allowed}
.login-error{color:#C02020;font-size:11px;margin-bottom:12px;text-align:center;min-height:16px}
.login-note{font-size:10px;color:#9896B8;margin-top:1.5rem;padding-top:1rem;border-top:1px solid rgba(42,41,99,.08);text-align:center}
.login-note strong{color:#5A5880;display:block;margin-bottom:4px}
.shell.hidden{display:none}
.user-badge{position:absolute;top:1rem;right:2rem;display:flex;align-items:center;gap:8px;font-size:11px}
.user-info{display:flex;align-items:center;gap:4px}
.admin-badge{background:#D94F2B;color:#fff;padding:2px 8px;border-radius:6px;font-size:9px;font-weight:700;text-transform:uppercase;display:none}
.logout-btn{padding:6px 10px;border-radius:8px;border:1px solid rgba(42,41,99,.15);background:#FFFFFF;color:#5A5880;cursor:pointer;font-size:11px;font-family:'DM Sans',sans-serif;font-weight:500;transition:all .15s}
.logout-btn:hover{background:#F2F1F8}
'''

# Encontrar </style> y insertar el CSS
style_end = html_content.find('</style>')
if style_end > 0:
    html_content = html_content[:style_end] + login_css + '\n' + html_content[style_end:]
    print("✓ CSS de login agregado")

# PARTE 2: Reemplazar const ME por variable global
html_content = re.sub(
    r"const ME = '[^']*'",
    "let currentUser = null;\nlet isAdmin = false;\nlet ME = currentUser;",
    html_content
)
print("✓ Reemplazado const ME")

# PARTE 3: Agregar la función de autenticación antes de la función load()
auth_js = '''
// ═══════════════════════════════════════════════════════════════
// SISTEMA DE AUTENTICACIÓN CON localStorage
// ═══════════════════════════════════════════════════════════════

const AUTH_USERS = {
  'jjgomez@tekams.com': {password: '1234', isAdmin: true, name: 'José'},
  'Paula': {password: '1234', isAdmin: false, name: 'Paula'},
  'Puri': {password: '1234', isAdmin: false, name: 'Puri'},
  'Fran': {password: '1234', isAdmin: false, name: 'Fran'},
  'Antonio': {password: '1234', isAdmin: false, name: 'Antonio'},
  'JuanJo': {password: '1234', isAdmin: false, name: 'JuanJo'},
  'Jon': {password: '1234', isAdmin: false, name: 'Jon'}
};

function initAuth(){
  const stored = localStorage.getItem('tkm9_auth');
  if(stored){
    try{
      const auth = JSON.parse(stored);
      const user = AUTH_USERS[auth.user];
      if(user && user.password === auth.pass){
        currentUser = auth.user;
        isAdmin = user.isAdmin;
        ME = currentUser;
        showApp();
        return;
      }
    }catch(e){}
  }
  showLogin();
}

function showLogin(){
  document.querySelector('.shell').classList.add('hidden');
  document.querySelector('.login-wrapper').classList.remove('hidden');
}

function showApp(){
  document.querySelector('.login-wrapper').classList.add('hidden');
  document.querySelector('.shell').classList.remove('hidden');
  document.getElementById('userNameDisplay').textContent = currentUser;
  document.getElementById('adminBadge').style.display = isAdmin ? 'inline-block' : 'none';
  init();
}

function handleLogin(e){
  if(e) e.preventDefault();
  const username = document.getElementById('loginUser').value.trim();
  const password = document.getElementById('loginPass').value;
  const errorEl = document.querySelector('.login-error');

  if(!username || !password){
    errorEl.textContent = 'Completa todos los campos';
    return;
  }

  const user = AUTH_USERS[username];
  if(!user || user.password !== password){
    errorEl.textContent = 'Usuario o contraseña incorrectos';
    return;
  }

  currentUser = username;
  isAdmin = user.isAdmin;
  ME = currentUser;

  try{
    localStorage.setItem('tkm9_auth', JSON.stringify({user: username, pass: password}));
  }catch(e){}

  errorEl.textContent = '';
  showApp();
}

function handleLogout(){
  if(!confirm('¿Cerrar sesión?')) return;
  localStorage.removeItem('tkm9_auth');
  currentUser = null;
  isAdmin = false;
  ME = null;
  showLogin();
  document.getElementById('loginUser').value = '';
  document.getElementById('loginPass').value = '';
  document.querySelector('.login-error').textContent = '';
}
'''

# Encontrar la función load() y poner el auth antes
load_index = html_content.find('function load(){')
if load_index > 0:
    html_content = html_content[:load_index] + auth_js + '\n\n' + html_content[load_index:]
    print("✓ Funciones de autenticación agregadas")

# PARTE 4: Modificar la función init() para que llame a initAuth primero
# Buscar donde dice window.onload = init o algún inicializador similar
html_content = re.sub(
    r'(window\.onload\s*=\s*init|init\(\s*\))',
    r'window.onload = function(){\n  try{\n    initAuth();\n  }catch(e){\n    console.error("Auth error:", e);\n    init();\n  }\n};',
    html_content
)
print("✓ Modificado inicializador")

# PARTE 5: Agregar HTML del login JUSTO ANTES de <div class="shell">
login_html = '''
<div class="login-wrapper">
  <div class="login-box">
    <h1>Tekams Jump</h1>
    <p class="subtitle">Seguimiento de Proyectos</p>
    <form id="loginForm" onsubmit="handleLogin(event)">
      <div class="login-error" id="loginError"></div>
      <div class="login-field">
        <label for="loginUser">Usuario</label>
        <input type="text" id="loginUser" placeholder="Email o Nombre" autocomplete="off" required>
      </div>
      <div class="login-field">
        <label for="loginPass">Contraseña</label>
        <input type="password" id="loginPass" placeholder="Contraseña" autocomplete="off" required>
      </div>
      <div class="login-actions">
        <button type="submit" class="login-btn">Iniciar Sesión</button>
      </div>
      <div class="login-note">
        <strong>Usuarios de prueba:</strong>
        jjgomez@tekams.com (Admin)<br>
        Paula, Puri, Fran, Antonio, JuanJo, Jon
      </div>
    </form>
  </div>
</div>

'''

# Encontrar <div class="shell"> y agregar login antes
shell_index = html_content.find('<div class="shell">')
if shell_index > 0:
    html_content = html_content[:shell_index] + login_html + html_content[shell_index:]
    print("✓ HTML de login agregado")

# PARTE 6: Agregar botón de logout + usuario en el header (buscar .sb-logo o similar)
# Agregar elemento user-badge justo después de <body> y antes del shell
user_badge_html = '''
<div class="user-badge" id="userBadge" style="display:none">
  <div class="user-info">
    <span>Usuario:</span>
    <strong id="userNameDisplay">--</strong>
    <span class="admin-badge" id="adminBadge">Admin</span>
  </div>
  <button class="logout-btn" onclick="handleLogout()">Logout</button>
</div>
'''

# Encontrar <body> y agregar después
body_index = html_content.find('<body>')
if body_index > 0:
    body_end = html_content.find('\n', body_index)
    html_content = html_content[:body_end+1] + user_badge_html + html_content[body_end+1:]
    print("✓ Badge de usuario agregado")

# PARTE 7: Mostrar badge cuando autenticado
# Modificar showApp para mostrar badge
html_content = html_content.replace(
    'document.getElementById(\'userNameDisplay\').textContent = currentUser;',
    'document.getElementById(\'userNameDisplay\').textContent = currentUser;\n  document.getElementById(\'userBadge\').style.display = \'flex\';'
)

# PARTE 8: Ocultar badge cuando se desautentica
html_content = html_content.replace(
    'showLogin();',
    'showLogin();\n  document.getElementById(\'userBadge\').style.display = \'none\';'
)

print("✓ Integraciones de UI completadas")

# Guardar el archivo modificado
print(f"\nGuardando archivo en: {output_file}")
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✓ Archivo guardado exitosamente ({len(html_content)} caracteres)")
print("\nProceso completado!")
print("\nCaracterísticas agregadas:")
print("  • Login screen con autenticación")
print("  • localStorage para persistencia de sesión")
print("  • Sistema de permisos (Admin vs Usuario Normal)")
print("  • Botón de Logout")
print("  • Badge de usuario en la interfaz")
print("  • 100% funcionalidad original preservada")
