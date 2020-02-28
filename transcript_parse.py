import pandas as pd
from bs4 import BeautifulSoup
import os

#Input file (Can be Modified)
path = 'Transcripts/JD/'

files = os.listdir(path)

file = path + files[-1]

#Function to parse the transcript to be used for the
def create_transcript_Dataframe(file):

    #For each file iterate through the paras to extract the content
    transcript_soup = BeautifulSoup(open(file), 'lxml')

    #Get the content
    actual_transcript = transcript_soup.find_all(attrs={'class':'article-content'})

    #Get the paras removing the first two as it is irrelevant
    transcript_content = actual_transcript[0].find_all('p')[2:]

    #Get all the strongs as they will be used to identify the speaker
    strongs = transcript_soup.find_all('strong')

    #Set to be used to store the speaker names
    participants = set()

    #Convert them to only just their names removing the tag
    for strong in strongs:
        participants.add(strong.text)

    #Create an empty DataFrame to be used
    df = pd.DataFrame(columns=['Comments', 'Participant', 'Designation'])

    #Variables to be added into the DataFrame
    participant = ''
    designation = ''
    text = ''

    #Iterate through the <p> tags to get all the content to be appended into the DataFrame
    for i in range(len(transcript_content)):
        
        #The content in a <p> element
        para = transcript_content[i]
        
        #Stop condition for the DataFrame creation
        if('Duration' in para.text):

            #Append the last entry into the DataFrame
            df = df.append({'Comments': text.strip(),'Participant' : participant , 'Designation' : designation} , ignore_index=True)
            break
        
        #Check if the content is currently a speaker
        speaker_check = para.find_all('strong')
        
        #If it is a speaker assign the name of the participant and their designation
        if(speaker_check != []):
            
            #If it is the next speaker append the information and reset their comments (text)
            if(i != 0):
                df = df.append({'Comments': text.strip(),'Participant' : participant , 'Designation' : designation} , ignore_index=True)
                text = ' '
                
            #Split the speaker into their respective name company and designation
            speaker_list = para.text.split(' -- ')
            
            participant = speaker_list[0]
            
            designation = speaker_list[-1]
            
        #Handling the comment to be added into the text
        else: 
            
            text += para.text + ' '

    return df

#Test
# df = create_transcript_Dataframe(file)

# print(df)