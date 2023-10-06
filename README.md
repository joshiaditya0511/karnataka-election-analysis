# Karnataka Assembly Elections: Data Analysis

This project is a comprehensive data analysis of the Karnataka Assembly Elections. It offers insights and visualizations on various aspects of the election, leveraging data from multiple sources.

## Contents
- [Project Overview](#project-overview)
- [Tools and Tech Used](#tools-and-tech-used)
- [Sources and References](#sources-and-references)
- [Links](#links)

## Project Overview

This analysis dives deep into the Karnataka Assembly Elections, exploring facets like vote count, candidate details, vote margins, impact of Bharat Jodo Yatra and more. All visualizations are interactive, offering users an engaging experience.

## Tools and Tech Used

### Data Gathering:

- **Webscraping**: 
  - `Requests`: Utilized for sending GET requests to retrieve webpage content.
  - `BeautifulSoup`: Employed for parsing HTML and extracting relevant data.
  - `Selenium`: Facilitated interaction with dynamically loaded pages, ensuring faster loading and maintaining cookies for improved data fetches.
  - `asyncio`: Enhanced performance by sending multiple requests asynchronously, ensuring efficient run times and adhering to rate limits.
  
- **PDF Extraction**:
  - Over 57,000 PDFs were processed to extract voter data for the 2023 elections.
  - `PyPDF2`: Modified PDFs, retaining only vital pages.
  - `pdf2image`: Transformed PDF pages into image formats.
  - `OpenCV`: Detected and retained table borders for precise data extraction.
  - `TesseractOCR`: Employed OCR for data extraction within detected table areas.
  - `asyncio` and `multiprocessing`: Used for asynchronous downloads and simultaneous processing of multiple PDFs.

### Data Wrangling:

- `Pandas` and `Regular Expressions`: These tools formed the backbone of data cleaning and wrangling operations.
- `OpenAI API`: Leveraged for segmenting and classifying education and profession details using the GPT-3.5 model, with data managed in chunks to adhere to token and rate limits.

### Data Visualization:

- `Plotly Express`: The primary library used for crafting interactive visualizations.
- `Flourish Studio`: Used to create and embed Parliamentary Chart as an HTML component.

### Database:

- `MySQL` in `AWS RDS`: The chosen DBMS for storage and retrieval, leveraging the free tier of AWS RDS.
- `MySQL's Python Connector API`: Facilitated database interactions, from table creation to data fetching, bridging the website and the database.

### Website and Deployment:

- `Streamlit`: The foundational framework for website creation, hosted on Streamlit's complimentary community cloud.

### Miscellaneous:

- `MapShaper`: Assisted in converting Karnataka’s assembly boundaries shape file to GeoJSON and smoothening boundaries for faster rendering.

## Sources and References

- **MyNeta**: Data concerning assets, liabilities, criminal cases, profession, and education of candidates across three assembly elections was scraped from MyNeta. This data was freely available to the general public.

- **NDTV**: Vote count data for every candidate contesting in the 2023 elections was scraped from NDTV's live election results page. This data was also freely available to the public.

- **OpenCity**: Detailed results for the 2013 Assembly elections were freely available on OpenCity in the form of a CSV file.

- **ECI (Election Commission of India)**: The Election Commission of India published the detailed results of the 2018 elections in September 2018. This data was freely accessible to the public.

- **CEO (Chief Election Officer) of Karnataka**: Information about eligible voters and their gender-wise distribution was available in PDF format for all polling stations in Karnataka. Although these PDFs were free for the public, they were protected by a captcha. Only data regarding the number of eligible voters and their gender distribution was retrieved.

- **KGIS (Karnataka Geographic Information System)**: The shape file for Karnataka's assembly constituency boundaries was obtained from the KGIS website owned by the Karnataka government. For visualization purposes, Bangalore district’s constituencies have been extracted and displayed separately due to their high number and smaller area. No harm or alteration to Karnataka's sovereign boundaries is intended.

- **MapShaper**: MapShaper was used to convert the Shape file to GeoJSON for better compatibility. The tool also smoothened the borders for quicker visualization rendering in this project. Again, no harm or alteration to Karnataka's sovereign boundaries is intended.

- **OpenAI**: OpenAI's API was employed to segment and classify the education and profession details provided by the candidates. This segmentation was done using OpenAI’s proprietary GPT-3.5 model, and while efficient, it may not be entirely accurate.

## Links

- [Project website](https://karnataka-election-analysis.streamlit.app/)
- [LinkedIn](https://www.linkedin.com/in/joshiaditya0511)
