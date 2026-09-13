# Script para procesar tekams_jump y agregar autenticación
$inputFile = "C:\Users\Jose J. Gómez\AppData\Roaming\Claude\local-agent-mode-sessions\45997731-6d35-4f60-84af-00b65211ddac\a39b206f-47a6-4fb5-b04c-4599015c17dd\local_e7034798-53ad-4f92-9cef-d2b4ccdcb33b\uploads\tekams_jump_2026-08-04-v1-2d00f029.html"
$outputFile = "C:\Users\Jose J. Gómez\Desktop\Seguimiento tareas\tekams_firebase.html"

Write-Host "Leyendo archivo..." -ForegroundColor Green
$content = [System.IO.File]::ReadAllText($inputFile, [System.Text.Encoding]::UTF8)
Write-Host "Tamaño original: $($content.Length) caracteres"

# CSS para login
$loginCSS = @"
    /* Login Screen Styles */
    .login-wrapper {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    .login-box {
        background: white;
        border-radius: 12px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        padding: 40px;
        width: 100%;
        max-width: 380px;
        text-align: center;
    }
    .login-box h1 {
        margin: 0 0 10px 0;
        color: #333;
        font-size: 28px;
        font-weight: 600;
    }
    .login-box p {
        color: #666;
        font-size: 14px;
        margin: 0 0 30px 0;
    }
    .login-field {
        width: 100%;
        padding: 12px 16px;
        margin-bottom: 12px;
        border: 1px solid #ddd;
        border-radius: 6px;
        font-size: 14px;
        font-family: inherit;
        box-sizing: border-box;
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    .login-field:focus {
        outline: none;
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    .login-btn {
        width: 100%;
        padding: 12px 16px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 6px;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .login-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
    }
    .login-btn:active {
        transform: translateY(0);
    }
    .login-error {
        color: #e74c3c;
        font-size: 13px;
        margin-bottom: 15px;
        padding: 10px;
        background: #fadbd8;
        border-radius: 4px;
        display: none;
    }
    .login-error.show {
        display: block;
    }
    .login-help {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 6px;
        margin-top: 20px;
        text-align: left;
    }
    .login-help strong {
        display: block;
        color: #333;
        margin-bottom: 8px;
        font-size: 13px;
    }
    .login-help p {
        color: #666;
        font-size: 12px;
        margin: 4px 0;
    }
    .user-badge {
        position: fixed;
        top: 10px;
        right: 10px;
        background: white;
        padding: 8px 12px;
        border-radius: 6px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 12px;
        z-index: 9999;
        display: none;
    }
    .admin-badge {
        background: #e74c3c;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 11px;
    }
    .logout-btn {
        background: #ecf0f1;
        color: #333;
        border: none;
        padding: 4px 10px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 12px;
        font-weight: 500;
        transition: background 0.2s;
    }
    .logout-btn:hover {
        background: #bdc3c7;
    }
    .shell.hidden {
        display: none;
    }
"@

# HTML del login
$loginHTML = @"
    <!-- Login Screen -->
    <div id="loginWrapper" class="login-wrapper">
        <div class="login-box">
            <h1>TekAMS</h1>
            <p>Sistema de Gestión</p>
            <form id="loginForm" onsubmit="handleLogin(event)">
                <input type="text" id="loginUsername" class="login-field" placeholder="Usuario" autocomplete="username" required>
                <input type="password" id="loginPassword" class="login-field" placeholder="Contraseña" autocomplete="current-password" required>
                <div id="loginError" class="login-error"></div>
                <button type="submit" class="login-btn">Iniciar Sesión</button>
            </form>
            <div class="login-help">
                <strong>Usuarios de prueba:</strong>
                <p><strong>Admin:</strong> jjgomez@tekams.com / admin</p>
                <p><strong>Usuarios:</strong> Paula, Puri, Fran, Antonio, JuanJo, Jon (cualquier contraseña)</p>
            </div>
        </div>
    </div>
"@

# User badge
$userBadgeHTML = @"
    <!-- User Badge -->
    <div id="userBadge" class="user-badge">
        <span id="currentUserName"></span>
        <span id="adminBadge" class="admin-badge" style="display: none;">ADMIN</span>
        <button class="logout-btn" onclick="handleLogout()">Salir</button>
    </div>
"@

# JavaScript de autenticación
$authJS = @"
    // ========== Authentication System ==========
    const AUTH_USERS = {
        'jjgomez@tekams.com': { password: 'admin', name: 'José Gómez', isAdmin: true },
        'paula': { password: '', name: 'Paula', isAdmin: false },
        'puri': { password: '', name: 'Puri', isAdmin: false },
        'fran': { password: '', name: 'Fran', isAdmin: false },
        'antonio': { password: '', name: 'Antonio', isAdmin: false },
        'juanjo': { password: '', name: 'JuanJo', isAdmin: false },
        'jon': { password: '', name: 'Jon', isAdmin: false }
    };

    let currentUser = null;
    let isAdmin = false;

    function initAuth() {
        const savedUser = localStorage.getItem('tekams_user');
        if (savedUser) {
            try {
                const user = JSON.parse(savedUser);
                currentUser = user.username;
                isAdmin = user.isAdmin;
                showApp();
                return;
            } catch (e) {
                localStorage.removeItem('tekams_user');
            }
        }
        showLogin();
    }

    function showLogin() {
        document.getElementById('loginWrapper').style.display = 'flex';
        document.querySelector('.shell').classList.add('hidden');
        document.getElementById('userBadge').style.display = 'none';
    }

    function showApp() {
        document.getElementById('loginWrapper').style.display = 'none';
        document.querySelector('.shell').classList.remove('hidden');
        document.getElementById('userBadge').style.display = 'flex';
        const user = AUTH_USERS[currentUser];
        document.getElementById('currentUserName').textContent = user.name;
        if (isAdmin) {
            document.getElementById('adminBadge').style.display = 'inline-block';
        } else {
            document.getElementById('adminBadge').style.display = 'none';
        }
        init();
    }

    function handleLogin(event) {
        event.preventDefault();
        const username = document.getElementById('loginUsername').value.trim();
        const password = document.getElementById('loginPassword').value;
        const errorEl = document.getElementById('loginError');
        errorEl.classList.remove('show');
        if (!AUTH_USERS[username]) {
            errorEl.textContent = 'Usuario no encontrado';
            errorEl.classList.add('show');
            return;
        }
        const user = AUTH_USERS[username];
        if (user.password && user.password !== password) {
            errorEl.textContent = 'Contraseña incorrecta';
            errorEl.classList.add('show');
            return;
        }
        currentUser = username;
        isAdmin = user.isAdmin;
        localStorage.setItem('tekams_user', JSON.stringify({
            username: username,
            isAdmin: isAdmin
        }));
        document.getElementById('loginUsername').value = '';
        document.getElementById('loginPassword').value = '';
        showApp();
    }

    function handleLogout() {
        currentUser = null;
        isAdmin = false;
        localStorage.removeItem('tekams_user');
        location.reload();
    }

"@

Write-Host "Aplicando transformaciones..."

# 1. Insertar CSS antes de </style>
$content = $content -replace '</style>', "`n$loginCSS`n</style>"
Write-Host "1. CSS insertado"

# 2. Insertar HTML de login y user badge después de <body>
$content = $content -replace '(<body>)', "`$1`n$loginHTML`n$userBadgeHTML"
Write-Host "2. HTML login y user badge insertados"

# 3. Insertar JavaScript de autenticación antes de function load()
$content = $content -replace '(function load\(\)\{)', "$authJS`n`n    `$1"
Write-Host "3. Sistema de autenticación insertado"

# 4. Reemplazar const ME = 'Jose' por let ME = currentUser
$content = $content -replace "const ME = 'Jose'", "let ME = currentUser"
Write-Host "4. ME reemplazado"

Write-Host "Tamaño final: $($content.Length) caracteres"
Write-Host "Guardando archivo..."
[System.IO.File]::WriteAllText($outputFile, $content, [System.Text.Encoding]::UTF8)
Write-Host "Archivo guardado: $outputFile" -ForegroundColor Green
Write-Host "Transformaciones completadas" -ForegroundColor Green
