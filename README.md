# House Price Prediction

## Introduction
As I started reading a new book to improve my skills in the field of machine learning. I wanted to do an end to end project based on this book and challenge myself. I chose to do a house price prediction project on a dataset that I collect by myself and get to know the complete lifecycle of a datascience project. 

## Geting Data.
I have collected the data from a real estate website magic bricks for which I have created a scraper which can be found in the folder get_data, there are a lot of problems with this which I will improve as I go through the data and understand what actually is required and what is not.

### First Step (Get Links of all the listed property)

The Scraper scrolls until the end of the website page and waits for all the data to load and then gathers all the links for a given city.
In a single go links of 1500 websites is collected as it is the limit of website.

### Second Step (Get Data from the links)

The Scrapper then goes through all the listed properties links and gather data related to all of them.

