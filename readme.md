# Project Phoenix

### Objective :
To make an AI assistant which is similar to the JARVIS we saw in the IRON MAN movie, technically we don't have such adv. technology to make such similar to JARVIS but there are some capabilities of JARVIS that were in my mind, and I thought of making it more of an AI Companion assistant, I haven't decided the capabiltites of what and how it is different than Google Assistant and SIRI, like if they are automating events etc,

 I am thinking of solving my problems and others problem when they came across using an AI Chat-bot, wether its the Chat-GPT or Google gemini, Phoenix is made to be SMART such that It will get your work done, it maybe not good at coding or performing some tasks, but it will smart help, guide and assist you how to do the task and how to get it done more efficiently, It will ensure that you won't face the frustration like sometimes, we don't get the results we want, we have to go this website that to get our things done, Phoenix will automate the things for you, and It will try to simply the problems and help you solve them effectively 

Project aims to solve problems Faced with current LLM's and also automating some things that are too hectic to do !
Like the thing to do research, mostly people use perplexity, google etc, here the research thing will be done by Phoenix itself and it will present and document it 

 ## Phoenix_v1

 1. Problems that I think, I always wanted an assistant to have a conversation flow with me, I know the fact that google assistant and siri, can also do conversation, my issue was not to write the prompt instead we can directly speak to get it done

 Solution :
 - Search for Speech-to-text model, all around well know high accuracy stt, model is from google, but it comes with a price and I wanted to implement this locally
 - then my research found out, OpenAI whisper is the model which OpenAI trained on Massive data, which also has good accuracy in the market and is opensource
 - I went on to the test of whisper model, where first thing was to record the audio then stop it, then load the model then give the audio to the model for transcription of the audio, and wait for the model to process, it was taking a lot of time as there are different whisper model depending upon their accuracy, like small,medium and large, and accuracy accordingy to their names, so even though my laptop having i5-13500h, it was still falling behind for the processing, so I again went on the research !
 - Further, I saw the model is open to use via Hugging Face API, so then I thought to give it a try and it did perform better than previous much better, but then I saw that I was taking a little bit time for saving the audio and then processing the audio, then I incorporated the concpet of threading and also recording the audio inform of chunks, utlizing all the cores of my cpu to process the audio which reduce the delayed of saving audio around 0.00 sec to 0.02 sec, even for 12-15 sec recording ( depending upon the cpu load),
 - Issue 3 : it was about, stopping the recording when the user stops speaking, the issue was it wasn't feeling like a conversation, everytime when you stop speaking you have to press the 'q' keyword to stop ( i specified the q keyword ), it seems too manul human work

 2. Problem I think, we can utilize the function calling property of the LLM model, for many cases we can automate things 

 3. Implementing screen capture to make the LLM model know what I am working on !

 4. As gemini 2.0 can now process video, as free tier is about 15 min, 4M token/sec, we need to utilize it for more comphrensive screen reading

 5. use of crawlee and selenium base for interacting with web-browser

 6. write_string function with AI in it, like it will write the content where the cursor is pointing

 7. 