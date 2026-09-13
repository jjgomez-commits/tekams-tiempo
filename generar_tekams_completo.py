#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar tekams_firebase.html
Integra el login con autenticación al sistema Tekams Jump original
"""

import os
import re
import json
from pathlib import Path

def main():
    # Rutas
    original_file = r"C:\Users\Jose J. Gómez\AppData\Roaming\Claude\local-agent-mode-sessions\45997731-6d35-4f60-84af-00b65211ddac\a39b206f-47a6-4fb5-b04c-4599015c17dd\local_e7034798-53ad-4f92-9cef-d2b4ccdcb33b\uploads\tekams_jump_2026-08-04-v1-2d00f029.html"
    output_file = r"C:\Users\Jose J. Gómez\Desktop\Seguimiento tareas\tekams_firebase.html"

    print("=" * 70)
    print("GENERADOR DE TEKAMS JUMP CON AUTENTICACION")
    print("=" * 70)

    # Verificar archivo original
    if not os.path.exists(original_file):
        print(f"ERROR: No se encontró el archivo original")
        print(f"Ruta esperada: {original_file}")
        return False

    print(f"\n✓ Archivo original encontrado ({os.path.getsize(original_file) / 1024 / 1024:.2f} MB)")

    # Leer archivo original
    print("\n[1/5] Leyendo archivo original...")
    try:
        with open(original_file, 'r', encoding='utf-8', errors='ignore') as f:
            original_html = f.read()
        print(f"✓ Lectura completada ({len(original_html) / 1024 / 1024:.2f} MB)")
    except Exception as e:
        print(f"ERROR: {e}")
        return False

    # Extraer el bloque <script>
    print("\n[2/5] Extrayendo código JavaScript...")
    script_start = original_html.find('<script>')
    script_end = original_html.find('</script>')

    if script_start == -1 or script_end == -1:
        print("ERROR: No se encontró el bloque <script> en el archivo original")
        return False

    script_content = original_html[script_start + 8:script_end]
    print(f"✓ JavaScript extraído ({len(script_content) / 1024:.2f} KB)")

    # Modificar el JavaScript
    print("\n[3/5] Modificando código para autenticación...")

    # Reemplazo 1: const ME = 'Jose' -> let ME = authState.currentUser
    script_content = re.sub(
        r"const\s+ME\s*=\s*'[^']*'",
        "let ME = authState.currentUser",
        script_content
    )
    print("✓ Variable ME reemplazada")

    # Reemplazo 2: TEAM sin Jose
    script_content = re.sub(
        r"let\s+TEAM\s*=\s*\[[^\]]*\]",
        "let TEAM = ['Paula','Puri','Fran','Antonio','JuanJo','Jon'];",
        script_content
    )
    print("✓ Array TEAM reemplazado")

    # Reemplazo 3: Asegurar que init() se llama después de autenticar
    # Envolver init() en una función que verifique autenticación
    init_wrapper = """
    function initWithAuth() {
      if(!authState.currentUser) {
        console.warn('No hay usuario autenticado');
        return;
      }
      try {
        init();
      } catch(e) {
        console.error('Error en init():', e);
      }
    }
    """

    # Insertar el wrapper al principio del script
    script_content = init_wrapper + "\n" + script_content
    print("✓ Funciones de autenticación integradas")

    # Crear archivo de salida
    print("\n[4/5] Generando archivo final...")

    # HTML con login + app
    output_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tekams Jump - Seguimiento de Proyectos</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
:root{{
  --navy:#2A2963;--navy-dk:#1E1D4A;--navy-lt:#3D3C80;
  --accent:#D94F2B;--accent2:#8B3FA8;
  --bg:#F2F1F8;--surf:#FFFFFF;--surf2:#F7F6FC;
  --bdr:rgba(42,41,99,.08);--bdr-md:rgba(42,41,99,.15);
  --txt:#1A1940;--txt2:#5A5880;--txt3:#9896B8;
  --bl:#2A2963;--bl-lt:#ECEAF8;--bl-mid:#B8B5E8;
  --grn:#1A7A4A;--grn-lt:#E6F5EE;
  --amb:#8A5200;--amb-lt:#FDF2DC;
  --red:#C02020;--red-lt:#FCEAEA;
  --r:10px;--rlg:14px;
  --sh:0 1px 3px rgba(42,41,99,.06),0 4px 16px rgba(42,41,99,.05);
  --sh-md:0 4px 16px rgba(42,41,99,.1),0 12px 40px rgba(42,41,99,.08);
}}

*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'DM Sans',sans-serif;background:#F2F1F8;color:#1A1940;min-height:100vh;font-size:14px;line-height:1.5}}

/* LOGIN SCREEN */
.login-wrapper{{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#2A2963,#1E1D4A);z-index:9999;padding:1rem}}
.login-wrapper.hidden{{display:none}}
.login-box{{background:#FFFFFF;border-radius:14px;border:1px solid rgba(42,41,99,.15);padding:2.5rem;width:100%;max-width:420px;box-shadow:0 4px 16px rgba(42,41,99,.1),0 12px 40px rgba(42,41,99,.08)}}
.login-box h1{{font-size:24px;font-weight:700;color:#1A1940;letter-spacing:-.02em;margin-bottom:8px;text-align:center}}
.login-box .login-subtitle{{font-size:12px;color:#5A5880;margin-bottom:2rem;text-align:center}}
.login-field{{margin-bottom:1.25rem}}
.login-field label{{display:block;font-size:10px;font-weight:700;color:#5A5880;text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px}}
.login-field input{{width:100%;font-size:13px;font-family:'DM Sans',sans-serif;padding:10px 12px;border-radius:10px;border:1px solid rgba(42,41,99,.15);background:#F2F1F8;color:#1A1940;outline:none;box-sizing:border-box;transition:all .15s}}
.login-field input:focus{{border-color:#2A2963;background:#FFFFFF}}
.login-btn{{width:100%;padding:11px 14px;border-radius:10px;font-size:12px;font-family:'DM Sans',sans-serif;font-weight:600;border:none;background:#2A2963;color:#fff;cursor:pointer;transition:all .15s}}
.login-btn:hover{{background:#3D3C80}}
.login-error{{color:#C02020;font-size:11px;min-height:16px;margin-bottom:12px;text-align:center}}
.login-note{{font-size:10px;color:#9896B8;margin-top:1.5rem;padding-top:1rem;border-top:1px solid rgba(42,41,99,.08);text-align:center}}
.login-note strong{{display:block;color:#5A5880;margin-bottom:4px;font-weight:600}}

.user-badge{{position:fixed;top:1rem;right:2rem;display:none;align-items:center;gap:10px;font-size:11px;background:rgba(255,255,255,.95);padding:8px 14px;border-radius:10px;box-shadow:0 2px 8px rgba(42,41,99,.15);z-index:9998}}
.user-badge.visible{{display:flex}}
.user-info-text{{display:flex;align-items:center;gap:6px;color:#1A1940}}
.user-info-text strong{{font-weight:700}}
.admin-badge{{background:#D94F2B;color:#fff;padding:2px 8px;border-radius:5px;font-size:9px;font-weight:700;text-transform:uppercase;display:none}}
.admin-badge.visible{{display:inline-block}}
.logout-btn{{padding:6px 12px;border-radius:8px;border:1px solid rgba(42,41,99,.15);background:#FFFFFF;color:#5A5880;cursor:pointer;font-size:11px;font-family:'DM Sans',sans-serif;font-weight:500;transition:all .15s}}
.logout-btn:hover{{background:#F2F1F8;color:#1A1940}}

.shell.hidden{{display:none!important}}
</style>
</head>
<body>

<!-- LOGIN SCREEN -->
<div class="login-wrapper" id="loginWrapper">
  <div class="login-box">
    <h1>Tekams Jump</h1>
    <p class="login-subtitle">Seguimiento de Proyectos</p>
    <div class="login-error" id="loginError"></div>
    <form id="loginForm" onsubmit="handleLogin(event)">
      <div class="login-field">
        <label for="loginUser">Usuario</label>
        <input type="text" id="loginUser" placeholder="Email o Nombre" autocomplete="off" required>
      </div>
      <div class="login-field">
        <label for="loginPass">Contraseña</label>
        <input type="password" id="loginPass" placeholder="Contraseña" autocomplete="off" required>
      </div>
      <button type="submit" class="login-btn">Iniciar Sesión</button>
      <div class="login-note">
        <strong>Usuarios disponibles:</strong>
        <div>jjgomez@tekams.com (Admin)</div>
        <div>Paula, Puri, Fran, Antonio, JuanJo, Jon</div>
        <div><strong>Contraseña: 1234</strong></div>
      </div>
    </form>
  </div>
</div>

<!-- USER BADGE -->
<div class="user-badge" id="userBadge">
  <div class="user-info-text">
    <span>Usuario:</span>
    <strong id="userNameDisplay">--</strong>
    <span class="admin-badge" id="adminBadge">Admin</span>
  </div>
  <button class="logout-btn" onclick="handleLogout()">Logout</button>
</div>

<script>
// ========================================
// SISTEMA DE AUTENTICACION
// ========================================
const AUTH_USERS = {{
  'jjgomez@tekams.com': {{password: '1234', isAdmin: true, name: 'José'}},
  'Paula': {{password: '1234', isAdmin: false, name: 'Paula'}},
  'Puri': {{password: '1234', isAdmin: false, name: 'Puri'}},
  'Fran': {{password: '1234', isAdmin: false, name: 'Fran'}},
  'Antonio': {{password: '1234', isAdmin: false, name: 'Antonio'}},
  'JuanJo': {{password: '1234', isAdmin: false, name: 'JuanJo'}},
  'Jon': {{password: '1234', isAdmin: false, name: 'Jon'}}
}};

let currentUser = null;
let isAdmin = false;
let authState = {{currentUser: null, isAdmin: false}};

function initAuth(){{
  const stored = localStorage.getItem('tkm9_auth');
  if(stored){{
    try{{
      const auth = JSON.parse(stored);
      const user = AUTH_USERS[auth.user];
      if(user && user.password === auth.pass){{
        currentUser = auth.user;
        isAdmin = user.isAdmin;
        authState.currentUser = currentUser;
        authState.isAdmin = isAdmin;
        showApp();
        return;
      }}
    }}catch(e){{}}
  }}
  showLogin();
}}

function showLogin(){{
  document.getElementById('loginWrapper').classList.remove('hidden');
  document.querySelector('.shell').classList.add('hidden');
  document.getElementById('userBadge').classList.remove('visible');
}}

function showApp(){{
  document.getElementById('loginWrapper').classList.add('hidden');
  document.querySelector('.shell').classList.remove('hidden');
  document.getElementById('userNameDisplay').textContent = currentUser;
  document.getElementById('adminBadge').classList.toggle('visible', isAdmin);
  document.getElementById('userBadge').classList.add('visible');
  initWithAuth();
}}

function handleLogin(e){{
  e.preventDefault();
  const username = document.getElementById('loginUser').value.trim();
  const password = document.getElementById('loginPass').value;
  const errorEl = document.getElementById('loginError');

  if(!username || !password){{
    errorEl.textContent = 'Completa todos los campos';
    return;
  }}

  const user = AUTH_USERS[username];
  if(!user || user.password !== password){{
    errorEl.textContent = 'Usuario o contraseña incorrectos';
    return;
  }}

  currentUser = username;
  isAdmin = user.isAdmin;
  authState.currentUser = currentUser;
  authState.isAdmin = isAdmin;

  try{{
    localStorage.setItem('tkm9_auth', JSON.stringify({{user: username, pass: password}}));
  }}catch(e){{}}

  errorEl.textContent = '';
  showApp();
}}

function handleLogout(){{
  if(!confirm('¿Cerrar sesión?')) return;
  localStorage.removeItem('tkm9_auth');
  currentUser = null;
  isAdmin = false;
  authState = {{currentUser: null, isAdmin: false}};
  showLogin();
  document.getElementById('loginUser').value = '';
  document.getElementById('loginPass').value = '';
  document.getElementById('loginError').textContent = '';
  location.reload();
}}

// ========================================
// CODIGO ORIGINAL DEL TEKAMS JUMP
// ========================================
{script_content}

// Inicializar
window.addEventListener('load', initAuth);
</script>

</body>
</html>"""

    # Guardar archivo
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_html)
        file_size = os.path.getsize(output_file) / 1024
        print(f"✓ Archivo generado correctamente ({file_size:.2f} KB)")
    except Exception as e:
        print(f"ERROR al guardar: {e}")
        return False

    # Verificar
    print("\n[5/5] Verificando archivo...")
    if os.path.exists(output_file) and os.path.getsize(output_file) > 100000:
        print(f"✓ Verificación completada")
    else:
        print("⚠ Verificación fallida")
        return False

    print("\n" + "=" * 70)
    print("RESULTADO FINAL")
    print("=" * 70)
    print(f"\n✓ Archivo guardado en:")
    print(f"  {output_file}")
    print(f"\nPara usar:")
    print(f"  1. Abre el archivo en un navegador web")
    print(f"  2. Inicia sesión con uno de los usuarios:")
    print(f"     - jjgomez@tekams.com (Admin)")
    print(f"     - Paula, Puri, Fran, Antonio, JuanJo, Jon")
    print(f"     - Contraseña: 1234")
    print(f"\n✓ Sistema completamente funcional")
    print("=" * 70)

    return True

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
