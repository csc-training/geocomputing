# Creating the notebooks Blueprint

## Prequisites 

- You have group owner rights in notebooks.csc.fi
- You have built your own notebooks docker image
- You have uploaded that image to Rahti image registry
- Anynomous pulling of images is enabled in your project in Rahti image registry

## Creating the blueprint

Blueprint is the description of your notebook in notebooks.csc.fi. It dictates the name, resources and various other thing related to the notebook instances. You can edit it any time after creation

- Navigate to notebooks.csc.fi, log in and make sure you have "Blueprints" tab visible. If not, you don't have sufficient rights and need to apply for them from servicedesk@csc.fi
- In the Blueprints tab you can create a new blueprint by clicking "Create blueprint next to existing tempaltes) (for example next to Rahti Jupyter Minimal)
- Fill in the relevant information. Here is information on some relevant fields
  - __image__: This is the URL for your image in Rahti container registry. You need to replace this one with your URL. You can find it from [Rahti Image Registry](https://registry-console.rahti.csc.fi/)
  - __memory limit__: This tells how much memory to reserve to one notebooks instance. Currently the absolute maximum is 8GB
  - __AUTODOWNLOAD_URL__: if you have a script somewhere that you would want to be executed every time an instance is launched (e.g. pull a repository), you need to specify it here and the file name also to the next field
 
 After creating the blueprint, you can find it in the Blueprint page under "Active blueprints". From here you can edit the settings and also copy the blueprint. 
 
 Note that blueprints have an expiry date and need to be renewed after that
