Scripts utilizados en el laboratorio.

- `auditoria_cis.py`: solo lectura. Genera `informes_cis/<equipo>/informe_inicial.md` y sobrescribe ese nombre al repetirse: guardar una copia del antes.
- `aplicar_cis.py`: se ejecutó en Ubuntu; debe copiarse literalmente desde el Ubuntu del laboratorio a esta carpeta. Solicita confirmación por dispositivo y genera `informe_posterior.md`.
- Cisco IOS 12.4 requirió algoritmos SSH legados por compatibilidad, exclusivamente en GNS3; no usarlos en producción.

Las contraseñas son solicitadas interactivamente y no se guardan en los informes.
