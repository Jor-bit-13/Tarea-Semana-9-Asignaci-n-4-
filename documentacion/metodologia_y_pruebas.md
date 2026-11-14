# Metodología, alcance y pruebas
Se utilizó GNS3 con R1 y SW1 ejecutando Cisco IOS 12.4, FortiGate 7.4.13 y Ubuntu Server con Python 3 y Pexpect. Las IP son de laboratorio y están documentadas en el README.

## Procedimiento reproducible
1. Verificar SSH desde Ubuntu a R1, SW1 y FG1 (la identidad del servidor debe haberse validado y guardado en known_hosts).
2. Ejecutar `python3 scripts/auditoria_cis.py` y guardar el informe **antes** sin sobrescribirlo.
3. Ejecutar `python3 scripts/aplicar_cis.py`, confirmar APLICAR por equipo, comprobar la salida y conservar la captura.
4. Volver a ejecutar `auditoria_cis.py` y guardar el informe posterior con otro nombre.
5. Contrastar estado SSH, bloqueos administrativos, conectividad y limitaciones de licencia.

## Comandos de verificación
- R1/SW1: `show ip ssh`, `show running-config | section line vty`, `show ip interface brief`.
- FortiGate: `get system status`, `show system interface port1`, `show system interface port2`, `show firewall policy`, `show full-configuration system global | grep admin`.
- Ubuntu: `ping -c 4 10.7.63.1`, `ping -c 4 10.7.63.2`, `ping -c 4 10.7.63.3`, `ip route get 10.7.66.10`.
- PC2: `show ip`, `ping 10.7.66.1`.

## Límites de interpretación
La ausencia de respuesta al ping entre subredes **no prueba** por sí sola el correcto filtrado. La licencia del firewall aparece Invalid y la política no fue validada extremo a extremo.
Las mediciones «13 cumple, 0 no cumple, 1 no verificado» son exclusivamente los controles seleccionados por el script. Los comandos adicionales visualizados en running-config no fueron evaluados todos por el programa.
El parámetro `strong-crypto` no produjo salida en FortiOS 7.4.13; no asumir que esté habilitado o deshabilitado.

## Seguridad operativa
Las opciones de SSH con diffie-hellman-group1-sha1, ssh-rsa y aes128-cbc se utilizaron únicamente para entrar a Cisco IOS antiguo dentro de GNS3. Son criptografía obsoleta. No utilizar fuera del laboratorio.
Los informes del script solo deben publicarse después de revisar secretos, direcciones sensibles y cualquier dato personal.
