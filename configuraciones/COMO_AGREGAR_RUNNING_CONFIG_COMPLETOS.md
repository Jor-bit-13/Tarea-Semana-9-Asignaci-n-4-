# Exportación de running-config completos (requisito del profesor)

El repositorio contiene **extractos depurados** de R1, SW1 y FG1, obtenidos de capturas. **No equivalen a los archivos completos exportados de cada dispositivo.** La exportación original solo está disponible en las consolas locales de GNS3/Ubuntu del estudiante.

## R1 y SW1 (Cisco IOS)

En la consola de **cada** equipo:
```text
enable
terminal length 0
show running-config
```

Copiar toda la salida, desde `Building configuration...` hasta `end`, en un archivo local de texto. Guardar como:
- `configuraciones/R1-CIS_running-config_DEPURADO.txt`
- `configuraciones/SW1-CIS_running-config_DEPURADO.txt`

**Antes de subir a GitHub**, borrar o reemplazar por `[REDACTADO]` todos los hashes de `enable secret`, `username ... secret`, contraseñas, comunidades SNMP, claves privadas, secretos compartidos y cualquier credencial. No usar screenshots sin censura de esas líneas.

## FortiGate
En la consola:
```text
show
```
Es la configuración no predeterminada, útil para mostrar su estado real. Para una exportación expandida que incluya valores predeterminados:
```text
show full-configuration
```
Es una salida muy extensa y puede incluir información sensible. Copiar a un archivo local, depurar contraseñas, tokens, claves, certificados, secretos de VPN y cuentas antes de cargar como `configuraciones/FG1-CIS_config_DEPURADO.txt`.

## Verificación del contenido
Revisar que los archivos incluya interfaces, rutas, SSH, líneas VTY (Cisco), controles globales y políticas (FortiGate). Comprobar que coincidan con las capturas y que los secretos se hayan ocultado. Incluir nota en el archivo de que las credenciales fueron censuradas.

## Video
[Demostración YouTube](https://youtu.be/YNStO33xZAQ)

> **Nunca publicar la exportación original sin revisar**. Las capturas de las configuraciones que se compartieron anteriormente contenían hashes de contraseñas.
