## Starting your application in Rahti
For the instructions below, we will assume you are using an image built from one of the Jupyter Notebooks images in CSC's [notebook-images repository](https://github.com/CSCfi/notebook-images) (or based on it).

Note that when you upload an image to Rahti's registry, it is stored at https://registry-console.rahti.csc.fi/, but it is directly available to use from the Rahti's platform at http://rahti.csc.fi:8443.

## Create a Rahti app
Log in to Rahti platform at http://rahti.csc.fi:8443.

In the main page, create a new project or select an existing one (see the right panel). Your application will be created in the active project.

To create your application:
- In the upper right, select **Add to project** > **Deploy Image**.
- Define the image to be use in **Image Stream Tag** and modify the **name** for the application if you like (this name will appear application's http link). When you click **Deploy**, your application will start building.
- You need to create a Route (an http link) to access your application. In our example it is the entry point to the Jupyter Notebook. Easiest way is to go to the **Overview** view (on the right menu), spawn your application's details (**>**), and click on **Create Route**, review the default details and click on **Create**. You will get a link where you can access your application, for ex. *http://appname-projectname.rahtiapp.fi*.

Note that the first time you start your application, the image file needs to be copied to Rahti's nodes and may take some minutes (dependin on the size of the image). Otherwise your application should start running in a few seconds.

## Accessing your application's terminal
To access your application's terminal:
- go to **Applications** > **Posd** and select your pod.
- click on **Terminal**
- your are now logged in as the default user, in the case of Jupyter Notebooks the user is Jovyan.
- Note that you don't have root permissions in Rahti's applications (if you need root access, consider running your containers locally).
