# Documentación de Sistema de Strikes

## Descripción General
El sistema de strikes permite llevar un registro de advertencias para miembros del grupo, incluyendo el motivo, quién lo solicitó y la fecha.

## Comandos Disponibles

### 1. `/renum_strikeadd` - Agregar Strike

Agrega un strike a un usuario del grupo.

**Formas de uso:**

#### Opción 1: Responder a un mensaje
```
[Responde al mensaje del usuario]
/renum_strikeadd Motivo del strike
```

#### Opción 2: Mencionar al usuario
```
/renum_strikeadd @usuario Motivo del strike
```

**Información almacenada:**
- Usuario que recibe el strike
- Motivo del strike
- Usuario que lo solicitó
- Fecha y hora

**Ejemplo:**
```
/renum_strikeadd @juan Spam en el grupo
```

### 2. `/renum_strikerem` - Remover Strike

Remueve el último strike de un usuario.

**Formas de uso:**

#### Opción 1: Responder a un mensaje
```
[Responde al mensaje del usuario]
/renum_strikerem
```

#### Opción 2: Mencionar al usuario
```
/renum_strikerem @usuario
```

**Ejemplo:**
```
/renum_strikerem @juan
```

### 3. `/renum_strikecheck` - Consultar Strikes

Consulta los strikes de un usuario.

**Formas de uso:**

#### Opción 1: Ver strikes propios
```
/renum_strikecheck
```

#### Opción 2: Responder a un mensaje
```
[Responde al mensaje del usuario]
/renum_strikecheck
```

#### Opción 3: Mencionar al usuario
```
/renum_strikecheck @usuario
```

**Ejemplo:**
```
/renum_strikecheck @juan
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

2. **Persistencia**: Los datos se guardan automáticamente en `strikes_data.json` y se mantienen entre reinicios del bot.

3. **Orden de remoción**: `/renum_strikerem` siempre remueve el último strike agregado (LIFO - Last In, First Out).

4. **Logs**: Todas las acciones de strikes se registran en el archivo de log para auditoría.

5. **Permisos**: Actualmente cualquier miembro del grupo puede agregar/remover strikes. Si deseas restringir esto solo a administradores, se puede implementar verificación de permisos.

## Próximas Mejoras Sugeridas

- Restringir comandos solo a administradores del grupo
- Agregar límite de strikes antes de acción automática (kick/ban)
- Comando para limpiar todos los strikes de un usuario
- Estadísticas de strikes del grupo
- Exportar historial de strikes
