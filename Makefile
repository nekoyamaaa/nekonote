APP = "nekonote"
ZIPNAME = build/${APP}.zip
BUNDLE_ZIPNAME = build/bundle.zip
FULL_ZIPNAME = build/${APP}-bundled.zip

SIKULI_PATH = ./bundle/sikulixapi.jar
JYTHON_PATH = ./bundle/jython-standalone-2.7.1.jar
jars = ${SIKULI_PATH} ${JYTHON_PATH}

LAUNCHERS = ${APP}.bat ${APP}.sh

.PHONY: clean cleanobj all full

all: ${ZIPNAME}

full: ${FULL_ZIPNAME}

clean: cleanobj
	rm -f ${ZIPNAME} ${FULL_ZIPNAME} ${LAUNCHERS}

cleanobj:
	find -name '*$.class' -type f -delete

ZIP_TARGETS = nekonote/* macros/* data/* ${LAUNCHERS} README.md
ZIP_ARGS = ${ZIP_TARGETS} --exclude @.zipignore

${ZIPNAME}: ${ZIP_TARGETS}
	zip -rv $@ ${ZIP_ARGS}

${FULL_ZIPNAME}: ${BUNDLE_ZIPNAME} ${ZIPNAME}
	cp -av ${BUNDLE_ZIPNAME} $@
	zip -urv $@ ${ZIP_ARGS}

settings.ini: data/default.ini
	sed -e "/Do not edit/d" $^ > $@

${BUNDLE_ZIPNAME}: ${jars}
	[ -f $@ ] && zip -uv $@ $^ || zip -v $@ $^

JAVA_ARGS = --add-opens java.base/sun.nio.ch=ALL-UNNAMED --add-opens java.base/java.io=ALL-UNNAMED

${APP}.bat:
	echo 'cmd /k java.exe ${JAVA_ARGS} -cp "${SIKULI_PATH};${JYTHON_PATH}" org.python.util.jython -m nekonote' > $@

${APP}.sh:
	echo 'java ${JAVA_ARGS} -cp "${SIKULI_PATH}:${JYTHON_PATH}" org.python.util.jython -m nekonote $$@' > $@
	chmod +x $@
