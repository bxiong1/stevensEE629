# stevensEE629

index.html files is the file that I solved the problem for students who are in China and are not able to get the access of the Google Map when he/she tries to do Lab 4 stevens project. The way I solve it is that I replaced Google Map with one of the famous map in China AMap. 

All you have to do is to go to the website https://lbs.amap.com/ and then register an account then you can pull out the API Key from the website. 


After doing all the steps above, you can then download the index.html file. In the file you need to modified the API Key:


  <script type="text/javascript" src="https://webapi.amap.com/maps?v=1.4.8&key=YOUR_KEY"></script>

Replacing YOUR_KEY with the API Key you obtained from the website. And then you can rerun the stevens project. 
The Result can be found on my course page: https://sites.google.com/view/bxiong-ee629/lab/lab4?authuser=0


About the Project:

The project that I am doing is "Facial Recognition Using Raspberry Pi" the source code is already contained in the Project folder. You can download the folder and then it contains every of the project. 

However, you need to pre-install some of the python module before running the program as well as purchase some of the hardware equipments. 

After you have all the module simply run: 
python3 facerec_from_webcam_faster.py 

It will automatically start to run the program and detect faces ones you locate the camera in front of a .jpg face picture.

If you are interested running the program, and see the demo of my project you can go to the website: https://sites.google.com/view/bxiong-ee629/project?authuser=0 
