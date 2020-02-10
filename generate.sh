#!/bin/sh
# This script configures the openapi-generator-cli from https://raw.githubusercontent.com/OpenAPITools/openapi-generator
# then uses it to generate server and client Python project stubs

#############################
###       Constants       ###
#############################

# This is a whitespace (space or tab) delimited list of lines that will be added to
# .openapi-generator-ignore prior to code generation, if they are not already present.
IGNORE_LIST=""

# This is where we will download openapi-generator-cli from the latest release;
# Override these settings if your local installation of the tool deviates
OPENAPI_GENERATOR_CLI="openapi-generator-cli"
OPENAPI_GENERATOR_CLI_PATH="/usr/local/bin/${OPENAPI_GENERATOR_CLI}"

# Here we define the default values of the code generation parameters
# guiding the generation of the server and client projects (these may be overridden in the invoking environment)
PROJECT_NAME="workflow-ara"

# Monarch Biolink client specification file doesn't really yet exist?
CLIENT_SPECIFICATION_FILE_PATH="./api/monarch_biolink.yaml"
CLIENT_OUTPUT_DIR="client"
CLIENT_PROJECT_NAME="${PROJECT_NAME}_${CLIENT_OUTPUT_DIR}"
CLIENT_PACKAGE_NAME="biolink_client"
CLIENT_PACKAGE_VERSION="0.0.1"
CLIENT_PACKAGE_URL="https://github.com/NCATS-Tangerine/biolink-beacon/tree/master/client"

SERVER_SPECIFICATION_FILE_PATH="./api/knowledge-beacon-api.yaml"
SERVER_OUTPUT_DIR="server"
SERVER_PROJECT_NAME="${PROJECT_NAME}_${SERVER_OUTPUT_DIR}"
SERVER_PACKAGE_NAME="beacon_server"
SERVER_PACKAGE_VERSION="1.1.1"
SERVER_PACKAGE_URL="https://github.com/NCATS-Tangerine/biolink-beacon/tree/master/server"
SERVER_PORT=8080

#############################
###        Methods        ###
#############################

# Called when there is an error with how the script is being used
usage() {
echo "usage: $(basename "$0") <command> [<specification>[ -- uses OpenAPI Generator to generate a python project stub

	command:
		validate	to validate the default or an (optional) API specification provided on the command line
		server		to generate a server
		client		to generate a client
		clean		to delete openapi-generator-cli script

	specification:
		path to an optional json or yaml specification file to be used for generating the server or client project stub"
	exit 1
}

# Ensures that the .openapi-generator-ignore file is set up and in place
ensureValidIgnoreFile() {
	DIRECTORY="$1"
	IGNORE_FILE="$DIRECTORY/.openapi-generator-ignore"

	if [ ! -f "$IGNORE_FILE" ]; then
		# Swagger automatically creates an empty .openapi-generator-ignore file, so this must mean that the project
		# hasn't ever been generated before. The ignore functionality applies not just to overwriting preexisting
		# files, but also creating files. So we don't want an ignore file active in this case.
		return
	fi

	for FILE_NAME in $IGNORE_LIST; do
		ANY_DIR_FILE_NAME='**/'"$FILE_NAME"

		if ! grep -q -x "$ANY_DIR_FILE_NAME" "$IGNORE_FILE" ; then
			echo "$ANY_DIR_FILE_NAME" >> "$IGNORE_FILE"
		fi

		if ! grep -q -x "$FILE_NAME" "$IGNORE_FILE" ; then
			echo "$FILE_NAME" >> "$IGNORE_FILE"
		fi
	done

}

#############################
###     Script Logic      ###
#############################

# Get the command
if [ -z "$1" ]; then
	usage
else
	COMMAND="$1"

	if [ "$COMMAND" = validate ]; then
		:
	#
	# Disabling the client generation here for now since the client in this project
	# is a custom Monarch Biolink client library without an OpenAPI schema
	#
	# elif [ "$COMMAND" = client ]; then
	#	:
	elif [ "$COMMAND" = server ]; then
		:
	elif [ "$COMMAND" = clean ]; then
		# redirect output to /dev/null to prevent it from printing
		rm ${OPENAPI_GENERATOR_CLI_PATH} 2> /dev/null || echo "There is nothing to clean"
		exit 0
	else
		echo "Invalid command\n"
		usage
	fi
fi

# Get a user specified specification file, if provided
if [ -n "$2" ]; then

	SPECIFICATION_FILE_PATH="$2"

	if [ "${SPECIFICATION_FILE_PATH#*.yaml}" != $SPECIFICATION_FILE_PATH ]; then
		:
	elif [ "${SPECIFICATION_FILE_PATH#*.json}" != $SPECIFICATION_FILE_PATH ]; then
		:
	else
		echo "Invalid specification file\n"
		usage
	fi

	# Command line overrides
    if [ "$COMMAND" = client ]; then
        CLIENT_SPECIFICATION_FILE_PATH=$SPECIFICATION_FILE_PATH
    elif [ "$COMMAND" = server ]; then
        SERVER_SPECIFICATION_FILE_PATH=$SPECIFICATION_FILE_PATH
    else
        echo "No default for unknown specification file\n"
        usage
    fi
fi

# Attempt to download openapi-generator-cli.jar if it doesn't already exist
if [ -f ${OPENAPI_GENERATOR_CLI_PATH} ]; then
	:
else
	echo "(Re-)installing OpenAPI Generator Tool (may need to be 'sudo' to succeed)"
	curl https://raw.githubusercontent.com/OpenAPITools/openapi-generator/master/bin/utils/openapi-generator-cli.sh \
		> ${OPENAPI_GENERATOR_CLI_PATH}
	chmod uga+x ${OPENAPI_GENERATOR_CLI_PATH}
	${OPENAPI_GENERATOR_CLI} version
fi

# Use openapi-generator-cli.jar to generate the server and client stub
if [ "$COMMAND" = validate ]; then

    if [ -z "$2" ]; then

		${OPENAPI_GENERATOR_CLI} validate --input-spec=${CLIENT_SPECIFICATION_FILE_PATH}
		${OPENAPI_GENERATOR_CLI} validate --input-spec=${SERVER_SPECIFICATION_FILE_PATH}
    else
		${OPENAPI_GENERATOR_CLI} validate --input-spec=$2
    fi

	exit 0

elif [ "$COMMAND" = client ]; then

	ensureValidIgnoreFile ${CLIENT_OUTPUT_DIR}

	${OPENAPI_GENERATOR_CLI} generate --input-spec=${CLIENT_SPECIFICATION_FILE_PATH} \
	                --output=${CLIENT_OUTPUT_DIR} \
	                --generator-name=python \
	                --package-name=${CLIENT_PACKAGE_NAME} \
	                --model-package=models \
	                --artifact-version=${CLIENT_PACKAGE_VERSION} \
	                --additional-properties=\
"projectName=${CLIENT_PROJECT_NAME},packageName=${CLIENT_PACKAGE_NAME},packageVersion=${CLIENT_PACKAGE_VERSION},packageUrl=${CLIENT_PACKAGE_URL}"

	exit 0

elif [ "$COMMAND" = server ]; then

	ensureValidIgnoreFile ${SERVER_OUTPUT_DIR}

	${OPENAPI_GENERATOR_CLI} generate --input-spec=${SERVER_SPECIFICATION_FILE_PATH} \
	                --output=${SERVER_OUTPUT_DIR} \
	                --generator-name=python-flask \
	                --package-name=${SERVER_PACKAGE_NAME} \
	                --model-package=models \
	                --artifact-version=${SERVER_PACKAGE_VERSION} \
	                --additional-properties=\
"projectName=${SERVER_PROJECT_NAME},packageName=${SERVER_PACKAGE_NAME},packageVersion=${SERVER_PACKAGE_VERSION},packageUrl=${SERVER_PACKAGE_URL},serverPort=${SERVER_PORT}"
	exit 0

else
	echo "Something went wrong, script should have terminated already"
	exit 1
fi
