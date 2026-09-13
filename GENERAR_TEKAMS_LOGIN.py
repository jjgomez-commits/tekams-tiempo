#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para procesar Tekams Jump y agregar sistema de login
"""
import sys
import os

def main():
    input_file = r"C:\Users\Jose J. Gómez\AppData\Roaming\Claude\local-agent-mode-sessions\45997731-6d35-4f60-84af-00b65211ddac\a39b206f-47a6-4fb5-b04c-4599015c17dd\local_e7034798-53ad-4f92-9cef-d2b4ccdcb33b\uploads\tekams_jump_2026-08-04-v1-2d00f029.html"
    output_file = r"C:\Users\Jose J. Gómez\Desktop\Seguimiento tareas\tekams_firebase.html"

    print("="*60)
    print("PROCESADOR DE TEKAMS JUMP CON SISTEMA DE LOGIN")
    print("="*60)
    print()

    try:
        # Leer archivo
        print(f"[1/5] Leyendo archivo original...")
        print(f"      {input_file}")
        with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        print(f"      OK - {len(content)} caracteres leídos")
        print()

        # Verificar estructura
        print(f"[2/5] Verificando estructura del archivo...")
        checks = {
            'const ME': content.count('const ME'),
            'function load()': content.count('function load()'),
            '<div class="shell">': content.count('<div class="shell">'),
            '</style>': content.count('</style>'),
        }

        for check, count in checks.items():
            status = "OK" if count > 0 else "FALTA"
            print(f"      {check}: {count} ({status})")
        print()

        # Preparar CSS de login
        print(f"[3/5] Preparando CSS de login...")
        login_css = '''

/* ─── LOGIN SCREEN ─── */
.login-screen{display:flex;align-items:center;justify-content:center;min-height:100vh;background:linear-gradient(135deg, #2A2963 0%, #3D3C80 100%);position:fixed;top:0;left:0;right:0;bottom:0;z-index:9999;font-family:'DM Sans',sans-serif}
.login-container{background:#FFFFFF;border-radius:14px;box-shadow:0 12px 40px rgba(42,41,99,.15);padding:3rem;width:100%;max-width:380px}
.login-header{margin-bottom:2rem;text-align:center}
.login-header h1{font-size:24px;font-weight:700;color:#1A1940;margin-bottom:0.5rem}
.login-header p{font-size:14px;color:#5A5880}
.login-form{display:flex;flex-direction:column;gap:1rem}
.form-group{display:flex;flex-direction:column}
.form-group label{font-size:12px;font-weight:600;color:#1A1940;margin-bottom:0.5rem;text-transform:uppercase;letter-spacing:0.05em}
.form-group input{padding:10px 12px;border:1px solid rgba(42,41,99,.15);border-radius:8px;font-size:14px;font-family:'DM Sans',sans-serif;transition:all .15s;background:#FFFFFF;color:#1A1940}
.form-group input:focus{outline:none;border-color:#D94F2B;box-shadow:0 0 0 3px rgba(217,79,43,.1)}
.login-button{padding:12px 16px;background:#D94F2B;color:#FFFFFF;border:none;border-radius:10px;font-size:14px;font-weight:600;cursor:pointer;transition:all .15s;font-family:'DM Sans',sans-serif;margin-top:0.5rem}
.login-button:hover{background:#C02020;transform:translateY(-1px);box-shadow:0 4px 16px rgba(217,79,43,.2)}
.login-button:active{transform:translateY(0)}
.login-error{background:#FCEAEA;border:1px solid #C02020;color:#C02020;padding:10px 12px;border-radius:8px;font-size:12px;margin-bottom:1rem}
.user-badge{position:fixed;top:1.5rem;right:2rem;display:flex;align-items:center;gap:8px;background:#FFFFFF;padding:8px 14px;border-radius:20px;border:1px solid rgba(42,41,99,.1);z-index:100;font-size:12px}
.user-badge.hidden{display:none}
.user-badge-name{font-weight:600;color:#1A1940}
.user-badge-role{font-size:11px;color:#5A5880}
.logout-btn{padding:4px 10px;background:#D94F2B;color:#FFFFFF;border:none;border-radius:6px;font-size:11px;cursor:pointer;font-family:'DM Sans',sans-serif;transition:all .15s}
.logout-btn:hover{background:#C02020}
'''
        print(f"      CSS agregado ({len(login_css)} caracteres)")
        print()

        # Agregar CSS
        print(f"[4/5] Modificando archivo...")
        content = content.replace('</style>', login_css + '\n</style>')
        print(f"      CSS insertado")

        # Agregar formulario de login
        login_html = '''<div id="login-screen" class="login-screen">
  <div class="login-container">
    <div class="login-header">
      <h1>Tekams Jump</h1>
      <p>Acceso al Sistema</p>
    </div>
    <div id="login-error" class="login-error" style="display:none;"></div>
    <form class="login-form" onsubmit="handleLogin(event)">
      <div class="form-group">
        <label>Correo</label>
        <input type="email" id="email" placeholder="usuario@tekams.com" required>
      </div>
      <div class="form-group">
        <label>Contraseña</label>
        <input type="password" id="password" placeholder="••••••" required>
      </div>
      <button type="submit" class="login-button">Acceder</button>
    </form>
  </div>
</div>
<div id="user-badge" class="user-badge hidden">
  <div>
    <div class="user-badge-name" id="badge-name">Usuario</div>
    <div class="user-badge-role" id="badge-role">Rol</div>
  </div>
  <button class="logout-btn" onclick="logout()">Salir</button>
</div>

'''
        content = content.replace('<div class="shell">', login_html + '<div class="shell">')
        print(f"      Formulario de login insertado")

        # Agregar JS de autenticación
        auth_js = '''
// ═════════════════════════════════════════════════════════════════
// ── AUTENTICACIÓN ──
const USERS_DB = {
  'jjgomez@tekams.com': { email: 'jjgomez@tekams.com', password: '1234', name: 'Jose Gomez', isAdmin: true, role: 'Admin' },
  'paula@tekams.com': { email: 'paula@tekams.com', password: '1234', name: 'Paula', isAdmin: false, role: 'Usuario' },
  'puri@tekams.com': { email: 'puri@tekams.com', password: '1234', name: 'Puri', isAdmin: false, role: 'Usuario' },
  'fran@tekams.com': { email: 'fran@tekams.com', password: '1234', name: 'Fran', isAdmin: false, role: 'Usuario' },
  'antonio@tekams.com': { email: 'antonio@tekams.com', password: '1234', name: 'Antonio', isAdmin: false, role: 'Usuario' },
  'juanjo@tekams.com': { email: 'juanjo@tekams.com', password: '1234', name: 'JuanJo', isAdmin: false, role: 'Usuario' },
  'jon@tekams.com': { email: 'jon@tekams.com', password: '1234', name: 'Jon', isAdmin: false, role: 'Usuario' }
};
let CURRENT_USER = null;
function handleLogin(event) {
  event.preventDefault();
  const email = document.getElementById('email').value.toLowerCase();
  const password = document.getElementById('password').value;
  const errorDiv = document.getElementById('login-error');
  if (!USERS_DB[email]) { errorDiv.textContent = 'Usuario no encontrado'; errorDiv.style.display = 'block'; return; }
  if (USERS_DB[email].password !== password) { errorDiv.textContent = 'Contraseña incorrecta'; errorDiv.style.display = 'block'; return; }
  CURRENT_USER = USERS_DB[email];
  sessionStorage.setItem('currentUser', JSON.stringify(CURRENT_USER));
  document.getElementById('login-screen').style.display = 'none';
  document.getElementById('user-badge').classList.remove('hidden');
  document.getElementById('badge-name').textContent = CURRENT_USER.name;
  document.getElementById('badge-role').textContent = CURRENT_USER.role;
  ME = CURRENT_USER.name;
  load();
  buildSB();
  renderDash();
}
function logout() {
  if (!confirm('¿Deseas cerrar sesión?')) return;
  CURRENT_USER = null;
  sessionStorage.removeItem('currentUser');
  document.getElementById('login-screen').style.display = 'flex';
  document.getElementById('user-badge').classList.add('hidden');
  document.getElementById('email').value = '';
  document.getElementById('password').value = '';
  document.getElementById('login-error').style.display = 'none';
  projs = [];
  pd = {};
}
function checkSession() {
  const userSession = sessionStorage.getItem('currentUser');
  if (userSession) {
    CURRENT_USER = JSON.parse(userSession);
    document.getElementById('login-screen').style.display = 'none';
    document.getElementById('user-badge').classList.remove('hidden');
    document.getElementById('badge-name').textContent = CURRENT_USER.name;
    document.getElementById('badge-role').textContent = CURRENT_USER.role;
    ME = CURRENT_USER.name;
    return true;
  }
  return false;
}

'''
        content = content.replace('const ME = \'Jose\';', 'let ME = \'\';' + auth_js)
        print(f"      Código de autenticación agregado")

        # Modificar inicialización
        content = content.replace(
            'load();buildSB();renderDash();',
            'if(checkSession()){load();buildSB();renderDash();}'
        )
        print(f"      Inicialización modificada")
        print()

        # Guardar archivo
        print(f"[5/5] Guardando archivo procesado...")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"      Archivo guardado: {output_file}")
        print(f"      Tamaño final: {len(content)} caracteres")
        print()

        print("="*60)
        print("PROCESO COMPLETADO EXITOSAMENTE")
        print("="*60)
        print()
        print("USUARIOS PARA LOGIN:")
        print("  - Admin: jjgomez@tekams.com")
        print("  - Usuario: paula@tekams.com | puri@tekams.com | fran@tekams.com")
        print("            antonio@tekams.com | juanjo@tekams.com | jon@tekams.com")
        print("  - Contraseña (todos): 1234")
        print()

        return 0

    except Exception as e:
        print()
        print("="*60)
        print(f"ERROR: {type(e).__name__}")
        print("="*60)
        print(str(e))
        print()
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
