import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Tekams - Control de Tiempos",
  description: "Sistema de control de tiempos para equipos",
};

export default function RootLayout() {
  return (
    <html lang="es">
      <body style={{ padding: '40px', textAlign: 'center', fontFamily: 'Arial' }}>
        <div>
          <h1 style={{ fontSize: '48px', color: '#2A2963' }}>¡FUNCIONA! 🎉</h1>
          <p style={{ fontSize: '20px', color: '#666' }}>La matriz está lista para cargar</p>
          <p style={{ marginTop: '40px', color: '#999' }}>Si ves esto, el proyecto está funcionando correctamente.</p>
        </div>
      </body>
    </html>
  );
}
