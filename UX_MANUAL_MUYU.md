# Documento de Experiencia de Usuario (UX) y Manejo de la App: Plataforma Muyu

## 1. Descripción General
La Plataforma Muyu es una aplicación web desarrollada en Streamlit, orientada a la gestión y administración de usuarios y recursos educativos. Está diseñada para tres roles principales: Administrador, Coach y Docente. Cada rol tiene acceso a diferentes dashboards y funcionalidades específicas.

## 2. Acceso y Autenticación
- Al ingresar a la plataforma, el usuario debe iniciar sesión con su nombre de usuario y contraseña.
- El sistema valida las credenciales y, si son correctas, genera un token de sesión (JWT) que permite el acceso seguro.
- Si la sesión expira, el usuario es notificado y debe volver a iniciar sesión.
- El botón "Cerrar sesión" está disponible en la barra lateral para finalizar la sesión en cualquier momento.

## 3. Roles, Dashboards y Credenciales de Acceso

### Administrador
- **Usuario:** admin
- **Contraseña:** 1234
- Acceso completo a la gestión de usuarios, documentos y videos.
- Puede ver y modificar información global de la plataforma.

### Coach
- **Usuario:** coach1
- **Contraseña:** 1234
- Acceso a recursos y reportes relacionados con el acompañamiento docente.
- Visualiza información relevante para el seguimiento de docentes.

### Docente
- **Usuario:** docente1
- **Contraseña:** 1234
- Acceso a sus propios documentos, observaciones y recursos de formación.
- Puede consultar y gestionar su información personal y profesional.

## 4. Navegación
- La navegación principal se realiza a través de dashboards personalizados según el rol.
- El menú lateral permite cerrar sesión y, en algunos casos, acceder a opciones adicionales según el rol.
- La interfaz es responsiva y se adapta a diferentes tamaños de pantalla.

## 5. Experiencia de Usuario
- La plataforma utiliza un diseño limpio y minimalista, priorizando la facilidad de uso.
- Los formularios de ingreso de datos son simples y claros.
- Los mensajes de error y advertencia son visibles y comprensibles (por ejemplo, credenciales incorrectas o sesión expirada).
- El flujo de trabajo es lineal: inicio de sesión → acceso al dashboard correspondiente → gestión de recursos → cierre de sesión.

## 6. Seguridad
- El acceso está protegido mediante autenticación JWT.
- Las sesiones tienen una duración limitada (2 horas) para mayor seguridad.
- Los datos sensibles (usuarios, contraseñas, roles) están gestionados de forma segura en el backend.

## 7. Recomendaciones de Uso
- Utilizar navegadores actualizados para una mejor experiencia.
- No compartir las credenciales de acceso.
- Cerrar sesión al finalizar el uso de la plataforma, especialmente en dispositivos compartidos.
