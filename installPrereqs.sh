source ./setEnv.sh

# ***** Install Python prerequisites for Google Calendar API
installPythonModules()
{
    pip3 install --upgrade \
                pandas>=1.3.0 \
                openpyxl>=3.0.0
}

# ***** MAIN EXECUTION
installPythonModules