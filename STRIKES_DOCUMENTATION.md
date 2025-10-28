# Documentación de Sistema de Strikes

## Descripción General
El sistema de strikes permite llevar un registro de advertencias para miembros del grupo, incluyendo el motivo, quién lo solicitó y la fecha.

## ⚠️ IMPORTANTE: Cómo Mencionar Usuarios

**MÉTODO RECOMENDADO**: Responder al mensaje del usuario

Los comandos funcionan **respondiendo al mensaje del usuario** al que quieres aplicar el strike. Este es el método más confiable y simple.

## Comandos Disponibles

### 1. `/renum_strikeadd` - Agregar Strike

Agrega un strike a un usuario del grupo.

**Cómo usar:**

1. Responde al mensaje del usuario
2. Escribe: `/renum_strikeadd [motivo]`

**Ejemplo:**
```
[Selecciona "Responder" en un mensaje de Juan]
/renum_strikeadd Spam en el grupo
```

**Información almacenada:**
- Usuario que recibe el strike
- Motivo del strike
- Usuario que lo solicitó
- Fecha y hora

### 2. `/renum_strikerem` - Remover Strike

Remueve el último strike de un usuario.

**Cómo usar:**

1. Responde al mensaje del usuario
2. Escribe: `/renum_strikerem`

**Ejemplo:**
```
[Selecciona "Responder" en un mensaje de Juan]
/renum_strikerem
```

### 3. `/renum_strikecheck` - Consultar Strikes

Consulta los strikes de un usuario.

**Cómo usar:**

#### Opción 1: Ver tus propios strikes
```
/renum_strikecheck
```

#### Opción 2: Ver strikes de otro usuario
```
[Selecciona "Responder" en un mensaje del usuario]
/renum_strikecheck
```

**Respuesta ejemplo:**
```
📋 Strikes de Juan (2 total):

1. 📝 Spam en el grupo
   👮 Por: Pedro
   📅 Fecha: 2025-10-28 14:30:45

2. 📝 Lenguaje inapropiado
   👮 Por: María
   📅 Fecha: 2025-10-28 15:20:10
```

## Almacenamiento

Los strikes se almacenan en el archivo `strikes_data.json` con la siguiente estructura:

```json
{
  "123456789": {
    "username": "juan",
    "strikes": [
      {
        "reason": "Spam en el grupo",
        "requested_by": 987654321,
        "requested_by_username": "pedro",
        "date": "2025-10-28 14:30:45"
      }
    ]
  }
}
```

## Notas Importantes

1. **Solo funciona en grupos**: Los comandos de strikes solo están disponibles en grupos y supergrupos.

2. **Método de uso**: Siempre debes **responder al mensaje del usuario**. No intentes mencionar con @ ya que Telegram tiene limitaciones con las menciones.

3. **Persistencia**: Los datos se guardan automáticamente en `strikes_data.json` y se mantienen entre reinicios del bot.

4. **Orden de remoción**: `/renum_strikerem` siempre remueve el último strike agregado (LIFO - Last In, First Out).

5. **Logs**: Todas las acciones de strikes se registran en el archivo de log para auditoría.

6. **Permisos**: Actualmente cualquier miembro del grupo puede agregar/remover strikes. Si deseas restringir esto solo a administradores, se puede implementar verificación de permisos.

## Flujo de Trabajo Típico

1. **Usuario comete infracción**
2. **Moderador responde al mensaje** del usuario infractor
3. **Moderador ejecuta** `/renum_strikeadd [motivo]`
4. **Bot confirma** el strike y muestra el total

## Próximas Mejoras Sugeridas

- Restringir comandos solo a administradores del grupo
- Agregar límite de strikes antes de acción automática (kick/ban)
- Comando para limpiar todos los strikes de un usuario
- Estadísticas de strikes del grupo
- Exportar historial de strikes
