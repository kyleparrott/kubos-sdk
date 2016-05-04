# Kubos SDK

### Usage: 

 Create a new project with kubos-rt added as a dependency:
 ```
 $ kubos_yt --init  
 ```
 Set target device: 
 ```
 $ kubos_yt --target <target> 
 ```

### Building kubos_yt executable
Install pyinstaller to bundle python scripts into executables:
```
$ pip install pyinstaller
```

Package python script into a linux executable:
```
$ pyinstaller --onefile kubos_yt.py
```
