Step1: To generate report install allure-pytest
       >> pip install allure-pytest.

Step2: Open Powershell and trigger below cmd.
       >> Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
       >> irm get.scoop.sh | iex
       >> scoop install allure

Step3: Verify Installation.
       >> allure --version

Step4: Trigger pytest with below cmd.
      >> pytes -v -s --alluredir=<reportdir>  <test file or folder>
      --> <reportdir> will be created automatically

Step5: Once execution done, trigger below cmd for viewing report:
      >> allure serve <reportdir>

Note:
1. JAVA JDK is required for allure, if not install, install it at path='C:\Program Files\Java\jdk-21
'
link: https://www.oracle.com/java/technologies/downloads/#jdk26-windows

Once JDK installed close powershell and open again and test the allure version.

PS C:\Users\ASUS> allure --version
May 09, 2026 5:35:48 PM io.qameta.allure.CommandLine main
INFO: APP_HOME is not set, using default configuration
2.40.0

>> RESTART VSCODE.
