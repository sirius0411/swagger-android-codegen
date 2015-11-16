# swagger-android-codegen
generate a swagger RESTful client on Android based on Retrofit and RxJava

This project is modified from the client generator part in our group's swagger workflow.

**still in development**


---
##Known Issues
---

- **format** is ignored(all 'number' 'integer' will be parsed as 'int'), format info will be placed in descriptions
- **enum** won't be parsed as a **Enum**, accept values are in description
- api method name may confilct
- many keys are ignored

---
##Requirements
---

- Python 3.0+
		
		My version is Python 3.4.3
		
- latest pystache (https://github.com/defunkt/pystache)

        pip install pystache
	
---
##Use it
---

		python swagger_codegen.py [option] -j jsonPath -l language [ -t template | -o output]
		
###Options and arguments:
- -j jsonPath : the source swagger json path (url or file path) (also --json=jsonPath)
- -l language : destination language, **ONLY SUPPORT** rxandroid yet (also --language=language)
- -t template : template directory that will be used (also --template==)
- -o output   : output directory that the code will be placed (also --output==)
- -v          : print the version info (also --version)
- -h          : print the help info (also --help)

###Rx part

This tool have a default generator for RxJava/RxAndroid.

Use

		python .\swagger_codegen.py -j ... -l rxandroid
		
to generate an Android Studio module.

Import the generated module ('rxandroid_api' by default).

		# in Android Studio
		File -> New -> Import Module -> add the rxandroid_api module's path
		
Now your project may look like this:

		YourProject----rxandroid_api
					 |
					 |-app
					 |
					 |-other module
					 
In your app module build.gradle, add the code

    	compile project(':rxandroid_api')
		
		
Now you can use the generated APIs easily in your module by using codes like below

		// get api instance by class
		// same as Retrofit
		NetManager.getInstance().getApi(YourApi.class)
		
		// the NetManager will hold the api instance as cache, you should release the resources by the code below
		NetManager.getInstance().recycle()
		
		// use changeBaseUrl() to reset Retrofit.baseUrl() to change different flavors
		NetManager.getInstance().changeBaseUrl(newBaseUrl)
		
		// edit NetManager's debug constants and getAPIRootUrl() method to change the url path generator's behavior


