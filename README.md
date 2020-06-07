# CS 338 Covid-19 Project 2 Team 1  
## Team Members:  
Naeem Patel, Owen Zhang, Raymond Liu, Emily Jenkins, Ryan Yejun Jeon, Tony Zhang, Alisa Liu, Saubhagya Shrestha, Stephanie Diao   

## Overview of our Project  
The goal of our project was to design an interactive website where users can view predicted COVID-19 outbreak numbers and hospital PPE shortages in the US. Our process in building this project consisted of three major components: 1) gathering data, 2) building a predictive model, and 3) creating a user-friendly, interactive website. We will go into specifics about each of these components in the sections below.  

## Gathering Data
We needed to gather two types of data for our project: 1) the number of COVID-19 cases per state and 2) the number of hospital PPE resources per state. We looked at data sources such as the New York Times, Johns Hopkins, and state-specific Department of Health websites. To obtain the data from state-specific Department of Health websites, we had to scrape them. One challenge that we encountered during this process was the inconsistency in which each state reported their hospital data. For instance, while some states provided detailed information on COVID-19 hopsital and PPE data, others did not include any of this information at all. Thus, our team decided to pivot our focus on predicted PPE shortages towards only the states that did provide this detailed information, rather than all the states. Although this was an issue for the hospital PPE data, it was not for the COVID-19 cases data, and we were still able to successfully gather data on COVID-19 cases for each state.

## Building a Predictive Model 

## Creating a User-Friendly, Interactive Website
We wanted to create a medium for users to interact with our predictions, so we chose to develop an interactive website. We used Flask for our web app, and we used Bokeh to create the data visualizations and interactions. There are two major components of our website: 1) visualization of our predictions for COVID-19 outbreak numbers and 2) visualizaiton of our predictions for hospital PPE shortages. For the first component, we created an interactive bar graph to display each state's predicted total number of COVID-19 cases. One interaction that we implemented was a hover tool; upon hovering on one of the bar columns in the graph, the user is able to see the specific state that bar is for and the predicted number of COVID-19 cases for that state. Another interaction that we added was to view a specific state. We included a drop-down menu where users can select a specific state they want to view. Upon selection, the graph re-renders such that it only shows the selected state's predictions. For the second component, we created a bar graph to show each state's predicted hospital PPE shortages. We were only able to include IL, Indiana, and DC due to issues with data collection, mentioned in the 'Gathering Data' section above. We implemented one interaction for this graph, which is the same as the second interaction for the first graph. Users can select a state (only Illinois, Indiana, or DC), and the second graph will re-render to show just that state's predicted hospital PPE shortages. 



