# Configuración del servidor

## Establecer configuración de Gmail

Crear un archivo con el nombre 'mail-config.properties' y añadirle la siguiente información:

mail.transport.protocol=smtp<br>
mail.smtp.host=smtp.gmail.com<br>
mail.smtp.port=465<br>
mail.smtp.auth=true<br>
mail.smtp.ssl.enable=true<br>
mail.smtp.socketFactory.port=465<br>
mail.smtp.socketFactory.class=javax.net.ssl.SSLSocketFactory<br>
mail.store.protocol=imaps<br>
mail.imaps.host=imap.gmail.com<br>
mail.imaps.port=993<br>
mail.imaps.timeout=10000<br>
mail.imap.partialfetch=false<br>
mail.poll.folder=INBOX<br>
mail.sender=usuario@gmail.com<br>
mail.sender.alias=alias<br>
mail.attachment.download=true<br>
mail.attachment.path=attachments<br>
mail.user=usuario@gmail.com<br>
mail.password=contraseña<br>

Ajustar el usuario y la contraseña y guardar este archivo en '**camunda-bpm-tomcat-X.X.X/server/apache-tomcat-X.X.X/conf/**', donde '**X.X.X**' es la versión de Camunda y Tomcat que se están usando.


## Configurar variable de entorno

### Sistemas operarivos UNIX

Abrir el archivo '**setenv.sh**', ubicado en '**camunda-bpm-tomcat-X.X.X/server/apache-tomcat-X.X.X/bin/**' y añadir '**export MAIL_CONFIG="$CATALINA_HOME/conf/mail-config.properties"**' en la primera línea.

### Windows

Abrir el archivo '**setenv.bat**', ubicado en '**camunda-bpm-tomcat-X.X.X/server/apache-tomcat-X.X.X/bin/**' y añadir '**set "MAIL_CONFIG=%CATALINA_HOME%\conf\mail-config.properties"**' en la primera línea.
