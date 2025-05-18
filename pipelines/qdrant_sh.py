# Creating a dynamic qdrant pipeline, which supports multiple format of data to export and save in the mongodb local and then save it in qdrant local through an emeddings model, for perfect rag
# the appraoch is total dynamic such that it will have CRUD operations for the collection database in the qdrant that is also link to the mongodb
# the working process :
'''

We will be given option to create a new collection of data or use existing one, the given the best 3 emeddings model option that provide generous free tier ( local embeddings too but in next phase of project), then it will ask the content of data that you want to save, then you can pass the pdf, md, csv, ppt and all other format of the files where it will utilze best of class techniques like for pdf, llamaindex is already world-class at OCR and output and similar for other datatypes and then they will be stored in an Mogo-db database as an md file for human understanding of what was the raw data later the raw data will be simulatneously send to qdrant to the specific collection that was given earlier, and then it will create vector embeddings, It will give various option for the type of search retrival and what are the types of features we want, then in the end it will give us an code that we can integrate in other application for using the collection data !

'''