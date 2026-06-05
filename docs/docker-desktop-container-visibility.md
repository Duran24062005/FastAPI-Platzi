# Docker Desktop y visibilidad del contenedor

## Problema

Al levantar la API con:

```bash
sudo docker compose up --build
```

el contenedor se creaba y quedaba ejecutándose correctamente, pero no aparecía donde se esperaba dentro de Docker Desktop.

Durante el diagnóstico también apareció este error al intentar usar Docker sin `sudo`:

```bash
permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock
```

## Qué lo causó

El problema fue una combinación de contexto y permisos:

1. El proyecto se levantó con `sudo`, por lo que los comandos se ejecutaron bajo el usuario `root`.
2. `sudo docker` estaba usando el contexto `default`, que apunta a:

```text
unix:///var/run/docker.sock
```

3. El usuario normal tenía disponibles dos contextos:

```text
default        -> unix:///var/run/docker.sock
desktop-linux  -> unix:///home/<usuario>/.docker/desktop/docker.sock
```

4. Docker Desktop usa su propio contexto (`desktop-linux`), mientras que el contenedor se estaba gestionando desde otro daemon/contexto.
5. Además, el usuario normal no tenía todavía permisos efectivos sobre `/var/run/docker.sock`, por eso `docker ps -a` fallaba sin `sudo`.

## Cómo se diagnosticó

Se verificó lo siguiente:

- El contenedor sí existía porque `docker compose up --build` mostraba `Container fastapi-application Recreated`.
- En el repositorio, el contenedor está definido explícitamente como `fastapi-application` en `docker-compose.yml`.
- `sudo docker ps -a` mostraba contenedores del daemon del sistema.
- `docker context ls` mostraba tanto `default` como `desktop-linux`.
- `docker` sin `sudo` fallaba por permisos sobre el socket del daemon.

## Solución aplicada

Se agregó el usuario al grupo `docker`:

```bash
sudo usermod -aG docker $USER
```

Después de eso, era necesario aplicar la membresía del grupo en una nueva sesión. Esto se puede hacer de dos formas:

```bash
newgrp docker
```

o cerrando sesión y volviendo a entrar al sistema.

Con eso aplicado, ya se puede operar Docker sin `sudo`:

```bash
docker ps -a
docker compose up --build
```

Si se quiere trabajar específicamente contra Docker Desktop, se debe seleccionar el contexto correcto:

```bash
docker context use desktop-linux
docker context ls
```

## Regla práctica

- Usar `docker ...` sin `sudo` para el flujo normal de desarrollo.
- Usar un único contexto de Docker de forma consistente durante la sesión.
- Si Docker Desktop no muestra un contenedor, revisar primero:
  - con qué usuario se levantó
  - qué contexto está activo
  - a qué socket está apuntando ese contexto

## Comandos útiles

```bash
docker context ls
docker context show
docker ps -a
sudo docker ps -a
groups
```

## Resultado esperado

Una vez corregidos los permisos y alineado el contexto, los contenedores levantados desde este proyecto deben poder administrarse sin `sudo` y verse en el entorno Docker correspondiente.
