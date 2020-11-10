# Exercise workflow

## Day 1

`scikit-learn` exercises will be done in Jupyter notebooks at CSC’s Notebooks (https://notebooks.csc.fi). Notebooks provide easy-to-use environments for working with data and programming. You can access everything via your web browser and CSC cloud environment computes on the background. 

All Python code is already in the Notebooks, data will be downloaded during the exercises.

* Point your browser to https://notebooks.csc.fi
* Login using:
	* HAKA or 
	* a CSC account (earlier Puhti/cPouta users) or 
	* Alternate login and a separate username and password, that you have recieved by e-mail
* Join "CSC-GIS-ML-Course"-group in Notebooks. Click "Account" -> "Join group" -> Insert token given during the course
* Go back to Dashboard and find *Spatial machine learning notebook* and click “Launch new”
* Wait until the “Open in browser” link appears, then click on it
* Select "Copy password and proceed"
* Copy the password to the "Password or token" field in the very beginning of the page (not the "Token" field at the bottom of the page).
* The JupyterLab notebook dashboard should appear
* Exercises: Navigate to `01_data_preparation` and open 01_vectorDataPreparations.ipynb
    * Execute the cells with *shift-enter* Continue from top to bottom.
	* If there is a star in front of the cell, the cell execution is still in progress. Some of the cells take longer time to execute.
	* If there is a number in front of the cell, the cell execution is finished.
* All exercises have numbers indicating in which order they have been planned to do.
* Only exercises from folders `01_data_preparation` and `02_shallows` are done using Notebooks.

## Day 2
Keras and solaris exercises will be done in CSC Puhti supercomputer in the GPU partition.

* Training account usernames and passwords you receive by email. 
* Below replace your personal training account number to the username training[XX].
* Training project is: project_2002044.
* Our working directory is /scratch/project_2002044
* /scratch/project_2002044/data has the input data for exercises
* /scratch/project_2002044/students/training[XX] for your code and results
* For Tuesday and Wednesday we have Puhti GPU reservation for 3 nodes, so that we do not have to wait in the general queue. Therefore in batch job files there is an extra row, which should be removed if using the file later. 
`#SBATCH --reservation ml_training`

1)	Download Puhti exercises material from Github to your local computer. Download as zip: https://github.com/csc-training/geocomputing/archive/master.zip or with git. Unzip the file.

2) Login to Puhti with ssh using the training account (do not use your own CSC account because reservation available only for training accounts):

   ```bash
   ssh trainingXX@puhti.csc.fi
   ```

Windows: Open Putty. Set `Host name` puhti.csc.fi. Keep `Port` as 22.
* When typing password no characters will show, but just keep typing.

3)	Open FileZilla/WinSCP and connect to puhti.csc.fi
* Open the local directory to the left side.
* On the right side, move to your work directory: /scratch/project_2002044/students
* Create yourself own working directory with the name of your Puhti account (training0[XX]) 
* Open your own working directory with double-click.
* For moving files between Puhti and local machine drag them from the left panel to the one on the right or the other way round.

4)	Go back to Terminal/Putty and change to your directory: 
```bash
cd /scratch/project_2002044/students/training0[XX]
```


### Edit and submit jobs

1. Edit files on your local computer with a Python editor or basic text editor.
* Find places marked with TOFIX. Mostly these are paths, set them correctly according to where you have your files in Puhti.
* Each exercice has usually 2 files: one .py and one .sh.
* The .py file includes the Python code.
* The .sh file includes information for Puhti scheduler, how much resources you need and what script to run.
* If ready, move the files with FileZilla/WinSCP to Puhti.

2. Submit jobs:

   ```bash
   sbatch 06_deepRegression.sh 
   ```
   
   Or the other .sh files.
   The command prints out your job number, the same number is used for output file. 

3. (See the status of your jobs or the queue you are using:)

   ```bash
   seff job_number
   squeue -l -u $USER
   squeue -l -p gpu
   ```

4. See the job output. If the job has not started yet, an error about file not existing will be displayed.

  ```bash
  tail -f slurm-job_number.out
  ```

5. After the job has finished, examine the results:

   ```bash
   less slurm-job_number.out
   ```

6. To see the results on map, move them back to local machine and open with QGIS/ArcGIS.

## Day 3
On day 3 we will use the Solaris framework for GIS machine learning by CosmiQ works. Also we will be using PyTorch rather than Tensorflow. 

We edit the files a bit on our local computer, transfer them to Puhti and submit the jobs to the GPU partition.

https://solaris.readthedocs.io/en/latest/
https://github.com/CosmiQ/solaris

### Excercise

1. Open the **04_solaris** excercise folder on your computer

2. Edit the file **08_1_train.sh** batch job file and replace **<YOUR-STUDENT-NUMBER>** with your training-account (like training068)
	
3. Edit the file **08_2_predict.sh** and do the same

4. Now you can submit the training job with 

   ```bash
   sbatch 08_1_train.sh
   ```
   
   When the job is running you can observe the logs live with the command 
   
   ```bash
   tail -f slurm-job_number.out
   ```
   
5. The training job creates a lot of **model_something_something.pth** files as it saves the model every time an epoch perfoms better than the previous (bug). You can safely delete all files starting with 'model' with

   ```bash
   rm model*
   ```
   
6. If the training has succeeded, you also have a file called **PredictSpruceForestsModel_final.pth** and you can run the prediction to the whole image by submitting the prediction job with

   ```bash
   sbatch 08_2_predict.sh
   ```

7. If it was succesfull you can inspect the performance measures from that job's slurm output file

8. There is now a file called **spruce_predicted.tif**. You can transfer that from Puhti to your local computer and look at the results

	
