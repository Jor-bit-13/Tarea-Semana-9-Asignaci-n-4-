# Archivos pendientes de incorporar desde Ubuntu y los equipos

El repositorio contiene documentación y extractos DEPURADOS basados en las capturas compartidas. La tarea exige los **running-configs completos**. Antes de la entrega, exportarlos desde cada consola y revisar que no contengan hashes/contraseñas.

## Exportar desde consola
- R1 y SW1: `terminal length 0` y `show running-config` → guardar salida completa como .txt; **depurar** líneas `enable secret`, `username ... secret`, SNMP communities, pre-shared keys, tokens.
- FG1: `show` o `show full-configuration` según se necesite; revisar secretos, hashes, claves, certificados, datos de administración. El estado `Invalid` debe constar.
- Ubuntu: copiar literalmente `~/auditoria_cis.py`, `~/aplicar_cis.py` y `~/informes_cis/{R1,SW1,FG1}/*` a sus rutas equivalentes (sin sobrescribir el informe inicial original por el posterior).

## Imágenes
Añadir capturas REALES a `imagenes/` con nombres descriptivos. No subir capturas que revelen hashes visibles en los running-config. La figura `diagramas/topologia.svg` ya se muestra en el README, pero todavía deben añadirse capturas de consola y GNS3.

## Video / entrega
Publicar en YouTube el video de máximo 10 min, donde aparezcan fecha/hora, rostro y voz. Sustituir `PENDIENTE DE PUBLICAR` por su enlace al principio del README y elaborar `<Nombre>_<Matricula>_A4.txt` con exactamente la URL real del repositorio y la del video. Evitar cualquier evidencia inventada o manipulada que altere los resultados técnicos.
